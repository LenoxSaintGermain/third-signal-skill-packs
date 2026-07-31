import os
import time
import re
import shutil
import subprocess
import google_auth_oauthlib.flow
import googleapiclient.discovery
from googleapiclient.http import MediaFileUpload

# SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
# Configure PIPELINE_DIR, OUTBOX_DIR, PROCESSED_DIR, REPO_DIR, DATA_TS_PATH

def get_youtube_client(client_secrets_file, token_path, scopes):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    creds = None
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, scopes)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return googleapiclient.discovery.build("youtube", "v3", credentials=creds)

def watch_outbox(outbox_dir, processed_dir, youtube_client, process_callback):
    """
    Watches an outbox directory for .mp4 files.
    When found, uploads to YouTube and calls the process_callback with the video_id.
    """
    print(f"[*] Auto-Publisher running. Watching {outbox_dir}...")
    while True:
        for filename in os.listdir(outbox_dir):
            if filename.endswith(".mp4"):
                asset_id = filename.replace(".mp4", "")
                file_path = os.path.join(outbox_dir, filename)
                print(f"\n[DETECTED] New render found: {filename}")
                
                try:
                    # Implement your upload logic here using youtube_client
                    video_id = "UPLOADED_VIDEO_ID" 
                    
                    if process_callback(asset_id, video_id):
                        shutil.move(file_path, os.path.join(processed_dir, filename))
                        print(f"[*] Pipeline complete for {asset_id}.")
                except Exception as e:
                    print(f"[FATAL] Failed processing {filename}: {e}")
                    
        time.sleep(5)
