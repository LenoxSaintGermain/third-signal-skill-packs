---
name: youtube-data-api
description: "Upload and manage YouTube videos via the YouTube Data API v3 for automated video pipelines."
category: media
---

# YouTube Data API Pipeline

Use this skill when you need to programmatically upload videos to YouTube, update metadata (titles, descriptions, privacy status), or retrieve embed URLs for front-end integration. This is specifically useful for video generation pipelines (like NotebookLM or AI video generators) that need to pipe MP4s directly to a YouTube channel.

## Prerequisites
The user must have a Google Cloud Project with the **YouTube Data API v3** enabled and an OAuth 2.0 Client ID downloaded as `client_secret.json`.

**Dependencies:**
```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## The Auto-Publisher Watcher Pattern (Agentic Delegation)

Instead of manually running the upload script, use the `scripts/youtube_auto_publisher.py` template. This pattern watches a local `outbox/` directory for `.mp4` files, automatically authenticates (saving the session token so it runs headless after the first run), uploads the video as unlisted, and can easily be extended to patch a frontend React codebase (e.g. injecting the YouTube Embed ID into a `data.ts` file) and trigger a `git push`.

**Critical Troubleshooting:**
If the script throws `ModuleNotFoundError: No module named 'google_auth_oauthlib'` when running as a background daemon (via `nohup python3 ...`), it means the `python3` command is defaulting to the system environment rather than the environment where you installed the dependencies. **Fix:** Provide the absolute path to the active python environment (e.g., `/Volumes/.../miniconda/bin/python3`) in the `nohup` command.

## Python Implementation (Upload Video)

Here is the canonical script to execute an authenticated upload. It handles the local OAuth flow (opening a browser the first time to get a `token.json` session) and uploads the video.

```python
# ... (see templates/auto-publisher.py for the full automated directory-watching & playlist-injecting pipeline)
```

## Automated Local-to-Cloud Interceptor & Playlist Pipeline

When running a rapid-prototyping video pipeline (e.g., generating cinematic briefs via NotebookLM inside a browser), having the user manually download, rename, and upload files is an anti-pattern. Instead, deploy an automated local background daemon that watches the local environment and automates the entire cloud syndication.

### Core Architectural Pattern:
1. **Chrome Downloads Interception:** Map your real browser downloads directory (resolving any local OS symlinks, like Mac Mini storage redirection to external drives).
2. **File Normalization:** Automatically handle Chrome's default behavior of replacing spaces with underscores during file downloads (e.g. normalizing `Architecting_Alpha__The_Signal_Hunter_OS.mp4` to match clean asset IDs).
3. **Automated Playlist Syndication:** Upon successful upload, automatically create or retrieve an unlisted playlist (`youtube.playlists().insert`) and insert the new video ID.
4. **Codebase Patching & Git Push:** Programmatically update your frontend metadata file (`data.ts` or `schema.json`), commit the changes, and execute a `git push` to trigger continuous deployment (e.g. GCP Cloud Build) completely hands-free.

*(The complete, runnable implementation of this watcher is saved under `templates/auto-publisher.py` inside this skill pack).*

## Pitfalls & Notes

For zero-touch workflows, build an automator daemon using `scripts/youtube_auto_publisher.py` (accessible via this skill). The daemon watches a local outbox directory, automatically uploads any new `.mp4` to YouTube, fetches the embed URL, patches the target codebase, and automatically commits and pushes to Git to trigger cloud redeployments. Do not ask the user to manually upload files if automation is possible.

## Pitfalls & Notes
- **Zero-Touch Automation (CRITICAL)**: NEVER hand the user a script to run manually for video uploads. The user explicitly expects automated pipelines. Always wrap YouTube API uploads in an autonomous `nohup` watcher daemon that monitors an "outbox" directory, auto-uploads, patches the relevant codebase, and pushes to Git.
- **Strict Model Policy**: Never fall back to legacy `gemini-1.5` generation models, even if an SDK compatibility error occurs. Always utilize the bleeding-edge Gemini 3.x frontier models (e.g., `gemini-3.1-pro-preview` or `gemini-3.5-flash` natively). Upgrading the target SDK version in `package.json` is always preferable to reverting the model to an obsolete generation.
- **Cloud-Builder Git Overwrites (AI Studio / Lovable Sync)**: Cloud builders use one-way Git syncs. If you push code from a local environment (like LANDSAT), the cloud editor remains unaware and will silently overwrite local changes (like `data.ts`) with its older cached state on its next commit. 
  *   **Mitigation:** When a git conflict occurs after a cloud-builder push, NEVER blindly run `git pull` or `git reset --hard origin/main`. Always diff the changes (`git diff <commit> -- src/data.ts`) to ensure your custom local implementations weren't wiped out. If overwritten, use a python patch script to force-restore your logic, bypass the cloud IDE, and deploy the resulting Docker image directly to GCP Cloud Run using a standard `gcloud run services replace` configuration.

## Pitfalls & Notes
- **Privacy Status**: Always default to `unlisted` for investor data rooms or internal portfolio assets unless explicitly told to make them public.
- **Privacy Status**: Always default to `unlisted` for investor data rooms or internal portfolio assets unless explicitly told to make them public.
- **Quota**: YouTube API v3 has a strict daily quota (usually 10,000 units). An upload costs 1,600 units. You can upload ~6 videos a day on the free tier.
- **Token Expiry**: The `token.json` generated by the script will persist session auth so you don't have to log in every time.

## Templates
- `youtube_outbox_watcher.py`: A daemon script that runs in the background and automatically uploads any `.mp4` files dropped into an `outbox` directory. Load via `skill_view('youtube-data-api', 'templates/youtube_outbox_watcher.py')`.
- `notebooklm-spec.md`: A structured markdown template designed to feed Google's NotebookLM cinematic video pipeline. Use this to enforce Third Signal branding (Dark/Copper/Cyan) and focus on EBITDA/Operating Leverage when generating marketing videos. Load via `skill_view('youtube-data-api', 'templates/notebooklm-spec.md')`.