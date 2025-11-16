# Publishing Guide: From DOCX to Ebook and Print

Complete guide for self-publishing your memoir in both ebook (EPUB) and print (PDF) formats.

## Overview

The publishing workflow converts your edited manuscript into professional formats suitable for distribution:

```
DOCX chapters → Markdown → { EPUB (ebook), PDF (print) }
```

**Key advantages:**
- Single source (Markdown) for both formats
- Pandoc handles professional formatting
- Maintain version control
- Easy to update and republish

## Prerequisites

### Required Software

**Already installed:**
- ✓ Python 3.7+
- ✓ Pandoc 3.7+

**Need to install:**

```bash
# LaTeX for PDF generation (large download ~4GB)
brew install --cask mactex

# Or install BasicTeX (smaller, ~100MB)
brew install --cask basictex
sudo tlmgr update --self
sudo tlmgr install collection-fontsrecommended
```

**Optional:**

```bash
# EPUB validator (recommended)
brew install epubcheck

# Ebook reader for testing
brew install --cask calibre
```

### Book Metadata

Edit `metadata.yaml` to include your book information:

```yaml
title: "From Walls to Bridges"
subtitle: "A Journey of Resilience and Connection"
author: "Derrick R. Burns"
date: "2025"
rights: "© 2025 Derrick R. Burns. All rights reserved."

# Add when you have them
isbn-13: "978-1234567890"
```

### Cover Image (Optional)

For EPUB, create a cover image:
- **Format:** JPG or PNG
- **Dimensions:** 1600 x 2560 pixels (recommended)
- **Aspect ratio:** 1:1.6 (standard book cover)
- **File size:** < 2MB
- **Name:** `cover.jpg` or `cover.png`

Place in project root directory.

## Publishing Workflow

### Option 1: Build Everything at Once

```bash
# Build both EPUB and PDF
python3 scripts/build_all.py

# With cover image
python3 scripts/build_all.py --cover cover.jpg
```

**Output:**
- `manuscript.md` - Markdown source
- `book.epub` - Ebook for Kindle, Apple Books, etc.
- `book.pdf` - Print-ready PDF

### Option 2: Step-by-Step

#### Step 1: Export to Markdown

```bash
# Convert DOCX chapters to single Markdown file
python3 scripts/export_markdown.py

# Custom output name
python3 scripts/export_markdown.py --output my_book.md
```

**What this does:**
1. Builds complete book from `book_structure.yaml`
2. Converts to Markdown using Pandoc
3. Extracts images to `media/` directory
4. Creates `manuscript.md`

#### Step 2: Build EPUB

```bash
# Build ebook
python3 scripts/build_epub.py

# With cover image
python3 scripts/build_epub.py --cover cover.jpg

# Custom output
python3 scripts/build_epub.py --output final_ebook.epub
```

**What this does:**
1. Reads `manuscript.md`
2. Applies metadata from `metadata.yaml`
3. Generates professional EPUB
4. Includes table of contents

#### Step 3: Build PDF

```bash
# Build print book
python3 scripts/build_pdf.py

# Custom output
python3 scripts/build_pdf.py --output print_book.pdf
```

**What this does:**
1. Reads `manuscript.md`
2. Applies metadata and PDF settings
3. Generates PDF via LaTeX
4. Formats for 6" x 9" print size

## Testing and Validation

### Test EPUB

```bash
# Open in Apple Books (Mac)
open book.epub

# Or use Calibre
open -a calibre book.epub

# Validate EPUB format
epubcheck book.epub
```

**Check for:**
- Proper chapter navigation
- Images display correctly
- Table of contents works
- Formatting looks good
- No broken links

### Test PDF

```bash
# Open in Preview
open book.pdf
```

**Check for:**
- Page breaks at chapter boundaries
- Images properly positioned
- Margins look correct
- Font size readable (11pt)
- Page numbers (if enabled)

## Customization

### Adjusting PDF Page Size

Edit `metadata.yaml`:

```yaml
# For 5" x 8" (smaller)
geometry:
  - paperwidth=5in
  - paperheight=8in
  - margin=0.5in

# For 8.5" x 11" (letter size)
geometry:
  - paperwidth=8.5in
  - paperheight=11in
  - margin=1in
```

### Changing Fonts (PDF)

Requires XeLaTeX. Edit `metadata.yaml`:

```yaml
mainfont: "Georgia"
sansfont: "Helvetica"
monofont: "Courier New"
```

### Adjusting EPUB Settings

Modify `scripts/build_epub.py`:

```python
cmd = [
    'pandoc',
    md_file,
    '-o', output_file,
    '--toc-depth=3',  # Deeper TOC
    '--epub-chapter-level=1',  # Different chapter breaks
]
```

## Distribution Platforms

### Ebook (EPUB)

**Amazon Kindle (KDP):**
- Upload `book.epub`
- KDP converts to MOBI automatically
- Set pricing and territories
- Publish

**Apple Books:**
- Upload `book.epub` via Books Partner
- Or use Transloadit service
- Set pricing
- Publish

**Google Play Books:**
- Upload `book.epub` to Google Play Books Partner Center
- Set pricing
- Publish

**Other platforms:**
- Kobo Writing Life
- Barnes & Noble Press
- Smashwords (distributes to many platforms)

### Print Book (PDF)

**Amazon KDP Print:**
- Upload `book.pdf` as interior file
- Upload cover (create separately)
- Select trim size (6" x 9")
- Set pricing based on page count
- Publish

**IngramSpark:**
- More professional distribution
- Better quality printing
- Wider distribution (bookstores)
- Upload `book.pdf`
- Requires separate cover file

**Other platforms:**
- Lulu
- BookBaby
- Draft2Digital (also does ebook)

## ISBNs

You need separate ISBNs for:
- Ebook version
- Print version

**Get ISBNs:**
- **US:** Buy from Bowker ($125 for one, $295 for 10)
- **Other countries:** Check your national ISBN agency
- **Free option:** KDP provides free ISBNs (but you don't own them)

Add ISBNs to `metadata.yaml`:

```yaml
isbn-13: "978-1234567890"  # For ebook
# Note: Print ISBN goes on cover, not in interior
```

## Updating Your Book

When you need to republish with changes:

```bash
# 1. Make edits to chapters in output/
# 2. Update book_structure.yaml if needed
# 3. Rebuild both formats
python3 scripts/build_all.py

# 4. Upload new versions to platforms
```

Platforms allow updating published books. Readers who already purchased will get the update (depending on platform).

## Troubleshooting

### "xelatex not found"

Install LaTeX:
```bash
brew install --cask mactex
```

### "pandoc not found"

Already installed, but if needed:
```bash
brew install pandoc
```

### PDF generation fails

Common issues:
- Check for special characters in text
- Verify images are in `media/` directory
- Try different PDF engine:
  ```bash
  python3 scripts/build_pdf.py --engine pdflatex
  ```

### EPUB images not showing

- Ensure `export_markdown.py` extracted media
- Check `media/` directory exists
- Verify image paths in `manuscript.md`

### Cover image not appearing

- Check file exists: `cover.jpg`
- Verify format (JPG or PNG)
- Check file size (< 2MB recommended)
- Use correct flag:
  ```bash
  python3 scripts/build_epub.py --cover cover.jpg
  ```

## Best Practices

1. **Always test before publishing**
   - Read through EPUB in ebook reader
   - Review PDF page by page
   - Have someone else proofread

2. **Keep source files**
   - Maintain your DOCX chapters
   - Keep `manuscript.md`
   - Version control everything

3. **Backup regularly**
   - Git commit after major changes
   - Keep final published versions
   - Save ISBNs and metadata

4. **Professional editing**
   - Hire professional editor before publishing
   - Use your comment extraction system for feedback
   - Address all editorial comments

5. **Cover design**
   - Consider hiring professional cover designer
   - Ebook covers should look good at thumbnail size
   - Print covers need spine width calculation

## Quick Reference

**Full publishing workflow:**
```bash
# 1. Finalize edits in Google Docs
# 2. Extract and address comments
python3 scripts/extract_comments.py --doc-id YOUR_DOC_ID
python3 scripts/match_comments_improved.py

# 3. Update chapters in output/
# 4. Build publication formats
python3 scripts/build_all.py --cover cover.jpg

# 5. Test outputs
open book.epub
open book.pdf

# 6. Upload to platforms
# 7. Publish!
```

## Resources

**Publishing platforms:**
- [Amazon KDP](https://kdp.amazon.com/)
- [IngramSpark](https://www.ingramspark.com/)
- [Draft2Digital](https://www.draft2digital.com/)

**Tools:**
- [Pandoc documentation](https://pandoc.org/MANUAL.html)
- [EPUB validator](https://www.epubcheck.org/)
- [Calibre](https://calibre-ebook.com/) (ebook management)

**ISBN info:**
- [Bowker (US)](https://www.myidentifiers.com/)
- [ISBN.org](https://www.isbn.org/)

**Self-publishing guides:**
- The Creative Penn (Joanna Penn)
- Alliance of Independent Authors
- Reedsy blog
