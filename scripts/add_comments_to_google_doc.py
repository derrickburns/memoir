#!/usr/bin/env python3
"""
Add comments to Google Doc for character introductions, timelines, and overlaps.

This script adds three types of comments:
1. Character introduction comments - flag first mention of each person
2. Timeline comments - specify year(s) and age(s) for each chapter
3. Overlap comments - identify chapters covering same time period

Usage:
    python3 scripts/add_comments_to_google_doc.py --doc-id YOUR_DOC_ID --dry-run
    python3 scripts/add_comments_to_google_doc.py --doc-id YOUR_DOC_ID
    python3 scripts/add_comments_to_google_doc.py --doc-id YOUR_DOC_ID --chapter 1
"""

import os
import sys
import argparse
import pickle
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.pickle.
# Need both Docs (to read) and Drive (to add comments)
SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive'
]


def get_credentials():
    """Get Google API credentials."""
    creds = None
    token_path = Path('data/token.pickle')
    creds_path = Path('data/credentials.json')

    # The file token.pickle stores the user's access and refresh tokens
    if token_path.exists():
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not creds_path.exists():
                print(f"ERROR: Credentials file not found at {creds_path}")
                print("Please follow GOOGLE_API_SETUP.md to set up credentials")
                sys.exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(
                str(creds_path), SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds


def find_text_in_doc(doc_content, search_text):
    """
    Find the index of text in the document.
    Returns tuple of (start_index, end_index) or None if not found.
    """
    # Get all text from the document
    full_text = ""
    index_map = []  # Maps character position to document index

    for element in doc_content.get('body', {}).get('content', []):
        if 'paragraph' in element:
            for elem in element['paragraph'].get('elements', []):
                if 'textRun' in elem:
                    text = elem['textRun']['content']
                    start_idx = elem['startIndex']

                    for i, char in enumerate(text):
                        full_text += char
                        index_map.append(start_idx + i)

    # Find the search text in full_text
    pos = full_text.find(search_text)
    if pos == -1:
        return None

    # Convert back to document indices
    start_index = index_map[pos]
    end_index = index_map[pos + len(search_text) - 1] + 1

    return (start_index, end_index)


def add_comment(docs_service, drive_service, doc_id, start_index, end_index, comment_text, dry_run=False):
    """
    Add an anchored comment to the document at the specified range.

    Uses a two-step process:
    1. Create a named range at the text location using Docs API
    2. Create a comment anchored to that named range using Drive API
    """
    if dry_run:
        print(f"[DRY RUN] Would add comment at indices {start_index}-{end_index}:")
        print(f"  {comment_text[:100]}...")
        return True

    try:
        # Step 1: Create a named range for the text span
        import time
        range_name = f"comment_range_{int(time.time() * 1000)}"  # Unique name

        requests = [{
            'createNamedRange': {
                'name': range_name,
                'range': {
                    'startIndex': start_index,
                    'endIndex': end_index
                }
            }
        }]

        docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={'requests': requests}
        ).execute()

        # Step 2: Create a comment anchored to the named range
        comment_body = {
            'content': comment_text,
            'anchor': range_name
        }

        drive_service.comments().create(
            fileId=doc_id,
            body=comment_body,
            fields='id,content,anchor'
        ).execute()

        print(f"✓ Added comment at {start_index}-{end_index}: {comment_text[:50]}...")
        return True

    except HttpError as error:
        print(f'✗ Error adding comment: {error}')
        return False


def get_chapter_comments():
    """
    Define all comments to add to the document.
    Returns list of dicts with: chapter, location_text, comment_text, comment_type

    Based on comprehensive analysis of all 34 chapters.
    """
    comments = []

    # CHAPTER 1: Two Worlds Converging
    comments.extend([
        {
            'chapter': 1,
            'location_text': 'Chapter 1: Two Worlds Converging',
            'comment_text': 'TIMELINE: April 1964 | Age 0 (birth) | Adoption story - birth and placement',
            'comment_type': 'timeline'
        },
        {
            'chapter': 1,
            'location_text': 'My birth mother had lived for months',
            'comment_text': 'INTRODUCE: Birth mother - 22 years old, Jewish woman, pregnant by Black law student, college student (needs full introduction with name, physical appearance, personality, relationship context)',
            'comment_type': 'character'
        },
        {
            'chapter': 1,
            'location_text': 'my future mother Willa Burns graded papers',
            'comment_text': 'INTRODUCE: Willa Burns - adoptive mother, 4\'11", special education teacher, determined, strict (give full introduction with physical description, personality traits, teaching background)',
            'comment_type': 'character'
        },
        {
            'chapter': 1,
            'location_text': 'Her husband Howard watched helplessly',
            'comment_text': 'INTRODUCE: Howard Burns - adoptive father, works at TACOM, photographer, quiet, methodical, WWII veteran (give full introduction with physical description, background, personality)',
            'comment_type': 'character'
        },
    ])

    # CHAPTER 2: The Perfect Shot
    comments.extend([
        {
            'chapter': 2,
            'location_text': 'Chapter 2: The Perfect Shot',
            'comment_text': 'TIMELINE: 1969 | Age 5 | Kindergarten graduation\n\nOVERLAPS WITH: Chapter 3 (also covers early childhood 1969-1970)',
            'comment_type': 'timeline'
        },
        {
            'chapter': 2,
            'location_text': 'At noon, Cille—our combination babysitter',
            'comment_text': 'INTRODUCE: Cille (Lucille Pryor) - combination babysitter and housekeeper, plays gin rummy with Derrick (give full introduction with physical description, personality, relationship to family)',
            'comment_type': 'character'
        },
    ])

    # CHAPTER 3: Lessons from Aunt Mae
    comments.extend([
        {
            'chapter': 3,
            'location_text': 'Chapter 3: Lessons from Aunt Mae',
            'comment_text': 'TIMELINE: 1969-1970 | Age 5-6 | Weekends with Aunt Mae\n\nOVERLAPS WITH: Chapter 2 (both cover 1969-1970 period), Chapter 4 (continues into school years)',
            'comment_type': 'timeline'
        },
        {
            'chapter': 3,
            'location_text': 'Aunt Mae was like the film negative of Mom',
            'comment_text': 'INTRODUCE: Classie Mae Walker (Aunt Mae) - Mom\'s sister and surrogate mother, tall, buxom, welcoming, unconditionally loving, NO CHILDREN OF HER OWN, lives at 18606 Mackay (give full introduction with physical description, personality)',
            'comment_type': 'character'
        },
        {
            'chapter': 3,
            'location_text': 'Hey Boy!\' he greeted me',
            'comment_text': 'INTRODUCE: Uncle John Walker - Aunt Mae\'s husband, plays checkers, likes his "juice" (orange juice with alcohol), never loses at checkers (give full introduction)',
            'comment_type': 'character'
        },
    ])

    # CHAPTER 4-20: Timeline comments for middle chapters
    # (Character introductions can be added based on detailed analysis in CHAPTER_SUMMARIES.md)

    comments.extend([
        {'chapter': 4, 'location_text': 'Chapter 4: The Project Begins', 'comment_text': 'TIMELINE: 1970-1975 | Age 6-11 | Elementary school years\n\nOVERLAPS WITH: Chapters 2-3 (early childhood)', 'comment_type': 'timeline'},
        {'chapter': 5, 'location_text': 'Chapter 5: Developing the Picture', 'comment_text': 'TIMELINE: 1970s | Age 6-13 | Elementary/middle school years', 'comment_type': 'timeline'},
        {'chapter': 6, 'location_text': 'Chapter 6: Dave Arrives', 'comment_text': 'TIMELINE: 1969-1970s | Age 5-10s | Dave\'s adoption and early childhood together', 'comment_type': 'timeline'},
        {'chapter': 7, 'location_text': 'Chapter 7: Two Different Boys', 'comment_text': 'TIMELINE: 1970s | Childhood | Contrasting personalities and paths of Derrick and Dave', 'comment_type': 'timeline'},
        {'chapter': 8, 'location_text': 'Chapter 8: Finding My Voice', 'comment_text': 'TIMELINE: 1970s-early 1980s | Age 10-17 | Adolescence and self-discovery', 'comment_type': 'timeline'},
        {'chapter': 9, 'location_text': 'Chapter 9: The Power of Belonging', 'comment_text': 'TIMELINE: 1970s-1980s | Adolescence | Community and identity formation', 'comment_type': 'timeline'},
        {'chapter': 10, 'location_text': 'Chapter 10: Performing Identity', 'comment_text': 'TIMELINE: 1970s-1980s | Teenage years | Learning to perform for acceptance', 'comment_type': 'timeline'},
        {'chapter': 11, 'location_text': 'Chapter 11: Finding My Voice', 'comment_text': 'TIMELINE: Late 1970s-early 1980s | Age 15-18 | High school years', 'comment_type': 'timeline'},
        {'chapter': 12, 'location_text': 'Chapter 12: Finding My Place at Princeton', 'comment_text': 'TIMELINE: 1982-1986 | Age 18-22 | Princeton undergraduate years', 'comment_type': 'timeline'},
        {'chapter': 13, 'location_text': 'Chapter 13: Understanding My Path', 'comment_text': 'TIMELINE: 1986-1990 | Age 22-26 | Post-graduation, early career', 'comment_type': 'timeline'},
        {'chapter': 14, 'location_text': 'Chapter 14: Encountering Love', 'comment_text': 'TIMELINE: 1990 | Age 26 | Meeting Gina (needs expansion)', 'comment_type': 'timeline'},
        {'chapter': 15, 'location_text': 'Chapter 15: Becoming Real', 'comment_text': 'TIMELINE: 1990s-2000s | Age 26-40s | Marriage, career, family\n\nOVERLAPS WITH: Chapters 16-21 (scrambled timeline - all cover 1990-2010 period)', 'comment_type': 'timeline'},
        {'chapter': 16, 'location_text': 'Chapter 16: What Blood Remembers', 'comment_text': 'TIMELINE: 1990s-2000s | Age 30s-40s | Search for birth parents\n\nOVERLAPS WITH: Chapters 15, 17-21', 'comment_type': 'timeline'},
        {'chapter': 17, 'location_text': 'Chapter 17: What Love Complicates', 'comment_text': 'TIMELINE: 1990s-2000s | Marriage and family challenges\n\nOVERLAPS WITH: Chapters 15-16, 18-21', 'comment_type': 'timeline'},
        {'chapter': 18, 'location_text': 'Chapter 18: Beyond the Algorithm', 'comment_text': 'TIMELINE: 2000s | Age 40s | Career in tech and innovation\n\nOVERLAPS WITH: Chapters 15-17, 19-21', 'comment_type': 'timeline'},
        {'chapter': 19, 'location_text': 'Chapter 19: Swimming with Sharks', 'comment_text': 'TIMELINE: 2000s | Age 40s | Corporate challenges and career advancement\n\nOVERLAPS WITH: Chapters 15-18, 20-21', 'comment_type': 'timeline'},
        {'chapter': 20, 'location_text': 'Chapter 20: Searching for Black Excellence', 'comment_text': 'TIMELINE: 2000s-2010s | Age 40s-50s | Professional identity and community\n\nOVERLAPS WITH: Chapters 15-19, 21', 'comment_type': 'timeline'},
    ])

    # CHAPTER 21: Courts of Transformation
    comments.extend([
        {
            'chapter': 21,
            'location_text': 'Chapter 21: Courts of Transformation',
            'comment_text': 'TIMELINE: 1989-2019 | Age 25-55 | Basketball at Cubberly and YMCA, spanning 30 years',
            'comment_type': 'timeline'
        },
        {
            'chapter': 21,
            'location_text': 'invitation from James:',
            'comment_text': 'INTRODUCE: James - 6\'4", 240+ pounds solid muscle, played basketball at Cubberly, quiet force/uber alpha, deep understanding of game, physical dominance, everyone wanted him on their team (Derrick\'s protector and first basketball mentor)',
            'comment_type': 'character'
        },
        {
            'chapter': 21,
            'location_text': 'Ed, a 5\'11", 220-pound engineer',
            'comment_text': 'INTRODUCE: Ed - 5\'11", 220 pounds, engineer, square glasses, body of tight end, played with intensity, court\'s conscience, demanded clean play and respect',
            'comment_type': 'character'
        },
    ])

    # CHAPTER 22: A Father's Love
    comments.extend([
        {
            'chapter': 22,
            'location_text': 'Chapter 22: A Father\'s Love',
            'comment_text': 'TIMELINE: 1986-2000 | Age 22-36 | Dad\'s retirement through death; covers Dad\'s stroke (1995), care at home, and death (May 5, 2000)\n\nOVERLAPS WITH: Chapter 23 (both cover Dad\'s death and aftermath in 2000)',
            'comment_type': 'timeline'
        },
    ])

    # CHAPTER 23: A Mother's Farewell
    comments.extend([
        {
            'chapter': 23,
            'location_text': 'Chapter 23: A Mother\'s Farewell',
            'comment_text': 'TIMELINE: 2000-2010 | Age 36-46 | After Dad\'s death through Mom\'s death (2010)\n\nOVERLAPS WITH: Chapter 22 (both cover 2000, Dad\'s death), Chapter 24 (both cover 2010, Mom\'s funeral)',
            'comment_type': 'timeline'
        },
        {
            'chapter': 23,
            'location_text': 'Sheila was tall and strong at 5\'10"',
            'comment_text': 'INTRODUCE: Sheila - 5\'10", tall and strong, home health aide with years of experience, steady brown eyes, capable frame, teenage son, hired to care for Mom, later rented house and stole Mom\'s belongings including furniture and jewelry',
            'comment_type': 'character'
        },
    ])

    # CHAPTER 24: Colliding Worlds
    comments.extend([
        {
            'chapter': 24,
            'location_text': 'Chapter 24: Colliding Worlds',
            'comment_text': 'TIMELINE: December 2010 | Age 46 | Mom\'s funeral\n\nOVERLAPS WITH: Chapter 23 (both cover Mom\'s death and funeral in 2010)',
            'comment_type': 'timeline'
        },
    ])

    # CHAPTER 25: Final Gestures
    comments.extend([
        {
            'chapter': 25,
            'location_text': 'Chapter 25: Final Gestures',
            'comment_text': 'TIMELINE: 2013 | Age 49 | Marcia\'s death (3 years after Mom\'s funeral)',
            'comment_type': 'timeline'
        },
        {
            'chapter': 25,
            'location_text': 'join him and Cara in Florida',
            'comment_text': 'INTRODUCE: Cara - Marcia\'s daughter (Derrick\'s half-sister), partner named Dave, present at Marcia\'s deathbed in Florida, stood at Marcia\'s left side during final moments',
            'comment_type': 'character'
        },
    ])

    # CHAPTER 26: Dave Becomes Jala
    comments.extend([
        {
            'chapter': 26,
            'location_text': 'Chapter 26: Dave Becomes Jala',
            'comment_text': 'TIMELINE: 1982-2011 | Age 18-47 | Dave leaving for college through first California visit as Jala\n\nOVERLAPS WITH: Multiple chapters covering 1980s-2000s (background), Chapter 27 (continues Jala\'s story into illness years)',
            'comment_type': 'timeline'
        },
    ])

    # CHAPTER 27: Holding On
    comments.extend([
        {
            'chapter': 27,
            'location_text': 'Chapter 27: Holding On',
            'comment_text': 'TIMELINE: 2017-2022 | Age 53-58 | Jala\'s quintuple bypass through Maya\'s wedding\n\nOVERLAPS WITH: Chapter 26 (continues Jala\'s story), Chapter 28 (continues to Jala\'s death in 2023)',
            'comment_type': 'timeline'
        },
    ])

    # CHAPTER 28: Letting Go
    comments.extend([
        {
            'chapter': 28,
            'location_text': 'Chapter 28: Letting Go',
            'comment_text': 'TIMELINE: November-December 2022 | Age 58 | Jala\'s final illness and death\n\nOVERLAPS WITH: Chapter 27 (continues from Thanksgiving 2022 hospitalization)',
            'comment_type': 'timeline'
        },
        {
            'chapter': 28,
            'location_text': 'ask Reverend Doctor William J. Barber II to preside',
            'comment_text': 'INTRODUCE: Reverend Doctor William J. Barber II (Doctor Barber/Bishop Barber) - led Poor People\'s Campaign where Jala was community organizer, Jala had his private number, deep connection with Jala, quoted Matthew 19:12 and Acts 8:26-40 about eunuchs, reassured Jala she wouldn\'t go to hell for being transgender or stopping dialysis, agreed to preside over her funeral',
            'comment_type': 'character'
        },
    ])

    # CHAPTER 29: The Diagnosis
    comments.extend([
        {
            'chapter': 29,
            'location_text': 'Chapter 29: The Diagnosis',
            'comment_text': 'TIMELINE: September-December 2023 | Age 59 | Cancer diagnosis\n\nOVERLAPS WITH: Chapter 28 (both in late 2023), Chapter 30 (continues cancer treatment story)',
            'comment_type': 'timeline'
        },
        {
            'chapter': 29,
            'location_text': 'I had emailed Daniel, Doctor Greenwood',
            'comment_text': 'INTRODUCE: Doctor Daniel Greenwood (Daniel) - Derrick\'s doctor for 15 years, gentle tone, recognized cancer screening questions needed, referred to Doctor Tang, close enough relationship that Derrick emailed him directly',
            'comment_type': 'character'
        },
        {
            'chapter': 29,
            'location_text': 'Doctor Tang, in head and neck surgery',
            'comment_text': 'INTRODUCE: Doctor Tang - Head and neck surgeon at Kaiser French Campus, diagnosed Derrick with squamous cell cancer on November 2, 2023, confident manner, used pediatric scope due to Derrick\'s small nasal passages, performed multiple biopsies',
            'comment_type': 'character'
        },
    ])

    # CHAPTER 30: A Problem to Overcome
    comments.extend([
        {
            'chapter': 30,
            'location_text': 'Chapter 30: A Problem to Overcome',
            'comment_text': 'TIMELINE: November-December 2023 | Age 59 | From diagnosis through first treatment\n\nOVERLAPS WITH: Chapter 29 (both cover November 2023 diagnosis period)',
            'comment_type': 'timeline'
        },
        {
            'chapter': 30,
            'location_text': 'I called Steve Van',
            'comment_text': 'INTRODUCE: Steve Van - friend who wrestled with health crises for decades including diabetes, told Derrick "treat this like a problem to overcome," helped Derrick understand cancer battle, mentor figure, Wednesday warrior, coached Derrick on diabetes management techniques',
            'comment_type': 'character'
        },
        {
            'chapter': 30,
            'location_text': 'I was assigned to Doctor Jed Katzel',
            'comment_text': 'INTRODUCE: Doctor Jed Katzel - head of head and neck cancer treatment across Kaiser nationwide, firm handshake, smile reached his eyes, explained P-16 positive squamous cell cancer (HPV-related), honest about difficult treatment, promised "we will get you through this," national leader',
            'comment_type': 'character'
        },
    ])

    # CHAPTER 31: The Battle
    comments.extend([
        {
            'chapter': 31,
            'location_text': 'Chapter 31: The Battle',
            'comment_text': 'TIMELINE: December 2023-March 2024 | Age 59-60 | Cancer treatment period\n\nOVERLAPS WITH: Chapter 30 (continues from December 2023 start of treatment)',
            'comment_type': 'timeline'
        },
        {
            'chapter': 31,
            'location_text': 'I reached out to Steve. We were estranged',
            'comment_text': 'INTRODUCE: Steve (throat cancer survivor, different from Steve Van) - had P-16 positive throat cancer, nearly died, coded in hospital, had larynx removed and throat rebuilt, cannot speak, lost 20+ pounds, sold meticulously constructed home to pay healthcare expenses, moved to small garden apartment, adopted and raised young girl, previously estranged from Derrick, reconnected during Derrick\'s cancer treatment',
            'comment_type': 'character'
        },
    ])

    # CHAPTER 32: The Triumph
    comments.extend([
        {
            'chapter': 32,
            'location_text': 'Chapter 32: The Triumph',
            'comment_text': 'TIMELINE: March-June 2024 | Age 60 | Post-treatment recovery\n\nOVERLAPS WITH: Chapter 31 (continues from treatment completion)',
            'comment_type': 'timeline'
        },
        {
            'chapter': 32,
            'location_text': 'JIMMY!\' I called one afternoon',
            'comment_text': 'INTRODUCE: Jimmy - high school friend, knew Derrick before the masks, knew parents when healthy, knew Dave before transition, marathon phone calls 2-3 times week after reconnection, kids out of college and wife back at work, responds "D. BURNS!"',
            'comment_type': 'character'
        },
    ])

    # CHAPTER 33: Full Circle
    comments.extend([
        {
            'chapter': 33,
            'location_text': 'Chapter 33: Full Circle',
            'comment_text': 'TIMELINE: 2024 | Age 60 | Work reorganization and decision to leave\n\nOVERLAPS WITH: Chapter 32 (both in 2024 recovery/return to work period)',
            'comment_type': 'timeline'
        },
        {
            'chapter': 33,
            'location_text': 'Over lunch with Willie Hooks, my longtime mentor',
            'comment_text': 'INTRODUCE: Willie Hooks - longtime mentor, walked path of stepping away from corporate ladder in his fifties, asked "What do you really want now?", guided Derrick\'s thinking about quality of life vs career advancement, Wednesday warrior',
            'comment_type': 'character'
        },
    ])

    # CHAPTER 34: Fearless Love
    comments.extend([
        {
            'chapter': 34,
            'location_text': 'Chapter 34: Fearless Love',
            'comment_text': 'TIMELINE: 2025 | Age 60-61 | Queens visit for Jasmine\'s art exhibition',
            'comment_type': 'timeline'
        },
        {
            'chapter': 34,
            'location_text': 'celebrate cousin Jasmine Gregory\'s solo exhibition',
            'comment_text': 'INTRODUCE: Cousin Jasmine Gregory (Jasmine) - major artist in Geneva, Switzerland, solo exhibition "Who Wants to Die for Glamour" at Museum of Modern Art PS1 in NYC, full-time job, separated by three time zones from west coast relatives and nine from her, created abstract art with clear meanings, Derrick\'s niece though not by blood',
            'comment_type': 'character'
        },
        {
            'chapter': 34,
            'location_text': 'I reached out to the other author. Elliot Aronson',
            'comment_text': 'INTRODUCE: Elliot Aronson - 92 years old, lives in Santa Cruz, co-authored 1962 research paper on communicator credibility with Burton (Derrick\'s birth father), was new assistant professor at Harvard when Burton took his class on social influence, called Burton "smart, courageous young man," great-nephew Brendan was in Maya\'s business school class',
            'comment_type': 'character'
        },
    ])

    return comments


def main():
    parser = argparse.ArgumentParser(
        description='Add timeline and character introduction comments to Google Doc',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--doc-id',
                       default='1I5aglDNAqYmdMYojLqwmCLdDzQj8UlPMdAjkviKN9hk',
                       help='Google Doc ID (default: memoir doc)')
    parser.add_argument('--dry-run',
                       action='store_true',
                       help='Show what would be done without actually doing it')
    parser.add_argument('--chapter',
                       type=int,
                       help='Only process specific chapter number')

    args = parser.parse_args()

    print("=" * 80)
    print("ADD COMMENTS TO GOOGLE DOC")
    print("=" * 80)
    print()

    if args.dry_run:
        print("*** DRY RUN MODE - No changes will be made ***")
        print()

    # Get credentials
    print("Authenticating with Google...")
    creds = get_credentials()

    # Build both Docs and Drive services
    docs_service = build('docs', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    # Get the document
    print(f"Fetching document {args.doc_id}...")
    try:
        document = docs_service.documents().get(documentId=args.doc_id).execute()
        print(f"✓ Document title: {document.get('title')}")
        print()
    except HttpError as error:
        print(f'Error fetching document: {error}')
        sys.exit(1)

    # Get comments to add
    all_comments = get_chapter_comments()

    # Filter by chapter if specified
    if args.chapter:
        all_comments = [c for c in all_comments if c['chapter'] == args.chapter]
        print(f"Processing only Chapter {args.chapter}")

    print(f"Found {len(all_comments)} comments to add")
    print()

    # Add each comment
    added = 0
    skipped = 0

    for comment in all_comments:
        chapter = comment['chapter']
        location = comment['location_text']
        text = comment['comment_text']

        print(f"Chapter {chapter}: Looking for '{location[:50]}...'")

        # Find the text in the document
        result = find_text_in_doc(document, location)

        if result:
            start_idx, end_idx = result
            success = add_comment(docs_service, drive_service, args.doc_id, start_idx, end_idx, text, args.dry_run)
            if success:
                added += 1
            else:
                skipped += 1
        else:
            print(f"  ⚠ WARNING: Could not find text in document")
            skipped += 1

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Comments added: {added}")
    print(f"Comments skipped: {skipped}")
    print(f"Total: {len(all_comments)}")

    if args.dry_run:
        print()
        print("This was a dry run - no changes were made to the document")
        print("Run without --dry-run to actually add comments")


if __name__ == '__main__':
    main()
