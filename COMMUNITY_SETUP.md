# Community features: deployment and editorial guide

## One-time setup

1. Create **Amankesarwani2202/endangered-oceans-atlas-data** as a **private** repository and initialise it with a README (so the `main` branch exists). Do not put drafts in the public code repository. The app refuses a public data repository.
2. Create a fine-grained GitHub token scoped to **only that data repository**, with **Contents: read and write** and metadata read access. Keep the token out of chat, code and commits. Give it an expiration date and rotate it before expiry.
3. In the hosted app's **Settings → Secrets**, paste the structure in `.streamlit/secrets.toml.example`, replace the token and choose a long random editor password. Locally use `.streamlit/secrets.toml` (ignored by git).
4. Deploy this branch with `Home.py` as entry point. Submit a test answer, open **Editor**, sign in, approve it and confirm it appears on Contributors. Test rejection and CSV export too. No data repo is needed for Map, Species, Analysis or Newsletters.

The app creates `submissions/YYYY-MM/<random-id>.json` on demand. Each answer is a separate file to avoid simultaneous visitors overwriting one shared JSON file. Decisions use GitHub's current file SHA, so stale editor saves fail rather than overwrite another decision. Refresh and try again on conflict. A failed request is never shown as a successful submission. Retrying the unchanged form in the same session reuses its ID.

## Monthly questions

Edit `content/questions.json`: keys are `YYYY-MM` and values are questions. Preload future questions if desired; the app automatically selects the current month in **Asia/Kolkata**. Without a configured question for a month, submissions close and archived questions remain available. Questions should not be edited after collecting answers: each answer also preserves the question it answered. Add a new month instead.

## Review and newsletter workflow

1. In **Editor**, choose the month and review pending answers. Approve useful contributions or reject spam. Only approved, consenting submissions appear in the public feed.
2. At month end, download **ALL submissions** for editorial review. This includes pending and rejected records with their statuses; it is not publication-ready.
3. Resolve pending decisions and download the **approved answers** CSV for the Canva newsletter. Include approved answers with contributor credit; never silently publish rejected content. The CSV neutralises spreadsheet formulas; remove any leading protective apostrophe in a display name before using it as newsletter text.
4. Design and proofread the newsletter in Canva. This implementation does not operate Canva or automatically publish on a schedule.
5. Add a Canva **view-only HTTPS link** to `content/newsletters.json`, for example:

```json
[
  {
    "month": "2026-10",
    "title": "Ocean Voices — October 2026",
    "description": "Our community's ideas for marine conservation.",
    "url": "https://www.canva.com/design/YOUR_DESIGN/view"
  }
]
```

Alternatively commit a PDF in `content/newsletters/` and add `"pdf": "ocean-voices-2026-10.pdf"` to the issue. Use only the filename, not an absolute path. Both PDF and link may be supplied. Commit the manifest/PDF update to publish it on the website.

## Add animals every few weeks

The scholar can now sign in to **Editor → Manage species**, complete **New animal profile**, check the research confirmation and click **Publish species**. This can be done weekly or every few weeks; there is no fixed limit or automatic publication schedule.

Required fields include species name, emoji, supported threat status, ocean/region, sample coordinates, population estimate, threats, conservation actions, how visitors can help, fun fact, an HTTPS source link and a source review date. If population is uncertain, say Unknown rather than inventing a number. The source link and review date appear on directory cards. Verify facts against dated authoritative sources; the app checks field formats but cannot verify scientific accuracy.

Published additions are saved to `atlas/species.json` in the existing **private data repository**, using the same token and Secrets. The original 15 profiles stay in the code repository's `content/species.json`; the app combines both sets. No extra permissions, code edits, redeployment or Streamlit reboot are needed for each new species. Home, Map, Species and Analysis read the additions when opened or refreshed. A browser page already open must be refreshed.

The form lists existing species and rejects duplicate names, invalid coordinates, missing fields and invalid source links. Writes use the catalogue SHA the editor originally loaded. If another editor publishes first, use **Reload catalogue** and try again; stale writes cannot overwrite another publication. The form currently adds profiles, rather than editing or deleting existing entries. Do not manually add the same species to both datasets. Keep regular backups through git history.

If storage is unavailable or the remote catalogue is invalid, public pages show a warning and the bundled original atlas; additions return when access is restored. Publishing is blocked while the catalogue cannot be loaded safely. The app reads one catalogue file per page visit and does not cache it, so newly published animals become visible on the next visit. This uses GitHub API quota; migrate storage if traffic grows.

## Operational limits

This is for a small, moderated educational project. Each monthly feed read fetches individual GitHub files and uses API quota. Do not use it for high traffic; migrate to a suitable database/object store as submissions grow. The app fails explicitly rather than displaying an incomplete archive at GitHub's 1,000-file directory limit. Private repository history retains prior versions: rejecting an answer hides it from the feed but does not erase it from git history.

The editor uses a shared password, a one-hour session and a session-level login delay. Contributor cooldown is also session-level and can be bypassed by a new session. These are not identity verification or comprehensive anti-spam protection. For a wider public launch, add identity-based editor authentication and server-side rate limiting/CAPTCHA. No private email or contact field is collected. The publication consent text includes the public display fields and newsletter; use your project's applicable consent process for younger students.

Local smoke checks: `python -m unittest discover -s tests` and `python -m compileall -q Home.py data.py community.py pages`. The live private-repository integration must be checked after Secrets are configured.
