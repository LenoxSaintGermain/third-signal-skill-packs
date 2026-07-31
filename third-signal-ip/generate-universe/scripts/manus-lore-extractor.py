import os
import requests
import json
import sys

# Intended to be run by the agent to bulk-extract lore tasks from Manus.
# Fetches matching tasks and saves them as JSON for the Worldtree Ingestion Engine to process.

def extract_lore(api_key, output_dir, keywords):
    headers = {"x-manus-api-key": api_key}
    url = "https://api.manus.ai/v2/task.list?limit=100"
    
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print("Failed to list tasks:", r.status_code)
        return

    tasks = r.json().get("data", [])
    for t in tasks:
        title = t.get('title', t.get('message', {}).get('content', ''))
        task_id = t.get('task_id') or t.get('id')
        
        for target in keywords:
            if target.lower() in title.lower():
                print(f"PULLING: {title} (ID: {task_id})")
                
                # Try V2 API
                detail_url = f"https://api.manus.ai/v2/task.detail?task_id={task_id}"
                dr = requests.get(detail_url, headers=headers)
                
                # Fallback to V1 API for older tasks (CRITICAL PITFALL)
                if dr.status_code != 200:
                    detail_url = f"https://api.manus.im/v1/tasks/{task_id}"
                    dr = requests.get(detail_url, headers={"Authorization": f"Bearer {api_key}"})

                if dr.status_code == 200:
                    filename = "".join(x if x.isalnum() else "_" for x in title)
                    filepath = os.path.join(output_dir, f"{filename}.json")
                    with open(filepath, "w") as out:
                        json.dump(dr.json(), out, indent=2)
                    print(f"  -> Saved to {filepath}")
                else:
                    print(f"  -> Failed to get details. Status: {dr.status_code}")

if __name__ == "__main__":
    # Set up output directory and keywords as needed
    # extract_lore("your-api-key", "/Volumes/Third Signal Lab HD/hermes/workspaces/Worldtree/raw/manus", ["Worldtree", "US-10.6", "Amirah"])
    pass
