#!/usr/bin/env python3
"""
Merge split DOCX chapters back into a single book.

This script reads all chapter files from the output directory
and combines them into a single DOCX file.
"""

import os
import sys
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn
import argparse
import re


def extract_sort_key(filename):
    """
    Extract a sort key from filename for proper ordering.

    Returns tuple of (order_priority, chapter_number, name) for sorting.
    """
    stem = filename.stem  # filename without extension

    # Front matter must come first
    if stem == '00_Front_Matter':
        return (0, 0, stem)

    # Timeline sections come right after front matter (before chapters)
    timeline_order = {
        'Early_Life_1964-1982': (1, 0),
        'Princeton_Years_1982-1986': (2, 0),
        'Graduate_School__Early_Career_1986-1990': (3, 0),
        'Silicon_Valley_Rise_1990-1997': (4, 0),
        'Professional_Peaks__Valleys_1998-2004': (5, 0),
        'Family_Transitions_2000-2013': (6, 0),
        'Personal_Growth_2010-2023': (7, 0),
        'Health_Crisis__Renewal_2023-2024': (8, 0),
        'Key_Relationships_Timeline': (9, 0),
    }

    if stem in timeline_order:
        priority, num = timeline_order[stem]
        return (priority, num, stem)

    # Extract chapter number for numbered chapters
    # Chapters come after timeline (priority 10+)
    match = re.match(r'chapter_(\d+)', stem)
    if match:
        chapter_num = int(match.group(1))
        # Priority is 10 + chapter number so they come after timeline
        return (10 + chapter_num, chapter_num, stem)

    # Default: sort alphabetically
    return (999, 0, stem)


class BookMerger:
    def __init__(self, input_dir="output", output_file="reconstructed.docx"):
        """
        Initialize the book merger.

        Args:
            input_dir: Directory containing chapter files
            output_file: Output filename for merged document
        """
        self.input_dir = Path(input_dir)
        self.output_file = output_file

    def merge(self):
        """Merge all chapter files into a single document."""
        print(f"Reading chapters from: {self.input_dir}")

        # Find all DOCX files in the input directory
        chapter_files = sorted(
            [f for f in self.input_dir.glob("*.docx")],
            key=extract_sort_key
        )

        if not chapter_files:
            print(f"ERROR: No DOCX files found in {self.input_dir}")
            return

        print(f"Found {len(chapter_files)} chapter files\n")

        # Create merged document
        merged_doc = None

        for idx, chapter_file in enumerate(chapter_files):
            print(f"Adding: {chapter_file.name}")
            chapter_doc = Document(chapter_file)

            if merged_doc is None:
                # First chapter: use it as the base document
                merged_doc = chapter_doc
            else:
                # Subsequent chapters: append their content
                self.append_document(merged_doc, chapter_doc)

        # Save merged document
        print(f"\nSaving merged document to: {self.output_file}")
        merged_doc.save(self.output_file)
        print("Done!")

    def append_document(self, base_doc, append_doc):
        """
        Append all content from append_doc to base_doc.

        Args:
            base_doc: The document to append to
            append_doc: The document to append from
        """
        import copy

        # First, merge styles from append_doc into base_doc if they don't exist
        existing_style_ids = {s.style_id for s in base_doc.styles}
        for style_element in append_doc.styles._element:
            style_id = style_element.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}styleId')
            if style_id and style_id not in existing_style_ids:
                base_doc.styles._element.append(copy.deepcopy(style_element))
                existing_style_ids.add(style_id)

        # Append all paragraphs by deep copying entire paragraph elements
        for para in append_doc.paragraphs:
            # Deep copy the entire paragraph element to preserve everything:
            # - style
            # - formatting
            # - runs
            # - images
            # - all properties
            new_para_element = copy.deepcopy(para._element)
            base_doc._element.body.append(new_para_element)

    def has_image(self, run):
        """Check if a run contains an image."""
        drawing_elements = run._element.findall(f'.//{qn("a:blip")}',
                                                 namespaces=run._element.nsmap)
        return len(drawing_elements) > 0


def main():
    parser = argparse.ArgumentParser(
        description="Merge split DOCX chapters back into a single book"
    )

    parser.add_argument('-i', '--input', default='output',
                        help='Input directory containing chapter files (default: output)')
    parser.add_argument('-o', '--output', default='reconstructed.docx',
                        help='Output filename for merged document (default: reconstructed.docx)')

    args = parser.parse_args()

    # Check if input directory exists
    if not os.path.exists(args.input):
        print(f"ERROR: Input directory not found: {args.input}")
        sys.exit(1)

    # Create merger and run
    merger = BookMerger(args.input, args.output)
    merger.merge()


if __name__ == '__main__':
    main()
