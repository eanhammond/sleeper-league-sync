// OPTIONAL backup clock for GitHub Actions.
// Copy this into a Cloudflare Worker, never put a token in the source.
// Configure TWO UTC cron triggers in the Cloudflare dashboard:
//   25 11,12 * * *   (7:25 AM America/New_York year round)
//   25 22,23 * * *   (6:25 PM America/New_York year round)
// Set encrypted Secret GITHUB_ACTIONS_TOKEN and two plain variables:
//   GITHUB_OWNER = your GitHub user/organization
//   GITHUB_REPO  = the PRIVATE repository created from this template
export default {
  async fetch() {
    // Visiting the public Worker URL is not a sync trigger.
    return new Response("Not found", { status: 404 });
  },

  async scheduled(controller, env) {
    const easternTime = new Intl.DateTimeFormat("en-GB", {
      timeZone: "America/New_York",
      hour: "2-digit",
      minute: "2-digit",
      hourCycle: "h23",
    }).format(new Date(controller.scheduledTime));

    if (easternTime !== "07:25" && easternTime !== "18:25") {
      console.log("Skipped: not a scheduled Eastern sync time.");
      return;
    }

    const owner = String(env.GITHUB_OWNER || "").trim();
    const repo = String(env.GITHUB_REPO || "").trim();
    if (!/^[A-Za-z0-9-]+$/.test(owner) || !/^[A-Za-z0-9._-]+$/.test(repo)) {
      throw new Error("Set valid GITHUB_OWNER and GITHUB_REPO Worker variables.");
    }
    if (!env.GITHUB_ACTIONS_TOKEN) {
      throw new Error("Missing GITHUB_ACTIONS_TOKEN encrypted Worker secret.");
    }

    const endpoint = `https://api.github.com/repos/${owner}/${repo}/actions/workflows/sleeper-sync.yml/dispatches`;
    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        Authorization: "Bearer " + env.GITHUB_ACTIONS_TOKEN,
        Accept: "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
        "User-Agent": "sleeper-league-sync-backup",
      },
      body: JSON.stringify({
        ref: "main",
        inputs: { trigger_source: "cloudflare-worker" },
      }),
    });
    if (!response.ok) {
      // Do not log response body, request headers, or the token.
      throw new Error("GitHub dispatch failed. HTTP " + response.status);
    }
    console.log("GitHub accepted workflow dispatch. HTTP " + response.status);
  },
};
