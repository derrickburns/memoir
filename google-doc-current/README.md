# Google Doc Current - Exact Split of Current Google Drive Document

**Last Updated:** 2025-11-14
**Source:** Google Drive memoir document

## What This Directory Contains

This directory contains **PRECISELY** the current state of your Google Doc memoir, split into individual chapter files.

These are exact conversions from .docx to .txt format with NO editing or restructuring.

## Files

- `chapter_01.txt` through `chapter_34.txt` - Current chapters from Google Doc
- 34 total chapters

## Purpose

This directory serves as:
1. **Reference** - See exactly what's in Google Docs right now
2. **Comparison** - Compare against proposed reorganization
3. **Backup** - Snapshot of current state before any changes

## DO NOT EDIT

These files are READ-ONLY snapshots. They represent the current Google Doc state.

Any proposed changes should be in `proposed-reorganization/` directory.

## How These Were Created

```bash
# Pulled from Google Drive on 2025-11-14
python3 scripts/refresh_from_google_drive.py
python3 scripts/convert_to_txt.py
```

## Related Directories

- `proposed-reorganization/` - Proposed new chapter structure (Chapters 3-6 reorganized)
- `docs-analysis/` - All analysis, timelines, and implementation notes
- `output/` - Legacy directory with various versions (being phased out)
