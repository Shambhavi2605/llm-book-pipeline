import subprocess
import sys

def run_step(step_name, script_path):
    print("\n" + "=" * 60)
    print(f"Running: {step_name}")
    print("=" * 60)

    result = subprocess.run([sys.executable, script_path])

    if result.returncode != 0:
        print(f"\nError in {step_name}. Stopping pipeline.")
        sys.exit(1)

def main():
    print("\nLLM Book Pipeline Started\n")

    #run_step("Fetching Transcripts", "scripts/01_fetch_transcripts.py")
    run_step("Cleaning and Chunking", "scripts/02_clean_and_chunk.py")
    run_step("Generating Outline", "scripts/03_deterministic_outline.py")
    run_step("Generating Chapters", "scripts/04_generating_chapters.py")
    run_step("Compiling Manuscript", "scripts/05_compile_manuscript.py")
    run_step("Rendering PDF", "scripts/06_render_pdf.py")

    print("\n" + "=" * 60)
    print("Pipeline completed successfully.")
    print("Final outputs available in /output directory")
    print("=" * 60)

if __name__ == "__main__":
    main()