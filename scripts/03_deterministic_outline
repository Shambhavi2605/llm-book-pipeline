import json
import os
from collections import defaultdict

CHUNKS_DIR = "data/chunks"
OUTPUT_PATH = "output/final_outline.json"

chapter_map = {
    1: range(1, 4),
    2: range(4, 7),
    3: range(7, 9),
    4: [9, 12],
    5: range(10, 12),
    6: range(13, 17),
    7: range(17, 19),
    8: range(19, 24),
    9: range(24, 29),
    10: range(29, 31),
    11: range(31, 33),
    12: range(33, 37),
    13: range(37, 43),
    14: [43]
}

chapter_titles = {
    1: "Introduction to LLMs",
    2: "Transformers and GPT Foundations",
    3: "Tokenization",
    4: "Data Preparation and Input Pipeline",
    5: "Embeddings",
    6: "Attention Mechanism",
    7: "Multi-Head Attention and Mathematics",
    8: "Transformer Architecture",
    9: "GPT Implementation and Training",
    10: "Inference and Sampling",
    11: "Model Saving and Loading",
    12: "Fine-tuning for Classification",
    13: "Instruction Fine-tuning",
    14: "Summary and Next Steps"
}

chapter_objectives = {
    1: "By the end of this chapter, readers will understand what LLMs are and the difference between pretraining and finetuning.",
    2: "By the end of this chapter, readers will understand the Transformer architecture and how GPT-3 works internally.",
    3: "By the end of this chapter, readers will understand how to build a tokenizer from scratch and implement Byte Pair Encoding.",
    4: "By the end of this chapter, readers will understand how to create input-target pairs and build efficient data pipelines.",
    5: "By the end of this chapter, readers will understand token embeddings and positional embeddings and why they are essential.",
    6: "By the end of this chapter, readers will understand self-attention from basics to full implementation including causal masking.",
    7: "By the end of this chapter, readers will understand multi-head attention including the full mathematical derivation.",
    8: "By the end of this chapter, readers will have implemented the complete LLM architecture including layer norm and transformer block.",
    9: "By the end of this chapter, readers will have coded the 124M parameter GPT-2 model and implemented the full pretraining loop.",
    10: "By the end of this chapter, readers will understand temperature scaling and top-k sampling for controlling text generation.",
    11: "By the end of this chapter, readers will understand how to save and load model weights and use pretrained OpenAI GPT-2 weights.",
    12: "By the end of this chapter, readers will understand how to fine-tune a pretrained LLM for spam classification.",
    13: "By the end of this chapter, readers will understand instruction fine-tuning using the Alpaca prompt format.",
    14: "By the end of this chapter, readers will have a complete overview of the entire LLM building process and clear next steps."
}

def load_chunks():
    all_chunks = []
    for file in sorted(os.listdir(CHUNKS_DIR)):
        if file.endswith("_chunks.json"):
            with open(os.path.join(CHUNKS_DIR, file), "r", encoding="utf-8") as f:
                chunks = json.load(f)
                all_chunks.extend(chunks)
    print(f"Loaded {len(all_chunks)} chunks")
    return all_chunks

def group_by_video(chunks):
    video_map = defaultdict(list)
    for c in chunks:
        video_map[c["video_index"]].append(c["chunk_id"])
    return video_map

def build_outline(video_map):
    outline = []
    for ch, vids in chapter_map.items():
        chunk_ids = []
        for v in vids:
            chunk_ids.extend(video_map.get(v, []))
        outline.append({
            "chapter_number": ch,
            "chapter_title": chapter_titles[ch],
            "learning_objective": chapter_objectives[ch],
            "chunk_ids": chunk_ids
        })
    return outline

def main():
    print("=" * 60)
    print("STEP 3: Building Outline from Chunk Files")
    print("=" * 60)

    chunks = load_chunks()
    video_map = group_by_video(chunks)

    outline = build_outline(video_map)

    final = {
        "book_title": "Building Large Language Models from Scratch",
        "chapters": outline
    }

    os.makedirs("output", exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2)

    print(f"\nOutline saved to {OUTPUT_PATH}")
    print(f"Total chapters: {len(outline)}")
    for ch in outline:
        print(f"  Chapter {ch['chapter_number']}: {ch['chapter_title']} ({len(ch['chunk_ids'])} chunks)")

if __name__ == "__main__":
    main()