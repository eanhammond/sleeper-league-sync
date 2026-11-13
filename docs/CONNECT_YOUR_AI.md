# How to ask your AI assistant about your Sleeper league

First, finish the instructions in the [main README](../README.md) and confirm your **private** repository has a fresh `data/latest/summary.json`.

This project works with any AI assistant that can read files. The synced data is plain JSON and Markdown, so you can use ChatGPT, Claude, Gemini, GitHub Copilot, or anything else you prefer. You can also switch assistants later without changing anything in your repository.

## Connect the private repository

Most assistants can connect to GitHub, but menu names, plan requirements, and features change often and differ between accounts. Use the notes below as a starting point, and check your assistant's own help pages if something looks different.

| Assistant | Where to look | Notes |
| --- | --- | --- |
| **ChatGPT** | Settings → **Apps** or **Plugins** (the name has changed over time) → GitHub | Sign in to GitHub, then install ChatGPT's GitHub app on your account and select your private Sleeper repository. Signing in alone doesn't grant access to private repositories. On some plans, GitHub works only in deep research or agent mode. |
| **Claude** | In a chat: **+** → **Add from GitHub**. In a Project: **+** next to project knowledge → **GitHub** | Pick your private repository and the `data/latest/` files. Files added to a Project can be refreshed with the **Sync** button; files added to a single chat are a one-time copy. |
| **Gemini** | **Add file** → **More Uploads** → **Import code** (on a computer, at gemini.google.com) | Paste your private repository's URL; Gemini will offer to link your GitHub account if needed. The import is a one-time copy, so re-import in a new chat to get a fresh snapshot. |
| **GitHub Copilot** | The **Copilot** button on github.com while viewing your private repository | Copilot uses your own GitHub access, so there's no separate connection to set up. You need a Copilot plan (a free tier is available, with fewer features). |
| **Anything else** | Upload the files by hand | Download `data/latest/summary.json`, `data/latest/overview.md`, and `data/latest/league.json` and attach them to your chat. |

Whichever you choose, only grant access to the **one private Sleeper repository**, not all of your repositories. Remember that these files include other league members' information.

## Three good starter questions

These prompts work in any assistant. Replace the placeholder with your own GitHub username and repository name.

### Check whether my data is current

> Read `data/latest/summary.json` and `data/latest/league.json` from `YOUR_GITHUB_USERNAME/my-sleeper-league`. Show the exact `fetched_at_utc` time, season, NFL week, my record and roster, and the scoring rules. Tell me if the data seems stale, and do not assume the league is half-PPR or full-PPR.

### Evaluate a waiver move

> Read my newest Sleeper league snapshot from GitHub. Verify that I own the player I'd drop and that the proposed addition is unrostered. Check current NFL injuries, roles, depth charts, byes, and fantasy rankings using my league's actual scoring settings. Recommend ADD, HOLD, or WAIT with risks and confidence. If true waiver eligibility can't be confirmed from the snapshot, tell me.

### Make my starting lineup

> Read my latest roster and league scoring settings from GitHub. Compare my startable roster (not IR or taxi) against official NFL opponents, byes, injuries, usage trends, and up-to-date projections. Label each suggestion START or SIT and say how confident you are. Do not start anyone inactive or on bye.

**Tip:** Questions about current injuries and projections work best if your assistant can search the web. Turn on web search if your assistant offers it.

## Optional scheduled report

Some assistants can run a prompt on a schedule (for example, a recurring or scheduled task). If yours can, ask it to deliver a daily league brief **after** your usual morning GitHub sync. Suggested instruction:

> Every morning at 8:00 AM America/New_York, read `data/latest/summary.json` and `data/latest/overview.md` in my private repository. Report the snapshot's exact timestamp first, my team/league changes, and meaningful NFL news. If the snapshot is stale, say so clearly. Use actual scoring settings in `league.json`. Do not invent waiver availability or pretend unfinished games are final.

**Remember:** The GitHub collector and your assistant's scheduled task are **two different schedules**. Creating one does not create the other, and a GitHub refresh does not automatically generate a new message from your assistant.

## What the saved files do not prove

- They are snapshots, not live Sleeper access.
- The player directory may be cached until the next calendar day.
- A player unrostered in the saved data may still be locked or on waivers.
- Matchup scores may be in progress.
- The collector cannot make moves on your behalf.
