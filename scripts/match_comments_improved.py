#!/usr/bin/env python3
"""
Improved comment matcher with better fuzzy matching algorithms.

Uses multiple strategies to find the best match for each comment:
1. Exact substring match
2. Normalized text match (ignore whitespace/punctuation)
3. Sliding window fuzzy match (find best local match)
4. Token set matching (ignore word order)
5. Partial ratio matching
"""

import json
import sys
import re
from pathlib import Path
from docx import Document
from rapidfuzz import fuzz, process
from collections import defaultdict


class ImprovedCommentMatcher:
    def __init__(self, comments_file='comments.json', chapters_dir='output'):
        """Initialize the improved matcher."""
        self.comments_file = comments_file
        self.chapters_dir = Path(chapters_dir)
        self.comments_data = None
        self.chapter_texts = {}
        self.chapter_paragraphs = {}

    def load_comments(self):
        """Load comments from JSON file."""
        print(f"Loading comments from {self.comments_file}...")

        if not Path(self.comments_file).exists():
            print(f"ERROR: {self.comments_file} not found!")
            print("\nRun extract_comments.py first to extract comments from Google Doc")
            sys.exit(1)

        with open(self.comments_file, 'r') as f:
            self.comments_data = json.load(f)

        print(f"✓ Loaded {self.comments_data['total_comments']} comments")
        return self.comments_data

    def load_chapter_texts(self):
        """Load all chapter files and extract their text."""
        print(f"\nLoading chapter files from {self.chapters_dir}...")

        chapter_files = sorted(self.chapters_dir.glob('*.docx'))

        for chapter_file in chapter_files:
            # Skip temporary Word files
            if chapter_file.name.startswith('~$'):
                continue

            try:
                doc = Document(chapter_file)
                paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
                text = '\n'.join(paragraphs)

                self.chapter_texts[chapter_file.name] = text
                self.chapter_paragraphs[chapter_file.name] = paragraphs
            except Exception as e:
                print(f"Warning: Could not read {chapter_file.name}: {e}")

        print(f"✓ Loaded {len(self.chapter_texts)} chapter files")

    def normalize_text(self, text):
        """Normalize text for matching."""
        if not text:
            return ''

        # Convert to lowercase
        text = text.lower()
        # Replace multiple whitespace with single space
        text = re.sub(r'\s+', ' ', text)
        # Strip leading/trailing whitespace
        text = text.strip()
        return text

    def aggressive_normalize(self, text):
        """More aggressive normalization - remove punctuation too."""
        text = self.normalize_text(text)
        # Remove most punctuation but keep apostrophes
        text = re.sub(r'[^\w\s\']', '', text)
        return text

    def tokenize(self, text):
        """Convert text to sorted tokens for token-based matching."""
        text = self.aggressive_normalize(text)
        tokens = sorted(text.split())
        return ' '.join(tokens)

    def sliding_window_match(self, search_text, chapter_text, window_factor=2.0):
        """
        Find best match using sliding window.

        Returns the best match score and position by sliding a window
        through the chapter text.
        """
        if not search_text or not chapter_text:
            return 0, -1, ''

        search_norm = self.normalize_text(search_text)
        chapter_norm = self.normalize_text(chapter_text)

        # Window size is search text length * factor
        search_len = len(search_text)
        window_size = int(search_len * window_factor)

        if window_size > len(chapter_text):
            # Text is shorter than window, just compare whole thing
            score = fuzz.ratio(search_norm, chapter_norm)
            return score, 0, chapter_text[:min(len(chapter_text), len(search_text) * 2)]

        best_score = 0
        best_pos = -1
        best_match = ''

        # Slide window through text
        for i in range(0, len(chapter_text) - window_size + 1, max(1, window_size // 4)):
            window = chapter_text[i:i + window_size]
            window_norm = self.normalize_text(window)

            # Try multiple scoring methods
            ratio = fuzz.ratio(search_norm, window_norm)
            partial = fuzz.partial_ratio(search_norm, window_norm)
            token_sort = fuzz.token_sort_ratio(search_norm, window_norm)

            # Use the best score from different methods
            score = max(ratio, partial, token_sort)

            if score > best_score:
                best_score = score
                best_pos = i
                best_match = window

        return best_score, best_pos, best_match

    def paragraph_level_match(self, search_text, paragraphs):
        """
        Match against individual paragraphs.

        Sometimes comments are on specific paragraphs, so check each one.
        """
        if not search_text or not paragraphs:
            return 0, -1, ''

        search_norm = self.normalize_text(search_text)

        best_score = 0
        best_idx = -1
        best_para = ''

        for idx, para in enumerate(paragraphs):
            para_norm = self.normalize_text(para)

            # Try multiple matching strategies
            ratio = fuzz.ratio(search_norm, para_norm)
            partial = fuzz.partial_ratio(search_norm, para_norm)
            token_sort = fuzz.token_sort_ratio(search_norm, para_norm)

            score = max(ratio, partial, token_sort)

            if score > best_score:
                best_score = score
                best_idx = idx
                best_para = para

        return best_score, best_idx, best_para

    def find_best_match(self, search_text, min_score=60):
        """
        Find the best match across all chapters using multiple strategies.

        Returns list of matches sorted by score (best first).
        """
        if not search_text or not search_text.strip():
            return []

        matches = []
        search_norm = self.normalize_text(search_text)
        search_aggressive = self.aggressive_normalize(search_text)

        for chapter_name, chapter_text in self.chapter_texts.items():
            chapter_norm = self.normalize_text(chapter_text)
            chapter_aggressive = self.aggressive_normalize(chapter_text)

            # Strategy 1: Exact substring match (best case)
            if search_norm in chapter_norm:
                pos = chapter_norm.index(search_norm)
                context_start = max(0, pos - 50)
                context_end = min(len(chapter_text), pos + len(search_text) + 50)
                context = chapter_text[context_start:context_end]

                matches.append({
                    'chapter': chapter_name,
                    'score': 100.0,
                    'method': 'exact',
                    'context': context,
                    'position': pos
                })
                continue  # Exact match found, skip other strategies

            # Strategy 2: Normalized exact match (ignore whitespace)
            if search_aggressive in chapter_aggressive:
                pos = chapter_aggressive.index(search_aggressive)
                # Approximate position in original text
                context = chapter_text[:min(len(chapter_text), len(search_text) * 2)]

                matches.append({
                    'chapter': chapter_name,
                    'score': 98.0,
                    'method': 'normalized_exact',
                    'context': context,
                    'position': pos
                })
                continue

            # Strategy 3: Sliding window fuzzy match
            window_score, window_pos, window_match = self.sliding_window_match(
                search_text, chapter_text, window_factor=2.5
            )

            # Strategy 4: Paragraph-level match
            para_score, para_idx, para_text = self.paragraph_level_match(
                search_text, self.chapter_paragraphs.get(chapter_name, [])
            )

            # Strategy 5: Token set ratio (whole chapter)
            token_score = fuzz.token_set_ratio(search_norm, chapter_norm)

            # Use the best score from fuzzy strategies
            best_fuzzy_score = max(window_score, para_score, token_score)

            if best_fuzzy_score >= min_score:
                # Determine which method won
                if window_score >= para_score and window_score >= token_score:
                    method = 'sliding_window'
                    context = window_match[:200] if window_match else ''
                elif para_score >= token_score:
                    method = 'paragraph'
                    context = para_text[:200] if para_text else ''
                else:
                    method = 'token_set'
                    context = chapter_text[:200]

                matches.append({
                    'chapter': chapter_name,
                    'score': best_fuzzy_score,
                    'method': method,
                    'context': context,
                    'position': window_pos if window_score == best_fuzzy_score else para_idx
                })

        # Sort by score (highest first)
        matches.sort(key=lambda x: x['score'], reverse=True)
        return matches

    def match_all_comments(self, min_score=60):
        """Match all comments to chapters using improved algorithm."""
        print(f"\nMatching comments to chapters (min score: {min_score})...")

        results = {
            'document_title': self.comments_data['document_title'],
            'total_comments': self.comments_data['total_comments'],
            'matched_comments': 0,
            'unmatched_comments': 0,
            'comment_matches': [],
            'match_quality': defaultdict(int)  # Track match quality distribution
        }

        for i, comment in enumerate(self.comments_data['comments'], 1):
            if i % 10 == 0:
                print(f"Processing comment {i}/{results['total_comments']}...", end='\r')

            quoted_text = comment.get('quoted_text', '')
            matches = self.find_best_match(quoted_text, min_score=min_score)

            comment_match = {
                'comment_id': comment['id'],
                'author': comment['author'],
                'content': comment['content'],
                'quoted_text': quoted_text,
                'created': comment['created'],
                'resolved': comment['resolved'],
                'matches': matches
            }

            if matches:
                results['matched_comments'] += 1
                best_match = matches[0]

                # Track match quality
                if best_match['score'] == 100:
                    results['match_quality']['exact'] += 1
                elif best_match['score'] >= 90:
                    results['match_quality']['excellent'] += 1
                elif best_match['score'] >= 80:
                    results['match_quality']['good'] += 1
                elif best_match['score'] >= 70:
                    results['match_quality']['fair'] += 1
                else:
                    results['match_quality']['weak'] += 1
            else:
                results['unmatched_comments'] += 1

            results['comment_matches'].append(comment_match)

        print()  # New line after progress
        print(f"✓ Matched {results['matched_comments']} comments")
        print(f"  {results['unmatched_comments']} comments could not be matched")

        # Print quality breakdown
        print("\nMatch Quality:")
        print(f"  Exact (100%): {results['match_quality']['exact']}")
        print(f"  Excellent (90-99%): {results['match_quality']['excellent']}")
        print(f"  Good (80-89%): {results['match_quality']['good']}")
        print(f"  Fair (70-79%): {results['match_quality']['fair']}")
        print(f"  Weak (60-69%): {results['match_quality']['weak']}")

        return results

    def export_matches(self, results, output_file='comment_matches_improved.json'):
        """Export comment matches to JSON and markdown."""
        print(f"\nExporting matches to {output_file}...")

        # Save JSON
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"✓ Saved to {output_file}")

        # Create markdown report
        md_file = output_file.replace('.json', '.md')
        with open(md_file, 'w') as f:
            f.write(f"# Improved Comment Matches: {results['document_title']}\n\n")
            f.write(f"**Total comments:** {results['total_comments']}\n\n")
            f.write(f"**Matched:** {results['matched_comments']} ({results['matched_comments']/results['total_comments']*100:.1f}%)\n\n")
            f.write(f"**Unmatched:** {results['unmatched_comments']} ({results['unmatched_comments']/results['total_comments']*100:.1f}%)\n\n")

            # Match quality
            f.write("## Match Quality Distribution\n\n")
            f.write(f"- Exact (100%): {results['match_quality']['exact']}\n")
            f.write(f"- Excellent (90-99%): {results['match_quality']['excellent']}\n")
            f.write(f"- Good (80-89%): {results['match_quality']['good']}\n")
            f.write(f"- Fair (70-79%): {results['match_quality']['fair']}\n")
            f.write(f"- Weak (60-69%): {results['match_quality']['weak']}\n\n")

            f.write("---\n\n")

            # Group by chapter
            by_chapter = defaultdict(list)
            unmatched = []

            for comment_match in results['comment_matches']:
                if comment_match['matches']:
                    best_match = comment_match['matches'][0]
                    chapter = best_match['chapter']
                    by_chapter[chapter].append({
                        'comment': comment_match,
                        'match': best_match
                    })
                else:
                    unmatched.append(comment_match)

            # Write by chapter
            f.write("## Comments by Chapter\n\n")

            for chapter in sorted(by_chapter.keys()):
                f.write(f"### {chapter} ({len(by_chapter[chapter])} comments)\n\n")

                for item in by_chapter[chapter]:
                    comment = item['comment']
                    match = item['match']
                    status = "✓" if comment['resolved'] else "○"

                    f.write(f"**{status} {comment['author']}** ({comment['created'][:10]})\n\n")

                    if comment['quoted_text']:
                        qt = comment['quoted_text'][:150]
                        if len(comment['quoted_text']) > 150:
                            qt += "..."
                        f.write(f"> {qt}\n\n")

                    f.write(f"**Comment:** {comment['content']}\n\n")
                    f.write(f"*Match: {match['method']}, score: {match['score']:.1f}%*\n\n")

                    if match.get('context'):
                        ctx = match['context'][:150]
                        if len(match.get('context', '')) > 150:
                            ctx += "..."
                        f.write(f"<details><summary>Context</summary>\n\n{ctx}\n\n</details>\n\n")

                    f.write("---\n\n")

            # Write unmatched
            if unmatched:
                f.write(f"## Unmatched Comments ({len(unmatched)})\n\n")

                for comment in unmatched[:50]:  # Limit to first 50
                    status = "✓" if comment['resolved'] else "○"
                    f.write(f"**{status} {comment['author']}** ({comment['created'][:10]})\n\n")
                    f.write(f"**Comment:** {comment['content']}\n\n")

                    if comment['quoted_text']:
                        qt = comment['quoted_text'][:100]
                        if len(comment['quoted_text']) > 100:
                            qt += "..."
                        f.write(f"**Quoted:** {qt}\n\n")

                    f.write("---\n\n")

                if len(unmatched) > 50:
                    f.write(f"\n*({len(unmatched) - 50} more unmatched comments not shown)*\n\n")

        print(f"✓ Created readable report: {md_file}")

        # Print summary
        print("\n" + "=" * 80)
        print("SUMMARY BY CHAPTER")
        print("=" * 80)
        for chapter in sorted(by_chapter.keys()):
            print(f"  {chapter}: {len(by_chapter[chapter])} comment(s)")

        if unmatched:
            print(f"\n  Unmatched: {len(unmatched)} comment(s)")

        print()


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Match comments to chapters using improved fuzzy matching',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Match with default settings (min score 60)
  %(prog)s

  # Use stricter matching (min score 80)
  %(prog)s --min-score 80

  # Use more lenient matching (min score 50)
  %(prog)s --min-score 50

This improved matcher uses multiple strategies:
- Exact substring matching
- Normalized text matching
- Sliding window fuzzy search
- Paragraph-level matching
- Token set matching

It will find significantly more matches than the basic matcher.
        """
    )

    parser.add_argument('-c', '--comments', default='data/comments.json',
                        help='Comments JSON file (default: data/comments.json)')
    parser.add_argument('-d', '--chapters-dir', default='output',
                        help='Directory with chapter DOCX files (default: output)')
    parser.add_argument('-o', '--output', default='data/comment_matches_improved.json',
                        help='Output file (default: data/comment_matches_improved.json)')
    parser.add_argument('-m', '--min-score', type=int, default=60,
                        help='Minimum match score 0-100 (default: 60)')

    args = parser.parse_args()

    # Validate min-score
    if not 0 <= args.min_score <= 100:
        print("ERROR: min-score must be between 0 and 100")
        sys.exit(1)

    # Create matcher
    matcher = ImprovedCommentMatcher(args.comments, args.chapters_dir)

    # Load data
    matcher.load_comments()
    matcher.load_chapter_texts()

    # Match comments
    results = matcher.match_all_comments(min_score=args.min_score)

    # Export
    matcher.export_matches(results, args.output)

    print("✓ Done!")


if __name__ == '__main__':
    main()
