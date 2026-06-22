# -*- coding: utf-8 -*-
"""Woodpecker client — READ + CREATE-ONLY, safe by construction.

This class deliberately has NO method that starts, pauses, resumes, stops, or
deletes a campaign. The only way to send is a verb that does not exist here, so
the contract's hardest rule ("never start a send") is structural, not a promise.

Safety posture:
  * dry_run=True by default — write methods make ZERO network calls and return a
    simulated result. You must pass dry_run=False AND set WOODPECKER_AGENT_BUILD=on
    to touch the live account.
  * create_campaign enforces mailbox isolation (allow-listed warmed secondary
    mailbox only; never primary/live).
  * add_prospects (a PII write) refuses unless: the campaign id is in the ledger
    (owned), its live status is DRAFT/PAUSED (never RUNNING), and every prospect
    was pre-cleared by presend_gate.
  * calls are serialized (max 1 in-flight) with exponential backoff on 429,
    because the rate limit is shared with Vishal's live campaigns.
"""
import json, time, threading, urllib.request, urllib.error
from . import config, ledger

_LOCK = threading.Lock()  # account-wide rate limit is shared -> serialize


class WoodpeckerError(RuntimeError):
    pass


class ForbiddenAction(RuntimeError):
    """Raised if a state-changing verb is ever attempted."""


class WoodpeckerClient:
    def __init__(self, key=None, dry_run=True, transport=None, max_retries=4):
        self._key = key or config.get_woodpecker_key()
        self.dry_run = dry_run
        self._transport = transport          # for tests: f(method, url, headers, body)->(status, bytes)
        self.max_retries = max_retries

    # ---- low-level, serialized, with 429 backoff ------------------------------
    def _http(self, method, path, body=None):
        # CHOKE POINT: only the read-list and create endpoints are ever issuable.
        # A /run, /pause, status=RUNNING PUT, etc. is refused here, by construction.
        if (method, path) not in config.ALLOWED_HTTP:
            raise ForbiddenAction("blocked verb/path: %s %s (only list + create permitted)" % (method, path))
        if self._transport is None and not self._key:
            raise WoodpeckerError("WOODPECKER_API_KEY not set in environment")
        url = config.WP_BASE + path
        headers = {"x-api-key": self._key or "", "Content-Type": "application/json"}
        data = json.dumps(body).encode("utf-8") if body is not None else None
        with _LOCK:
            delay = 1.0
            for attempt in range(self.max_retries + 1):
                if self._transport is not None:
                    status, raw = self._transport(method, url, headers, data)
                else:
                    req = urllib.request.Request(url, data=data, headers=headers, method=method)
                    try:
                        with urllib.request.urlopen(req, timeout=30) as r:
                            status, raw = r.status, r.read()
                    except urllib.error.HTTPError as e:
                        status, raw = e.code, e.read()
                    except urllib.error.URLError as e:
                        raise WoodpeckerError("network error: %s" % e.reason)
                if status == 429:               # shared limit hit -> back off + yield
                    if attempt == self.max_retries:
                        raise WoodpeckerError("429 rate-limited; aborting (never retry-storm)")
                    time.sleep(delay); delay *= 2
                    continue
                return status, raw
        raise WoodpeckerError("unreachable")

    # ---- READ (metadata only, no PII) -----------------------------------------
    def list_campaigns(self):
        """GET /rest/v1/campaign_list — names, ids, status, sender. No prospect PII."""
        status, raw = self._http("GET", config.WP_LIST_PATH)
        if status != 200:
            raise WoodpeckerError("campaign_list returned HTTP %s" % status)
        return json.loads(raw or b"[]")

    def get_status(self, campaign_id):
        """Live status of a campaign (read via v1 list; v2 GET is 405)."""
        for c in self.list_campaigns():
            if str(c.get("id")) == str(campaign_id):
                return c.get("status")
        return None

    # ---- CREATE-ONLY ----------------------------------------------------------
    def create_campaign(self, name, mailbox_id, settings, steps, run_id=None, created_at_utc=None):
        """POST /rest/v2/campaigns — builds a DRAFT campaign. Never starts it.

        Enforces the kill switch + mailbox isolation. On success (dry-run or live)
        the caller is responsible for nothing else: this appends to the ledger.
        """
        if not config.build_enabled():
            raise ForbiddenAction("WOODPECKER_AGENT_BUILD is off — zero write calls permitted")
        if not name.startswith(config.NAME_PREFIX):
            raise ForbiddenAction("campaign name must be namespaced '%s ...'" % config.NAME_PREFIX)
        self._assert_mailbox_isolated(mailbox_id)
        if not steps:
            raise WoodpeckerError("refusing to create a campaign with no steps")
        # Collision scan (contract §4.2): whenever we can actually enumerate the
        # account, ABORT if the name collides with a non-owned campaign.
        if (not self.dry_run) or (self._transport is not None):
            self._assert_no_collision(name)

        body = {"name": name, "email_account_ids": [mailbox_id], "settings": settings, "steps": steps}

        if self.dry_run:
            cid = "DRYRUN-%s" % (run_id or "x")
        else:
            status, raw = self._http("POST", config.WP_CREATE_PATH, body)
            if status != 201:
                # a 405 on a POST create is a REAL failure — surface, never silent-retry
                raise WoodpeckerError("create returned HTTP %s (expected 201)" % status)
            cid = str(json.loads(raw).get("id"))
            # Read the status back — never assert DRAFT by comment alone.
            live = self.get_status(cid)
            if live not in config.NON_SENDING_STATUSES:
                raise WoodpeckerError("created campaign %s is %s, expected DRAFT/PAUSED — ALERT" % (cid, live))

        ledger.append({
            "run_id": run_id, "campaign_id": cid, "exact_name": name,
            "sender_mailbox": mailbox_id, "created_at_utc": created_at_utc,
            "dry_run": self.dry_run,
        })
        final_status = "DRAFT" if self.dry_run else live
        return {"campaign_id": cid, "status": final_status, "dry_run": self.dry_run}

    def _assert_no_collision(self, name):
        """ABORT if `name` case-insensitively equals/prefixes a campaign we do not own.
        If the list can't be enumerated, treat detection as FAILED -> abort (fail closed)."""
        try:
            campaigns = self.list_campaigns()
        except WoodpeckerError as e:
            raise ForbiddenAction("collision check could not enumerate campaigns: %s" % e)
        owned = ledger.owned_ids()
        nl = name.strip().lower()
        for c in campaigns:
            cn = str(c.get("name", "")).strip().lower()
            if (cn == nl or cn.startswith(nl)) and str(c.get("id")) not in owned:
                raise ForbiddenAction("name collides with non-owned campaign id=%s" % c.get("id"))

    # ---- ENROLL (PII write) — gated hard --------------------------------------
    def add_prospects(self, campaign_id, cleared_prospects, gate_verdict):
        """Add prospects to an OWNED, NON-SENDING campaign — only if the gate ALLOWed.

        cleared_prospects: records that passed presend_gate.check_record.
        gate_verdict: the dict from presend_gate.evaluate (must be verdict == 'ALLOW').
        """
        from . import presend_gate  # local import avoids a cycle at module load
        if not config.build_enabled():
            raise ForbiddenAction("WOODPECKER_AGENT_BUILD is off — zero write calls permitted")
        if gate_verdict.get("verdict") != "ALLOW":
            raise ForbiddenAction("pre-send gate did not ALLOW: %s" % gate_verdict.get("halts"))
        if not ledger.owns(campaign_id):
            raise ForbiddenAction("campaign %s is not in the creation ledger (foreign/read-only)" % campaign_id)
        if not cleared_prospects:
            return {"enrolled": 0, "reason": "no_cleared_prospects"}
        # Do NOT trust the passed verdict for these prospects — re-verify EACH record
        # here (the verdict could be from a different cohort). Any failure -> refuse all.
        for rec in cleared_prospects:
            ok, reasons = presend_gate.check_record(rec)
            if not ok:
                raise ForbiddenAction("prospect failed re-verification at enroll: %s" % reasons)
        # status MUST be DRAFT/PAUSED, re-checked immediately before enroll — run this
        # whenever we can reach the account (live, or dry-run with a transport stub).
        if (not self.dry_run) or (self._transport is not None):
            st = self.get_status(campaign_id)
            if st not in config.NON_SENDING_STATUSES:
                raise ForbiddenAction("target status is %s; enroll only into DRAFT/PAUSED" % st)
        if not self.dry_run:
            # real enroll endpoint intentionally left to the MCP server / a reviewed
            # follow-up; this client does not bulk-write the global prospect pool blind.
            raise WoodpeckerError("live enroll is not enabled in this build (stage-zero today)")
        return {"enrolled": len(cleared_prospects), "dry_run": True}

    # ---- guards ---------------------------------------------------------------
    def _assert_mailbox_isolated(self, mailbox_id):
        m = (mailbox_id or "").strip()
        if not m:
            raise ForbiddenAction("no mailbox — cannot create (no sender-less create)")
        if m in config.FORBIDDEN_MAILBOXES or m.endswith("@" + config.PRIMARY_DOMAIN):
            raise ForbiddenAction("mailbox '%s' is live/primary — never borrow it" % m)
        allow = config.allowed_mailbox_ids()
        if not allow:
            raise ForbiddenAction("no allow-listed warmed mailbox provisioned (infra gap) — abort")
        if m not in allow:
            raise ForbiddenAction("mailbox '%s' not in WOODPECKER_ALLOWED_MAILBOX_IDS" % m)

    # Any attempt to call a state-changing verb is refused by name (defense in depth
    # on top of the _http allow-list). Compare lowercase so casing can't slip past.
    def __getattr__(self, item):
        if isinstance(item, str) and item.lower() in config.FORBIDDEN_VERBS:
            def _refuse(*a, **k):
                raise ForbiddenAction("'%s' is never the agent's to call — humans only" % item)
            return _refuse
        raise AttributeError(item)
