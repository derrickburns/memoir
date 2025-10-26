#!/usr/bin/env python3
"""
Delete all comments from Google Doc.

This script removes all comments that were added to the memoir document.

Usage:
    python3 scripts/delete_all_comments.py --doc-id YOUR_DOC_ID --dry-run
    python3 scripts/delete_all_comments.py --doc-id YOUR_DOC_ID
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

# Need Drive scope to access comments
SCOPES = [
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


def main():
    parser = argparse.ArgumentParser(
        description='Delete all comments from Google Doc',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--doc-id',
                       default='1I5aglDNAqYmdMYojLqwmCLdDzQj8UlPMdAjkviKN9hk',
                       help='Google Doc ID (default: memoir doc)')
    parser.add_argument('--dry-run',
                       action='store_true',
                       help='Show what would be done without actually doing it')

    args = parser.parse_args()

    print("=" * 80)
    print("DELETE ALL COMMENTS FROM GOOGLE DOC")
    print("=" * 80)
    print()

    if args.dry_run:
        print("*** DRY RUN MODE - No changes will be made ***")
        print()

    # Get credentials
    print("Authenticating with Google...")
    creds = get_credentials()

    # Build Drive service
    drive_service = build('drive', 'v3', credentials=creds)

    # Get all comments (handle pagination)
    print(f"Fetching comments from document {args.doc_id}...")
    try:
        comments = []
        page_token = None

        while True:
            comments_response = drive_service.comments().list(
                fileId=args.doc_id,
                fields='comments(id,content,createdTime,author),nextPageToken',
                pageToken=page_token
            ).execute()

            comments.extend(comments_response.get('comments', []))
            page_token = comments_response.get('nextPageToken')

            if not page_token:
                break
        print(f"✓ Found {len(comments)} comments")
        print()

        if len(comments) == 0:
            print("No comments to delete.")
            return

        # Show comments
        print("Comments to delete:")
        for i, comment in enumerate(comments, 1):
            author = comment.get('author', {}).get('displayName', 'Unknown')
            content = comment.get('content', '')[:60]
            created = comment.get('createdTime', '')
            print(f"{i}. [{author}] {content}...")

        print()

        if args.dry_run:
            print("This was a dry run - no comments were deleted")
            return

        # Delete each comment
        deleted = 0
        failed = 0

        print("Deleting comments...")
        for comment in comments:
            comment_id = comment['id']
            try:
                drive_service.comments().delete(
                    fileId=args.doc_id,
                    commentId=comment_id
                ).execute()
                deleted += 1
                print(f"✓ Deleted comment {deleted}/{len(comments)}")
            except HttpError as error:
                print(f"✗ Error deleting comment {comment_id}: {error}")
                failed += 1

        print()
        print("=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Comments deleted: {deleted}")
        print(f"Failed: {failed}")
        print(f"Total: {len(comments)}")

    except HttpError as error:
        print(f'Error fetching comments: {error}')
        sys.exit(1)


if __name__ == '__main__':
    main()
