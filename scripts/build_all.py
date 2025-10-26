#!/usr/bin/env python3
"""
Build all publication formats (EPUB and PDF) from Markdown.

This convenience script runs the full publishing workflow:
1. Exports to Markdown (if needed)
2. Builds EPUB
3. Builds PDF
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_script(script_name, args=[]):
    """Run a Python script and check for errors."""
    cmd = ['python3', f'scripts/{script_name}'] + args

    print(f"\n{'=' * 80}")
    print(f"Running: {' '.join(cmd)}")
    print('=' * 80)

    result = subprocess.run(cmd)

    if result.returncode != 0:
        print(f"\nERROR: {script_name} failed")
        sys.exit(1)

    return result


def main():
    parser = argparse.ArgumentParser(
        description='Build all publication formats',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Build everything with defaults
  %(prog)s

  # Skip Markdown export (use existing manuscript.md)
  %(prog)s --skip-export

  # Add cover image to EPUB
  %(prog)s --cover cover.jpg

  # Use custom source Markdown
  %(prog)s --markdown my_book.md

This script orchestrates the complete publishing workflow:
  1. Export DOCX → Markdown (optional)
  2. Build EPUB from Markdown
  3. Build PDF from Markdown

Output files:
  - manuscript.md (Markdown source)
  - book.epub (ebook)
  - book.pdf (print book)
        """
    )

    parser.add_argument('--skip-export', action='store_true',
                        help='Skip Markdown export, use existing file')
    parser.add_argument('--markdown', default='manuscript.md',
                        help='Markdown source file (default: manuscript.md)')
    parser.add_argument('--epub', default='book.epub',
                        help='EPUB output file (default: book.epub)')
    parser.add_argument('--pdf', default='book.pdf',
                        help='PDF output file (default: book.pdf)')
    parser.add_argument('--cover', default=None,
                        help='Cover image for EPUB')
    parser.add_argument('--metadata', default='metadata.yaml',
                        help='Metadata file (default: metadata.yaml)')

    args = parser.parse_args()

    print("=" * 80)
    print("BUILDING ALL PUBLICATION FORMATS")
    print("=" * 80)

    # Step 1: Export to Markdown
    if not args.skip_export:
        print("\nStep 1: Exporting to Markdown...")
        run_script('export_markdown.py', [
            '--output', args.markdown
        ])
    else:
        print(f"\nStep 1: Skipping export, using existing: {args.markdown}")
        if not Path(args.markdown).exists():
            print(f"ERROR: File not found: {args.markdown}")
            sys.exit(1)

    # Step 2: Build EPUB
    print("\nStep 2: Building EPUB...")
    epub_args = [
        '--input', args.markdown,
        '--output', args.epub,
        '--metadata', args.metadata
    ]
    if args.cover:
        epub_args.extend(['--cover', args.cover])

    run_script('build_epub.py', epub_args)

    # Step 3: Build PDF
    print("\nStep 3: Building PDF...")
    run_script('build_pdf.py', [
        '--input', args.markdown,
        '--output', args.epub,
        '--metadata', args.metadata
    ])

    # Summary
    print("\n" + "=" * 80)
    print("✓ ALL FORMATS BUILT SUCCESSFULLY")
    print("=" * 80)

    print("\nOutput files:")
    if not args.skip_export:
        print(f"  - {args.markdown} (Markdown source)")
    print(f"  - {args.epub} (EPUB ebook)")
    print(f"  - {args.pdf} (PDF print book)")

    print("\nNext steps:")
    print("  1. Test EPUB in ebook reader")
    print("  2. Review PDF for print quality")
    print("  3. Upload to publishing platforms")


if __name__ == '__main__':
    main()
