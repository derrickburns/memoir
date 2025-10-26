#!/usr/bin/env python3
"""
Add suggestions to Google Doc for character introductions and timelines.

This script uses Google Docs API suggestions (not Drive API comments) because
suggestions can be properly anchored to specific text ranges, while comments cannot.

The suggestions will appear as tracked changes that you can review and accept/reject.

Usage:
    python3 scripts/add_suggestions_to_google_doc.py --doc-id YOUR_DOC_ID --dry-run
    python3 scripts/add_suggestions_to_google_doc.py --doc-id YOUR_DOC_ID
    python3 scripts/add_suggestions_to_google_doc.py --doc-id YOUR_DOC_ID --chapter 1
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
SCOPES = [
    'https://www.googleapis.com/auth/documents',
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


def add_note_at_location(docs_service, doc_id, start_index, end_index, note_text, dry_run=False):
    """
    Add a footnote at the specified location.

    Since we can't create anchored comments via API, we'll insert a footnote
    which IS supported and will be anchored to the specific location.
    """
    if dry_run:
        print(f"[DRY RUN] Would add footnote at indices {start_index}-{end_index}:")
        print(f"  {note_text[:100]}...")
        return True

    try:
        # Insert a footnote at the end of the range
        # Footnotes are automatically anchored to their location
        requests = [{
            'createFootnote': {
                'location': {
                    'index': end_index  # Insert footnote at end of range
                },
                'footnoteElements': [
                    {
                        'paragraph': {
                            'elements': [
                                {
                                    'textRun': {
                                        'content': note_text,
                                        'textStyle': {
                                            'fontSize': {
                                                'magnitude': 8,
                                                'unit': 'PT'
                                            }
                                        }
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }]

        docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={'requests': requests}
        ).execute()

        print(f"✓ Added footnote at {start_index}-{end_index}: {note_text[:50]}...")
        return True

    except HttpError as error:
        print(f'✗ Error adding footnote: {error}')
        return False


print("""
================================================================================
LIMITATION: Google APIs don't support creating anchored comments programmatically
================================================================================

Unfortunately, after investigation, neither the Google Docs API nor the Drive API
supports creating text-anchored comments for Google Docs through code.

The current comments in your document are file-level comments (not anchored to
specific text).

ALTERNATIVE SOLUTIONS:

1. MANUAL COMMENT ADDITION (Recommended)
   - Use the detailed comment list in docs/ADD_COMMENTS_GUIDE.md
   - Manually add comments in Google Docs UI where they're needed
   - This gives you full control and proper text anchoring

2. USE THE EXISTING FILE-LEVEL COMMENTS
   - The 51 comments contain all the information you need
   - They specify document indices for reference
   - Review them as a checklist while editing

3. EXPORT TO WORD
   - Export your Google Doc to Microsoft Word (.docx)
   - Use a Word automation tool that DOES support anchored comments
   - Re-import to Google Docs

4. GOOGLE APPS SCRIPT (Advanced)
   - Write a Google Apps Script that runs within Google Docs
   - Apps Script has access to internal comment APIs
   - More complex to set up but would work

For now, the 51 file-level comments serve as a comprehensive checklist of:
- Timeline information for all 34 chapters
- Character introduction needs for key characters
- Chapter overlap identification

I recommend using them as a reference guide while manually adding anchored
comments in the Google Docs UI where you want them.

Would you like me to:
A) Create a formatted checklist document you can work through?
B) Research the Google Apps Script approach?
C) Something else?

Press Ctrl+C to exit.
""")

sys.exit(0)
