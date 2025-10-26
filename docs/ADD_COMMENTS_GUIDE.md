# Google Doc Comment Addition Guide

## Overview

The `add_comments_to_google_doc.py` script automatically adds anchored comments to your Google Doc memoir. These comments highlight:

1. **Timeline information** - Year(s), age(s), and time period for each chapter
2. **Character introductions** - Flags where key characters first appear with notes on proper introduction
3. **Chapter overlaps** - Identifies chapters covering the same time periods

## Current Status

### Comments Defined: 54 total

- **Timeline comments**: All 34 chapters
- **Character introduction comments**: Chapters 1-3, 21-34 (key characters only)
- **Coverage**: Chapters 4-20 have timeline comments but limited character introduction comments

### Test Results

- ✓ Successfully creates anchored comments (attached to specific text)
- ✓ Uses Named Ranges to link comments to text locations
- ✓ 51/54 comments successfully match text in document
- ✓ 3 comments couldn't find their location text (may need adjustment)

## How It Works

The script uses a two-step process to create text-anchored comments:

1. **Create Named Range**: Uses Google Docs API to create a named range at the specific text location
2. **Add Comment**: Uses Google Drive API to create a comment anchored to that named range

This is the only way to programmatically create text-specific comments in Google Docs.

## Usage

### Prerequisites

- Google API credentials (already configured in `data/credentials.json`)
- Python 3 with required packages
- The script uses the memoir doc ID: `1I5aglDNAqYmdMYojLqwmCLdDzQj8UlPMdAjkviKN9hk`

### Commands

**1. Dry run (recommended first)**
```bash
python3 scripts/add_comments_to_google_doc.py --dry-run
```
Shows what would be done without actually adding comments.

**2. Add all comments**
```bash
python3 scripts/add_comments_to_google_doc.py
```
Adds all 54 defined comments to the Google Doc.

**3. Add comments for specific chapter**
```bash
python3 scripts/add_comments_to_google_doc.py --chapter 12
```
Only adds comments for the specified chapter.

**4. Dry run for specific chapter**
```bash
python3 scripts/add_comments_to_google_doc.py --chapter 12 --dry-run
```

### First Run

On first run with new scopes, you'll need to:
1. Authorize in your browser when prompted
2. The script will save credentials in `data/token.pickle`
3. Subsequent runs will use saved credentials

## What Comments Are Added

### Timeline Comments (All 34 Chapters)

Example from Chapter 1:
```
TIMELINE: April 1964 | Age 0 (birth) | Adoption story - birth and placement
```

Example from Chapter 15 (with overlap note):
```
TIMELINE: 1990s-2000s | Age 26-40s | Marriage, career, family

OVERLAPS WITH: Chapters 16-21 (scrambled timeline - all cover 1990-2010 period)
```

### Character Introduction Comments (Selective)

Example from Chapter 1:
```
INTRODUCE: Willa Burns - adoptive mother, 4'11", special education teacher,
determined, strict (give full introduction with physical description,
personality traits, teaching background)
```

Example from Chapter 28:
```
INTRODUCE: Reverend Doctor William J. Barber II (Doctor Barber/Bishop Barber) -
led Poor People's Campaign where Jala was community organizer, Jala had his
private number, deep connection with Jala, quoted Matthew 19:12 and Acts
8:26-40 about eunuchs, reassured Jala she wouldn't go to hell for being
transgender or stopping dialysis, agreed to preside over her funeral
```

## Extending the Script

### Adding More Character Introduction Comments

The comprehensive character analysis is available in:
- `docs/CHARACTER_INTRODUCTIONS_COMPLETE.md` - All 119+ characters needing introduction
- `docs/CHAPTER_SUMMARIES.md` - Detailed chapter summaries with all characters

To add more comments, edit the `get_chapter_comments()` function in the script:

```python
comments.extend([
    {
        'chapter': 5,
        'location_text': 'exact text where character first appears',
        'comment_text': 'INTRODUCE: Name - description, relationship, context',
        'comment_type': 'character'
    },
])
```

### Finding Location Text

The `location_text` must match exactly how it appears in the document. To find it:
1. Open the Google Doc
2. Search for the text where you want the comment
3. Copy the exact first few words
4. Use that as `location_text`

## Known Limitations

1. **3 skipped comments**: Some location text couldn't be found in the document
   - These may need adjustment to match exact text
   - Run with `--dry-run` to see which ones fail

2. **Named ranges remain**: Each comment creates a named range in the document
   - These are invisible but remain in the document structure
   - Generally harmless, but many may accumulate

3. **No bulk delete**: The script only adds comments, doesn't remove them
   - Comments must be deleted manually from Google Docs UI if needed

## Testing

The script was tested successfully:
- ✓ Chapter 1: Added 4 comments (timeline + 3 character introductions)
- ✓ Chapter 34: Added 3 comments (timeline + 2 character introductions)
- ✓ All comments are properly anchored to specific text

## Next Steps

1. **Review the comments** in dry-run mode:
   ```bash
   python3 scripts/add_comments_to_google_doc.py --dry-run
   ```

2. **Add comments incrementally** by chapter to test:
   ```bash
   python3 scripts/add_comments_to_google_doc.py --chapter 1
   ```

3. **Add all comments** when ready:
   ```bash
   python3 scripts/add_comments_to_google_doc.py
   ```

4. **Expand character comments** for chapters 4-20 using the detailed analysis in:
   - `docs/CHARACTER_INTRODUCTIONS_COMPLETE.md`
   - `docs/PUBLICATION_ACTION_PLAN.md`

## Related Documentation

- `docs/PUBLICATION_ACTION_PLAN.md` - 10-12 week plan to publication
- `docs/CHARACTER_INTRODUCTIONS_COMPLETE.md` - All 119+ characters needing introduction
- `docs/CHAPTER_SUMMARIES.md` - Comprehensive chapter summaries
- `docs/READER_ENGAGEMENT_ANALYSIS.md` - Chapter-by-chapter reader experience analysis
