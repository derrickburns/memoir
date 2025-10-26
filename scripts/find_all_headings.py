#!/usr/bin/env python3
"""
Find all headings at all levels.
"""

import sys
import re
from docx import Document


def extract_chapter_number(text):
    """Extract chapter number from text."""
    patterns = [
        r'[Cc]hapter\s+(\d+)',
        r'[Cc]h\.\s*(\d+)',
        r'^(\d+)\.',
        r'^(\d+)\s+[A-Z]',
        r'^(\d+)$',
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return int(match.group(1))

    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python find_all_headings.py <file.docx>")
        sys.exit(1)

    filename = sys.argv[1]
    doc = Document(filename)

    print(f"Analyzing: {filename}\n")

    # Check all heading levels
    for level in range(1, 7):
        print(f"\n{'=' * 80}")
        print(f"HEADING {level} SECTIONS:")
        print(f"{'=' * 80}")

        count = 0
        chapter_numbers = []

        for i, para in enumerate(doc.paragraphs):
            if para.style and para.style.name == f"Heading {level}":
                count += 1
                text = para.text.strip()
                chapter_num = extract_chapter_number(text)

                if chapter_num:
                    chapter_numbers.append(chapter_num)
                    display_text = text[:60] if len(text) <= 60 else text[:57] + "..."
                    print(f"{count:3d}. Para {i:4d}: Chapter {chapter_num:2d} - {display_text}")
                elif count <= 20:  # Show first 20
                    display_text = text[:60] if len(text) <= 60 else text[:57] + "..."
                    print(f"{count:3d}. Para {i:4d}: (no number) - {display_text}")

        if count > 20:
            print(f"... ({count - 20} more)")

        print(f"\nTotal: {count} headings at level {level}")

        if chapter_numbers:
            print(f"Numbered chapters: {sorted(chapter_numbers)}")
            print(f"Range: {min(chapter_numbers)} to {max(chapter_numbers)}")

            if level == 2:  # Check for 1-37 at level 2
                expected = set(range(1, 38))
                actual = set(chapter_numbers)
                missing = sorted(expected - actual)

                if missing:
                    print(f"\n⚠️  Missing chapter numbers (expected 1-37): {missing}")
                else:
                    print(f"\n✓ All chapters 1-37 present!")


if __name__ == '__main__':
    main()
