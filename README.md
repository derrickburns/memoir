# Book Splitter - Complete Memoir Management System

A comprehensive toolkit for splitting, editing, and managing book manuscripts in DOCX format.

## Features

### Core Functionality
- **Split** books by heading styles (Heading 1, Heading 2, etc.)
- **Merge** chapters back into complete book
- **Extract** images into chapter-specific directories
- **Preserve** all formatting, styles, and embedded images
- **Idempotent** operations (split→merge produces identical output)

### Editing & Management
- **Manifest-based editing** - Reorder, exclude, or merge chapters via YAML
- **Comment extraction** - Extract Google Doc comments and match to chapters
- **Chapter renumbering** - Automatically renumber chapters sequentially
- **Style simplification** - Consolidate styles to canonical set
- **Empty heading removal** - Clean formatting artifacts

### Workflow Support
- **Multiple versions** - Create short, full, and alternate versions
- **Version control friendly** - Text-based manifest for git tracking
- **Batch operations** - Process all chapters at once

## Directory Structure

```
memoir-split/
├── scripts/              # All Python tools and utilities
│   ├── split_book.py    # Split book into chapters
│   ├── merge_book.py    # Merge chapters back
│   ├── build_book.py    # Build from manifest
│   ├── extract_comments.py
│   ├── match_comments_improved.py
│   └── ...
├── docs/                # Documentation
│   ├── QUICK_START.md
│   ├── MANIFEST_GUIDE.md
│   ├── COMMENTS_GUIDE.md
│   └── ...
├── output/              # Split chapter files (DOCX)
├── data/                # Comments, credentials, matches
│   ├── credentials.json # Google API credentials (private)
│   ├── comments.json    # Extracted comments
│   └── comment_matches_improved.json
├── archive/             # Old/test files
├── book_structure.yaml  # Manifest file
├── requirements.txt
└── README.md
```

## Quick Start - Refresh from Google Drive

**New! Automated workflow for updating chapters from Google Drive:**

```bash
# 1. Download from Google Drive
#    File > Download > Microsoft Word (.docx)

# 2. Run refresh script (auto-detects download and processes it)
python3 scripts/refresh_from_google_drive.py

# That's it! Chapters are split and renumbered automatically.
```

See [REFRESH_WORKFLOW.md](docs/REFRESH_WORKFLOW.md) for details.

---

## Setup

### 1. Install Required Python Libraries

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install python-docx Pillow
```

### 2. Download Your Book from Google Drive

1. Open your Google Doc
2. Go to **File > Download > Microsoft Word (.docx)**
3. File will be saved to ~/Downloads/

### 3. Run Refresh Script

```bash
python3 scripts/refresh_from_google_drive.py
```

This automatically:
- Finds the latest download
- Splits into chapters
- Renumbers sequentially
- Extracts all images

---

## Manual Usage

### Basic Usage

```bash
python3 scripts/split_book.py mybook.docx
```

This will:
- Split the book by Heading 1 styles
- Create an `output` directory with:
  - `chapter_01_Title.docx`
  - `chapter_02_Title.docx`
  - `chapter_01_images/` (if chapter has images)
  - `chapter_02_images/` (if chapter has images)
  - etc.

### Advanced Options

**Specify output directory:**
```bash
python scripts/split_book.py mybook.docx --output chapters
```

**Use different heading level (e.g., Heading 2):**
```bash
python scripts/split_book.py mybook.docx --heading-level 2
```

**Full example:**
```bash
python scripts/split_book.py mybook.docx -o my_chapters -l 1
```

### Command-Line Options

- `input_file` - Path to your DOCX file (required)
- `-o, --output` - Output directory (default: `output`)
- `-l, --heading-level` - Heading level for chapters (1-9, default: 1)
- `-h, --help` - Show help message

## Output Structure

After running the script, you'll get:

```
output/
├── chapter_01_Introduction.docx
├── chapter_01_images/
│   ├── image_001.jpg
│   └── image_002.png
├── chapter_02_Getting_Started.docx
├── chapter_02_images/
│   ├── image_001.jpg
│   ├── image_002.jpg
│   └── image_003.png
├── chapter_03_Advanced_Topics.docx
└── ...
```

## Troubleshooting

### No chapters found

If you see "ERROR: No chapters found!", the script will list available heading styles in your document. You may need to:

1. Check which heading style is actually used in your document
2. Use the `--heading-level` option with the correct level
3. Or update your document to use consistent heading styles

### Images not extracting

- Make sure images are embedded in the document (not just linked)
- Google Docs should embed images when exporting to DOCX
- Some image formats may not be supported

### Permission errors

- Make sure you have write permissions in the output directory
- On macOS/Linux, you may need to make the script executable: `chmod +x split_book.py`

## Additional Tools

### Extract Comments from Google Doc

Extract comments and match them to split chapters:

```bash
# Set up Google API credentials (one-time setup)
# See GOOGLE_API_SETUP.md for detailed instructions

# Extract comments from your Google Doc
python3 scripts/extract_comments.py --doc-id YOUR_DOCUMENT_ID

# Match comments to chapter files (99.5% match rate!)
python3 scripts/match_comments_improved.py

# Review the report
open data/comment_matches_improved.md
```

See [COMMENTS_GUIDE.md](COMMENTS_GUIDE.md) for complete instructions.

### Manifest-Based Book Editing

Easily reorder, exclude, or merge chapters using a YAML manifest:

```bash
# View current book structure
python3 scripts/build_book.py --show-structure

# Edit the manifest file
open book_structure.yaml

# Build the book according to manifest
python3 scripts/build_book.py --output my_book.docx
```

See [docs/QUICK_START.md](docs/QUICK_START.md) or [docs/MANIFEST_GUIDE.md](docs/MANIFEST_GUIDE.md) for details.

### Renumber Chapters

Renumber chapters to be sequential:

```bash
python3 scripts/renumber_chapters.py
```

### Remove Empty Headings

Clean up formatting artifacts:

```bash
# Analyze document
python3 scripts/remove_empty_headings.py mybook.docx --analyze

# Remove empty headings
python3 scripts/remove_empty_headings.py mybook.docx -o cleaned.docx
```

### Simplify Styles

Consolidate styles to a canonical set:

```bash
python3 scripts/simplify_styles.py mybook.docx -o simplified.docx
```

## Complete Workflow

Here's a typical workflow for managing a memoir:

```bash
# 1. Download from Google Docs
# File > Download > Microsoft Word (.docx)

# 2. Split into chapters
python3 scripts/split_book.py mybook.docx --heading-level 2

# 3. Renumber chapters if needed
python3 scripts/renumber_chapters.py

# 4. Extract comments from Google Doc
python3 scripts/extract_comments.py --doc-id YOUR_DOC_ID
python3 scripts/match_comments_improved.py

# 5. Edit individual chapters (use your text editor)

# 6. Use manifest to reorder/exclude chapters
python3 scripts/build_book.py --show-structure
# Edit book_structure.yaml as needed

# 7. Build final book
python3 scripts/build_book.py --output final_draft.docx
```

## Publishing (Ebook & Print)

When ready to publish, convert to EPUB (ebook) and PDF (print):

```bash
# Build both formats at once
python3 scripts/build_all.py --cover cover.jpg

# Or build individually
python3 scripts/export_markdown.py  # DOCX → Markdown
python3 scripts/build_epub.py       # Markdown → EPUB
python3 scripts/build_pdf.py        # Markdown → PDF
```

**Output:**
- `book.epub` - Ebook for Kindle, Apple Books, etc.
- `book.pdf` - Print-ready PDF for KDP Print, IngramSpark, etc.

See **[docs/PUBLISHING_GUIDE.md](docs/PUBLISHING_GUIDE.md)** for complete publishing workflow.

## Documentation

- **[docs/QUICK_START.md](docs/QUICK_START.md)** - Quick reference for manifest-based editing
- **[docs/MANIFEST_GUIDE.md](docs/MANIFEST_GUIDE.md)** - Complete guide to manifest system
- **[docs/COMMENTS_GUIDE.md](docs/COMMENTS_GUIDE.md)** - Extract and match Google Doc comments
- **[docs/PUBLISHING_GUIDE.md](docs/PUBLISHING_GUIDE.md)** - Convert to EPUB and PDF for publication
- **[docs/GOOGLE_API_SETUP.md](docs/GOOGLE_API_SETUP.md)** - Set up Google API credentials
- **[docs/RENUMBERING_SUMMARY.md](docs/RENUMBERING_SUMMARY.md)** - Chapter renumbering details

## Requirements

- Python 3.7 or higher
- python-docx library
- Pillow (PIL) library
- PyYAML library (for manifest system)
- Google API libraries (for comment extraction)

Install all requirements:
```bash
pip install -r requirements.txt
```

## How It Works

1. Opens the DOCX file using python-docx
2. Scans all paragraphs looking for specified heading style
3. Groups content between headings into chapters
4. For each chapter:
   - Creates a new DOCX document
   - Copies the chapter content with formatting
   - Extracts embedded images to a dedicated directory
   - Saves the chapter file with a sanitized filename

## Tips

- Use consistent heading styles in your Google Doc before exporting
- Heading 1 is typically used for chapters
- Heading 2 could be used for major sections if your book is structured differently
- The script preserves formatting, so your chapters will look like the original
