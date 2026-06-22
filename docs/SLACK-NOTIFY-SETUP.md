# iKshana skill notifications — setup

GitHub Action `.github/workflows/notify-slack.yml` posts as the **iKshana** Slack bot:

1. **PR opened** -> DM to **DJ only** ("approval needed", with the review link).
2. **DJ approves the PR** -> DM to the **person who opened the PR**.
3. **PR merged (goes live)** -> post to **#ikshana-updates** (`C0B8HGW3WDR`) with the new skill's
   name and what it does (pulled from its `SKILL.md` description).

## One-time admin setup (DJ)
1. **Repo secret:** Settings -> Secrets and variables -> Actions -> add `SLACK_BOT_TOKEN` = the
   iKshana Bot User OAuth token (`xoxb-...`).
2. **Slack scopes:** `chat:write` + `im:write` (DMs). Bot must be in `#ikshana-updates`.
3. **Branch protection on `main`:** require a PR + your review, block direct pushes — so DJ stays
   the sole approver and "merged" always means "DJ approved."
4. **Handle map:** add each contributor to `.github/slack-handles.json` so their approval DM lands.
5. **Merge this to `main`** — workflows run from the base branch, so it takes effect for PRs opened
   after it's on `main`.

## Contributor note
Branch within this repo; do **not** fork (GitHub withholds the token from fork PRs).
