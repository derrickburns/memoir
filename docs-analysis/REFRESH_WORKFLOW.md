# Refresh Workflow - Updating Chapters from Google Drive

**Purpose:** Automatically download, split, and renumber memoir chapters from Google Drive
**Created:** 2025-10-24

---

## Quick Start

### 1. Download from Google Drive
```
Open Google Doc → File → Download → Microsoft Word (.docx)
```
The file will be saved to your Downloads folder.

### 2. Run Refresh Script
```bash
python3 scripts/refresh_from_google_drive.py
```

That's it! The script will:
- ✅ Find the latest download automatically
- ✅ Copy it to the project directory
- ✅ Split into chapters (by Heading 2)
- ✅ Renumber chapters sequentially (1-34)
- ✅ Extract all images to chapter-specific directories

---

## Detailed Workflow

### Manual Process (Before This Script)

The old way required multiple steps:

```bash
# 1. Download from Google Drive (manual)
# 2. Move file to project directory (manual)
# 3. Split the book
python3 scripts/split_book.py "memoir.docx" --output output --heading-level 2
# 4. Renumber chapters
python3 scripts/renumber_chapters.py output
# 5. Verify structure
python3 scripts/build_book.py --show-structure
```

### New Automated Process

Now it's a single command:

```bash
python3 scripts/refresh_from_google_drive.py
```

The script handles all steps automatically!

---

## Command Options

### Basic Usage
```bash
# Auto-detect latest download and process
python3 scripts/refresh_from_google_drive.py
```

### Specify Source File
```bash
# Use a specific file instead of auto-detection
python3 scripts/refresh_from_google_drive.py --source ~/Downloads/memoir.docx
```

### Archive Old Chapters
```bash
# Save old chapters to archive/ before replacing
python3 scripts/refresh_from_google_drive.py --archive
```

### Dry Run
```bash
# See what would be done without actually doing it
python3 scripts/refresh_from_google_drive.py --dry-run
```

### Custom Options
```bash
# Full control
python3 scripts/refresh_from_google_drive.py \
  --source ~/Downloads/memoir.docx \
  --output output \
  --heading-level 2 \
  --archive
```

---

## What the Script Does

### Step 1: Find Source File
Searches for the most recently downloaded memoir file in:
- `~/Downloads/` (most common)
- `~/Desktop/` (alternative)
- Current directory (fallback)

Looks for filenames matching:
- `From Walls to Bridges*.docx`
- `memoir*.docx`
- `*memoir*.docx`

### Step 2: Copy to Project
Copies the source file to the project root directory for processing.

### Step 3: Archive Old Chapters (Optional)
If `--archive` is used, moves old chapters to:
```
archive/chapters_YYYYMMDD_HHMMSS/
```

### Step 4: Split the Book
Runs `split_book.py` to:
- Extract front matter
- Extract timeline sections (9 timelines)
- Extract chapters (34 chapters)
- Extract all images to chapter-specific directories

### Step 5: Renumber Chapters
Runs `renumber_chapters.py` to:
- Renumber chapters 1-34 sequentially
- Handle the gap in original numbering (1-12, 16-37 → 1-34)

### Step 6: Summary
Shows what was processed:
- Number of chapters
- Number of timeline sections
- Output directory location
- Next steps

---

## Output Structure

After running the script, the output/ directory contains:

```
output/
├── 00_Front_Matter.docx
├── 00_Front_Matter_images/
│   └── image_001.png
│
├── Early_Life_1964-1982.docx
├── Princeton_Years_1982-1986.docx
├── Graduate_School__Early_Career_1986-1990.docx
├── Silicon_Valley_Rise_1990-1997.docx
├── Professional_Peaks__Valleys_1998-2004.docx
├── Family_Transitions_2000-2013.docx
├── Personal_Growth_2010-2023.docx
├── Health_Crisis__Renewal_2023-2024.docx
├── Key_Relationships_Timeline.docx
├── Key_Relationships_Timeline_images/
│   └── image_001.jpg
│
├── chapter_01_Chapter_1_Two_Worlds_Converging.docx
├── chapter_01_images/
├── chapter_02_Chapter_2_The_Perfect_Shot.docx
├── chapter_02_images/
├── ...
├── chapter_34_Chapter_34_Fearless_Love.docx
└── chapter_34_images/ (if chapter has images)
```

**Total Files:**
- 1 front matter file
- 9 timeline section files
- 34 chapter files
- Image directories for chapters with photos

---

## When to Use This Script

### Regular Updates from Google Drive

**Scenario:** You edit the memoir in Google Docs and want to refresh the local chapter files.

**Steps:**
1. Make edits in Google Docs
2. Download: File → Download → Microsoft Word (.docx)
3. Run: `python3 scripts/refresh_from_google_drive.py`
4. Done!

### After Major Edits

**Scenario:** You've made significant changes and want to preserve old chapters.

**Steps:**
```bash
python3 scripts/refresh_from_google_drive.py --archive
```

Old chapters will be saved to `archive/chapters_YYYYMMDD_HHMMSS/` before being replaced.

### Testing Changes

**Scenario:** You want to see what would happen without making changes.

**Steps:**
```bash
python3 scripts/refresh_from_google_drive.py --dry-run
```

### Using a Specific File

**Scenario:** The file isn't in Downloads or you have multiple versions.

**Steps:**
```bash
python3 scripts/refresh_from_google_drive.py --source /path/to/memoir.docx
```

---

## Verification Steps

After running the refresh script, verify everything worked:

### 1. Check Chapter Count
```bash
ls output/chapter_*.docx | wc -l
```
Should show: **34**

### 2. View Book Structure
```bash
python3 scripts/build_book.py --show-structure
```
Should show:
- Front Matter: ✓
- 9 Timeline Sections: ✓
- 34 Chapters: ✓ (numbered 1-34)

### 3. Verify Specific Chapters
```bash
ls output/chapter_01*.docx  # Chapter 1
ls output/chapter_22*.docx  # Chapter 22 (A Father's Love - most commented)
ls output/chapter_34*.docx  # Chapter 34 (last chapter)
```

### 4. Check Images
```bash
ls output/chapter_*_images | head -5  # See first 5 image directories
```

---

## Troubleshooting

### "Could not find memoir DOCX file"

**Problem:** Script can't find the downloaded file.

**Solutions:**
1. Check the file is in ~/Downloads/
2. Verify filename contains "memoir" or "From Walls to Bridges"
3. Specify file manually: `--source ~/Downloads/your-file.docx`

### "ERROR: Split failed"

**Problem:** The split_book.py script encountered an error.

**Solutions:**
1. Check the source file is a valid DOCX
2. Verify the file isn't corrupted
3. Try re-downloading from Google Drive
4. Check for error messages in the output

### "ERROR: Renumbering failed"

**Problem:** The renumber_chapters.py script encountered an error.

**Solutions:**
1. Verify chapters were created successfully
2. Check output/ directory isn't empty
3. Look for error messages indicating which chapter failed

### Too Many/Too Few Chapters

**Problem:** Not getting the expected 34 chapters.

**Causes:**
1. Wrong heading level (should be 2)
2. Source document structure changed
3. Previous chapter files not cleaned up

**Solutions:**
```bash
# Clean and retry
rm -rf output/chapter_*.docx output/chapter_*_images
python3 scripts/refresh_from_google_drive.py
```

---

## Integration with Other Workflows

### With Comment Extraction

After refreshing chapters, re-match comments to the new files:

```bash
# 1. Refresh chapters from Google Drive
python3 scripts/refresh_from_google_drive.py

# 2. Extract comments
python3 scripts/extract_comments.py --doc-id YOUR_DOC_ID

# 3. Match comments to new chapter files
python3 scripts/match_comments_improved.py

# 4. Review matches
open data/comment_matches_improved.md
```

### With Publishing Workflow

After refreshing, build publication formats:

```bash
# 1. Refresh chapters
python3 scripts/refresh_from_google_drive.py

# 2. Build book
python3 scripts/build_book.py --output final_draft.docx

# 3. Publish
python3 scripts/build_all.py --cover cover.jpg
```

### With Character Introduction Fixes

After making character introduction edits in Google Docs:

```bash
# 1. Refresh to get latest edits
python3 scripts/refresh_from_google_drive.py

# 2. Verify character introductions were applied
# Check specific chapters where you made changes
```

---

## Best Practices

### 1. Regular Refreshes
Refresh chapters whenever you make significant edits in Google Docs:
```bash
# Quick refresh after editing
python3 scripts/refresh_from_google_drive.py
```

### 2. Archive Before Major Changes
Before major restructuring, archive old chapters:
```bash
# Preserve old version
python3 scripts/refresh_from_google_drive.py --archive
```

### 3. Verify After Each Refresh
Always check the structure after refreshing:
```bash
python3 scripts/build_book.py --show-structure
```

### 4. Keep Google Doc as Source of Truth
- Edit in Google Docs (collaborative, comments, version history)
- Refresh local chapters regularly
- Use local chapters for publishing/analysis

---

## Script Location

**File:** `scripts/refresh_from_google_drive.py`
**Executable:** Yes (`chmod +x` applied)
**Requirements:**
- Python 3.7+
- python-docx (from requirements.txt)
- Other memoir-split scripts (split_book.py, renumber_chapters.py)

---

## Related Documentation

- **README.md** - Main project documentation
- **docs/QUICK_START.md** - Quick reference for editing workflow
- **docs/CHAPTER_RENUMBERING_SUMMARY.md** - Chapter numbering details
- **docs/PUBLISHING_GUIDE.md** - Publishing workflow

---

## Summary

The refresh workflow automates the process of updating local chapter files from Google Drive:

1. **Download** from Google Drive (manual step)
2. **Run script** - `python3 scripts/refresh_from_google_drive.py`
3. **Verify** - Check structure with `build_book.py --show-structure`

This replaces the old multi-step manual process with a single automated command, ensuring consistent chapter numbering and proper image extraction every time.
