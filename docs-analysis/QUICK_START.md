# Quick Start: Manifest-Based Editing

## Setup Complete! ✓

Your book is now set up for easy editing via a manifest file.

## Files Created

- ✓ `book_structure.yaml` - **Edit this to change your book**
- ✓ `build_book.py` - Build the book from the manifest
- ✓ `remove_empty_headings.py` - Clean up empty headings
- ✓ `From Walls to Bridges_no_empty_headings.docx` - Cleaned version (20 empty headings removed)

## Your Book Structure

```
Front Matter (1 file)
├── Title page, dedication, chronological guide

Timeline Sections (9 files)
├── Early Life (1964-1982)
├── Princeton Years (1982-1986)
├── Graduate School & Early Career (1986-1990)
├── Silicon Valley Rise (1990-1997)
├── Professional Peaks & Valleys (1998-2004)
├── Family Transitions (2000-2013)
├── Personal Growth (2010-2023)
├── Health Crisis & Renewal (2023-2024)
└── Key Relationships Timeline

Chapters (34 files, sequential 1-34)
├── Chapter 1: Two Worlds Converging
├── Chapter 2: The Perfect Shot
├── ...
└── Chapter 34: Fearless Love

Total: 44 independent sections
```

## Three-Step Workflow

### 1. VIEW the current structure

```bash
python build_book.py --show-structure
```

See what's included/excluded, the order, etc.

### 2. EDIT the manifest

```bash
# Open in your favorite text editor
open book_structure.yaml
```

Examples of what you can do:
- Move chapter 10 before chapter 5 (cut & paste in YAML)
- Exclude chapter 8 (set `include: false`)
- Add notes (`# TODO: revise this chapter`)

### 3. BUILD the book

```bash
python build_book.py --output my_book.docx
```

Creates `my_book.docx` with your changes applied.

## Common Tasks

### Exclude a Chapter

In `book_structure.yaml`, find the chapter and change `include`:

```yaml
  - number: 8
    file: "output/chapter_08_*.docx"
    title: "Finding My Voice"
    include: false  # ← Changed from true
```

Build again, chapter 8 will be skipped.

### Reorder Two Chapters

Just cut and paste the entries in the YAML file:

**Want chapter 10 to come before chapter 9?**

Cut the chapter 10 entry and paste it above chapter 9. Build. Done.

### Add Editorial Notes

```yaml
  - number: 15
    file: "output/chapter_15_*.docx"
    title: "Becoming Real"
    include: true
    # NOTE: Consider expanding the Stanford section
    # TODO: Add more dialogue with Gina
```

Comments (lines starting with `#`) are ignored by the builder.

## Example: Creating a Short Version

1. Copy the manifest:
   ```bash
   cp book_structure.yaml book_structure_short.yaml
   ```

2. Edit `book_structure_short.yaml`:
   - Exclude some timeline sections
   - Exclude some chapters
   - Keep only the essential story

3. Build both versions:
   ```bash
   python build_book.py --manifest book_structure.yaml --output full.docx
   python build_book.py --manifest book_structure_short.yaml --output short.docx
   ```

4. Now you have two versions!

## Benefits

✓ **No file juggling** - Edit one text file instead of moving DOCX files
✓ **Reversible** - Just change the manifest back
✓ **Version control** - Track changes with git
✓ **Visible structure** - See entire book at a glance
✓ **Experiment safely** - Original files never change

## What Changed from Original?

**Before:**
- Chapters numbered 1-12, 16-37 (gap at 13-15)
- Empty heading artifacts
- Hard to reorder or exclude chapters

**After:**
- Chapters renumbered 1-34 (sequential)
- Empty headings removed
- Easy to edit via manifest
- All Heading 1 sections preserved (Acts, etc.)

## Pro Tips

1. **Always check structure first:**
   ```bash
   python build_book.py --show-structure
   ```

2. **Make small changes** - one at a time, build, review

3. **Use git** to track your manifest changes:
   ```bash
   git add book_structure.yaml
   git commit -m "Excluded chapter 8, moved chapter 10"
   ```

4. **Keep multiple versions** - full, short, chronological, etc.

5. **Add comments** to track your thinking:
   ```yaml
   # Excluding this chapter because it's redundant with chapter 12
   ```

## Need Help?

- **Full guide:** See `MANIFEST_GUIDE.md`
- **Splitting/merging:** See `README.md`
- **Renumbering:** See `RENUMBERING_SUMMARY.md`

## You're Ready!

Your memoir is now a **flexible, editable system**:
- 44 independent section files
- 1 manifest that controls structure
- Simple tools to build different versions

**Next:** Open `book_structure.yaml` and take a look around. Try excluding one chapter and rebuilding!
