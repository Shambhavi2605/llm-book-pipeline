import os
import json
import time
from together import Together
from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIR = "output"
CHUNKS_DIR = "data/chunks"
os.makedirs(OUTPUT_DIR, exist_ok=True)

client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
MODEL = "meta-llama/Llama-3.3-70B-Instruct-Turbo"

MERGE_SIZE = 6     # increased to reduce groups
BATCH_SIZE = 10

# ── Load chunks ────────────────────────────────────
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

# ── Merge chunks ───────────────────────────────────
def merge_chunks(all_chunks, merge_size=MERGE_SIZE):
    merged = []
    for i in range(0, len(all_chunks), merge_size):
        group = all_chunks[i:i + merge_size]
        combined_text = " ".join([c['text'] for c in group])

        merged.append({
            "merge_id": f"merge_{i//merge_size:03d}",
            "chunk_ids": [c['chunk_id'] for c in group],
            "text": combined_text[:3000]
        })

    print(f"Merged into {len(merged)} groups")
    return merged

# ── Select subset to reduce API usage ──────────────
def select_subset(merged_groups, step=3):
    selected = merged_groups[::step]
    print(f"Selected {len(selected)} groups out of {len(merged_groups)}")
    return selected

# ── Summarize group ────────────────────────────────
def summarize_merged_group(group):
    prompt = f"""Summarize the following transcript from a course on building LLMs.
Write 2-3 sentences only. Do NOT add new information.

{group['text']}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=120
    )

    return response.choices[0].message.content.strip()

# ── Group summaries ────────────────────────────────
def group_summaries(summaries, batch_size=BATCH_SIZE):
    batches = []
    for i in range(0, len(summaries), batch_size):
        batch = summaries[i:i + batch_size]

        combined = "\n\n".join([
            f"{s['summary']}" for s in batch
        ])

        batches.append({
            "batch_id": i // batch_size,
            "combined_text": combined,
            "chunk_ids": [cid for s in batch for cid in s['chunk_ids']]
        })

    print(f"Grouped into {len(batches)} batches")
    return batches

# ── Get topics ─────────────────────────────────────
def get_batch_topic(batch):
    prompt = f"""Extract 2-3 main technical themes from these summaries.
Be concise.

{batch['combined_text']}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=100
    )

    return response.choices[0].message.content.strip()

# ── Final outline ──────────────────────────────────
def generate_final_outline(batch_topics):
    topics_text = "\n".join([bt['topic'] for bt in batch_topics])

    prompt = f"""Create a book outline with 8-10 chapters based ONLY on these topics.

Topics:
{topics_text}

Return simple list of chapters with titles.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=800
    )

    return response.choices[0].message.content.strip()

# ── Save ───────────────────────────────────────────
def save_json(data, filename):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Saved: {path}")

# ── MAIN ───────────────────────────────────────────
def main():
    print("="*50)
    print("Generating Book Outline (Optimized)")
    print("="*50)

    chunks = load_all_chunks()

    # Merge
    merged = merge_chunks(chunks)

    # Select subset (IMPORTANT)
    selected = select_subset(merged, step=3)

    # Summarize
    summaries = []
    for i, group in enumerate(selected):
        print(f"[{i+1}/{len(selected)}] {group['merge_id']}")

        try:
            summary = summarize_merged_group(group)
        except Exception as e:
            print("API failed. Paste manually:")
            print(group['text'][:300])
            summary = input("Enter summary: ")

        summaries.append({
            "chunk_ids": group['chunk_ids'],
            "summary": summary
        })

        time.sleep(1)

    save_json(summaries, "summaries.json")

    # Group summaries
    batches = group_summaries(summaries)

    # Topics
    batch_topics = []
    for batch in batches:
        try:
            topic = get_batch_topic(batch)
        except:
            print("Manual topic:")
            print(batch['combined_text'][:300])
            topic = input("Enter topic: ")

        batch_topics.append({
            "topic": topic,
            "chunk_ids": batch['chunk_ids']
        })

    save_json(batch_topics, "topics.json")

    # Final outline
    try:
        outline = generate_final_outline(batch_topics)
    except:
        print("Manual outline:")
        outline = input("Paste outline: ")

    with open(os.path.join(OUTPUT_DIR, "outline.txt"), "w") as f:
        f.write(outline)

    print("\nDONE! Check output folder.")

if __name__ == "__main__":
    main()