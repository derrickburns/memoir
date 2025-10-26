# Directory Organization

This document describes the organization of the memoir-split directory and explains where to find each component.

## Directory Structure

```
memoir-split/
├── scripts/              # All Python tools and utilities
├── docs/                # Documentation files
├── output/              # Split chapter files (DOCX)
├── data/                # Comments, credentials, and analysis data
├── archive/             # Old versions and test files
├── book_structure.yaml  # Main manifest file
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # Main documentation
```

## Detailed Directory Contents

### `/scripts/` - Python Tools

All executable Python scripts for book management:

**Core Workflow:**
- `split_book.py` - Split DOCX book into individual chapter files
- `merge_book.py` - Merge chapter files back into complete book
- `build_book.py` - Build book from manifest file

**Chapter Management:**
- `renumber_chapters.py` - Renumber chapters sequentially
- `remove_empty_headings.py` - Clean formatting artifacts
- `simplify_styles.py` - Consolidate document styles

**Comment Extraction:**
- `extract_comments.py` - Extract comments from Google Doc
- `match_comments.py` - Basic comment matching (37% match rate)
- `match_comments_improved.py` - Improved comment matching (99.5% match rate)

**Utilities:**
- `compare_docx.py` - Compare two DOCX files for differences
- `analyze_docx.py` - Analyze document structure
- `find_all_headings.py` - List all headings in document
- `find_chapters.py` - Find chapter boundaries

### `/docs/` - Documentation

All guides and documentation:

- `QUICK_START.md` - Quick reference for manifest-based editing
- `MANIFEST_GUIDE.md` - Complete guide to the manifest system
- `COMMENTS_GUIDE.md` - Guide for extracting and matching comments
- `GOOGLE_API_SETUP.md` - Step-by-step Google API credential setup
- `RENUMBERING_SUMMARY.md` - Summary of chapter renumbering changes
- `STYLE_SIMPLIFIER_README.md` - Guide for style simplification tool

### `/output/` - Chapter Files

Contains 44 split chapter files in DOCX format:
- `00_Front_Matter.docx`
- `chapter_01_*.docx` through `chapter_34_*.docx`
- 9 timeline section files
- Images are in chapter-specific subdirectories (e.g., `chapter_01_images/`)

### `/data/` - Working Data Files

Runtime data and credentials:

**Google API Credentials (PRIVATE - in .gitignore):**
- `credentials.json` - OAuth 2.0 credentials for Google API
- `token.pickle` - Saved authentication token

**Comment Data (safe to share):**
- `comments.json` - All extracted comments (383 total)
- `comments.md` - Human-readable comment list
- `comment_matches.json` - Basic matcher results
- `comment_matches.md` - Basic matcher report (readable)
- `comment_matches_improved.json` - Improved matcher results
- `comment_matches_improved.md` - Improved matcher report (readable)

### `/archive/` - Old Files

Historical versions and test files (excluded from git):

**Old Versions:**
- `From Walls to Bridges_clean.docx`
- `From Walls to Bridges_no_empty_headings.docx`
- `renumbered.docx`

**Test/Intermediate Files:**
- `reconstructed.docx`
- `reconstructed2.docx`
- `test_build.docx`
- `book_final.docx`
- `output2/` - Old output directory

### Root Level Files

**Essential Files:**
- `book_structure.yaml` - Manifest defining book structure
- `requirements.txt` - Python package dependencies
- `README.md` - Main documentation
- `ORGANIZATION.md` - This file
- `.gitignore` - Git ignore patterns

**Source Material:**
- `From Walls to Bridges_ A Journey of Resilience and Connection.docx` - Original manuscript

## File Paths in Scripts

All scripts now use correct paths:

**Running scripts from root directory:**
```bash
python3 scripts/split_book.py mybook.docx
python3 scripts/extract_comments.py --doc-id DOC_ID
python3 scripts/match_comments_improved.py
python3 scripts/build_book.py --show-structure
```

**Default input/output paths:**
- Comments: `data/comments.json`
- Comment matches: `data/comment_matches_improved.json`
- Chapters: `output/`
- Credentials: `data/credentials.json`
- Token: `data/token.pickle`

## What's in .gitignore

Protected files (won't be committed to git):

```
# Private credentials
data/credentials.json
data/token.pickle

# Archive directory
archive/

# Python cache
__pycache__/
*.pyc

# Temporary Word files
~$*.docx
```

## Common Tasks

### Extract and Match Comments

```bash
# From root directory
python3 scripts/extract_comments.py --doc-id YOUR_DOC_ID
python3 scripts/match_comments_improved.py

# Review results
open data/comment_matches_improved.md
```

### Build Book from Manifest

```bash
# View structure
python3 scripts/build_book.py --show-structure

# Build book
python3 scripts/build_book.py --output final.docx
```

### Split a New Book

```bash
python3 scripts/split_book.py mybook.docx --heading-level 2
```

## Organization Benefits

1. **Clean root directory** - Only essential files at top level
2. **Logical grouping** - Related files together
3. **Security** - Credentials isolated in data/ and .gitignored
4. **Version control friendly** - Archive excluded, source organized
5. **Easy navigation** - Know where everything is
6. **Scalability** - Easy to add new scripts or docs

## Moving Forward

When adding new files:

- **Python scripts** → `scripts/`
- **Documentation** → `docs/`
- **Generated data** → `data/`
- **Old versions** → `archive/`
- **Split chapters** → `output/`

## Getting Started

After cloning or setting up:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Google API** (for comment extraction):
   - Follow `docs/GOOGLE_API_SETUP.md`
   - Place `credentials.json` in `data/` directory

3. **Review documentation:**
   - Start with `README.md`
   - Read `docs/QUICK_START.md` for manifest editing
   - See `docs/COMMENTS_GUIDE.md` for comment extraction

4. **Explore the structure:**
   ```bash
   ls scripts/     # See available tools
   ls docs/        # See available guides
   ls output/      # See split chapters
   ```

## Notes

- All paths in scripts and documentation updated to reflect new structure
- Original working files preserved in archive/
- Data files (comments, matches) tracked separately for easy sharing
- Credentials properly secured and excluded from version control
