# Claude Instructions: Memoir Management Project

This document provides instructions for Claude Code on how this project is organized and how to help effectively.

## Project Overview

This is a comprehensive memoir manuscript management system. The user has a 300-page memoir in Google Docs that has been:
1. Split into 44 individual chapter files (DOCX format)
2. Set up with a manifest-based editing system (YAML)
3. Configured for comment extraction and matching from Google Docs
4. Organized with a clean directory structure

**Original manuscript:** "From Walls to Bridges: A Journey of Resilience and Connection" by Derrick R. Burns

## Directory Structure

```
memoir-split/
├── scripts/              # All Python tools (13 scripts)
├── docs/                # Documentation (6 guides)
├── output/              # 44 split chapter files (DOCX)
├── data/                # Comments, credentials, matches
├── archive/             # Old versions, test files
├── book_structure.yaml  # Main manifest
├── requirements.txt
└── README.md
```

## Key Files You Should Know

### Main Workflow Scripts (in scripts/)
- `refresh_from_google_drive.py` - **NEW!** Auto-refresh chapters from Google Drive download
- `split_book.py` - Split book by headings
- `build_book.py` - Build from manifest
- `extract_comments.py` - Get comments from Google Docs
- `match_comments_improved.py` - Match comments to chapters (99.5% accuracy)
- `renumber_chapters.py` - Renumber chapters sequentially

### Documentation (in docs/)
- `QUICK_START.md` - Quick reference
- `MANIFEST_GUIDE.md` - Complete manifest guide
- `COMMENTS_GUIDE.md` - Comment extraction guide
- `GOOGLE_API_SETUP.md` - API setup instructions

### Data Files (in data/)
- `credentials.json` - Google API credentials (PRIVATE, .gitignored)
- `comments.json` - 383 extracted comments
- `comment_matches_improved.json` - Comment→chapter mappings

### Root Level
- `book_structure.yaml` - Defines book structure (44 sections)
- `ORGANIZATION.md` - Detailed directory organization
- This file (`claude.md`) - Instructions for you

## Project State

### What's Complete
✓ Book split into 44 chapter files (1 front matter, 9 timelines, 34 chapters)
✓ Chapters renumbered 1-34 (sequential, was 1-12, 16-37)
✓ Manifest system created for easy reordering/exclusion
✓ Comment extraction from Google Docs (383 comments)
✓ Comment matching to chapters (381/383 matched = 99.5%)
✓ Directory structure organized
✓ All documentation complete

### Current Status
- Original DOCX: `From Walls to Bridges_ A Journey of Resilience and Connection.docx`
- Split chapters: `output/` (44 files)
- Comments extracted and matched
- Ready for editing workflow

## How to Help the User

### Common Tasks

#### 0. Refresh Chapters from Google Drive (NEW WORKFLOW)

**User edits in Google Docs and wants to update local chapters:**

```bash
# User downloads from Google Drive: File > Download > Microsoft Word (.docx)
# Then runs:
python3 scripts/refresh_from_google_drive.py
```

**What this does:**
- Auto-detects latest download in ~/Downloads/
- Copies file to project directory
- Splits into 44 files (1 front matter + 9 timelines + 34 chapters)
- Renumbers chapters sequentially (1-34)
- Extracts all images

**With archiving (preserves old chapters):**
```bash
python3 scripts/refresh_from_google_drive.py --archive
```

See: `docs/REFRESH_WORKFLOW.md` for full documentation.

#### 1. Working with Comments

**View comment summary:**
```bash
# Comments are in data/comment_matches_improved.md (readable)
# Most commented chapter: chapter_22 (A Father's Love) - 95 comments
```

**Extract new comments:**
```bash
python3 scripts/extract_comments.py --doc-id 1I5aglDNAqYmdMYojLqwmCLdDzQj8UlPMdAjkviKN9hk
python3 scripts/match_comments_improved.py
```

#### 2. Building the Book

**View structure:**
```bash
python3 scripts/build_book.py --show-structure
```

**Build book:**
```bash
python3 scripts/build_book.py --output final_draft.docx
```

#### 3. Editing Book Structure

The user can reorder/exclude chapters by editing `book_structure.yaml`:
- Move chapter entries to reorder
- Set `include: false` to exclude
- Comments in YAML are allowed

After changes, rebuild with `build_book.py`

#### 4. Adding New Chapters or Sections

If the user adds new DOCX files to `output/`:
1. Add entry to `book_structure.yaml`
2. Specify file, title, include flag
3. Rebuild book

### Important Conventions

**Running scripts:**
- Always run from project root directory
- Scripts are in `scripts/` subdirectory
- Use: `python3 scripts/script_name.py`

**File paths:**
- Comments/credentials: `data/`
- Chapters: `output/`
- Old files: `archive/`
- Docs: `docs/`

**Google Doc ID:**
- The memoir's Google Doc ID: `1I5aglDNAqYmdMYojLqwmCLdDzQj8UlPMdAjkviKN9hk`
- Used for extracting comments

### What NOT to Do

❌ Don't modify files in `archive/` - they're historical
❌ Don't commit `data/credentials.json` or `data/token.pickle` - they're .gitignored
❌ Don't run scripts from inside the `scripts/` directory - run from root
❌ Don't manually renumber chapters - use `renumber_chapters.py`
❌ Don't use basic `match_comments.py` - use `match_comments_improved.py` (99.5% vs 37% match rate)

### Typical User Requests

**"Extract comments"**
→ Run extract + match scripts, show summary from comment_matches_improved.md

**"Show me the most commented chapters"**
→ Read data/comment_matches_improved.md, summarize by chapter

**"Build the book"**
→ Run build_book.py with --show-structure first, then build

**"Reorder chapters"**
→ Edit book_structure.yaml, explain how to cut/paste entries

**"Exclude a chapter"**
→ Edit book_structure.yaml, set include: false

**"What's the current structure?"**
→ Run build_book.py --show-structure

**"How many comments are there?"**
→ 383 total, 381 matched to chapters (99.5%)
→ Most on chapter_22 (95 comments)

### Problem Solving

**"Comments not matching well"**
→ They're already using improved matcher (99.5% rate)
→ Only 2/383 unmatched - this is excellent

**"Chapter numbering is wrong"**
→ Run renumber_chapters.py to fix
→ Or manually edit chapter file names and book_structure.yaml

**"Need to split a new version"**
→ Use split_book.py with --heading-level 2 (their chapters are H2)

**"Build failed"**
→ Check book_structure.yaml syntax
→ Ensure all files in manifest exist in output/

### Code Quality Standards

When writing new scripts:
- Use python-docx for DOCX operations
- Add to `scripts/` directory
- Include argparse with --help
- Follow existing code patterns
- Update requirements.txt if adding dependencies
- Document in ORGANIZATION.md if significant

### Testing Workflow

Before major changes:
1. Check current structure: `build_book.py --show-structure`
2. Make change (edit YAML, add script, etc.)
3. Test build: `build_book.py --output test.docx`
4. Verify output
5. If good, use for final: `build_book.py --output final.docx`

## Technical Details

### Technologies Used
- **python-docx** - DOCX manipulation
- **PyYAML** - Manifest parsing
- **rapidfuzz** - Fuzzy text matching (for comments)
- **Google API Client** - Comment extraction from Google Docs

### Book Statistics
- **Total pages:** ~300
- **Chapters:** 34 (numbered sequentially)
- **Timeline sections:** 9
- **Front matter:** 1 file
- **Total sections:** 44
- **Comments:** 383 (from Google Doc)
- **Match rate:** 99.5% (381/383)

### Idempotence
The split→merge workflow is idempotent:
- split_book.py preserves all content, styles, images
- merge_book.py reconstructs identically
- Verified: split→merge→split→merge produces identical files

### Publishing System
- **Pandoc-based** - DOCX → Markdown → {EPUB, PDF}
- **EPUB** - Ebook for Kindle, Apple Books, etc.
- **PDF** - Print-ready for KDP Print, IngramSpark
- **Metadata** - Book info in metadata.yaml
- **Single source** - Markdown for both formats
- **No Typst** - User decided against it

## Publishing Workflow

When the user is ready to publish:

### Publishing Commands
```bash
# Build both EPUB and PDF
python3 scripts/build_all.py --cover cover.jpg

# Or step by step:
python3 scripts/export_markdown.py   # DOCX → Markdown
python3 scripts/build_epub.py        # Markdown → EPUB
python3 scripts/build_pdf.py         # Markdown → PDF
```

### Publishing Scripts (in scripts/)
- **export_markdown.py** - Convert from DOCX to Markdown
- **build_epub.py** - Generate EPUB ebook
- **build_pdf.py** - Generate PDF via LaTeX
- **build_all.py** - Build both formats at once

### Publishing Files
- **metadata.yaml** - Book metadata (title, author, ISBN, etc.)
- **cover.jpg** - Cover image for EPUB (1600x2560px)
- **docs/PUBLISHING_GUIDE.md** - Complete publishing guide
- **PUBLISHING_SETUP.md** - Setup summary

### Prerequisites for Publishing
**Installed:**
- ✓ Pandoc 3.7+ (already installed)

**Needed:**
- LaTeX for PDF generation:
  ```bash
  brew install --cask mactex
  # Or smaller: brew install --cask basictex
  ```

**Optional:**
- epubcheck (EPUB validation)
- calibre (ebook reader/testing)

### Publishing Output
- `manuscript.md` - Markdown source (single source of truth)
- `book.epub` - Ebook for distribution
- `book.pdf` - Print book (6" x 9" format)
- `media/` - Extracted images

### Distribution Platforms
**Ebook:**
- Amazon KDP (Kindle)
- Apple Books
- Google Play Books
- Draft2Digital (aggregator)

**Print:**
- Amazon KDP Print
- IngramSpark
- Lulu

### Common Publishing Tasks

**"Build for publishing"**
→ Run build_all.py, outputs EPUB and PDF

**"I need to publish"**
→ Check if LaTeX installed, guide through build_all.py, explain distribution options

**"How do I get an ISBN?"**
→ Bowker (US) $125 for one, or use free KDP ISBN

**"Update the cover"**
→ Replace cover.jpg (1600x2560px), rebuild with --cover flag

**"Change book size/formatting"**
→ Edit metadata.yaml geometry settings

**"Publishing failed"**
→ Check if LaTeX installed, review error messages, consult PUBLISHING_GUIDE.md

## Quick Reference

**Most used commands:**
```bash
# Show book structure
python3 scripts/build_book.py --show-structure

# Build book
python3 scripts/build_book.py --output book.docx

# Extract comments
python3 scripts/extract_comments.py --doc-id 1I5aglDNAqYmdMYojLqwmCLdDzQj8UlPMdAjkviKN9hk

# Match comments
python3 scripts/match_comments_improved.py

# View comments report
open data/comment_matches_improved.md

# Publish (EPUB + PDF)
python3 scripts/build_all.py --cover cover.jpg
```

**Most viewed files:**
```bash
# Main documentation
cat README.md

# Book structure
cat book_structure.yaml

# Comment matches
cat data/comment_matches_improved.md

# Organization
cat ORGANIZATION.md
```

## When User is Stuck

1. **Check README.md** - Has workflow examples
2. **Check docs/** - Specific guides for each feature
3. **Check ORGANIZATION.md** - File locations
4. **Run --help** on any script - All have built-in help
5. **Check this file** - You're reading it!

## Your Goals When Helping

1. **Be efficient** - User knows what they want, execute quickly
2. **Use correct paths** - Scripts in scripts/, data in data/
3. **Preserve work** - Don't overwrite without asking
4. **Show results** - Summarize outputs, show key findings
5. **Stay organized** - Keep the clean directory structure

## Remember

- This is a professional memoir project
- User has spent significant time on organization
- All systems are working - help maintain them
- Focus on the content/editing workflow
- The technical infrastructure is complete

## Last Session Summary

The last session:
1. Created improved comment matcher (99.5% vs 37% match rate)
2. Reorganized entire directory structure
3. Updated all paths in scripts and docs
4. Created comprehensive documentation
5. Identified chapter 22 has 95 comments (needs most work)

User is now ready to work on addressing comments and refining the manuscript.
