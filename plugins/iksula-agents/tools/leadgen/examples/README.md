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
