# Publishing System Setup Summary

Complete Pandoc-based publishing system installed and configured.

## What's Been Created

### Publishing Scripts (in scripts/)

1. **export_markdown.py** - Convert DOCX → Markdown
   - Builds book from manifest
   - Exports to clean Markdown
   - Extracts images to `media/`

2. **build_epub.py** - Generate EPUB ebook
   - Professional EPUB output
   - Includes metadata and TOC
   - Supports cover images
   - Compatible with Kindle, Apple Books, etc.

3. **build_pdf.py** - Generate PDF print book
   - Print-ready PDF via LaTeX
   - 6" x 9" format (customizable)
   - Professional typography
   - Suitable for KDP Print, IngramSpark

4. **build_all.py** - Build both formats at once
   - Complete publishing workflow
   - One command to publish

### Configuration Files

**metadata.yaml** - Book metadata
- Title, author, copyright
- ISBN placeholders
- PDF page size and formatting
- EPUB settings

### Documentation

**docs/PUBLISHING_GUIDE.md** - Complete publishing guide
- Setup instructions
- Publishing workflow
- Platform-specific guidance
- Troubleshooting
- Distribution options

## Quick Start

### 1. Install LaTeX (Required for PDF)

```bash
# Full LaTeX distribution (recommended)
brew install --cask mactex

# Or smaller BasicTeX
brew install --cask basictex
sudo tlmgr update --self
sudo tlmgr install collection-fontsrecommended
```

### 2. Edit Metadata

```bash
# Edit book information
open metadata.yaml

# Add:
# - Your title/subtitle
# - Author name
# - Copyright info
# - ISBN (when you have it)
```

### 3. Create Cover (Optional)

```bash
# Create cover image
# - Format: JPG or PNG
# - Size: 1600 x 2560 pixels
# - Save as: cover.jpg

# Or hire a designer:
# - Fiverr, 99designs, Reedsy
```

### 4. Build Everything

```bash
# Single command to publish
python3 scripts/build_all.py --cover cover.jpg

# Output:
# - manuscript.md (Markdown source)
# - book.epub (ebook)
# - book.pdf (print book)
```

## Publishing Workflow

```
┌─────────────────────────────────────┐
│ 1. Edit in Google Docs              │
│    Extract & address comments       │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ 2. Update DOCX chapters in output/  │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ 3. Build final manuscript           │
│    python3 scripts/build_all.py     │
└──────────────┬──────────────────────┘
               ↓
       ┌───────┴────────┐
       ↓                ↓
┌────────────┐   ┌─────────────┐
│ book.epub  │   │  book.pdf   │
│ (ebook)    │   │  (print)    │
└──────┬─────┘   └──────┬──────┘
       ↓                ↓
┌────────────┐   ┌─────────────┐
│ Amazon KDP │   │  KDP Print  │
│ Apple Books│   │ IngramSpark │
│ Others     │   │ Others      │
└────────────┘   └─────────────┘
```

## What You Need Before Publishing

### For Ebook (EPUB)

✓ Final edited manuscript
✓ Book metadata (in metadata.yaml)
✓ Cover image (1600 x 2560 px)
✓ ISBN-13 (optional, KDP provides free)

### For Print (PDF)

✓ Final edited manuscript
✓ Book metadata (in metadata.yaml)
✓ Print cover design (separate from ebook)
✓ ISBN-13 (optional, KDP provides free)

### Publishing Accounts

Create accounts on:
- **Amazon KDP** (Kindle ebook + print)
- **IngramSpark** (wider print distribution)
- **Apple Books** (optional, for ebook)
- **Google Play Books** (optional, for ebook)

## Distribution Options

### Ebook Distribution

**Primary:**
- Amazon KDP (Kindle) - Largest market
- Apple Books - iOS users
- Google Play Books

**Aggregators** (distribute to multiple platforms):
- Draft2Digital - Easy, 10% commission
- Smashwords - Wide distribution
- PublishDrive

### Print Distribution

**Print-on-Demand:**
- Amazon KDP Print - Easy, integrated with ebook
- IngramSpark - Professional, wide distribution
- Lulu - Good for special editions

### Pricing Guidance

**Ebook:**
- Self-published memoirs: $2.99 - $9.99
- Sweet spot: $4.99 - $6.99
- KDP Select: 70% royalty at $2.99+

**Print:**
- Cost = printing + distribution fee
- Typical: $12.99 - $19.99
- Check KDP calculator for your page count

## Next Steps After Setup

1. **Finish editing**
   - Address all comments
   - Professional editing recommended
   - Multiple proofreading passes

2. **Get ISBN** (optional)
   - Buy from Bowker (US): $125 for one, $295 for 10
   - Or use free KDP ISBN

3. **Design cover**
   - Hire professional designer ($100-500)
   - Or use Canva, BookBrush
   - Different cover for ebook vs print

4. **Test build**
   ```bash
   python3 scripts/build_all.py --cover cover.jpg
   ```

5. **Review output**
   - Read EPUB in ebook reader
   - Check PDF page by page
   - Get beta readers' feedback

6. **Publish**
   - Upload to KDP
   - Set pricing
   - Launch!

## Updating After Publication

If you need to fix errors or update content:

```bash
# 1. Make edits to chapters
# 2. Rebuild
python3 scripts/build_all.py

# 3. Upload new files to platforms
# Readers get automatic updates
```

## Tools Summary

**Built and ready to use:**
- ✓ Markdown export
- ✓ EPUB generation
- ✓ PDF generation
- ✓ Batch builder
- ✓ Metadata system
- ✓ Complete documentation

**Need to install:**
- LaTeX (for PDF generation)
- Optional: epubcheck, calibre

**Ready for:**
- Amazon Kindle (KDP)
- Apple Books
- Google Play Books
- KDP Print
- IngramSpark
- All major platforms

## Resources

**Publishing platforms:**
- [Amazon KDP](https://kdp.amazon.com/)
- [IngramSpark](https://www.ingramspark.com/)
- [Draft2Digital](https://www.draft2digital.com/)

**Tools:**
- [Pandoc docs](https://pandoc.org/MANUAL.html)
- [EPUB validator](https://www.epubcheck.org/)
- [ISBN agency (US)](https://www.myidentifiers.com/)

**Learning:**
- The Creative Penn podcast
- Alliance of Independent Authors
- Reedsy blog
- /r/selfpublish subreddit

## Support

**For issues:**
1. Check docs/PUBLISHING_GUIDE.md
2. Run scripts with --help flag
3. Review error messages carefully
4. Check Pandoc documentation

**Common commands:**
```bash
# Get help on any script
python3 scripts/build_epub.py --help
python3 scripts/build_pdf.py --help

# View book structure
python3 scripts/build_book.py --show-structure

# Test without building
python3 scripts/export_markdown.py --keep-docx
```

## You're Ready!

Your publishing system is complete and ready to convert your memoir into professional ebook and print formats. When you're ready to publish, just run the build scripts and upload to your chosen platforms.

Good luck with your memoir! 📚
