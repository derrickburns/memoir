#!/usr/bin/env python3
"""
Refresh memoir chapters from Google Drive.

This script:
1. Copies the latest DOCX file from Downloads (where Google Drive saves it)
2. Splits it into chapters
3. Renumbers chapters sequentially
4. Updates the manifest

Usage:
    python3 scripts/refresh_from_google_drive.py
    python3 scripts/refresh_from_google_drive.py --source ~/Downloads/memoir.docx
    python3 scripts/refresh_from_google_drive.py --dry-run
"""

import os
import sys
import shutil
import argparse
import subprocess
from pathlib import Path
from datetime import datetime


def find_latest_memoir_file(search_paths):
    """Find the most recently downloaded memoir DOCX file."""
    candidates = []

    for search_path in search_paths:
        path = Path(search_path).expanduser()
        if not path.exists():
            continue

        # Look for files matching memoir patterns
        patterns = [
            "From Walls to Bridges*.docx",
            "memoir*.docx",
            "*memoir*.docx"
        ]

        for pattern in patterns:
            for file in path.glob(pattern):
                if file.is_file():
                    candidates.append(file)

    if not candidates:
        return None

    # Return the most recently modified file
    return max(candidates, key=lambda f: f.stat().st_mtime)


def main():
    parser = argparse.ArgumentParser(
        description='Refresh memoir chapters from Google Drive',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Auto-find latest download and process
    %(prog)s

    # Specify source file
    %(prog)s --source ~/Downloads/memoir.docx

    # Dry run (show what would be done)
    %(prog)s --dry-run

    # Keep old chapters in archive
    %(prog)s --archive

Workflow:
    1. Download from Google Drive: File > Download > Microsoft Word (.docx)
    2. Run this script to automatically process the download
    3. Chapters will be split and renumbered
    4. Manifest will be updated
        """
    )

    parser.add_argument('--source',
                        help='Source DOCX file (auto-detected from Downloads if not specified)')
    parser.add_argument('--output', default='output',
                        help='Output directory (default: output)')
    parser.add_argument('--heading-level', type=int, default=2,
                        help='Heading level for splitting (default: 2)')
    parser.add_argument('--archive', action='store_true',
                        help='Archive old chapters before replacing')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be done without doing it')

    args = parser.parse_args()

    # Get project root (parent of scripts/)
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    print("=" * 80)
    print("MEMOIR REFRESH FROM GOOGLE DRIVE")
    print("=" * 80)
    print()

    # Step 1: Find or verify source file
    if args.source:
        source_file = Path(args.source).expanduser()
        if not source_file.exists():
            print(f"ERROR: Source file not found: {source_file}")
            sys.exit(1)
        print(f"✓ Using specified source: {source_file}")
    else:
        print("Searching for latest memoir download...")
        search_paths = [
            "~/Downloads",
            "~/Desktop",
            "."  # Current directory
        ]
        source_file = find_latest_memoir_file(search_paths)

        if not source_file:
            print("\nERROR: Could not find memoir DOCX file in:")
            for path in search_paths:
                print(f"  - {path}")
            print("\nPlease either:")
            print("  1. Download from Google Drive: File > Download > Microsoft Word (.docx)")
            print("  2. Specify source with --source <file>")
            sys.exit(1)

        print(f"✓ Found latest download: {source_file}")
        mod_time = datetime.fromtimestamp(source_file.stat().st_mtime)
        print(f"  Last modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Step 2: Copy to project root
    dest_file = project_root / source_file.name

    if args.dry_run:
        print(f"\n[DRY RUN] Would copy:")
        print(f"  From: {source_file}")
        print(f"  To:   {dest_file}")
    else:
        print(f"\nCopying to project directory...")
        shutil.copy2(source_file, dest_file)
        print(f"✓ Copied to: {dest_file.name}")

    # Step 3: Archive old chapters if requested
    if args.archive and not args.dry_run:
        output_dir = Path(args.output)
        if output_dir.exists():
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            archive_dir = project_root / 'archive' / f'chapters_{timestamp}'

            print(f"\nArchiving old chapters...")
            archive_dir.mkdir(parents=True, exist_ok=True)

            # Move chapter files to archive
            for chapter_file in output_dir.glob('chapter_*.docx'):
                shutil.move(str(chapter_file), str(archive_dir / chapter_file.name))

            # Move image directories
            for img_dir in output_dir.glob('chapter_*_images'):
                shutil.move(str(img_dir), str(archive_dir / img_dir.name))

            print(f"✓ Archived to: {archive_dir}")

    # Step 4: Split the book
    print(f"\n{'=' * 80}")
    print("SPLITTING BOOK INTO CHAPTERS")
    print('=' * 80)
    print()

    split_cmd = [
        'python3', 'scripts/split_book.py',
        str(dest_file),
        '--output', args.output,
        '--heading-level', str(args.heading_level)
    ]

    if args.dry_run:
        print(f"[DRY RUN] Would run: {' '.join(split_cmd)}")
    else:
        result = subprocess.run(split_cmd)
        if result.returncode != 0:
            print("\nERROR: Split failed")
            sys.exit(1)

    # Step 5: Renumber chapters
    print(f"\n{'=' * 80}")
    print("RENUMBERING CHAPTERS SEQUENTIALLY")
    print('=' * 80)
    print()

    renumber_cmd = [
        'python3', 'scripts/renumber_chapters.py',
        args.output
    ]

    if args.dry_run:
        print(f"[DRY RUN] Would run: {' '.join(renumber_cmd)}")
    else:
        result = subprocess.run(renumber_cmd)
        if result.returncode != 0:
            print("\nERROR: Renumbering failed")
            sys.exit(1)

    # Step 6: Show summary
    print(f"\n{'=' * 80}")
    print("REFRESH COMPLETE")
    print('=' * 80)
    print()

    if not args.dry_run:
        # Count chapters
        output_dir = Path(args.output)
        chapter_files = list(output_dir.glob('chapter_*.docx'))
        timeline_files = list(output_dir.glob('*Timeline*.docx')) + \
                        list(output_dir.glob('Early_Life*.docx')) + \
                        list(output_dir.glob('*Years*.docx')) + \
                        list(output_dir.glob('*Career*.docx')) + \
                        list(output_dir.glob('*Valley*.docx')) + \
                        list(output_dir.glob('*Peaks*.docx')) + \
                        list(output_dir.glob('*Transitions*.docx')) + \
                        list(output_dir.glob('*Growth*.docx')) + \
                        list(output_dir.glob('*Crisis*.docx'))

        print(f"✓ Chapters: {len(chapter_files)}")
        print(f"✓ Timelines: {len(timeline_files)}")
        print(f"✓ Output directory: {output_dir}")

        print("\nNext steps:")
        print("  1. Review chapters: ls output/chapter_*.docx")
        print("  2. Check structure: python3 scripts/build_book.py --show-structure")
        print("  3. Update manifest: edit book_structure.yaml (if needed)")
    else:
        print("[DRY RUN] No changes made")
        print("\nRun without --dry-run to execute")


if __name__ == '__main__':
    main()
