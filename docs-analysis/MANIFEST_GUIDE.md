# Manifest-Based Book Editing Guide

This system allows you to easily edit, rearrange, exclude, and merge chapters using a simple manifest file.

## Overview

The manifest-based system separates **content** (individual chapter files) from **structure** (the manifest file). This makes it easy to:

- ✓ See the entire book structure at a glance
- ✓ Reorder chapters by editing a text file
- ✓ Exclude chapters without deleting files
- ✓ Merge chapters by listing multiple files
- ✓ Track which chapters are included/excluded
- ✓ Experiment with different structures

## Files

```
memoir-split/
├── book_structure.yaml     ← EDIT THIS to change book structure
├── build_book.py           ← Run this to build the book
├── output/                 ← Individual chapter files (DOCX)
│   ├── chapter_01_*.docx
│   ├── chapter_02_*.docx
│   └── ...
└── book.docx               ← Built output
```

## The Manifest File: `book_structure.yaml`

This is a simple text file that defines your book's structure:

```yaml
# Book metadata
book:
  title: "Your Book Title"
  author: "Your Name"

# Front matter
front_matter:
  - file: "output/00_Front_Matter.docx"
    title: "Front Matter"
    include: true

# Timeline sections
timeline:
  - file: "output/Early_Life_1964-1982.docx"
    title: "Early Life"
    include: true
  # ... more timeline sections

# Chapters
chapters:
  - number: 1
    file: "output/chapter_01_*.docx"
    title: "Chapter Title"
    include: true
  # ... more chapters
```

## Common Editing Tasks

### 1. Exclude a Chapter (Don't Delete, Just Skip)

Change `include: true` to `include: false`:

```yaml
chapters:
  - number: 5
    file: "output/chapter_05_*.docx"
    title: "Developing the Picture"
    include: false  # ← Chapter will be skipped
```

Or comment it out:

```yaml
chapters:
  # - number: 5
  #   file: "output/chapter_05_*.docx"
  #   title: "Developing the Picture"
  #   include: true
```

### 2. Reorder Chapters

Just cut and paste entries in the YAML file. The chapters will be renumbered automatically when built:

**Before:**
```yaml
chapters:
  - number: 3
    file: "output/chapter_03_*.docx"
    title: "Lessons from Aunt Mae"

  - number: 4
    file: "output/chapter_04_*.docx"
    title: "The Project Begins"
```

**After (swapped):**
```yaml
chapters:
  - number: 4  # Now appears first
    file: "output/chapter_04_*.docx"
    title: "The Project Begins"

  - number: 3  # Now appears second
    file: "output/chapter_03_*.docx"
    title: "Lessons from Aunt Mae"
```

### 3. Merge Chapters

To merge multiple chapter files into one section, list them together:

```yaml
chapters:
  - number: 1
    title: "Early Years (Combined)"
    files:  # ← Note: 'files' plural
      - "output/chapter_01_*.docx"
      - "output/chapter_02_*.docx"
      - "output/chapter_03_*.docx"
    include: true
```

### 4. Add Notes/Comments

Use `#` for comments:

```yaml
chapters:
  - number: 5
    file: "output/chapter_05_*.docx"
    title: "Developing the Picture"
    include: true
    # TODO: This chapter needs revision
    # Note: Consider merging with chapter 6
```

### 5. Temporarily Disable Entire Sections

```yaml
# Uncomment to include timeline sections
# timeline:
#   - file: "output/Early_Life_1964-1982.docx"
#     ...
```

## Building the Book

### View the Current Structure

```bash
python build_book.py --show-structure
```

Output:
```
================================================================================
BOOK STRUCTURE
================================================================================

Title: From Walls to Bridges: A Journey of Resilience and Connection
Author: Derrick R. Burns

====================================Chapters====================================
  ✓ Chapter 1: Two Worlds Converging
  ✓ Chapter 2: The Perfect Shot
  ✗ Chapter 3: Lessons from Aunt Mae (EXCLUDED)
  ✓ Chapter 4: The Project Begins
  ...

  → 32 of 34 chapters included
```

### Build the Book

```bash
# Build to default output (book.docx)
python build_book.py

# Build to specific output file
python build_book.py --output final_draft.docx

# Build quietly (minimal output)
python build_book.py --quiet
```

## Workflow Example

Let's say you want to experiment with a different chapter order:

```bash
# 1. Check current structure
python build_book.py --show-structure

# 2. Edit book_structure.yaml
#    - Move chapter 10 to position 5
#    - Exclude chapters 8 and 9 temporarily

# 3. Build new version
python build_book.py --output experimental_order.docx

# 4. Review the output

# 5. If you like it, make it the main version
python build_book.py --output book.docx

# 6. If not, revert book_structure.yaml using git
git checkout book_structure.yaml
```

## Advanced: Multiple Versions

You can maintain multiple manifest files for different versions:

```bash
# Full version
book_structure.yaml

# Shorter version (exclude some chapters)
book_structure_short.yaml

# Reordered version
book_structure_chronological.yaml
```

Build each version:

```bash
python build_book.py --manifest book_structure.yaml --output full.docx
python build_book.py --manifest book_structure_short.yaml --output short.docx
python build_book.py --manifest book_structure_chronological.yaml --output chrono.docx
```

## Tips

1. **Always use `--show-structure` first** to see what will be built
2. **Keep the manifest in version control** (git) so you can track changes
3. **The original chapter files never change** - only the manifest changes
4. **Make incremental changes** - change one thing, build, review
5. **Add comments** to track your reasoning for changes

## Removing Empty Headings

Your original document had 20 empty heading paragraphs (formatting artifacts). To clean it:

```bash
# Check for empty headings
python remove_empty_headings.py original.docx --analyze

# Remove them
python remove_empty_headings.py original.docx -o cleaned.docx
```

## Requirements

```bash
pip install pyyaml
```

(python-docx already installed)

## Your Current Structure

Your memoir has:
- **1 front matter file** (Title, Dedication, Chronological Guide)
- **9 timeline sections** (Early Life through Key Relationships)
- **34 chapters** (now sequential, 1-34)
- **All Heading 1 sections preserved** (Acts, Preface, Acknowledgments)

Total: **44 sections** that can be rearranged independently.

## Next Steps

1. Review `book_structure.yaml` - this is your book's table of contents
2. Try `python build_book.py --show-structure` to see the current layout
3. Experiment with excluding a chapter: set `include: false`
4. Build and review: `python build_book.py --output test.docx`
5. When satisfied, build the final version

The manifest makes your book structure **visible**, **editable**, and **version-controllable**!
