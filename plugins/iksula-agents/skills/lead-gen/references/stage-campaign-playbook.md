# Stage-campaign playbook — sheet → 3-step Woodpecker DRAFT (operator path)

**When to use.** An operator hands you a prospect sheet (e.g. an Apollo/CFO `.xlsx`) and says *"create / stage a
Woodpecker campaign", "load these into Woodpecker", "build the sequence"*. This is the **"AI preps, a human
sends"** operator path: it is **data-hygiene-gated**, and the **human who presses Run owns lawful basis**. It is
distinct from the autonomous funnel staging in `SKILL.md §5b` / `sending-stack.md`, which stays hard
lawful-basis-gated (`presend_gate`). Do not confuse the two: this path uses `sheet_to_ready` / `stage_campaign` /
`enroll_to_draft`, NOT `add_prospects`.

**The invariant (unchanged).** The agent has **no send verb**. It builds a DRAFT and enrolls; a human opens the
draft and presses **Run**. `enroll_to_draft` writes only into a **DRAFT/PAUSED** campaign it **owns** (ledger), from
an allow-listed **secondary-domain** mailbox. Never `/run`, never a primary `@iksula.com` mailbox, never a campaign
you didn't create.

## Prerequisites
- Env: `WOODPECKER_AGENT_BUILD=on`, `WOODPECKER_ALLOWED_MAILBOX_IDS=<mailbox id>`, and `WOODPECKER_API_KEY` in a
  gitignored local file (never committed/pasted into chat).
- Mailbox: a **warmed, secondary-domain** id only — e.g. `779855` = `vishal.sobti@us.iksula.com`. Never a primary
  `@iksula.com` address. The id must be in `WOODPECKER_ALLOWED_MAILBOX_IDS` or the build refuses (by design).
- Connectors: **Zoho CRM** (for suppression) and **Google Drive** (for a private sheet).
- Run toolkit commands from `plugins/iksula-agents/tools/`.

## The recipe

1. **Read the sheet.** `.xlsx` → `openpyxl.load_workbook(path, read_only=True, data_only=True)`; or CSV; or, for a
   private Google Sheet, fetch it via the Drive connector. Find the email column and any existing copy columns
   (e.g. `Warm InMail 1 / 2`, `Direct InMail`). Pull `email, first_name, last_name, company, title` per row. Keep
   PII local (scratchpad) — never to the Brain.

2. **Clean + dedupe.** Use `leadgen.sheet_to_ready.clean` (case-insensitive dedupe, drop malformed emails). Report
   what was dropped.

3. **Suppress against Zoho — read the gotchas.** Query existing **Leads** and **Contacts** by email and drop any
   match (don't cold-pitch a current lead/client). Two hard rules:
   - COQL `Email in ('a','b',…)` is **capped at 100 values** → batch in chunks of **≤95**.
   - **Run the batches SEQUENTIALLY, one query per turn.** Firing COQL queries in parallel **misroutes responses**
     across modules (a Leads-module query can come back with Contact record ids). A 204/"empty response" means
     genuinely zero matches. Collect the matched emails → write them to a `suppress.csv` and feed `--suppress`,
     or just exclude them when you assemble step 5.
   - (If asked for full existing-client suppression, also diff company **domains** against Account/Deal records —
     see `seam-and-compliance.md §6`.)

4. **Generate copy for anyone who doesn't already have it.** Three messages per prospect:
   `Warm InMail 1` (lead with one **specific, true** company fact → the finance/commerce pain it implies → the
   relevant Iksula capability → soft "20-minute call?"), `Warm InMail 2` (a different angle, softer), and
   `Direct InMail` ("Hi <First>, I'm from Iksula. We help <segment> <value>. Given <fact>, <pain> is likely live.
   Could we find 20 minutes…"). Voice: Iksula = e-commerce / digital-commerce services (process automation, data &
   insights, commerce analytics, PIM, financial consolidation/faster close); peer-to-peer, ~55–85 words, no hype,
   no emojis, no subject line in the snippet. **NO FABRICATION** — only cite a fact you verified on the web or
   confidently know; otherwise personalise on the real industry/business-model/scale and mark it low-confidence.
   Flag low-confidence prospects for the human to eyeball. Fanning this out across prospects (a workflow / parallel
   agents) is fine; the copy itself is the agent's judgement, not a deterministic step.

5. **Assemble the recipients CSV.** One row per kept prospect, columns:
   `email, first_name, last_name, company, title, snippet1, snippet2, snippet3` where
   **snippet1 = Warm InMail 1, snippet2 = Warm InMail 2, snippet3 = Direct InMail**. Drop the suppressed emails.
   Every row must have all three snippets non-empty.

6. **Build + enroll — USE THE CLI, don't hand-build the API call.** The schema is fiddly and already encoded:
   ```
   WOODPECKER_AGENT_BUILD=on WOODPECKER_ALLOWED_MAILBOX_IDS=779855 \
   python -m leadgen.stage_campaign --recipients recipients.csv --mailbox 779855 \
     --sender-name "Vishal Sobti" --sender-title "Partnerships"
   ```
   (`--sender-name/--sender-title` fill the one template signature — set them to the **mailbox owner** so the
   signature matches the From. The copy's own sign-off is stripped automatically.)
   That runs **DRY** (nothing written). Show the operator 2–3 rendered sample sequences. On their "go", re-run with
   `--commit` to create the live DRAFT and enroll everyone (batched). It prints the campaign id.

7. **Verify on the account (read-only).** `GET /rest/v2/campaigns/<id>` → `status` is `DRAFT`,
   `email_account_ids` is `[<mailbox>]`, and there are **3 EMAIL steps**. `GET /rest/v1/prospects?campaigns_id=<id>`
   → the expected count, and `snippet1` is populated on a sample (proves per-prospect copy loaded).

8. **Hand off — the human checklist.** Before anyone presses Run: real **physical postal address** in the footer
   (replace `[REGISTERED POSTAL ADDRESS…]`), a **warmed** mailbox, a **ramp** (don't blast — `daily_enroll`
   throttles; spread multi-contact companies across days), review the low-confidence copy, send a seed test. Then a
   human presses **Run**. The agent never does.

## Hard gotchas (verified live 24 Jun 2026 — these cost several HTTP 400s to learn)
- **Snippet token in the message body** is exactly `{{SNIPPET_1 | "fallback"}}` — **underscore** in the name,
  **spaces** around the pipe, fallback in **double quotes**. The prospect **field** is `snippet1` (no underscore).
  Any other form → `400 "message contains one or more incorrect snippet, snippet fallback or spintax elements"`.
  `stage_campaign` / `build_sequence_draft` already emit the correct form — prefer them over a raw API call.
- **Unsubscribe:** set `gdpr_unsubscribe: true` in settings and let Woodpecker auto-append the link. Do **not** put a
  hand-written `{{UNSUBSCRIBE=…}}` token in the body — it 400s as a bad element.
- **Multi-step schema:** `steps` is a single nested object `START → EMAIL → EMAIL → …`; each EMAIL carries
  `followup_after: {"range":"DAY","value":N}` (the gap to the *next* step; START has none → first email is
  immediate), a `delivery_time` day-map, and `body.versions[0] = {id, version:"A", subject, message,
  signature:"SENDER", track_opens:true}`. Mailbox is set via `email_account_ids: [<id>]`. API-created campaigns
  default to **DRAFT**.
- **COQL** IN-clause limit is **100**; suppression queries run **sequentially**, never in parallel.
- **Mailbox** must be a warmed **secondary** domain in the allow-list; primary `@iksula.com` is refused by
  construction.
- **Newlines collapse → wall of text (verified live 1 Jul 2026).** Woodpecker **drops raw `\n` newlines** when it
  renders a snippet value into the HTML body, so copy that looks nicely paragraphed in the CSV arrives as one
  unbroken block in the inbox. `stage_campaign.paragraphize` fixes this automatically — it converts the author's
  blank-line breaks to `<br><br>` and single newlines to `<br>` (and, for a single-blob message with no newlines,
  segments greeting/body/CTA). Never rely on bare newlines for structure. **Still preview one rendered email on the
  first campaign** to confirm the `<br>`s render (only the Woodpecker UI shows the final render).
- **One signature, and it must match the sender.** The step template appends **one** signature + the legally
  required postal-address line (Woodpecker auto-appends unsubscribe). So the **copy must be sign-off-free** —
  `stage_campaign.strip_signoff` removes a trailing valediction (`Best,\n<name>` …) so it can't double the
  template's signature or clash names. Pass `--sender-name "<mailbox owner>" --sender-title "<title>"` so the
  signature matches the **From** address (a body signed by a different person than the sending mailbox hurts trust
  and deliverability).

## Compliance note (say this to the operator)
This operator path checks **data hygiene only — NOT lawful basis**. The sender owns permission / legitimate
interest, a working unsubscribe, and the postal address. For a **100%-US** B2B list, cold email is permitted under
CAN-SPAM *with* those three things. If the list is **not** all-US (EU/UK/India data subjects), **stop** — that needs
a recorded lawful basis we don't have (`seam-and-compliance.md`).
