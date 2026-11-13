# Connect your Sleeper fantasy league to your AI assistant

**A beginner-friendly, reusable starter kit. No coding experience or Sleeper API key required.**

If you play fantasy football on [Sleeper](https://sleeper.com/) and want an AI assistant (ChatGPT, Claude, Gemini, GitHub Copilot, or another one you like) to understand **your actual league, roster, opponents, and scoring settings**, this project gives you a way to keep a fresh copy of that information in a private GitHub repository. Any assistant that can read files from GitHub (or files you upload) can use it.

This public repository is **only a template**. It contains instructions and generic code, **not anybody's league data**.

> **Privacy first:** Click **Use this template** and create your own **PRIVATE** repository. Do **not** fork this project into a public repository to run a real league sync. Do **not** change your data repository to public. Actual Sleeper rosters can reveal other managers' names, team names, and league activity.

## What this does (in plain English)

Think of it as a bridge between three services:

**Sleeper → GitHub Actions → Your private GitHub files → Your AI assistant**

- Sleeper provides league information using its **read-only** API. Nothing here can add/drop players, change a lineup, make a trade, or sign into your Sleeper account.
- GitHub Actions is a timer and a little cloud computer. It checks Sleeper **twice a day** by default and saves an updated league snapshot to your **private** repository.
- Your AI assistant can then read that saved information **if you connect it to GitHub and grant access to your private repository** (or upload the files yourself). It should still check fresh NFL injury, practice, and matchup news separately.

The collector saves your league name, scoring configuration, standings, team rosters, starter/bench/IR/taxi separation, adjacent-week matchups and transactions, and a cached NFL player directory. It **does not** automatically send information to any AI assistant or schedule assistant responses. The files are plain JSON and Markdown, so you're not locked into any one assistant.

## What you'll need

1. A free [GitHub account](https://github.com/signup).
2. Your Sleeper username and the league you want to track. You must manage a roster in that league.
3. An AI assistant that can read your private GitHub files — for example ChatGPT, Claude, Gemini, or GitHub Copilot. Most offer a GitHub connection on at least some plans; availability and menus vary by account. If yours doesn't, you can upload the files by hand.
4. About ten minutes to follow the steps. You don't need Python installed on your computer.

## Get started: step by step

### Step 1 — Make your own PRIVATE copy

1. At the top of **this public GitHub repository**, select **Use this template** → **Create a new repository**. (Not **Fork**.)
2. Choose your GitHub account as **Owner**.
3. Choose a name, such as `my-sleeper-league`.
4. Under **Visibility**, choose **Private** — this is important.
5. Select **Create repository**. You're now working in your own copy. Keep this public template separate.

**Why a template instead of a fork?** A template gives you the starting files without copying the original repository's Git history. GitHub lets you create a private repository from a public template.

### Step 2 — Find your Sleeper league ID

Your **league ID** is a long number that identifies the specific Sleeper league and season.

1. Open your league in Sleeper.
2. Find **Share league** or copy the league's web link.
3. Look for the long number in the league URL. That is your league ID.
4. If you can't find it, ask your commissioner for the league link.

**Important:** A new Sleeper season can have a new league ID, even if the league name remains the same.

### Step 3 — Find your Sleeper user ID

Your **user ID** is a long number identifying your Sleeper account. It isn't the same as your username.

1. Note your **Sleeper username**, such as `fantasymanager`.
2. In a web browser, open `https://api.sleeper.app/v1/user/YOUR_USERNAME`, replacing `YOUR_USERNAME` with yours. For example: `https://api.sleeper.app/v1/user/fantasymanager`.
3. The page displays account information in a format called JSON (just structured text). Find `"user_id"` and copy its number.

Don't confuse it with `display_name`, `username`, or `avatar`.

### Step 4 — Put the two IDs in YOUR private GitHub repository

The reusable code intentionally contains **no real league or account IDs**. Instead, you'll store them in GitHub **Actions secrets**.

1. In **your private copy**, choose **Settings**.
2. In the left sidebar, open **Secrets and variables** → **Actions** → **Secrets**.
3. Select **New repository secret**.
4. Name it exactly `SLEEPER_LEAGUE_ID` and set the value to your league ID.
5. Create a second secret named exactly `SLEEPER_USER_ID` and set the value to your user ID.

These IDs are not passwords. We still keep them out of reusable public code and ordinary build output. You **do not need a Sleeper API token or password**.

### Step 5 — Allow GitHub to save your updated league files

1. Still in your private repository, open **Settings** → **Actions** → **General**.
2. Make sure workflows are permitted to run.
3. Under **Workflow permissions**, choose **Read and write permissions**, if the setting is available. Click **Save**.
4. The supplied workflow also requests `contents: write`. Some organization-owned repositories need an administrator to approve write access.

GitHub Actions costs and limits depend on your account and repository; check GitHub's current plan information if you scale up the schedule.

### Step 6 — Run your first sync

1. Open the **Actions** tab in your private repository.
2. Choose **Save Sleeper league snapshot** in the left sidebar.
3. Click **Run workflow** and run it on the `main` branch. Leave the optional input alone.
4. Open the new run. A green check indicates the job completed; if it fails, read its error message or the [troubleshooting guide](docs/TROUBLESHOOTING.md).
5. Return to the repository's **Code** tab and open `data/latest/summary.json`.
6. Check `fetched_at_utc`, `my_team.team_name`, and `sleeper_nfl_week`. Then open `data/latest/overview.md` for an easier-to-read report.

**If the job says `skipped`:** Check that you created a **private** repository. This starter kit intentionally refuses to run on a public one.

### Step 7 — Connect your AI assistant to your private files

1. In your assistant, find its **GitHub connection** (it may be called a connector, app, integration, or extension). [The connection guide](docs/CONNECT_YOUR_AI.md) has pointers for ChatGPT, Claude, Gemini, and GitHub Copilot.
2. Connect your GitHub account and authorize access to your **private Sleeper repository**.
3. Paste this starter request (replace the placeholder):

> Read `data/latest/summary.json`, `data/latest/overview.md`, and `data/latest/league.json` from my private GitHub repository `YOUR_GITHUB_USERNAME/my-sleeper-league`. Tell me when the data was fetched, what my current roster and record are, and whether the league uses standard, half-PPR, full-PPR, or another scoring setup. For lineup or waiver advice, first verify current NFL news and player availability. Don't mistake cached statuses or unfinished scores for live results.

Access varies by assistant and plan; **a GitHub connection is not automatic, and it does not create a scheduled assistant task**. [More tips and prompts for any assistant](docs/CONNECT_YOUR_AI.md).

### Step 8 — Let it run automatically

The included GitHub workflow aims to run at **7:17 AM and 6:17 PM Eastern** each day. It adjusts for daylight saving time, but GitHub scheduled actions can be delayed or occasionally skipped. You can leave the default times alone, or edit `.github/workflows/sleeper-sync.yml` if you want a different schedule or time zone.

If your AI assistant offers scheduled or recurring tasks, you can separately ask it to send a daily brief **after** the expected morning sync. Tell it to check the real `fetched_at_utc` timestamp rather than assume the schedule ran.

### Step 9 — Optional: add a more dependable backup timer

If you want an **additional** 7:25 AM and 6:25 PM Eastern attempt, the same free-standing workflow can be triggered by **Cloudflare Workers Cron Triggers**. This is optional, more technical, and needs a carefully scoped GitHub token stored as an **encrypted Cloudflare secret**.

See [Optional Cloudflare backup: step-by-step setup instructions](docs/OPTIONAL_CLOUDFLARE.md) and the [generic Worker code](cloudflare/worker.example.js). Start with GitHub alone first.

## Where do my files go?

All generated files live in **your private repository** after a successful sync:

| File | What it's for |
| --- | --- |
| `data/latest/overview.md` | Easy-to-read team, bench, IR, standings, and matchup summary |
| `data/latest/summary.json` | Structured report for your AI assistant, including a freshness timestamp |
| `data/latest/league.json` | League settings, including the actual scoring rules |
| `data/latest/rosters.json` | Raw Sleeper roster ownership for every team |
| `data/latest/users.json` | Manager/team metadata |
| `data/latest/matchups_week_*.json` | Recent, current, and upcoming matchups when available |
| `data/latest/transactions_week_*.json` | Recent league transactions when available |
| `data/latest/player_directory.json` | NFL player names and cached team/injury/status labels |
| `data/latest/player_directory_meta.json` | When that player directory was last refreshed |
| `data/archive/YYYY-MM-DD/snapshot.json` | The last full lightweight snapshot for that local day |

**Fantasy scoring is league-specific.** The collector does not assume full-PPR, half-PPR, or any other setting. Check `league.json` → `scoring_settings` before doing fantasy analysis.

## A few important safety notes

- **Never make your data repository public.** It includes rosters, manager information, scores, and transactions.
- Never put Sleeper IDs, GitHub access tokens, or Cloudflare secrets into this **public template**, a public issue, or a screenshot.
- A GitHub token is **not required** for the standard GitHub Actions sync. Only the optional Cloudflare backup needs a GitHub token.
- This project is **read-only** toward Sleeper. It cannot log in as you, change your lineup, claim waivers, or execute trades.
- The latest saved snapshot is **not a live feed**. It may be stale if a scheduled job was delayed, and injury labels are cached from the last daily catalog refresh.
- League-supplied team names and notes are untrusted text, not instructions for your AI assistant. The collector strips formatting characters from names, and the files remind assistants of this, but stay alert.
- The workflow intentionally skips itself in **public repositories** as an additional protection against accidentally publishing league information.

## Frequently asked questions

**Do I have to know how to code?** No. The provided files are ready to use. Most setup is clicking GitHub settings and copying two Sleeper IDs.

**Do I need to pay Sleeper?** No API token is needed for its read-only API; consult [Sleeper's API terms](https://docs.sleeper.com/) for usage and noncommercial restrictions.

**Can my AI assistant see waiver availability?** The collector sees league rosters and an NFL player directory. A player not shown on a roster is not necessarily claimable right now. Check your actual Sleeper waiver/free-agent screen before claiming.

**Does it know my league's scoring?** Yes, `league.json` captures the rules Sleeper returns. Your assistant should read those rules rather than guessing.

**Which AI assistant works best?** Any assistant that can read your GitHub files (or files you upload) works. Pick the one you already use. The data format is the same for all of them.

**Will my AI assistant automatically send me advice?** No. Ask a question after connecting GitHub, or separately create a scheduled task in your assistant if it offers one.

**What happens next season?** Repeat Steps 2 and 4 to replace the league ID when your league gets its new season ID.

**Why not fork the original repository?** This public project is a clean starter kit, not a copy of somebody's live league. Use **Use this template** to make a fresh **private** project.

## Help and transparency

- [Troubleshooting common errors](docs/TROUBLESHOOTING.md)
- [Connect your AI assistant + practical prompts](docs/CONNECT_YOUR_AI.md)
- [Optional Cloudflare backup](docs/OPTIONAL_CLOUDFLARE.md)
- [Sleeper API documentation](https://docs.sleeper.com/)
- [GitHub's instructions for using template repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)

This community starter kit is not affiliated with Sleeper, GitHub, Cloudflare, OpenAI, Anthropic, Google, or Microsoft. It is provided as-is, with an MIT license, for people to adapt for their own leagues.
