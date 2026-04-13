import os
import json
import time
import ollama
from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIR = "output"
CHUNKS_DIR = "data/chunks"
os.makedirs(OUTPUT_DIR, exist_ok=True)

MODEL = "llama3"
MERGE_SIZE = 10   # merge 10 chunks into 1 group → 35 groups
BATCH_SIZE = 5    # group 5 summaries into 1 batch → 7 batches

# ── Step 1: Load all chunks ────────────────────────────────────
def load_all_chunks():
    all_chunks = []
    chunk_files = sorted([
        f for f in os.listdir(CHUNKS_DIR)
        if f.endswith("_chunks.json")
    ])
    for filename in chunk_files:
        filepath = os.path.join(CHUNKS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            chunks = json.load(f)
        all_chunks.extend(chunks)
    print(f"Loaded {len(all_chunks)} chunks")
    return all_chunks

# ── Step 2: Merge chunks (Pure Python) ────────────────────────
def merge_chunks(all_chunks):
    merged = []
    for i in range(0, len(all_chunks), MERGE_SIZE):
        group = all_chunks[i:i + MERGE_SIZE]
        combined_text = " ".join([c['text'] for c in group])
        merged.append({
            "merge_id": f"merge_{i//MERGE_SIZE:03d}",
            "chunk_ids": [c['chunk_id'] for c in group],
            "video_titles": list(set([c['video_title'] for c in group])),
            "text": combined_text[:4000]
        })
    print(f"Merged {len(all_chunks)} chunks into {len(merged)} groups")
    return merged

# ── Step 3: Summarize each merged group (Ollama) ──────────────
def summarize_group(group):
    prompt = f"""You are summarizing a segment from a video course on building LLMs from scratch.

Summarize the following transcript in 2-3 sentences.
Focus only on technical concepts covered.
Do not add anything not present in the text.

Transcript:
{group['text']}

Summary:"""

    response = ollama.chat(
        model=MODEL,
        options={"temperature": 0, "seed": 42},
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content'].strip()

# ── Step 4: Group summaries into batches (Pure Python) ────────
def group_summaries(summaries):
    batches = []
    for i in range(0, len(summaries), BATCH_SIZE):
        batch = summaries[i:i + BATCH_SIZE]
        combined = "\n\n".join([
            f"[Group {s['merge_id']}]: {s['summary']}"
            for s in batch
        ])
        batches.append({
            "batch_id": i // BATCH_SIZE,
            "chunk_ids": [cid for s in batch for cid in s['chunk_ids']],
            "combined_text": combined
        })
    print(f"Grouped {len(summaries)} summaries into {len(batches)} batches")
    return batches

# ── Step 5: Extract topics from each batch (Ollama) ───────────
def get_batch_topic(batch):
    prompt = f"""You are analyzing summaries from a course on building LLMs from scratch.

List 2-3 main technical themes covered in these summaries.
Be specific. One line per theme.

Summaries:
{batch['combined_text']}

Main themes:"""

    response = ollama.chat(
        model=MODEL,
        options={"temperature": 0, "seed": 42},
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content'].strip()

# ── Step 6: Generate final outline (Ollama) ───────────────────
def generate_final_outline(batch_topics):
    topics_text = ""
    for i, bt in enumerate(batch_topics):
        topics_text += f"\n[Section {i+1}]\n{bt['topic']}\n"

    prompt = f"""You are a technical book editor creating an outline for "Building Large Language Models from Scratch."

Below are the main themes from each section of the course.
Create exactly 10 logical chapters that flow naturally from basics to advanced.
Each chapter must reference which section numbers it covers.

Output ONLY valid JSON, no other text:
{{
  "book_title": "Building Large Language Models from Scratch",
  "chapters": [
    {{
      "chapter_number": 1,
      "chapter_title": "Title here",
      "learning_objective": "By the end of this chapter, readers will understand...",
      "section_numbers": [1, 2]
    }}
  ]
}}

Course sections:
{topics_text}

JSON:"""

    response = ollama.chat(
        model=MODEL,
        options={"temperature": 0, "seed": 42},
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content'].strip()

# ── Step 7: Map section numbers to chunk IDs ──────────────────
def map_sections_to_chunks(outline_parsed, batch_topics):
    for chapter in outline_parsed['chapters']:
        chunk_ids = []
        for sec_num in chapter.get('section_numbers', []):
            idx = sec_num - 1
            if 0 <= idx < len(batch_topics):
                chunk_ids.extend(batch_topics[idx]['chunk_ids'])
        chapter['chunk_ids'] = chunk_ids
        if 'section_numbers' in chapter:
            del chapter['section_numbers']
    return outline_parsed

def save_json(data, filename):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        if isinstance(data, str):
            f.write(data)
        else:
            json.dump(data, f, indent=2)
    print(f"Saved: {path}")

# ── Main ───────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("STEP 3: Generating Book Outline")
    print("Pipeline: Merge → Summarize → Group → Topics → Outline")
    print("=" * 60)

    # Load all chunks
    all_chunks = load_all_chunks()

    # Phase 1: Merge (Pure Python)
    print("\n[Phase 1] Merging chunks (no LLM)...")
    merged_groups = merge_chunks(all_chunks)

    # Phase 2: Summarize merged groups (Ollama)
    summaries_path = os.path.join(OUTPUT_DIR, "merged_summaries.json")
    if os.path.exists(summaries_path):
        print("\n[Phase 2] Loading existing summaries...")
        with open(summaries_path, "r", encoding="utf-8") as f:
            merged_summaries = json.load(f)
        print(f"Loaded {len(merged_summaries)} summaries")
    else:
        print(f"\n[Phase 2] Summarizing {len(merged_groups)} merged groups...")
        merged_summaries = []
        for i, group in enumerate(merged_groups):
            print(f"  [{i+1}/{len(merged_groups)}] {group['merge_id']}...")
            summary = summarize_group(group)
            merged_summaries.append({
                "merge_id": group['merge_id'],
                "chunk_ids": group['chunk_ids'],
                "summary": summary
            })
        save_json(merged_summaries, "merged_summaries.json")

    # Phase 3: Group summaries (Pure Python)
    print("\n[Phase 3] Grouping summaries (no LLM)...")
    batches = group_summaries(merged_summaries)

    # Phase 4: Extract topics (Ollama)
    print(f"\n[Phase 4] Extracting topics from {len(batches)} batches...")
    batch_topics = []
    for i, batch in enumerate(batches):
        print(f"  Batch [{i+1}/{len(batches)}]...")
        topic = get_batch_topic(batch)
        batch_topics.append({
            "batch_id": batch['batch_id'],
            "chunk_ids": batch['chunk_ids'],
            "topic": topic
        })
        print(f"  → {topic[:60]}...")
    save_json(batch_topics, "batch_topics.json")

    # Phase 5: Generate final outline (Ollama)
    print("\n[Phase 5] Generating final outline...")
    outline_raw = generate_final_outline(batch_topics)
    outline_clean = outline_raw.replace("```json", "").replace("```", "").strip()

    try:
        outline_parsed = json.loads(outline_clean)
        outline_parsed = map_sections_to_chunks(outline_parsed, batch_topics)

        print(f"\nOutline generated!")
        print(f"Chapters: {len(outline_parsed['chapters'])}")
        for ch in outline_parsed['chapters']:
            print(f"  Chapter {ch['chapter_number']}: {ch['chapter_title']}")

        save_json(json.dumps(outline_parsed, indent=2), "outline.json")

    except json.JSONDecodeError:
        print("JSON parse failed. Raw output:")
        print(outline_raw[:500])
        save_json(outline_raw, "outline_raw.txt")

    print("\n" + "=" * 60)
    print("DONE: Check output/outline.json")
    print("=" * 60)

if __name__ == "__main__":    main()