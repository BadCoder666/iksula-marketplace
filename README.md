# Iksula Marketplace

The internal marketplace for Iksula's Cowork skills and agents. Subscribe once and
your team receives the firm's standard-compliant skills — and every future update —
through Cowork's plugin system. No re-sharing files.

> **New here? Start with [`docs/COLLEAGUE-GUIDE.md`](docs/COLLEAGUE-GUIDE.md)** — the
> complete guide to the agentic architecture: the vision, connecting to the Brain, and
> creating, updating, and using skills.

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

## Governance

This is a governed repository. Anyone may **propose** changes via pull request;
only **maintainers** merge to `main`. See `CONTRIBUTING.md` for the Iksula skill
authoring standard every new or edited skill must meet, and `plugins/iksula-agents/SKILL-TEMPLATE.md`
for a compliant starting point.
