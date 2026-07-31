import os, sys, time, shutil, subprocess
import google_auth_oauthlib.flow
import googleapiclient.discovery
from googleapiclient.http import MediaFileUpload

# Required: client_secret.json in PIPELINE_DIR
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
PIPELINE_DIR = "./youtube-pipeline"
OUTBOX_DIR = os.path.join(PIPELINE_DIR, "outbox")
PROCESSED_DIR = os.path.join(PIPELINE_DIR, "processed")

def get_youtube_client():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    token_path = os.path.join(PIPELINE_DIR, 'token.json')
    client_secrets = os.path.join(PIPELINE_DIR, 'client_secret.json')
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    return googleapiclient.discovery.build("youtube", "v3", credentials=creds)

def watch_outbox():
    youtube = get_youtube_client()
    while True:
        for filename in os.listdir(OUTBOX_DIR):
            if filename.endswith(".mp4"):
                file_path = os.path.join(OUTBOX_DIR, filename)
                print(f"New render: {filename} - uploading...")
                
                # ... execute upload logic here, patch codebase, and trigger git push ...
                
                shutil.move(file_path, os.path.join(PROCESSED_DIR, filename))
        time.sleep(5)

if __name__ == "__main__":
    watch_outbox()