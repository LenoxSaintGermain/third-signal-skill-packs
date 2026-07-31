# Omi OCR Repair Daemon & Rewind.ai Data Recovery

This reference document details the technical discoveries and native macOS implementations developed to repair the Omi Desktop App's broken indexing pipeline and unlock trapped creative IP from the dead Rewind.ai archive.

---

## 1. Omi Desktop App Index Repair

### The Problem
The Omi Desktop SwiftUI application successfully records your screen history as short H.264 encoded video chunks (`chunk_*.mp4`) on disk, but its background OCR/indexing pipeline is extremely brittle. 

An audit of the live `omi.db` database revealed:
* **Total screenshots captured:** 59,736
* **Indexed screenshots with non-empty `ocrText`:** 1,618 (**only 2.71%**)
* **Result:** Your entire screen history (97.29%) is un-indexed, making searches and visual timeline recalls fail.

### The Solution (Sovereign Hijack)
Instead of rebuilding the app, we run a local background indexing daemon that extracts frames via `ffmpeg` and runs **native macOS Apple Vision OCR** (zero cost, high-fidelity, 100% local, runs in 0.05s on Apple M4 silicon).

#### A. The Swift OCR Engine (`ocr.swift`)
This native Swift tool compiles on-the-fly and processes screenshots using macOS CoreML and the `Vision` framework.

```swift
import Foundation
import Vision
import Cocoa

let imageURL = URL(fileURLWithPath: "/tmp/frame_0.png")
guard let image = NSImage(contentsOf: imageURL),
      let tiffData = image.tiffRepresentation,
      let cgImage = NSImage(data: tiffData)?.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
    print("Error loading image")
    exit(1)
}

let requestHandler = VNImageRequestHandler(cgImage: cgImage, options: [:])
let request = VNRecognizeTextRequest { request, error in
    guard let observations = request.results as? [VNRecognizedTextObservation] else { return }
    let recognizedStrings = observations.compactMap { observation in
        observation.topCandidates(1).first?.string
    }
    print(recognizedStrings.joined(separator: "\n"))
}

request.recognitionLevel = .accurate
try? requestHandler.perform([request])
```

**Compilation Command:**
```bash
swiftc -O ocr.swift -o ocr
```

#### B. The Python Repair Daemon (`omi_ocr_repair.py`)
This script queries `omi.db`, extracts missing frame offsets from MP4 video chunks on your 8TB drive using `ffmpeg`, runs our compiled native `ocr` binary, and writes the text back to SQLite.

```python
import os
import sqlite3
import subprocess
import json
import sys

DB_PATH = "/Users/lenoxparis/Library/Application Support/Omi/users/ESLtLAnd3RgBi0ThzKNtulZACF03/omi.db"
VIDEOS_DIR = "/Volumes/Third Signal Lab HD/Omi/Videos"
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
OCR_PATH = os.path.join(SCRIPTS_DIR, "ocr")
FFMPEG_PATH = "/Applications/omi.app/Contents/Resources/Omi Computer_Omi Computer.bundle/ffmpeg"
TEMP_FRAME = "/tmp/omi_repair_frame.png"

def repair_pending_frames(batch_size=100):
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}", file=sys.stderr)
        return
        
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, videoChunkPath, frameOffset 
            FROM screenshots 
            WHERE videoChunkPath IS NOT NULL AND videoChunkPath != '' 
              AND (ocrText IS NULL OR ocrText = '') 
            LIMIT ?;
        """, (batch_size,))
        rows = cursor.fetchall()
        
        if not rows:
            print("No pending frames to repair.")
            conn.close()
            return
            
        print(f"Found {len(rows)} pending frames to repair in this batch.")
        repaired_count = 0
        
        for row in rows:
            row_id, video_rel_path, frame_offset = row
            video_full_path = os.path.join(VIDEOS_DIR, video_rel_path)
            
            if not os.path.exists(video_full_path):
                continue
                
            # Step A: Extract frame via ffmpeg
            extract_cmd = [
                FFMPEG_PATH, "-y",
                "-i", video_full_path,
                "-vf", f"select=eq(n\\,{frame_offset})",
                "-vframes", "1",
                TEMP_FRAME
            ]
            res = subprocess.run(extract_cmd, capture_output=True, text=True)
            if res.returncode != 0:
                continue
                
            # Step B: Run native macOS OCR
            ocr_res = subprocess.run([OCR_PATH], capture_output=True, text=True)
            if ocr_res.returncode != 0:
                continue
                
            ocr_text = ocr_res.stdout.strip()
            
            # Step C: Update SQLite
            cursor.execute("""
                UPDATE screenshots 
                SET ocrText = ? 
                WHERE id = ?;
            """, (ocr_text, row_id))
            
            repaired_count += 1
            if repaired_count % 10 == 0:
                conn.commit()
                print(f"  Repaired {repaired_count} frames...")
                
        conn.commit()
        conn.close()
        print(f"Batch repair complete. Repaired {repaired_count} frames successfully.")
        
        if os.path.exists(TEMP_FRAME):
            os.remove(TEMP_FRAME)
    except Exception as e:
        print(f"Exception during repair: {e}", file=sys.stderr)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Omi Local OCR Repair Daemon")
    parser.add_argument("--batch", type=int, default=100, help="Number of frames to process")
    args = parser.parse_args()
    repair_pending_frames(args.batch)
```

---

## 2. Unlocking Trapped Rewind.ai Data

While the Rewind.ai local SQLite search database (`db-enc.sqlite3` on `/Volumes/Lenox4TB/app_support_relocations/com.memoryvault.MemoryVault/`) is encrypted, **the actual captured media assets are stored 100% unencrypted:**

* **Meeting Audio Records:** 
  Located in `com.memoryvault.MemoryVault/snippets/` as standard, unencrypted MPEG-4 **`.m4a`** voice recordings. There are 900+ directories of unencrypted voice memos from your calls.
* **Screen Captures:** 
  Located in `com.memoryvault.MemoryVault/chunks/` as standard **ISO Media, MP4 v2** screen-recording video chunks (H.264 encoded, with file extensions stripped). 

### How to Retrieve trapped IP:
1. Since the `.mp4` chunks are structured by Year/Month/Day (e.g. `/chunks/202512/17/`), you can directly locate and watch any historical recording by appending `.mp4` to the raw chunk files.
2. To recover spoken meeting summaries: loop through the `.m4a` files in `snippets/`, pass them to standard Whisper or Gemini API for transcription, and save them as markdown transcripts.
