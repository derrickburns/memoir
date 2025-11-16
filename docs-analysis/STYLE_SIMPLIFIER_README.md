# Style Simplifier

A tool to consolidate DOCX document styles into a minimal canonical set.

## Purpose

Word documents often accumulate many similar styles (e.g., "Body Text", "Body Text 2", "Body Text 3", "First Paragraph") that serve the same purpose. This script consolidates them into a clean, minimal set of canonical styles.

## Canonical Style Set

The script maps all styles to these 8 canonical styles:

| Canonical Style | Purpose | Maps From |
|----------------|---------|-----------|
| **Title** | Document title | Title, Document Title |
| **Subtitle** | Document subtitle | Subtitle, Document Subtitle |
| **Heading 1** | Major sections (Acts, Parts) | Heading 1 |
| **Heading 2** | Chapters | Heading 2 |
| **Heading 3** | Subsections | Heading 3, 4, 5, 6, 7, 8, 9 |
| **Normal** | Body text | Normal, Body Text, Body Text 2, Body Text 3, First Paragraph, List Paragraph, etc. |
| **Quote** | Block quotes | Quote, Block Quote, Intense Quote |
| **Caption** | Captions/meta text | Caption, Header, Footer |

## Usage

### Analyze styles (no changes)
```bash
python simplify_styles.py mybook.docx --analyze
```

Shows:
- How many styles are in the document
- How they would be consolidated
- Number of paragraphs using each style

### Dry run (preview changes)
```bash
python simplify_styles.py mybook.docx --dry-run
```

Shows what would change without actually modifying the file.

### Simplify styles
```bash
# Creates mybook_simplified.docx
python simplify_styles.py mybook.docx

# Specify output filename
python simplify_styles.py mybook.docx --output clean.docx
```

## Example Output

```
Analyzing: mybook.docx
================================================================================

Total paragraphs: 3184
Unique styles: 15
Would consolidate to: 6 canonical styles

================================================================================
CANONICAL STYLE MAPPING:
================================================================================

Normal (2850 paragraphs):
  • normal: 2500 paragraphs → will map to Normal
  • Body Text: 200 paragraphs → will map to Normal
  • Body Text 2: 100 paragraphs → will map to Normal
  • First Paragraph: 50 paragraphs → will map to Normal

Heading 1 (20 paragraphs):
  • Heading 1: 20 paragraphs (canonical)

Heading 2 (48 paragraphs):
  • Heading 2: 45 paragraphs (canonical)
  • Chapter Heading: 3 paragraphs → will map to Heading 2

Heading 3 (193 paragraphs):
  • Heading 3: 150 paragraphs (canonical)
  • Heading 4: 30 paragraphs → will map to Heading 3
  • Heading 5: 13 paragraphs → will map to Heading 3
```

## Benefits

1. **Cleaner documents** - Easier to understand and maintain
2. **Better consistency** - All similar content uses the same style
3. **Simpler formatting** - Fewer styles to manage
4. **Easier splitting** - Chapter detection works better with consistent styles
5. **Better portability** - Simplified documents work better across platforms

## Your Document

Your memoir "From Walls to Bridges" is already very clean:
- Only 5 unique styles
- All already canonical except "normal" → "Normal"
- No consolidation needed!

This is excellent practice for document formatting.

## Advanced: Customizing Mappings

Edit the `STYLE_MAPPING` dictionary in `simplify_styles.py` to customize how styles are mapped:

```python
STYLE_MAPPING = {
    'Your Custom Style': 'Normal',
    'Another Style': 'Heading 2',
    # ...
}
```

## Integration with Split Script

After simplifying styles, the split script will work even more reliably:

```bash
# 1. Simplify styles (optional, your doc is already clean)
python simplify_styles.py mybook.docx -o mybook_clean.docx

# 2. Split into chapters
python split_book.py mybook_clean.docx --heading-level 2

# 3. Merge back
python merge_book.py
```

## Requirements

Same as the split script:
- Python 3.7+
- python-docx library
