#!/usr/bin/env python3
"""
Export book to Markdown format for publishing.

This script builds the book from the manifest and exports to Markdown,
which serves as the source for both EPUB and PDF generation.
"""

import sys
import subprocess
import argparse
from pathlib import Path


def build_docx(manifest='book_structure.yaml', output='manuscript.docx'):
    """Build the complete book DOCX from manifest."""
    print(f"Building book from manifest: {manifest}")

    result = subprocess.run([
        'python3', 'scripts/build_book.py',
        '--manifest', manifest,
        '--output', output,
        '--quiet'
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"ERROR building book: {result.stderr}")
        sys.exit(1)

    print(f"✓ Built DOCX: {output}")
    return output


def export_to_markdown(docx_file, md_file, extract_media=True):
    """Convert DOCX to Markdown using Pandoc."""
    print(f"\nConverting to Markdown: {md_file}")

    # Check if pandoc is available
    result = subprocess.run(['which', 'pandoc'], capture_output=True)
    if result.returncode != 0:
        print("ERROR: pandoc not found!")
        print("\nInstall with: brew install pandoc")
        sys.exit(1)

    # Build pandoc command
    cmd = [
        'pandoc',
        docx_file,
        '-o', md_file,
        '--extract-media', 'media' if extract_media else None,
        '--wrap=none',  # Don't wrap lines
        '--markdown-headings=atx',  # Use # style headings
    ]

    # Remove None values
    cmd = [c for c in cmd if c is not None]

    print(f"Running: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"ERROR converting to Markdown: {result.stderr}")
        sys.exit(1)

    print(f"✓ Exported to Markdown: {md_file}")

    if extract_media:
        print(f"✓ Media files extracted to: media/")

    return md_file


def main():
    parser = argparse.ArgumentParser(
        description='Export book to Markdown for publishing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Export using default settings
  %(prog)s

  # Export with custom filenames
  %(prog)s --output my_book.md

  # Don't extract media files
  %(prog)s --no-extract-media

  # Use custom manifest
  %(prog)s --manifest book_structure_final.yaml

This script:
  1. Builds the complete book from book_structure.yaml
  2. Converts it to Markdown using Pandoc
  3. Extracts images to media/ directory (optional)

The resulting Markdown file can be used to generate:
  - EPUB (ebook) using build_epub.py
  - PDF (print) using build_pdf.py
        """
    )

    parser.add_argument('-m', '--manifest', default='book_structure.yaml',
                        help='Book manifest file (default: book_structure.yaml)')
    parser.add_argument('-o', '--output', default='manuscript.md',
                        help='Output Markdown file (default: manuscript.md)')
    parser.add_argument('--docx', default='manuscript.docx',
                        help='Intermediate DOCX file (default: manuscript.docx)')
    parser.add_argument('--no-extract-media', action='store_true',
                        help="Don't extract media files to separate directory")
    parser.add_argument('--keep-docx', action='store_true',
                        help='Keep intermediate DOCX file')

    args = parser.parse_args()

    print("=" * 80)
    print("EXPORTING BOOK TO MARKDOWN")
    print("=" * 80)

    # Build the DOCX
    docx_file = build_docx(args.manifest, args.docx)

    # Convert to Markdown
    md_file = export_to_markdown(
        docx_file,
        args.output,
        extract_media=not args.no_extract_media
    )

    # Clean up intermediate DOCX unless requested to keep
    if not args.keep_docx:
        Path(docx_file).unlink()
        print(f"✓ Removed intermediate file: {docx_file}")

    print("\n" + "=" * 80)
    print("✓ EXPORT COMPLETE")
    print("=" * 80)
    print(f"\nMarkdown source: {md_file}")

    if not args.no_extract_media:
        print(f"Media files: media/")

    print("\nNext steps:")
    print("  - Build EPUB: python3 scripts/build_epub.py")
    print("  - Build PDF: python3 scripts/build_pdf.py")
    print("  - Build both: python3 scripts/build_all.py")


if __name__ == '__main__':
    main()
