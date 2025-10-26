#!/usr/bin/env python3
"""
Build PDF print book from Markdown source.

Uses Pandoc + LaTeX to generate a professional PDF suitable for
print-on-demand services like IngramSpark, KDP Print, etc.
"""

import sys
import subprocess
import argparse
from pathlib import Path


def check_latex():
    """Check if LaTeX is installed."""
    result = subprocess.run(['which', 'xelatex'], capture_output=True)

    if result.returncode != 0:
        print("ERROR: XeLaTeX not found!")
        print("\nLaTeX is required for PDF generation.")
        print("\nInstall MacTeX:")
        print("  brew install --cask mactex")
        print("\nOr install BasicTeX (smaller):")
        print("  brew install --cask basictex")
        print("  sudo tlmgr update --self")
        print("  sudo tlmgr install collection-fontsrecommended")
        sys.exit(1)


def build_pdf(md_file, output_file, metadata_file='metadata.yaml', pdf_engine='xelatex'):
    """Build PDF from Markdown using Pandoc + LaTeX."""
    print(f"Building PDF from: {md_file}")

    # Check if pandoc is available
    result = subprocess.run(['which', 'pandoc'], capture_output=True)
    if result.returncode != 0:
        print("ERROR: pandoc not found!")
        print("\nInstall with: brew install pandoc")
        sys.exit(1)

    # Check LaTeX
    check_latex()

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
        '--pdf-engine', pdf_engine,
        '--metadata-file', metadata_file if Path(metadata_file).exists() else None,
        '--toc',
        '--number-sections',
        # LaTeX settings for better typography
        '-V', 'geometry:paperwidth=6in',
        '-V', 'geometry:paperheight=9in',
        '-V', 'geometry:margin=0.75in',
        '-V', 'fontsize=11pt',
        '-V', 'linestretch=1.15',
    ]

    # Remove None values
    cmd = [c for c in cmd if c is not None]

    print(f"Running: {' '.join(cmd)}")
    print("\n(This may take a minute...)")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"ERROR building PDF: {result.stderr}")
        sys.exit(1)

    # Get file size
    size_mb = Path(output_file).stat().st_size / (1024 * 1024)
    pages_estimate = size_mb * 100  # Rough estimate

    print(f"✓ Built PDF: {output_file} ({size_mb:.2f} MB, ~{pages_estimate:.0f} pages)")
    return output_file


def main():
    parser = argparse.ArgumentParser(
        description='Build PDF print book from Markdown',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Build PDF with default settings
  %(prog)s

  # Build with custom files
  %(prog)s --input my_book.md --output my_book.pdf

  # Use custom metadata
  %(prog)s --metadata custom_metadata.yaml

  # Use pdflatex instead of xelatex
  %(prog)s --engine pdflatex

This script uses Pandoc + LaTeX to generate a print-ready PDF.
The PDF can be used for:
  - Print-on-demand (KDP Print, IngramSpark)
  - Professional printing
  - Preview before finalizing

Prerequisites:
  - Pandoc installed (brew install pandoc)
  - LaTeX installed (brew install --cask mactex)
  - Markdown source file (run export_markdown.py first)
  - metadata.yaml file with book information

PDF Settings:
  - Page size: 6" x 9" (standard memoir size)
  - Margins: 0.75" (adjust in metadata.yaml)
  - Font size: 11pt
  - Line spacing: 1.15

To customize, edit metadata.yaml:
  - Change page size with geometry settings
  - Change fonts (requires XeLaTeX)
  - Adjust margins, spacing, etc.
        """
    )

    parser.add_argument('-i', '--input', default='manuscript.md',
                        help='Input Markdown file (default: manuscript.md)')
    parser.add_argument('-o', '--output', default='book.pdf',
                        help='Output PDF file (default: book.pdf)')
    parser.add_argument('-m', '--metadata', default='metadata.yaml',
                        help='Metadata YAML file (default: metadata.yaml)')
    parser.add_argument('-e', '--engine', default='xelatex',
                        choices=['xelatex', 'pdflatex', 'lualatex'],
                        help='LaTeX engine (default: xelatex)')

    args = parser.parse_args()

    print("=" * 80)
    print("BUILDING PDF")
    print("=" * 80)

    # Build PDF
    pdf_file = build_pdf(
        args.input,
        args.output,
        args.metadata,
        args.engine
    )

    print("\n" + "=" * 80)
    print("✓ PDF BUILD COMPLETE")
    print("=" * 80)
    print(f"\nPrint book file: {pdf_file}")
    print("\nNext steps:")
    print("  1. Open and review the PDF")
    print("  2. Check for formatting issues")
    print("  3. Verify page breaks and images")
    print("  4. Upload to print-on-demand service")
    print("\nPrint-on-demand options:")
    print("  - Amazon KDP Print (easiest)")
    print("  - IngramSpark (wider distribution)")
    print("  - Lulu")
    print("  - BookBaby")


if __name__ == '__main__':
    main()
