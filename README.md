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
   /plugin marketplace add <git-url-of-this-repo>
   ```

2. Install the plugin from the `/plugin` menu, or:

   ```
   /plugin install iksula-agents@iksula-marketplace
   ```

When maintainers publish a new version, you receive it through the same subscription.

## What's inside

### `iksula-agents` plugin
The four commercial-pipeline agents:

| Skill | What it does |
|-------|--------------|
| `vertical-process-mapping` | Maps an industry vertical's functions (L1/L2/L3) and scores post-LLM automation opportunities into a 6-tab workbook + solution roadmap. |
| `solutions-architect-create` | Turns a diagnosed opportunity into a packaged, sellable solution — intro deck + client pitch deck. |
| `thought-leadership` | Produces opinion-led, bylined thought-leadership articles that build authority with senior buyers. |
| `content-creator` | The central content engine — atomizes a hero asset into a multi-format, multi-channel campaign + publishing calendar. |

## Governance

This is a governed repository. Anyone may **propose** changes via pull request;
only **maintainers** merge to `main`. See `CONTRIBUTING.md` for the Iksula skill
authoring standard every new or edited skill must meet, and `plugins/iksula-agents/SKILL-TEMPLATE.md`
for a compliant starting point.
