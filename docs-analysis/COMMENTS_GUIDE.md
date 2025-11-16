# Comment Extraction and Matching Guide

This guide explains how to extract comments from your Google Doc and match them to your split chapter files.

## Overview

The comment extraction system consists of three main components:

1. **extract_comments.py** - Fetches comments from Google Docs via API
2. **match_comments.py** - Matches comments to split chapter files
3. **Google API credentials** - Required for accessing Google Docs

## Quick Start

### 1. Set Up Google API Access

Follow the detailed instructions in [GOOGLE_API_SETUP.md](GOOGLE_API_SETUP.md) to:
- Create a Google Cloud project
- Enable Google Docs and Drive APIs
- Download OAuth credentials
- Get your document ID

**Summary:**
```bash
# Place your downloaded credentials.json in this directory
# Get your document ID from the Google Doc URL:
# https://docs.google.com/document/d/YOUR_DOC_ID_HERE/edit
```

### 2. Extract Comments from Google Doc

```bash
# Run the extraction script with your document ID
python3 extract_comments.py --doc-id YOUR_DOCUMENT_ID

# First run will open a browser for authentication
# Subsequent runs will use saved credentials
```

**Output:**
- `comments.json` - Structured JSON with all comments
- `comments.md` - Human-readable markdown version

### 3. Match Comments to Chapters

```bash
# Use the IMPROVED matcher (recommended - 99.5% match rate!)
python3 match_comments_improved.py

# This creates:
# - comment_matches_improved.json (structured data)
# - comment_matches_improved.md (readable report)

# Alternative: Basic matcher (37% match rate, faster but less accurate)
# python3 match_comments.py
```

### 4. Review the Results

Open `comment_matches_improved.md` to see:
- Comments grouped by chapter
- Author, date, and status (open/resolved)
- The quoted text and comment content
- Match quality (exact or fuzzy)

## Workflow Examples

### Extract and Match in One Go

```bash
# Extract comments
python3 extract_comments.py --doc-id YOUR_DOC_ID

# Match to chapters (using improved algorithm)
python3 match_comments_improved.py

# Review the report
open comment_matches_improved.md
```

### Use Custom File Names

```bash
# Extract to specific file
python3 extract_comments.py --doc-id YOUR_DOC_ID --output my_comments.json

# Match using that file
python3 match_comments_improved.py --comments my_comments.json --output my_matches.json
```

### Adjust Matching Sensitivity

```bash
# Use stricter matching (only scores 80+)
python3 match_comments_improved.py --min-score 80

# Use more lenient matching (scores 50+, may have false positives)
python3 match_comments_improved.py --min-score 50
```

## Why Two Matchers?

**match_comments_improved.py** (RECOMMENDED)
- Uses 5 different matching strategies
- 99.5% match rate (vs 37% for basic)
- Finds exact matches, normalized matches, sliding window, paragraph-level, and token-based matches
- Shows match quality score for each comment
- Takes ~60-90 seconds for 383 comments
- Requires `rapidfuzz` library

**match_comments.py** (Basic, for comparison)
- Simple exact + fuzzy matching
- 37% match rate
- Faster (~10 seconds) but misses most comments
- Kept for reference/comparison

## Understanding the Output

### comments.json

Contains the raw comments from Google Docs:

```json
{
  "document_title": "From Walls to Bridges...",
  "total_comments": 42,
  "comments": [
    {
      "id": "comment123",
      "content": "This needs more detail",
      "author": "Jane Smith",
      "created": "2024-01-15T10:30:00Z",
      "resolved": false,
      "quoted_text": "He walked into the room..."
    }
  ]
}
```

### comment_matches.json

Contains comments matched to chapters:

```json
{
  "total_comments": 42,
  "matched_comments": 38,
  "unmatched_comments": 4,
  "comment_matches": [
    {
      "comment_id": "comment123",
      "content": "This needs more detail",
      "matches": [
        {
          "chapter": "chapter_05_Developing_the_Picture.docx",
          "similarity": 1.0,
          "match_type": "exact"
        }
      ]
    }
  ]
}
```

### comment_matches.md

Human-readable report organized by chapter:

```markdown
## Comments by Chapter

### chapter_05_Developing_the_Picture.docx

○ Open - Jane Smith (2024-01-15)

> He walked into the room...

**Comment:** This needs more detail

*Match: exact, similarity: 100.00%*
```

## Matching Algorithm

The matcher uses two strategies:

1. **Exact matching** - Looks for the exact quoted text in chapters
2. **Fuzzy matching** - Uses similarity scoring for partial matches

### Match Quality

- **1.0 (100%)** - Exact match, text found verbatim
- **0.9-0.99** - Very similar, likely correct chapter
- **0.6-0.89** - Somewhat similar, may be correct
- **< 0.6** - Not matched (below threshold)

## Troubleshooting

### No comments found

**Cause:** The Google Doc may not have any comments, or comments may be resolved/deleted.

**Solution:**
- Check the Google Doc in a browser - are there visible comments?
- The Drive API only returns unresolved comments by default
- Try adding `includeDeleted=True` in extract_comments.py if needed

### Comments extracted but not matched

**Possible causes:**
1. The quoted text was edited after the comment was made
2. The text is in a section that wasn't split (like a table or image caption)
3. The threshold is too strict

**Solutions:**
- Review unmatched comments in comment_matches.md
- Lower the threshold: `--threshold 0.4`
- Manually search for the quoted text in the original DOCX

### Authentication errors

**Cause:** Invalid or expired credentials

**Solution:**
- Delete `token.pickle`
- Run extract_comments.py again
- Re-authenticate in the browser

### Permission denied

**Cause:** The Google account doesn't have access to the document

**Solution:**
- Make sure you're authenticating with the account that owns/can access the doc
- Add your email as a test user in Google Cloud Console OAuth consent screen

## Advanced Usage

### Programmatic Access

You can use the extracted data in your own scripts:

```python
import json

# Load comment matches
with open('comment_matches.json', 'r') as f:
    data = json.load(f)

# Find all open comments in a specific chapter
chapter_name = 'chapter_05_Developing_the_Picture.docx'

for comment in data['comment_matches']:
    if not comment['resolved'] and comment['matches']:
        for match in comment['matches']:
            if match['chapter'] == chapter_name:
                print(f"{comment['author']}: {comment['content']}")
```

### Filtering Comments

You can modify extract_comments.py to filter:
- Only unresolved comments
- Comments by specific authors
- Comments after a certain date

Edit the `fetch_comments()` method in extract_comments.py.

### Embedding Comments in Chapter Files

Future enhancement: Create a script to embed comments directly in the DOCX files as Word comments. This would allow:
- Viewing comments in Microsoft Word
- Preserving comment threads
- Maintaining comment-to-text anchors

## Files Created

The comment extraction process creates:

```
memoir-split/
├── credentials.json        # OAuth credentials (keep private!)
├── token.pickle           # Auth token (keep private!)
├── comments.json          # Extracted comments (can share)
├── comments.md            # Readable comments (can share)
├── comment_matches.json   # Matched comments (can share)
└── comment_matches.md     # Readable matches (can share)
```

**Important:** Add to .gitignore:
```
credentials.json
token.pickle
```

## Integration with Book Structure

Comments are now separate from your book structure manifest. This allows:

1. **Work with comments independently** - Review and address comments without modifying chapters
2. **Track progress** - Mark comments as resolved in Google Doc
3. **Preserve context** - Comments remain linked to original text via quoted_text

### Workflow Recommendation

1. Extract comments from Google Doc
2. Review comment_matches.md to see which chapters have comments
3. Edit those chapters in the split files
4. Rebuild the book with manifest system
5. Re-extract comments to see updated resolved status

## Next Steps

After extracting and matching comments, you might want to:

1. **Create a TODO list** from unresolved comments
2. **Prioritize chapters** with the most comments for revision
3. **Track progress** by re-extracting periodically
4. **Export specific comments** for sharing with editors/reviewers

See [MANIFEST_GUIDE.md](MANIFEST_GUIDE.md) for editing and rebuilding your book after addressing comments.
