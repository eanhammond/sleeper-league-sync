# Troubleshooting

Open your **private** repository → **Actions** → **Save Sleeper league snapshot**, then click the most recent run to see what went wrong.

| What you see | What to check |
| --- | --- |
| Job says **skipped** | Make sure your repository is **Private**. The public template skips real syncs on purpose. |
| `Missing SLEEPER_LEAGUE_ID` | Add the Actions secret with exactly that name, in **your private repository**. |
| `Missing SLEEPER_USER_ID` | Add the second Actions secret. |
| `This Sleeper user does not own a roster` | Check that the user ID belongs to your own account in the selected league and season. |
| `Unable to retrieve required Sleeper endpoint` | Check the IDs, internet/API availability, and whether the league exists for the selected season. |
| `Unable to save snapshot` or permission denied | Check **Settings → Actions → General → Workflow permissions** and repository branch protection. |
| No `data/latest/` folder | Check that the **full job completed** and that GitHub committed the files, not just that a run was queued. |
| Scheduled run did not happen on time | GitHub scheduled jobs can start late or be skipped. Run manually or consider the optional Cloudflare backup. |
| Your AI assistant can't see your private repository | Check that its GitHub connection is installed and authorized for the right repository (on GitHub, also check **Settings → Applications** for the assistant's app and its repository access). It may not be available on every plan. You can always upload the files by hand instead. |
| Wrong fantasy scoring assumption | Ask your AI assistant to read `data/latest/league.json` → `scoring_settings` before giving rankings or recommendations. |
| Player looks on bench but is actually IR | Check `summary.json` → `my_team` → `reserve` and `my_team` → `taxi`; both are excluded from `my_team` → `bench`. |
| Injury news is outdated | `player_directory.json` is cached daily. Verify latest official NFL news separately. |
| You changed seasons | Update the `SLEEPER_LEAGUE_ID` Actions secret to the new season's league ID. |

## Safety reminder

Don't paste GitHub token values or screenshot a secrets page with an exposed secret. Do not post `data/latest/*.json` from a family or private league in a public issue. If you're asking for help publicly, share the error message **after removing account IDs, league IDs, and manager names**.

## Why two different timestamps?

`summary.json`'s `fetched_at_utc` is the league snapshot time. `player_directory_meta.json`'s `refreshed_at_utc` records the last time the large NFL player catalog was refreshed. The catalog is intentionally cached, so it may be older than the league snapshot.

## Changing the schedule or time zone

Edit `.github/workflows/sleeper-sync.yml`. The default is **7:17 AM and 6:17 PM America/New_York**. Change both the cron and `timezone` if desired. Also change the `REPORT_TIMEZONE` environment variable in that workflow if you want archive folders named according to your own local calendar date. This is optional; it only affects the archive date and player-cache date, not NFL game scheduling.
