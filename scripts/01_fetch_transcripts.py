import os
import json
import time
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv

load_dotenv()

PLAYLIST_URL = "https://www.youtube.com/watch?v=Xpr8D6LeAtw&list=PLPTV0NXA_ZSgsLAr8YCgCwhPIJNNtexWu"
RAW_DIR = "data/raw_transcripts"
os.makedirs(RAW_DIR, exist_ok=True)

def get_playlist_videos(playlist_url):
    print("Fetching playlist metadata...")
    ydl_opts = {
        "quiet": True,
        "extract_flat": "in_playlist",
        "ignoreerrors": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
        print(f"Keys in info: {list(info.keys()) if info else 'None'}")

        videos = []
        entries = info.get("entries", [])
        print(f"Number of entries found: {len(entries)}")

        for i, entry in enumerate(entries):
            if entry is None:
                continue
            videos.append({
                "index": i + 1,
                "video_id": entry.get("id", ""),
                "title": entry.get("title", f"Video {i+1}"),
                "url": f"https://www.youtube.com/watch?v={entry.get('id', '')}"
            })

        print(f"Found {len(videos)} videos in playlist")
        return videos

def get_transcript(video_id, title):
    try:
        ytt = YouTubeTranscriptApi()
        fetched = ytt.fetch(video_id)
        full_text = " ".join([entry.text for entry in fetched])
        print(f"  ✓ Got transcript: {len(full_text)} characters")
        return full_text
    except Exception as e:
        print(f"  ✗ Error for {title}: {e}")
        return None

def save_transcript(video, transcript_text):
    safe_title = "".join(
        c for c in video["title"]
        if c.isalnum() or c in (" ", "-", "_")
    ).strip()[:60]

    filename = f"{video['index']:02d}_{safe_title}.txt"
    filepath = os.path.join(RAW_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"TITLE: {video['title']}\n")
        f.write(f"URL: {video['url']}\n")
        f.write(f"VIDEO_ID: {video['video_id']}\n")
        f.write(f"INDEX: {video['index']}\n")
        f.write("=" * 60 + "\n\n")
        f.write(transcript_text)

    return filepath

def save_metadata(videos):
    metadata_path = os.path.join(RAW_DIR, "metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(videos, f, indent=2)
    print(f"Metadata saved to {metadata_path}")

def main():
    print("=" * 60)
    print("STEP 1: Fetching YouTube Playlist Transcripts")
    print("=" * 60)

    videos = get_playlist_videos(PLAYLIST_URL)

    if not videos:
        print("ERROR: No videos found. Check your internet connection.")
        return

    save_metadata(videos)

    print("\nFetching transcripts...")
    success_count = 0

    for video in videos:
        print(f"\n[{video['index']}/{len(videos)}] {video['title']}")
        transcript = get_transcript(video["video_id"], video["title"])

        if transcript:
            filepath = save_transcript(video, transcript)
            video["transcript_file"] = filepath
            video["has_transcript"] = True
            success_count += 1
        else:
            video["transcript_file"] = None
            video["has_transcript"] = False

        time.sleep(1)

    save_metadata(videos)

    print("\n" + "=" * 60)
    print(f"DONE: {success_count}/{len(videos)} transcripts fetched")
    print(f"Saved to: {RAW_DIR}/")
    print("=" * 60)

if __name__ == "__main__":
    main()