# leadgen examples

Sample, **PII-free** inputs so you can dry-run the pre-send gate on your own machine.
Nothing here sends email; the dry-run is expected to **HALT** (the sample rows have no
lawful basis, which is correct).

From the `tools/` folder (`plugins/iksula-agents/tools/`):

```bash
python -m leadgen.preflight \
  --prospects leadgen/examples/leads.csv \
  --template  leadgen/examples/c0_body.txt \
  --subject   leadgen/examples/c0_subject.txt \
  --source    clean_sheet
```

Expected: `VERDICT: HALT` — held for `zero_eligible_records` (no row has a lawful basis),
and exit code `2`. That is the wall working as designed. See
`docs/lead-gen-agent-complete-guide.md` for the full explanation.

## Sheet → ready-to-send (AI preps, a human sends)

Turn a raw recipient sheet + email copy into a cleaned, de-duplicated,
suppression-scrubbed, merge-validated package a human imports into Woodpecker and
sends. **It never sends and never enrolls via the agent** — the human owns the send.
`dj_sheet.csv` has deliberately dirty data (a case-duplicate, a bad email, an existing
client to suppress).

```bash
python -m leadgen.sheet_to_ready \
  --recipients leadgen/examples/dj_sheet.csv \
  --subject    leadgen/examples/dj_subject.txt \
  --body       leadgen/examples/dj_body.txt \
  --suppress   leadgen/examples/dj_suppress.csv \
  --out ready_package
```
Expected: `VERDICT: READY` — 6 rows in, **3 ready**, 1 bad email + 1 duplicate + 1
suppressed dropped, merge preview clean. It writes `ready_package/` with
`recipients_ready.csv` (import this into Woodpecker), `email_copy.txt`, and
`READY_SUMMARY.md`. If any `{{field}}` would render literally, the verdict is
**NOT READY** until the copy/data is fixed.

### Straight from a Google Sheet link

Instead of `--recipients`, pass a **Google Sheet link** with `--sheet-url` — it fetches
the sheet as CSV and runs the same pipeline:

```bash
python -m leadgen.sheet_to_ready \
  --sheet-url "https://docs.google.com/spreadsheets/d/<SHEET_ID>/edit#gid=0" \
  --subject leadgen/examples/dj_subject.txt --body leadgen/examples/dj_body.txt \
  --out ready_package
```
The sheet must be shared **"Anyone with the link can view"** (or published to the web).
For a **private** sheet, either File → Download → CSV and use `--recipients`, or — in
Claude Code — just give the agent the Sheet link and it downloads it via the Google Drive
connector, then runs this tool and hands back the ready package + dropped-row report.

## Green-light path (shows the gate ALLOWing)

`leads_cleared.csv` has a lawful basis recorded on each row. With the switches on and a
**dummy** mailbox + approval token, the gate ALLOWs — proving it proceeds once the real
prerequisites exist. It still never sends (preflight only *decides*):

```bash
# PowerShell: set the two $env vars first, then run the python line.
WOODPECKER_AGENT_BUILD=on WOODPECKER_ALLOWED_MAILBOX_IDS=warm-1 \
python -m leadgen.preflight --prospects leadgen/examples/leads_cleared.csv \
  --template leadgen/examples/c0_body.txt --subject leadgen/examples/c0_subject.txt \
  --source clean_sheet --mailbox warm-1 --approved demo-approved
```
Expected: `VERDICT: ALLOW` with `eligible_count: 2`.
