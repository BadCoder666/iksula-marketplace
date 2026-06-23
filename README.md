# Iksula Marketplace

The internal marketplace for Iksula's Cowork skills and agents. Subscribe once and
your team receives the firm's standard-compliant skills — and every future update —
through Cowork's plugin system. No re-sharing files.

> **New here? Start with [`docs/COLLEAGUE-GUIDE.md`](docs/COLLEAGUE-GUIDE.md)** — the
> complete guide to the agentic architecture: the vision, connecting to the Brain, and
> creating, updating, and using skills.
>
> **Complete plain-English guides to the two execution agents** (what they are, how they
> were made, how to set them up and run them, every capability, and every connected tool —
> no technical background needed):
> **[Growth Hacker](docs/growth-hacker-agent-complete-guide.md)** ·
> **[Lead Gen](docs/lead-gen-agent-complete-guide.md)** (branded PDF versions sit alongside in `docs/`).

## For consumers — install in 2 steps

1. Add the marketplace (one time):

   ```
   /plugin marketplace add https://github.com/BadCoder666/iksula-marketplace.git
   ```

2. Install the plugin from the `/plugin` menu, or:

   ```
   /plugin install iksula-agents@iksula-marketplace
   ```

When maintainers publish a new version, you receive it through the same subscription.

## What's inside

### `iksula-agents` plugin
The agentic-org skills (Product/Offering + Commercial):

| Skill | What it does |
|-------|--------------|
| `vertical-process-mapping` | Maps an industry vertical's functions (L1/L2/L3) and scores post-LLM automation opportunities into a 6-tab workbook + solution roadmap. |
| `solutions-architect-create` | Turns a diagnosed opportunity into a packaged, sellable solution — intro deck + client pitch deck. |
| `research-solutions` | Deep-dives a shortlisted opportunity (market sizing, competitor teardown, buyer evidence) and writes competitive intel back to the Brain. |
| `thought-leadership` | Produces opinion-led, bylined thought-leadership articles that build authority with senior buyers. |
| `content-creator` | The central content engine — atomizes a hero asset into a multi-format, multi-channel campaign + publishing calendar. |
| `media-planner` | Turns a hero asset into a distribution brief and a costed media plan across channels. |
| `growth-hacker` | Executes the publishing calendar on the online/1-to-many channel — publishes native, runs distribution + A/B experiments, drafts voice-governed community replies, captures raw performance to the Brain, and surfaces content-sourced interest to Lead Gen (never qualifies). |
| `lead-gen` | The one demand-capture funnel across all four channels: capture → de-anonymize (geo-gated) → qualify (MQL→SQL) → nurture → ABM → convert, routing SQLs to Sales (new) or KAM (existing clients), with compliance gates enforced before every send. |
| `pranaam` | Session bootstrap — connects this Claude instance to the iKshana Brain/Spine and loads the operating rules, so every later skill reads the Brain on demand. |

## Run the execution toolkits on your machine

The `growth-hacker` and `lead-gen` skills are backed by small Python "toolkits" that
**enforce** the safety rules in code — the agent literally cannot send, post, or leak
prospect data. They live in [`plugins/iksula-agents/tools/`](plugins/iksula-agents/tools/),
and everything you need to run them on **your own** system is in this repo.

**Prerequisites:** Claude Code with the plugin installed (the 2 steps above) · **Python 3.9+** ·
`git clone https://github.com/BadCoder666/iksula-marketplace` to get the toolkit files locally.

**Nothing sends or posts by default.** Every switch is OFF until you turn it on, and the
gates HALT until the real prerequisites (lawful basis, a warmed mailbox, a human approval)
exist. A dry-run that HALTs is the system working — not an error.

### 1. Set your environment (your OWN accounts — never anyone else's)
Copy the variable **names** from [`plugins/iksula-agents/tools/.env.example`](plugins/iksula-agents/tools/.env.example)
and set real values in your shell. **Never commit secrets** — they are gitignored.

| Variable | For | Default |
|---|---|---|
| `WOODPECKER_API_KEY` | your Woodpecker account's API key | (unset) |
| `WOODPECKER_AGENT_BUILD` | Lead-Gen build switch | `off` |
| `WOODPECKER_ALLOWED_MAILBOX_IDS` | warmed mailbox ids the agent may use | (empty) |
| `GROWTH_PUBLISH` | Growth-Hacker publish switch | `off` |

### 2. Connectors you set up with your OWN accounts
- **Google Drive** (the Brain/Spine) via your `@your-workspace` account — the `pranaam` skill connects + verifies it.
- **Zoho CRM** (your org) via the native Zoho MCP server or an OAuth Self-Client — never a shared password.
- **Woodpecker** (your account) — API key in `WOODPECKER_API_KEY`.
- **Slack** (your workspace) — for the human-approval gate.
- **Apollo / BuiltWith / dialer / etc.** — your own logins, used by the operator.

### 3. Dry-run + safety tests (from the `tools/` folder)
```bash
cd plugins/iksula-agents/tools

# Lead Gen — pre-send gate over sample data (expect HALT: the samples have no lawful basis):
python -m leadgen.preflight --prospects leadgen/examples/leads.csv \
  --template leadgen/examples/c0_body.txt --subject leadgen/examples/c0_subject.txt --source clean_sheet

# Growth Hacker — publish gate + seam emit over samples:
GROWTH_PUBLISH=on python -m growthhacker.preflight \
  --action growthhacker/examples/action.json --event growthhacker/examples/event.json

# Safety tests (52 total, no network, no live account):
python -m unittest leadgen.tests.test_safety
python -m unittest growthhacker.tests.test_safety
```
On Windows PowerShell, set switches with `$env:GROWTH_PUBLISH = "on"` before the command.

**Full instructions** — setup, running, every capability, every connected tool, and the
guardrails — are in the per-agent guides in [`docs/`](docs/).

## Governance

This is a governed repository. Anyone may **propose** changes via pull request;
only **maintainers** merge to `main`. See `CONTRIBUTING.md` for the Iksula skill
authoring standard every new or edited skill must meet, and `plugins/iksula-agents/SKILL-TEMPLATE.md`
for a compliant starting point.
