import os
import json
import ollama
from dotenv import load_dotenv

load_dotenv()

CHUNKS_DIR = "data/chunks"
OUTPUT_DIR = "output/chapters"
OUTLINE_PATH = "output/final_outline.json"

os.makedirs(OUTPUT_DIR, exist_ok=True)

MODEL = "llama3"

# ── Step 1: Load outline ───────────────────────────────────────
def load_outline():
    with open(OUTLINE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# ── Step 2: Load all chunks into memory ───────────────────────
def load_all_chunks():
    all_chunks = {}
    chunk_files = sorted([
        f for f in os.listdir(CHUNKS_DIR)
        if f.endswith("_chunks.json")
    ])
    for filename in chunk_files:
        filepath = os.path.join(CHUNKS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            chunks = json.load(f)
        for chunk in chunks:
            all_chunks[chunk["chunk_id"]] = chunk
    print(f"Loaded {len(all_chunks)} chunks into memory")
    return all_chunks

# ── Step 3: Get chunks for a chapter ──────────────────────────
def get_chapter_chunks(chapter, all_chunks):
    chunks = []
    for chunk_id in chapter["chunk_ids"]:
        if chunk_id in all_chunks:
            chunks.append(all_chunks[chunk_id])
    return chunks

# ── Step 4: Merge chunks into context ─────────────────────────
def build_context(chunks, max_words=3000):
    """
    Merge chunk texts into one context block.
    Cap at max_words to stay within Ollama context window.
    """
    combined = " ".join([c["text"] for c in chunks])
    words = combined.split()
    if len(words) > max_words:
        combined = " ".join(words[:max_words])
    return combined

# ── Step 5: Generate chapter using Ollama ─────────────────────
def generate_chapter(chapter, context):
    """
    Core function — sends transcript context to Ollama
    and gets back a fully written book chapter.

    Key prompt design decisions:
    - Explicitly forbid adding information not in transcript
    - Ask for structured output with sections
    - Specify audience (beginner ML engineers)
    - Request flowing prose not bullet points
    """
    prompt = f"""You are a technical book author writing a chapter for "Building Large Language Models from Scratch."

Chapter {chapter['chapter_number']}: {chapter['chapter_title']}
Learning Objective: {chapter['learning_objective']}

STRICT RULES:
1. Only use information present in the transcript excerpts below
2. Do not add external knowledge or invented examples
3. Write in clear flowing prose — not bullet points
4. Explain every technical term when first introduced
5. Write for an audience of beginner ML engineers
6. Use the following structure:
   - Introduction (what this chapter covers)
   - Main sections with clear headings
   - Key Takeaways at the end

Transcript excerpts from course lectures:
{context}

Now write Chapter {chapter['chapter_number']}: {chapter['chapter_title']}

---"""

    response = ollama.chat(
        model=MODEL,
        options={
            "temperature": 0,
            "seed": 42,
            "num_ctx": 8192
        },
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content'].strip()

# ── Step 6: Save chapter as markdown ──────────────────────────
def save_chapter(chapter, content):
    filename = f"chapter_{chapter['chapter_number']:02d}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# Chapter {chapter['chapter_number']}: {chapter['chapter_title']}\n\n")
        f.write(f"**Learning Objective:** {chapter['learning_objective']}\n\n")
        f.write("---\n\n")
        f.write(content)
    return filepath

# ── Main ───────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("STEP 4: Generating Book Chapters")
    print("=" * 60)

    outline = load_outline()
    all_chunks = load_all_chunks()
    chapters = outline["chapters"]

    print(f"\nTotal chapters to generate: {len(chapters)}")

    for chapter in chapters:
        chapter_num = chapter['chapter_number']
        chapter_title = chapter['chapter_title']

        # Checkpointing — skip if already generated
        filename = f"chapter_{chapter_num:02d}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)
        if os.path.exists(filepath):
            print(f"\n[SKIP] Chapter {chapter_num}: {chapter_title} (already exists)")
            continue

        print(f"\n[{chapter_num}/{len(chapters)}] Generating: {chapter_title}")
        print(f"  Chunks: {len(chapter['chunk_ids'])}")

        # Get chunks for this chapter
        chunks = get_chapter_chunks(chapter, all_chunks)

        if not chunks:
            print(f"  WARNING: No chunks found for chapter {chapter_num}")
            continue

        # Build context
        context = build_context(chunks)
        print(f"  Context words: {len(context.split())}")

        # Generate chapter
        print(f"  Generating with Ollama...")
        content = generate_chapter(chapter, context)

        # Save
        saved_path = save_chapter(chapter, content)
        print(f"  Saved: {saved_path}")
        print(f"  Words generated: {len(content.split())}")

    print("\n" + "=" * 60)
    print("DONE: All chapters saved to output/chapters/")
    print("=" * 60)

if __name__ == "__main__":
    main()