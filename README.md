# Building LLMs from Scratch → Automated eBook Pipeline

## Project Overview

This project converts a YouTube playlist on "Building Large Language Models from Scratch" into a structured, eBook-quality manuscript using a combination of large language models (LLMs) and deterministic system design.

The pipeline transforms raw transcripts into a well-organized book through multi-stage processing, hierarchical summarization, and structural refinement.

---

## Motivation

This project was built to:

- Understand how to design real-world LLM pipelines
- Handle practical challenges such as token limits, hallucination, and noisy data
- Build a reproducible system rather than one-off outputs
- Demonstrate system-level thinking and problem-solving

---

## Problem Statement

Given a long YouTube playlist (43 lectures):

- Convert it into a structured book
- Handle:
  - Large input sizes (token limits)
  - Noisy transcripts
  - Logical content structuring
  - Hallucination in LLM outputs
- Ensure reproducibility?

---

## Solution Approach

The system follows a hierarchical pipeline:

Transcripts → Cleaning → Chunking → Summarization → Topics → Outline → Chapters → Book

Key design principle:

LLM (generation) + deterministic logic (correction)

---

1. Data Collection
   Extract transcripts from YouTube videos

2. Cleaning & Preprocessing
   Remove noise and normalize text

3. Chunking
   Split transcripts into manageable segments

4. Outline Generation
   Deterministically map video lectures to chapters based on actual lecture titles

5. Chapter Generation
   Generate detailed chapter content from source chunks using local Ollama LLM

6. Faithfulness Verification
   Verify generated content against source transcripts using LLM-based scoring

7. Manuscript Compilation
   Combine all chapters into a single markdown document

8. PDF Rendering
   Convert manuscript to professional PDF using Pandoc

---

## Technologies Used

- Python
- Ollama (local LLM runtime)
- JSON for structured storage
- Git and GitHub

---

## Features

- Fully automated pipeline
- Runs locally without external APIs
- Handles large transcript datasets
- Hierarchical summarization design
- Deterministic post-processing for correctness
- Reproducible outputs using cached intermediate files
- Modular and extensible architecture

---

## Challenges Faced

Token Limits  
Resolved using chunking and hierarchical summarization

API Rate Limits  
Resolved by switching to a local LLM using Ollama

Incorrect Outline Generation  
LLM-generated outlines contained duplication and poor ordering  
Resolved using a deterministic refinement layer

System Constraints  
Handled memory limitations and execution interruptions during long runs

---

## Key Learnings

- LLMs are effective for local text generation but weak at global structuring
- Reliable systems require combining LLM outputs with deterministic logic
- Real-world ML systems involve handling constraints, debugging, and trade-offs

---

## What Makes This Project Stand Out

- Focuses on system design, not just LLM usage
- Handles real-world constraints such as rate limits and memory limits
- Introduces reproducibility through caching and structured outputs
- Combines generative models with rule-based validation

---

## Project Structure
llm-book-pipeline/  
│  
├── data/  
│ ├── raw_transcripts/  
│ ├── cleaned/  
│ ├── chunks/  
│  
├── output/  
│ ├── batch_topics.json  
│ ├── book.pdf  
│ ├── final_outline.json   
│ ├── manuscript.md  
│ ├── merged_summaries.json    
│ ├── outline.json  
│  
├── scripts/  
│ ├── 01_fetch_transcripts.py  
│ ├── 02_clean_and_chunk.py  
│ ├── 03_deterministic_outline.py  
│ ├── 03_generate_outline.py  
│ ├── 04_build_final_outline.py  
│ ├── 05_compile_manuscript.py  
│ ├── 06_render_pdf.py  
│   
├── README.md  
├── pipeline.py


---

## Installation

Clone the repository:
git clone https://github.com/YOUR_USERNAME/llm-book-pipeline.git

cd llm-book-pipeline


Create virtual environment:
python -m venv venv
venv\Scripts\activate


Install dependencies:
pip install youtube-transcript-api python-dotenv tqdm requests

Install Ollama from: https://ollama.com

---

## Running the Pipeline
python pipeline.py


---

## Usage

All outputs are stored in the `output/` directory:
 
- batch_topics.json  
- outline.json  
- final_outline.json  
- book.pdf  
- merged_summaries.json  
- manuscript.md  

The final structured book outline is available in `final_outline.json`.
The unformatted book in non-pdf form with all the chapters is available in `manuscript.md`.
The final book pdf is `book.pdf`.

---

## Future Improvements

- Add a verification layer to detect hallucinations
- Build a retrieval-based query system (RAG)
- Improve semantic chunking using embeddings
- Add a lightweight interface for interaction

---

## Credits

Based on the "Building LLMs from Scratch" lecture series

---

## License

MIT License
