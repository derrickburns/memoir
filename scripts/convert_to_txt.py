#!/usr/bin/env python3
"""Convert DOCX chapter files to TXT format."""

import os
import glob
import docx2txt
from pathlib import Path

def main():
    output_dir = Path('output')
    txt_dir = output_dir / 'txt'
    txt_dir.mkdir(exist_ok=True)

    # Get all chapter files
    chapter_files = sorted(glob.glob(str(output_dir / 'chapter_*.docx')))

    print(f"Converting {len(chapter_files)} chapters to text...")

    for docx_path in chapter_files:
        filename = Path(docx_path).stem
        # Extract chapter number from filename like "chapter_12_..."
        parts = filename.split('_')
        if len(parts) >= 2 and parts[1].isdigit():
            chapter_num = parts[1]
            txt_path = txt_dir / f'chapter_{chapter_num}.txt'

            try:
                text = docx2txt.process(docx_path)
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"  ✓ {filename} → chapter_{chapter_num}.txt")
            except Exception as e:
                print(f"  ✗ Failed to convert {filename}: {e}")

    print("\nDone!")

if __name__ == '__main__':
    main()
