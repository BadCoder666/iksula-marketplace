# -*- coding: utf-8 -*-
"""Safety tests — assert the guardrails actually hold. Run from D:\\Y\\DJ:
    python -m unittest leadgen.tests.test_safety
No network, no live account, no sending.
"""
import os, json, tempfile, unittest
from leadgen import config, presend_gate, merge_preview, ledger
from leadgen.wp_client import WoodpeckerClient, ForbiddenAction

CLEARED = {  # a record that passes every per-record check
    "email": "priya@acme-corp.com", "data_processing_basis": "Legitimate Interests",
    "region": "US", "email_opt_out": False,
}
GOOD_CTX = {  # cohort context that satisfies every gate
    "source_type": "clean_sheet", "mailbox_id": "warm-1",
    "merge_preview_clean": True, "approval_token": "approved-by-vishal",
}


class GateTests(unittest.TestCase):
    def setUp(self):
        os.environ["WOODPECKER_AGENT_BUILD"] = "on"
        os.environ["WOODPECKER_ALLOWED_MAILBOX_IDS"] = "warm-1,warm-2"

    def test_null_basis_halts_with_zero_eligible(self):
        recs = [{"email": "a@acme.com", "data_processing_basis": "", "region": "US"}]
        v = presend_gate.evaluate(recs, GOOD_CTX)
        self.assertEqual(v["verdict"], "HALT")
        self.assertEqual(v["eligible_count"], 0)
        self.assertIn("zero_eligible_records (no record cleared lawful basis + suppression)", v["halts"])

    def test_existing_client_and_optout_suppressed(self):
        ok, reasons = presend_gate.check_record({**CLEARED, "is_existing_client": True})
        self.assertFalse(ok); self.assertIn("existing_client", reasons)
        ok2, r2 = presend_gate.check_record({**CLEARED, "email_opt_out": True})
        self.assertFalse(ok2); self.assertIn("opted_out", r2)

    def test_foreign_cctld_and_webmail_blocked(self):
        ok, r = presend_gate.check_record({**CLEARED, "email": "x@theguardian.co.uk"})
        self.assertFalse(ok); self.assertIn("foreign_cctld", r)
        ok2, r2 = presend_gate.check_record({**CLEARED, "email": "x@gmail.com"})
        self.assertFalse(ok2); self.assertIn("free_webmail", r2)

    def test_raw_zoho_source_halts(self):
        v = presend_gate.evaluate([CLEARED], {**GOOD_CTX, "source_type": "raw_zoho"})
        self.assertEqual(v["verdict"], "HALT")
        self.assertTrue(any("source_not_clean_sheet" in h for h in v["halts"]))

    def test_build_switch_off_halts(self):
        os.environ["WOODPECKER_AGENT_BUILD"] = "off"
        v = presend_gate.evaluate([CLEARED], GOOD_CTX)
        self.assertEqual(v["verdict"], "HALT")
        self.assertTrue(any("build_switch_off" in h for h in v["halts"]))

    def test_no_approval_halts(self):
        v = presend_gate.evaluate([CLEARED], {**GOOD_CTX, "approval_token": None})
        self.assertTrue(any("no_human_approval" in h for h in v["halts"]))

    def test_full_pass_allows(self):
        v = presend_gate.evaluate([CLEARED], GOOD_CTX)
        self.assertEqual(v["verdict"], "ALLOW")
        self.assertEqual(v["eligible_count"], 1)

    def test_string_false_is_not_suppressed(self):
        # CSV booleans arrive as strings; "false" must NOT count as suppressed.
        rec = {**CLEARED, "email_opt_out": "false", "is_existing_client": "FALSE"}
        ok, reasons = presend_gate.check_record(rec)
        self.assertTrue(ok, reasons)
        self.assertNotIn("opted_out", reasons)
        self.assertNotIn("existing_client", reasons)

    def test_unknown_suppression_value_fails_safe(self):
        # A garbled/unknown suppression value must SUPPRESS, not slip through.
        ok, reasons = presend_gate.check_record({**CLEARED, "email_opt_out": "weird"})
        self.assertFalse(ok); self.assertIn("opted_out", reasons)

    def test_unknown_region_rejected_failclosed(self):
        ok, reasons = presend_gate.check_record({**CLEARED, "region": ""})
        self.assertFalse(ok); self.assertIn("region_unknown_or_not_permitted", reasons)

    def test_verdict_carries_no_pii(self):
        recs = [{"email": "leak@acme.com", "data_processing_basis": "", "region": "US"}]
        v = presend_gate.evaluate(recs, GOOD_CTX)
        blob = json.dumps(v)
        self.assertNotIn("@", blob)                      # no email anywhere in verdict
        for r in v["rejected_sample"]:
            self.assertNotIn("email", r)
            self.assertIn("row_index", r)


class MergePreviewTests(unittest.TestCase):
    def test_detects_token_leak(self):
        out = merge_preview.validate("Hi {{first_name}}, re {{company}}",
                                     [{"first_name": "Priya", "company": ""}])
        self.assertFalse(out["clean"])
        self.assertEqual(out["leaking_rows"][0]["leaked_fields"], ["company"])

    def test_fallback_is_not_a_leak(self):
        out = merge_preview.validate("Hi {{first_name|there}}", [{"first_name": ""}])
        self.assertTrue(out["clean"])

    def test_clean_when_all_present(self):
        out = merge_preview.validate("Hi {{first_name}}", [{"first_name": "Sam"}])
        self.assertTrue(out["clean"])


class ClientSafetyTests(unittest.TestCase):
    def setUp(self):
        os.environ["WOODPECKER_AGENT_BUILD"] = "on"
        os.environ["WOODPECKER_ALLOWED_MAILBOX_IDS"] = "warm-1"
        self._tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jsonl").name
        self._orig = config.LEDGER_PATH
        config.LEDGER_PATH = self._tmp
        self.c = WoodpeckerClient(key="test", dry_run=True)

    def tearDown(self):
        config.LEDGER_PATH = self._orig
        try: os.remove(self._tmp)
        except OSError: pass

    def test_no_send_verbs_exist(self):
        # incl. mixed-case spellings that previously slipped past the guard
        for verb in ("run", "start", "resume", "pause", "stop", "delete",
                     "runCampaign", "RunCampaign", "PauseCampaign", "DELETE"):
            with self.assertRaises(ForbiddenAction):
                getattr(self.c, verb)("any-id")

    def test_http_layer_blocks_send_paths(self):
        # the unconstrained-primitive hole: a hand-built /run or status PUT is refused
        for method, path in (("POST", "/rest/v1/campaigns/123/run"),
                             ("PUT", "/rest/v2/campaigns/123"),
                             ("DELETE", "/rest/v2/campaigns/123")):
            with self.assertRaises(ForbiddenAction):
                self.c._http(method, path)

    def test_enroll_reverifies_each_prospect(self):
        res = self.c.create_campaign("[LG-AGENT] us 2606 r1", "warm-1",
                                     {"timezone": "EST", "daily_enroll": 20},
                                     [{"type": "START"}], run_id="r1", created_at_utc="t")
        allow = presend_gate.evaluate([CLEARED], GOOD_CTX)
        self.assertEqual(allow["verdict"], "ALLOW")
        bad = {"email": "x@acme.com", "data_processing_basis": "", "region": "US"}
        with self.assertRaises(ForbiddenAction):          # ALLOW verdict can't smuggle a bad record
            self.c.add_prospects(res["campaign_id"], [bad], allow)

    def test_dry_run_enroll_happy_path(self):
        res = self.c.create_campaign("[LG-AGENT] us 2606 r1", "warm-1",
                                     {"timezone": "EST", "daily_enroll": 20},
                                     [{"type": "START"}], run_id="r1", created_at_utc="t")
        allow = presend_gate.evaluate([CLEARED], GOOD_CTX)
        out = self.c.add_prospects(res["campaign_id"], [CLEARED], allow)
        self.assertEqual(out["enrolled"], 1)

    def test_create_blocked_when_switch_off(self):
        os.environ["WOODPECKER_AGENT_BUILD"] = "off"
        with self.assertRaises(ForbiddenAction):
            self.c.create_campaign("[LG-AGENT] x", "warm-1", {"timezone": "EST", "daily_enroll": 20},
                                   [{"type": "START"}], run_id="r1", created_at_utc="t")

    def test_create_blocked_with_primary_mailbox(self):
        with self.assertRaises(ForbiddenAction):
            self.c.create_campaign("[LG-AGENT] x", "sam@iksula.com",
                                   {"timezone": "EST", "daily_enroll": 20},
                                   [{"type": "START"}], run_id="r1", created_at_utc="t")

    def test_create_blocked_without_namespace(self):
        with self.assertRaises(ForbiddenAction):
            self.c.create_campaign("cold blast", "warm-1", {"timezone": "EST", "daily_enroll": 20},
                                   [{"type": "START"}], run_id="r1", created_at_utc="t")

    def test_dry_run_create_ledgers_and_owns(self):
        res = self.c.create_campaign("[LG-AGENT] us 2606 r1", "warm-1",
                                     {"timezone": "EST", "daily_enroll": 20},
                                     [{"type": "START"}], run_id="r1", created_at_utc="t")
        self.assertTrue(res["dry_run"])
        self.assertTrue(ledger.owns(res["campaign_id"]))

    def test_enroll_refused_unless_gate_allows(self):
        res = self.c.create_campaign("[LG-AGENT] us 2606 r1", "warm-1",
                                     {"timezone": "EST", "daily_enroll": 20},
                                     [{"type": "START"}], run_id="r1", created_at_utc="t")
        with self.assertRaises(ForbiddenAction):
            self.c.add_prospects(res["campaign_id"], [CLEARED], {"verdict": "HALT", "halts": ["x"]})

    def test_enroll_refused_on_foreign_campaign(self):
        good = presend_gate.evaluate([CLEARED], GOOD_CTX)
        with self.assertRaises(ForbiddenAction):
            self.c.add_prospects("not-in-ledger", [CLEARED], good)


if __name__ == "__main__":
    unittest.main(verbosity=2)
