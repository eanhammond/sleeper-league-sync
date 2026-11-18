# Changelog

## 2026-11-17 — Playoff fixes and updates

- Updated `actions/checkout` and `actions/setup-python` to `v7` (GitHub Actions runners no longer provide Node 20).
- Playoff byes and eliminated teams no longer get paired with a random "opponent." Matchups now include `has_matchup`, and `overview.md` says "no matchup" for those weeks.
- Records show ties when a team has any, and standings count a tie as half a win. The summary field is renamed `standings_by_record_then_points`.
- The player directory now includes NFL team defenses (`DEF`), so waiver questions about defenses work.
- Collector User-Agent is now `SleeperLeagueSyncTemplate/1.2`.

## 2026-11-13 — Works with any AI assistant

- Renamed the project to "Connect your Sleeper fantasy league to your AI assistant." It no longer favors ChatGPT.
- Replaced `docs/CONNECT_CHATGPT.md` with `docs/CONNECT_YOUR_AI.md`, which covers ChatGPT, Claude, Gemini, GitHub Copilot, and manual upload.
- Made the README, troubleshooting, and publishing guide assistant-neutral.
- Changed the collector's User-Agent to `SleeperLeagueSyncTemplate/1.1`.

## 2026-11-13 — Public starter template

First public-ready, anonymous release of the Sleeper → private GitHub → ChatGPT guide. Includes a generic read-only collector, private-repository-only workflow, optional Cloudflare backup, beginner instructions, and troubleshooting notes.

No actual Sleeper account, league, user, GitHub token, Cloudflare token, or archived league snapshots are included.
