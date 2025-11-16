#!/usr/bin/env python3
"""Extract age markers and timeline from chapters."""

import re
from pathlib import Path

def extract_timeline(chapter_num, text):
    """Extract age markers and key events from chapter text."""

    events = []

    # Age patterns to search for
    age_patterns = [
        r'(?:age|aged?)\s+(\d+)',
        r'(\d+)\s+years?\s+old',
        r'(?:At|When|By)\s+(\d+)',
        r'(?:turned|was)\s+(\d+)',
        r'(\d+)\s+(?:year|yr)',
    ]

    # Grade patterns
    grade_patterns = [
        r'(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|eleventh|twelfth)\s+grade',
        r'grade\s+(\d+)',
        r'kindergarten',
        r'nursery\s+school',
    ]

    # Time markers
    time_patterns = [
        r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}',
        r'\d{4}',  # Just years
    ]

    lines = text.split('\n')

    for i, line in enumerate(lines, 1):
        # Check for age markers
        for pattern in age_patterns:
            matches = re.findall(pattern, line, re.IGNORECASE)
            if matches:
                events.append({
                    'chapter': chapter_num,
                    'line': i,
                    'type': 'age',
                    'value': matches[0] if isinstance(matches[0], str) else matches[0][0],
                    'context': line.strip()[:100]
                })

        # Check for grade markers
        for pattern in grade_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                events.append({
                    'chapter': chapter_num,
                    'line': i,
                    'type': 'grade',
                    'value': re.search(pattern, line, re.IGNORECASE).group(),
                    'context': line.strip()[:100]
                })

        # Check for year markers
        for pattern in time_patterns:
            matches = re.findall(pattern, line)
            if matches:
                for match in matches:
                    if len(match) == 4 and match.startswith('19'):  # Only 19xx years
                        events.append({
                            'chapter': chapter_num,
                            'line': i,
                            'type': 'year',
                            'value': match,
                            'context': line.strip()[:100]
                        })

    return events

def main():
    output_dir = Path('output/txt')

    all_events = []

    # Process chapters 1-11
    for num in range(1, 12):
        chapter_file = output_dir / f'chapter_{num:02d}.txt'
        if chapter_file.exists():
            with open(chapter_file, 'r', encoding='utf-8') as f:
                text = f.read()
                events = extract_timeline(num, text)
                all_events.extend(events)
                print(f"\nChapter {num}: Found {len(events)} timeline markers")

    # Write results
    output_file = Path('docs/CHRONOLOGY_AUDIT.md')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Chronology Audit: Chapters 1-11\n\n")
        f.write("## Timeline Markers by Chapter\n\n")

        for ch in range(1, 12):
            ch_events = [e for e in all_events if e['chapter'] == ch]
            if ch_events:
                f.write(f"\n### Chapter {ch}\n\n")
                f.write("| Line | Type | Value | Context |\n")
                f.write("|------|------|-------|----------|\n")
                for event in ch_events:
                    f.write(f"| {event['line']} | {event['type']} | {event['value']} | {event['context']} |\n")

        f.write("\n\n## Timeline Summary\n\n")
        f.write("Age markers found:\n\n")
        age_events = sorted([e for e in all_events if e['type'] == 'age'],
                          key=lambda x: (x['chapter'], int(x['value']) if x['value'].isdigit() else 0))
        for event in age_events:
            f.write(f"- Chapter {event['chapter']}, Line {event['line']}: Age {event['value']}\n")

    print(f"\n\nResults written to: {output_file}")

if __name__ == '__main__':
    main()
