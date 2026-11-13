# Optional: Cloudflare as an extra backup timer

**Start with the basic GitHub Actions sync in the [main README](../README.md).** Only use this optional setup after you've confirmed a manual sync succeeds in your **private** repository.

## Why add Cloudflare?

Sometimes GitHub schedules a run later than the exact minute you wanted, or does not start it at all. Cloudflare Workers can send GitHub a separate request to run the existing workflow, without storing any Sleeper data in Cloudflare. It improves the odds that the job starts on time, but GitHub can still be delayed or fail.

This extra timer is **not required** for the basic setup. It uses a short-lived GitHub access token, so there is a little more maintenance.

## Before you begin

- Have a **PRIVATE** GitHub repository from this public template.
- Confirm a manual **Save Sleeper league snapshot** Action succeeds.
- Have a Cloudflare account with Workers available.
- Know your GitHub username/organization and your private repository name.
- Never enter tokens into the public README, source code, chat, or screenshots.

## Step 1 — Create a narrowly scoped GitHub token

1. Open [GitHub fine-grained personal access tokens](https://github.com/settings/personal-access-tokens).
2. Create a new token for your own GitHub account.
3. Under **Repository access**, choose **Only select repositories**, and select **only your private Sleeper data repository**.
4. Under **Repository permissions**, allow **Actions: Read and write**. GitHub may add mandatory **Metadata: Read-only**.
5. Give it an expiration date (for example, 90 days), and put a calendar reminder one week before expiration.
6. Keep the actual token private. It should **never** be committed to GitHub.

This token can dispatch workflows in that private repository; restrict it carefully and protect your GitHub and Cloudflare accounts with multi-factor authentication. Revoke and replace it if you think it was exposed.

## Step 2 — Create one Cloudflare Worker

1. Open [Cloudflare dashboard](https://dash.cloudflare.com/) → **Workers & Pages**.
2. Create a Worker, perhaps named `sleeper-sync-backup`.
3. Open **Edit code**. Replace the starter Worker code with the contents of [`cloudflare/worker.example.js`](../cloudflare/worker.example.js).
4. Click **Deploy**.
5. The code's `fetch()` function returns **Not found (HTTP 404)** for an ordinary browser visit. **This is intentional**, not a failure. Only Cloudflare's scheduled handler triggers GitHub.

## Step 3 — Add one encrypted secret and two ordinary variables

In your Worker, open **Settings → Variables and Secrets**:

| Name | Type | Value |
| --- | --- | --- |
| `GITHUB_ACTIONS_TOKEN` | **Secret** (encrypted) | Your fine-grained GitHub token |
| `GITHUB_OWNER` | Variable (plain text) | Your GitHub username or organization |
| `GITHUB_REPO` | Variable (plain text) | Your **private** Sleeper data repository name |

Deploy/save the changes. Do not put the token in an ordinary plaintext variable.

## Step 4 — Add the two scheduled triggers

Cloudflare Cron Triggers use **UTC**. For these Eastern-time backups, add **two separate triggers** at **Settings → Trigger events → Cron triggers**:

```text
25 11,12 * * *
25 22,23 * * *
```

The Worker code checks `America/New_York` so only one UTC attempt from each pair actually sends the GitHub request. The other one is intentionally skipped.

| Target Eastern time | While Eastern is on daylight time | While Eastern is on standard time |
| --- | --- | --- |
| 7:25 AM | 11:25 UTC | 12:25 UTC |
| 6:25 PM | 22:25 UTC | 23:25 UTC |

Cloudflare's dashboard shows the two UTC hours, not the single Eastern time. Both lines are needed for daylight saving time. Wait for changes to propagate.

## Step 5 — Check whether it worked

1. After a scheduled time, look for a run called **`Sleeper sync (cloudflare-worker)`** in your private repository's **Actions** tab.
2. Open the run and confirm it completed successfully. The Worker dispatch being accepted is not enough.
3. Open `data/latest/summary.json` and confirm its `fetched_at_utc` is after that dispatch.
4. You can check Cloudflare **Observability / Trigger events** for messages such as `GitHub accepted workflow dispatch. HTTP 204` or `Skipped: not a scheduled Eastern sync time.`

You can leave **Workers Traces** disabled; basic Worker logs are sufficient for this use. The public Worker URL returning `Not found` is expected.

## Important maintenance

- The GitHub token expires. **Renew it before the chosen expiration date** and update the Cloudflare `GITHUB_ACTIONS_TOKEN` secret. You do not need to change the schedule when rotating it.
- A Worker error may not automatically notify you or retry. Check GitHub's run history or consider monitoring stale snapshots.
- The original GitHub-native schedule continues independently. Don't remove it until the external backup has proved reliable over multiple days.
- This is a generic example. Use your **own** GitHub owner/repository names; do not point it at anyone else's league.
