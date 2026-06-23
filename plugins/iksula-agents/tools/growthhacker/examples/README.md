# growthhacker examples

Sample inputs so you can dry-run the publish gate and the seam emitter on your own
machine. **Nothing here posts anything** — the preflight only *decides*; the seam event
is written to a throwaway temp queue. The sample `action.json` is a complete, instrumented,
Scheduled organic post, so it **ALLOWs** once `GROWTH_PUBLISH=on` (turn the switch off and
it HOLDs). A named-byline reply or a paid post would HOLD until you add an approval token /
budget approval.

From the `tools/` folder (`plugins/iksula-agents/tools/`):

```bash
# PowerShell:  $env:GROWTH_PUBLISH = "on"
GROWTH_PUBLISH=on python -m growthhacker.preflight \
  --action growthhacker/examples/action.json \
  --event  growthhacker/examples/event.json
```

Expected: the publish gate returns a verdict (the sample `organic_post` is instrumented
and Scheduled, so it can ALLOW once `GROWTH_PUBLISH=on`), and the seam emit returns
`emitted` with a fresh ULID and a `non-US: company-level ONLY` lawful-basis tag (because
`region` is `DE`). See `docs/growth-hacker-agent-complete-guide.md` for the full walkthrough.
