# For the template publisher: how to put this starter kit on GitHub

This page is for the person publishing the **public starter project**. Everyone else should begin with the main [README](README.md) and choose **Use this template**.

## Before publishing

- This folder is a fresh, generic starter kit. **Do not use your existing private league repo as the public repository.** Keep it private.
- Verify that this public folder does **not** include a `data/` directory, credentials, `.env` files, real Sleeper IDs, private screenshots, or real league histories.
- Read the bundled MIT license; replace it with your preferred license if you want different sharing terms.

## Publish through GitHub's website

1. Unzip the downloaded starter kit on your computer.
2. Visit [github.com/new](https://github.com/new) while signed in.
3. Choose a name such as **`sleeper-league-sync`**.
4. Add a description such as **`A beginner-friendly, privacy-conscious guide to syncing Sleeper league data to a private GitHub repo for any AI assistant (ChatGPT, Claude, Gemini, Copilot).`**
5. Choose **Public**. (This is the **template**, not your real data repository.)
6. Create the empty repository **without** adding another README, `.gitignore`, or license, because this kit already contains them.
7. On the new repo's Quick Setup screen, select **uploading an existing file**, or use **Add file → Upload files**.
8. Upload the **contents of the extracted folder**, keeping the directory names intact, including the hidden `.github/workflows` directory. **Do not upload the ZIP as a single file.**
9. Select **Commit changes**.
10. Check that GitHub shows `README.md`, `scripts/sync_sleeper.py`, and `.github/workflows/sleeper-sync.yml` in the correct locations.

**On Mac:** `.github` begins with a dot and may be hidden in Finder. Press **Command + Shift + .** to toggle hidden files. If uploading folders in your browser does not preserve the layout, create the workflow file manually through GitHub's **Add file → Create new file** using the full filename `.github/workflows/sleeper-sync.yml` and paste the contents from the extracted file. Repeat as needed for other nested files. GitHub Desktop can also publish the whole extracted folder while preserving its structure.

## Turn it into a template

1. On the **new public repository**, open **Settings**.
2. Under **General**, find the **Template repository** checkbox.
3. Turn it on. Visitors should now see **Use this template** above the file list.
4. Consider turning off GitHub Actions **in the public template**, since the public repo is only for sharing code. Anyone who creates a **private copy** can enable Actions there using the README. The included workflow has an additional guard that skips in public repositories.

## What to test

- Open the README as someone who knows nothing about GitHub or code. Can they find the **Use this template** button and understand why their copy must be **Private**?
- Create a disposable **private** repository from the public template. Confirm `.github/workflows/sleeper-sync.yml` exists, the **Actions** tab appears when enabled, and the two Sleeper ID secrets can be added.
- A real end-to-end live test would require your own league IDs; keep any test output in that **private** disposable repository only.
- Once everything looks right, share the **public** repository URL, not any private league-data URL.

## Keep this project safe

Whenever updating public instructions, transfer only generic changes. Do not copy a file from a working private league project into this public repository without reviewing it carefully for identifying data and credentials.
