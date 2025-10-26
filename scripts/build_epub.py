#!/usr/bin/env python3
"""
Build EPUB ebook from Markdown source.

Uses Pandoc to generate a professional EPUB file suitable for
distribution on Amazon Kindle, Apple Books, etc.
"""

import sys
import subprocess
import argparse
from pathlib import Path


def build_epub(md_file, output_file, metadata_file='metadata.yaml', cover_image=None):
    """Build EPUB from Markdown using Pandoc."""
    print(f"Building EPUB from: {md_file}")

    # Check if pandoc is available
    result = subprocess.run(['which', 'pandoc'], capture_output=True)
    if result.returncode != 0:
        print("ERROR: pandoc not found!")
        print("\nInstall with: brew install pandoc")
        sys.exit(1)

    # Check if source file exists
    if not Path(md_file).exists():
        print(f"ERROR: Source file not found: {md_file}")
        print("\nRun: python3 scripts/export_markdown.py")
        sys.exit(1)

    # Build pandoc command
    cmd = [
        'pandoc',
        md_file,
        '-o', output_file,
        '--metadata-file', metadata_file if Path(metadata_file).exists() else None,
        '--toc',
        '--toc-depth=2',
        '--epub-chapter-level=2',
    ]

    # Add cover image if provided
    if cover_image and Path(cover_image).exists():
        cmd.extend(['--epub-cover-image', cover_image])
        print(f"Using cover image: {cover_image}")

    # Remove None values
    cmd = [c for c in cmd if c is not None]

    print(f"Running: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"ERROR building EPUB: {result.stderr}")
        sys.exit(1)

    # Get file size
    size_mb = Path(output_file).stat().st_size / (1024 * 1024)

    print(f"✓ Built EPUB: {output_file} ({size_mb:.2f} MB)")
    return output_file


def validate_epub(epub_file):
    """Validate EPUB file (requires epubcheck if installed)."""
    result = subprocess.run(['which', 'epubcheck'], capture_output=True)

    if result.returncode == 0:
        print(f"\nValidating EPUB...")
        result = subprocess.run(['epubcheck', epub_file], capture_output=True, text=True)

        if result.returncode == 0:
            print("✓ EPUB validation passed")
        else:
            print("⚠ EPUB validation warnings:")
            print(result.stdout)
    else:
        print("\nNote: Install epubcheck for EPUB validation")
        print("  brew install epubcheck")


def main():
    parser = argparse.ArgumentParser(
        description='Build EPUB ebook from Markdown',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Build EPUB with default settings
  %(prog)s

  # Build with custom files
  %(prog)s --input my_book.md --output my_book.epub

  # Add cover image
  %(prog)s --cover cover.jpg

  # Use custom metadata
  %(prog)s --metadata custom_metadata.yaml

This script uses Pandoc to generate a professional EPUB file.
The EPUB can be distributed on:
  - Amazon Kindle (KDP)
  - Apple Books
  - Google Play Books
  - Barnes & Noble Nook
  - Kobo
  - And other ebook platforms

Prerequisites:
  - Pandoc installed (brew install pandoc)
  - Markdown source file (run export_markdown.py first)
  - metadata.yaml file with book information
        """
    )

    parser.add_argument('-i', '--input', default='manuscript.md',
                        help='Input Markdown file (default: manuscript.md)')
    parser.add_argument('-o', '--output', default='book.epub',
                        help='Output EPUB file (default: book.epub)')
    parser.add_argument('-m', '--metadata', default='metadata.yaml',
                        help='Metadata YAML file (default: metadata.yaml)')
    parser.add_argument('-c', '--cover', default=None,
                        help='Cover image file (JPG or PNG)')
    parser.add_argument('--validate', action='store_true',
                        help='Validate EPUB after building (requires epubcheck)')

    args = parser.parse_args()

    print("=" * 80)
    print("BUILDING EPUB")
    print("=" * 80)

    # Build EPUB
    epub_file = build_epub(
        args.input,
        args.output,
        args.metadata,
        args.cover
    )

    # Validate if requested
    if args.validate:
        validate_epub(epub_file)

    print("\n" + "=" * 80)
    print("✓ EPUB BUILD COMPLETE")
    print("=" * 80)
    print(f"\nEbook file: {epub_file}")
    print("\nNext steps:")
    print("  1. Test in ebook reader (Apple Books, Calibre, etc.)")
    print("  2. Upload to KDP for Kindle")
    print("  3. Distribute on other platforms")


if __name__ == '__main__':
    main()
