import os
import json
import ollama

CHAPTERS_DIR = "output/chapters"
CHUNKS_DIR = "data/chunks"
OUTLINE_PATH = "output/final_outline.json"
OUTPUT_PATH = "output/faithfulness_report.json"

MODEL = "llama3"

# ── Load outline ───────────────────────────────────
def load_outline():
    with open(OUTLINE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# ── Load all chunks ────────────────────────────────
def load_all_chunks():
    all_chunks = {}
    for file in sorted(os.listdir(CHUNKS_DIR)):
        if file.endswith("_chunks.json"):
            with open(os.path.join(CHUNKS_DIR, file), "r", encoding="utf-8") as f:
                chunks = json.load(f)
            for chunk in chunks:
                all_chunks[chunk["chunk_id"]] = chunk
    return all_chunks

# ── Load chapter content ───────────────────────────
def load_chapter(chapter_num):
    filename = f"chapter_{chapter_num:02d}.md"
    filepath = os.path.join(CHAPTERS_DIR, filename)
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

# ── Build source context ───────────────────────────
def build_source(chunk_ids, all_chunks, max_words=2000):
    texts = []
    for cid in chunk_ids:
        if cid in all_chunks:
            texts.append(all_chunks[cid]["text"])
    combined = " ".join(texts)
    words = combined.split()[:max_words]
    return " ".join(words)

# ── Verify one chapter ─────────────────────────────
def verify_chapter(chapter_content, source_text, chapter_title):
    prompt = f"""You are a fact-checker verifying a book chapter against source transcripts.

Your job: Identify any claims in the chapter that are NOT supported by the source transcript.

Chapter Title: {chapter_title}

SOURCE TRANSCRIPT (ground truth):
{source_text}

GENERATED CHAPTER:
{chapter_content[:2000]}

Analyze the chapter and answer:
1. Faithfulness Score: X/10 (how faithful is the chapter to the source?)
2. Unsupported Claims: List any specific sentences that appear to be hallucinated or not in the source. If none, say "None found."
3. Overall Assessment: One sentence summary.

Be specific and concise."""

    response = ollama.chat(
        model=MODEL,
        options={"temperature": 0, "seed": 42},
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content'].strip()

# ── Main ───────────────────────────────────────────
def main():
    print("=" * 60)
    print("STEP 7: Verifying Chapter Faithfulness")
    print("=" * 60)

    outline = load_outline()
    all_chunks = load_all_chunks()
    chapters = outline["chapters"]

    report = {
        "total_chapters": len(chapters),
        "chapters": []
    }

    total_score = 0
    verified = 0

    for chapter in chapters:
        chapter_num = chapter["chapter_number"]
        chapter_title = chapter["chapter_title"]

        print(f"\n[{chapter_num}/{len(chapters)}] Verifying: {chapter_title}")

        # Load chapter content
        content = load_chapter(chapter_num)
        if not content:
            print(f"  SKIP: Chapter file not found")
            continue

        # Build source context
        source = build_source(chapter["chunk_ids"], all_chunks)

        # Verify
        verification = verify_chapter(content, source, chapter_title)

        # Extract score (simple parse)
        score = None
        for line in verification.split("\n"):
            if "Faithfulness Score" in line:
                try:
                    score = float(line.split(":")[1].strip().split("/")[0].strip())
                except:
                    score = None
                break

        if score:
            total_score += score
            verified += 1

        print(f"  Score: {score}/10" if score else "  Score: Could not parse")
        print(f"  {verification[:100]}...")

        report["chapters"].append({
            "chapter_number": chapter_num,
            "chapter_title": chapter_title,
            "faithfulness_score": score,
            "verification": verification
        })

    # Overall score
    avg_score = total_score / verified if verified > 0 else 0
    report["average_faithfulness_score"] = round(avg_score, 2)
    report["verified_chapters"] = verified

    # Save report
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("\n" + "=" * 60)
    print(f"DONE: Faithfulness Verification Complete")
    print(f"Average Score: {avg_score:.1f}/10")
    print(f"Report saved to: {OUTPUT_PATH}")
    print("=" * 60)

if __name__ == "__main__":
    main()