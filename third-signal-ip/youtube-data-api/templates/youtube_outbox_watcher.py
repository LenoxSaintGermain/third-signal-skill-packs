import os
import sys
import time
import shutil
import google_auth_oauthlib.flow
import googleapiclient.discovery
from googleapiclient.http import MediaFileUpload

# Required: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
PIPELINE_DIR = "./youtube-pipeline"
OUTBOX_DIR = os.path.join(PIPELINE_DIR, "outbox")
PROCESSED_DIR = os.path.join(PIPELINE_DIR, "processed")
CLIENT_SECRETS_FILE = os.path.join(PIPELINE_DIR, "client_secret.json")

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

def upload_to_youtube(youtube, file_path, title):
    print(f"[YOUTUBE] Uploading {file_path} as '{title}'...")
    request = youtube.videos().insert(
        part="snippet,status",
        body={
          "snippet": {"categoryId": "27", "description": "Automated upload", "title": title},
          "status": {"privacyStatus": "unlisted"}
        },
        media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True)
    )
    response = request.execute()
    return response['id']

def watch_outbox():
    print(f"[*] Auto-Publisher running. Watching {OUTBOX_DIR}...")
    youtube = get_youtube_client()
    if not youtube:
        sys.exit(1)
        
    while True:
        for filename in os.listdir(OUTBOX_DIR):
            if filename.endswith(".mp4"):
                file_path = os.path.join(OUTBOX_DIR, filename)
                print(f"\n[DETECTED] New render found: {filename}")
                try:
                    video_id = upload_to_youtube(youtube, file_path, filename.replace(".mp4", ""))
                    print(f"[*] Uploaded successfully. ID: {video_id}")
                    shutil.move(file_path, os.path.join(PROCESSED_DIR, filename))
                except Exception as e:
                    print(f"[FATAL] Failed processing {filename}: {e}")
        time.sleep(5)

if __name__ == "__main__":
    watch_outbox()
