#!/usr/bin/env python3
"""Map the actual chapter structure from the downloaded files."""

import glob
from pathlib import Path

def main():
    output_dir = Path('output')
    chapters = {}

    # Parse all chapter files
    for docx_path in sorted(glob.glob(str(output_dir / 'chapter_*.docx'))):
        filename = Path(docx_path).stem
        # Extract chapter number from filename like "chapter_12_Chapter_12_..."
        parts = filename.split('_')
        if len(parts) >= 2 and parts[1].isdigit():
            seq_num = int(parts[1])
            # Get the title (everything after the first two parts)
            title = '_'.join(parts[2:])

            if seq_num not in chapters:
                chapters[seq_num] = []
            chapters[seq_num].append(title)

    # Print unique chapters
    print("=" * 80)
    print("ACTUAL CHAPTER STRUCTURE")
    print("=" * 80)
    print()

    unique_chapters = {}
    for seq_num in sorted(chapters.keys()):
        titles = chapters[seq_num]
        # Use the first occurrence
        if len(titles) > 1:
            print(f"WARNING: Chapter {seq_num:02d} has {len(titles)} versions:")
            for title in titles:
                print(f"  - {title}")
            print(f"  Using: {titles[0]}")
            print()
        unique_chapters[seq_num] = titles[0]

    print()
    print("=" * 80)
    print("UNIQUE CHAPTERS (1-37)")
    print("=" * 80)
    print()

    for i in range(1, 38):
        if i in unique_chapters:
            title = unique_chapters[i].replace('_', ' ')
            print(f"Chapter {i:2d}: {title}")
        else:
            print(f"Chapter {i:2d}: [MISSING]")

    print()
    print(f"\nTotal unique chapters: {len(unique_chapters)}")

if __name__ == '__main__':
    main()
