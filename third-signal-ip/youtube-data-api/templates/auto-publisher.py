import os
import sys
import time
import json
import re
import shutil
import subprocess
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]
PIPELINE_DIR = "/Volumes/Mini_2T/lenoxparis data/Dev/Investor-hub/landsat-bridge/youtube-pipeline"
OUTBOX_DIR = os.path.join(PIPELINE_DIR, "outbox")
PROCESSED_DIR = os.path.join(PIPELINE_DIR, "processed")
DOWNLOADS_DIR = "/Volumes/Mini_2T/lenoxparis data/Downloads"
REPO_DIR = "/Volumes/Mini_2T/lenoxparis data/Dev/Investor-hub"
DATA_TS_PATH = os.path.join(REPO_DIR, "src", "data.ts")
CLIENT_SECRETS_FILE = os.path.join(PIPELINE_DIR, "client_secret.json")

# NotebookLM File Name to Portfolio ID mapping dictionary
MAPPING_DICTIONARY = {
    "Architecting Alpha": "wealth-signals",
    "Third Signal Showcase": "third-signal-showcase",
    "The Endowment Engine": "tripoli-hub",
    "Architecting the Sovereign": "orbital-os",
    "ORBITAL CLIMATE SYSTEMS": "orbital-climate",
    "Architecting the Autonomous Workforce": "the-line-agent",
    "Saint & Summer Adventures": "saint-and-summer"
}

def get_youtube_client():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    if not os.path.exists(CLIENT_SECRETS_FILE):
        print(f"[ERROR] client_secret.json missing in {PIPELINE_DIR}")
        return None

    creds = None
    token_path = os.path.join(PIPELINE_DIR, 'token.json')
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return googleapiclient.discovery.build("youtube", "v3", credentials=creds)

def get_or_create_playlist(youtube):
    playlist_file = os.path.join(PIPELINE_DIR, "playlist_id.json")
    if os.path.exists(playlist_file):
        with open(playlist_file, "r") as f:
            return json.load(f)["playlist_id"]
            
    print("[PLAYLIST] Creating 'Third Signal Venture Studio Portfolio' Playlist...")
    try:
        response = youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": "Third Signal Venture Studio Portfolio",
                    "description": "Prismatic walkthroughs of the 7 core assets running the Third Signal AI Venture Studio."
                },
                "status": {
                    "privacyStatus": "unlisted"
                }
            }
        ).execute()
        
        playlist_id = response['id']
        with open(playlist_file, "w") as f:
            json.dump({"playlist_id": playlist_id}, f)
        print(f"[PLAYLIST] Playlist created successfully with ID: {playlist_id}")
        return playlist_id
    except Exception as e:
        print(f"[PLAYLIST ERROR] Failed to create playlist: {e}")
        return None

def add_video_to_playlist(youtube, playlist_id, video_id):
    print(f"[PLAYLIST] Adding video {video_id} to playlist {playlist_id}...")
    try:
        youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        ).execute()
        print(f"[PLAYLIST] Video successfully added to playlist.")
    except Exception as e:
        print(f"[PLAYLIST ERROR] Failed to add video to playlist: {e}")

def upload_to_youtube(youtube, file_path, asset_id):
    title = f"{asset_id.replace('-', ' ').title()} - Third Signal Portfolio Overview"
    description = f"Cinematic analyst overview for the {title} asset within the Third Signal Venture Studio data room."
    
    print(f"[YOUTUBE] Uploading {file_path} as '{title}'...")
    request = youtube.videos().insert(
        part="snippet,status",
        body={
          "snippet": {"categoryId": "27", "description": description, "title": title},
          "status": {"privacyStatus": "unlisted"}
        },
        media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True)
    )
    response = request.execute()
    video_id = response['id']
    
    playlist_id = get_or_create_playlist(youtube)
    if playlist_id:
        add_video_to_playlist(youtube, playlist_id, video_id)
        
    return video_id

def patch_data_ts(asset_id, video_id):
    embed_url = f"https://www.youtube.com/embed/{video_id}"
    print(f"[CODEBASE] Patching src/data.ts to inject {embed_url} into asset '{asset_id}'")
    
    with open(DATA_TS_PATH, 'r') as f:
        content = f.read()
        
    asset_block_pattern = rf'(\"id\":\s*\"{asset_id}\"[\s\S]*?)(,?\s*\"media\":\s*\{{[\s\S]*?\}})?(\s*}})'
    replacement = r'\1,\n      "media": {\n        "type": "youtube",\n        "url": "' + embed_url + r'"\n      }\3'
    
    new_content = re.sub(asset_block_pattern, replacement, content)
    new_content = new_content.replace(',,', ',')
    
    with open(DATA_TS_PATH, 'w') as f:
        f.write(new_content)
    print("[CODEBASE] Injection successful.")
    return True

def push_to_github(asset_id):
    print(f"[GIT] Committing and pushing updates for {asset_id} to trigger GCP build...")
    try:
        subprocess.run(["git", "add", "src/data.ts"], cwd=REPO_DIR, check=True)
        subprocess.run(["git", "commit", "-m", f"chore(media): auto-embed cinematic video for {asset_id}"], cwd=REPO_DIR, check=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=REPO_DIR, check=True)
        print("[GIT] Push complete.")
    except subprocess.CalledProcessError as e:
        print(f"[GIT ERROR] {e}")

def intercept_chrome_downloads():
    for filename in os.listdir(DOWNLOADS_DIR):
        if filename.endswith(".mp4"):
            for prefix, asset_id in MAPPING_DICTIONARY.items():
                normalized_filename = filename.replace("_", " ")
                if normalized_filename.startswith(prefix):
                    src_path = os.path.join(DOWNLOADS_DIR, filename)
                    dest_path = os.path.join(OUTBOX_DIR, f"{asset_id}.mp4")
                    print(f"\n[INTERCEPT] Caught NotebookLM download: {filename}")
                    print(f"[INTERCEPT] Moving to outbox as: {asset_id}.mp4")
                    try:
                        shutil.move(src_path, dest_path)
                    except Exception as e:
                        print(f"[INTERCEPT ERROR] {e}")

def watch_outbox():
    print(f"[*] Third Signal Auto-Publisher running.")
    print(f"[*] Watching Chrome Downloads: {DOWNLOADS_DIR}")
    print(f"[*] Watching Outbox: {OUTBOX_DIR}")
    
    youtube = get_youtube_client()
    if not youtube:
        sys.exit(1)
        
    while True:
        intercept_chrome_downloads()
        for filename in os.listdir(OUTBOX_DIR):
            if filename.endswith(".mp4"):
                asset_id = filename.replace(".mp4", "")
                file_path = os.path.join(OUTBOX_DIR, filename)
                print(f"\n[DETECTED] New outbox file ready: {filename}")
                
                try:
                    video_id = upload_to_youtube(youtube, file_path, asset_id)
                    success = patch_data_ts(asset_id, video_id)
                    if success:
                        push_to_github(asset_id)
                    shutil.move(file_path, os.path.join(PROCESSED_DIR, filename))
                    print(f"[*] Pipeline complete for {asset_id}.")
                except Exception as e:
                    print(f"[FATAL] Failed processing {filename}: {e}")
                    
        time.sleep(5)

if __name__ == "__main__":
    watch_outbox()
