import os
import subprocess

MANUSCRIPT_PATH = "output/manuscript.md"
PDF_PATH = "output/book.pdf"

def render_pdf():
    print("=" * 60)
    print("STEP 6: Rendering PDF")
    print("=" * 60)

    if not os.path.exists(MANUSCRIPT_PATH):
        print(f"ERROR: {MANUSCRIPT_PATH} not found. Run Script 05 first.")
        return

    print(f"Converting {MANUSCRIPT_PATH} to PDF...")

    cmd = [
        "pandoc",
        MANUSCRIPT_PATH,
        "-o", PDF_PATH,
        "--toc",                          # Table of contents
        "--toc-depth=2",                  # TOC depth
        "--number-sections",              # Number chapters
        "-V", "geometry:margin=1in",      # Page margins
        "-V", "fontsize=12pt",            # Font size
        "-V", "linestretch=1.5",          # Line spacing
        "-V", "mainfont=Georgia",         # Font
        "--pdf-engine=xelatex",           # PDF engine
        "--highlight-style=tango"         # Code highlighting
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            size = os.path.getsize(PDF_PATH) / 1024
            print(f"PDF generated successfully!")
            print(f"File size: {size:.1f} KB")
            print(f"Saved to: {PDF_PATH}")
        else:
            print("ERROR generating PDF:")
            print(result.stderr)

    except FileNotFoundError:
        print("ERROR: Pandoc not found. Install from pandoc.org")

    print("=" * 60)

if __name__ == "__main__":
    render_pdf()