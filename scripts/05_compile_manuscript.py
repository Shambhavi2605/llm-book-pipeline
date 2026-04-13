import os
from dotenv import load_dotenv

load_dotenv()

CHAPTERS_DIR = "output/chapters"
OUTPUT_PATH = "output/manuscript.md"

def compile_manuscript():
    print("=" * 60)
    print("STEP 5: Compiling Manuscript")
    print("=" * 60)

    # Get all chapter files in order
    chapter_files = sorted([
        f for f in os.listdir(CHAPTERS_DIR)
        if f.endswith(".md")
    ])

    print(f"\nFound {len(chapter_files)} chapter files")

    manuscript = []

    # ── Book Title Page ────────────────────────────────────────
    manuscript.append("---")
    manuscript.append("title: 'Building Large Language Models from Scratch'")
    manuscript.append("author: 'Generated from YouTube Playlist by LLM Pipeline'")
    manuscript.append("date: '2025'")
    manuscript.append("---")
    manuscript.append("")

    # ── Preface ────────────────────────────────────────────────
    manuscript.append("# Preface")
    manuscript.append("")
    manuscript.append("This book was generated from the YouTube playlist 'Building LLMs from Scratch' using an automated LLM pipeline. The content is derived entirely from the original lecture transcripts. Each chapter corresponds to one or more lectures from the series.")
    manuscript.append("")
    manuscript.append("The pipeline used to generate this book:")
    manuscript.append("")
    manuscript.append("1. Fetched transcripts from 43 YouTube lectures")
    manuscript.append("2. Cleaned and chunked transcripts into 347 semantic segments")
    manuscript.append("3. Organized chunks into 14 chapters based on lecture topics")
    manuscript.append("4. Generated each chapter using a local Ollama LLM (llama3.2)")
    manuscript.append("5. Compiled all chapters into this manuscript")
    manuscript.append("")
    manuscript.append("---")
    manuscript.append("")
    manuscript.append("\\newpage")
    manuscript.append("")

    # ── Chapters ───────────────────────────────────────────────
    for i, filename in enumerate(chapter_files):
        filepath = os.path.join(CHAPTERS_DIR, filename)

        print(f"  Adding: {filename}")

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        manuscript.append(content)
        manuscript.append("")

        # Page break between chapters
        if i < len(chapter_files) - 1:
            manuscript.append("")
            manuscript.append("\\newpage")
            manuscript.append("")

    # ── Join and save ──────────────────────────────────────────
    full_manuscript = "\n".join(manuscript)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(full_manuscript)

    # Stats
    word_count = len(full_manuscript.split())
    print(f"\nManuscript compiled successfully!")
    print(f"Total words: {word_count}")
    print(f"Total chapters: {len(chapter_files)}")
    print(f"Saved to: {OUTPUT_PATH}")
    print("=" * 60)

if __name__ == "__main__":
    compile_manuscript()