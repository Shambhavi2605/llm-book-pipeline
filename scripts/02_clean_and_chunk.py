import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

RAW_DIR = "data/raw_transcripts"
CLEANED_DIR = "data/cleaned"
CHUNKS_DIR = "data/chunks"
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 200

os.makedirs(CLEANED_DIR, exist_ok=True)
os.makedirs(CHUNKS_DIR, exist_ok=True)

def count_tokens(text):
    words = len(text.split())
    return int(words / 0.75)

def clean_transcript(raw_text):
    fillers = [
        r"\buh\b", r"\bum\b", r"\byou know\b",
        r"\bbasically\b", r"\bright\b",
        r"\bokay so\b", r"\bso so\b",
        r"\bkind of\b", r"\bsort of\b"
    ]
    text = raw_text
    for filler in fillers:
        text = re.sub(filler, "", text, flags=re.IGNORECASE)
    text = re.sub(r'\b(\w+)( \1\b)+', r'\1', text)
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    text = text.strip()
    return text

def read_transcript_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    parts = content.split("=" * 60)
    if len(parts) >= 2:
        return parts[1].strip()
    return content

def chunk_text(text, video_title, video_index):
    words = text.split()
    total_words = len(words)
    chunk_words = int(CHUNK_SIZE * 0.75)
    overlap_words = int(CHUNK_OVERLAP * 0.75)
    chunks = []
    start = 0
    chunk_index = 0
    while start < total_words:
        end = min(start + chunk_words, total_words)
        chunk_words_list = words[start:end]
        chunk_text_str = " ".join(chunk_words_list)
        chunks.append({
            "chunk_id": f"v{video_index:02d}_c{chunk_index:03d}",
            "video_index": video_index,
            "video_title": video_title,
            "chunk_index": chunk_index,
            "text": chunk_text_str,
            "token_count": count_tokens(chunk_text_str),
            "word_count": len(chunk_words_list)
        })
        chunk_index += 1
        start += chunk_words - overlap_words
    return chunks

def save_cleaned(video_index, video_title, cleaned_text):
    safe_title = "".join(
        c for c in video_title
        if c.isalnum() or c in (" ", "-", "_")
    ).strip()[:60]
    filename = f"{video_index:02d}_{safe_title}_cleaned.txt"
    filepath = os.path.join(CLEANED_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(cleaned_text)
    return filepath

def save_chunks(video_index, video_title, chunks):
    safe_title = "".join(
        c for c in video_title
        if c.isalnum() or c in (" ", "-", "_")
    ).strip()[:60]
    filename = f"{video_index:02d}_{safe_title}_chunks.json"
    filepath = os.path.join(CHUNKS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)
    return filepath

def main():
    print("=" * 60)
    print("STEP 2: Cleaning and Chunking Transcripts")
    print("=" * 60)

    metadata_path = os.path.join(RAW_DIR, "metadata.json")
    with open(metadata_path, "r", encoding="utf-8") as f:
        videos = json.load(f)

    total_chunks = 0
    processed = 0

    for video in videos:
        if not video.get("has_transcript"):
            print(f"\n[SKIP] {video['title']} - no transcript")
            continue

        print(f"\n[{video['index']}/43] {video['title']}")
        raw_text = read_transcript_file(video["transcript_file"])
        cleaned = clean_transcript(raw_text)
        approx_tokens = count_tokens(cleaned)
        print(f"  Approx tokens: {approx_tokens}")
        save_cleaned(video["index"], video["title"], cleaned)
        chunks = chunk_text(cleaned, video["title"], video["index"])
        print(f"  Chunks created: {len(chunks)}")
        save_chunks(video["index"], video["title"], chunks)
        total_chunks += len(chunks)
        processed += 1

    print("\n" + "=" * 60)
    print(f"DONE: {processed} videos processed")
    print(f"Total chunks created: {total_chunks}")
    print("=" * 60)

if __name__ == "__main__":
    main()