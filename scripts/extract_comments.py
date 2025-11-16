#!/usr/bin/env python3
"""
Extract comments from a Google Doc and associate them with their anchor text.

This script uses the Google Docs API to fetch a document with its comments,
then exports them in a structured format that can be matched to the split chapters.
"""

import os
import sys
import json
import pickle
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/documents.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]

class CommentExtractor:
    def __init__(self, document_id):
        """Initialize the extractor with a Google Doc ID."""
        self.document_id = document_id
        self.creds = None
        self.docs_service = None
        self.drive_service = None

    def authenticate(self):
        """Authenticate with Google API."""
        print("Authenticating with Google...")

        # Token file stores the user's access and refresh tokens
        token_path = 'data/token.pickle'
        credentials_path = 'data/credentials.json'

        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                self.creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                # Check for environment variables first
                client_id = os.environ.get('MEMOIR_CLIENT_ID')
                client_secret = os.environ.get('MEMOIR_CLIENT_SECRET')

                if client_id and client_secret:
                    # Create credentials from environment variables
                    print("Using credentials from environment variables (MEMOIR_CLIENT_ID and MEMOIR_CLIENT_SECRET)")
                    client_config = {
                        "installed": {
                            "client_id": client_id,
                            "client_secret": client_secret,
                            "redirect_uris": ["http://localhost"],
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token"
                        }
                    }
                    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
                    self.creds = flow.run_local_server(port=0)
                elif os.path.exists(credentials_path):
                    # Fall back to credentials.json file
                    print(f"Using credentials from {credentials_path}")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        credentials_path, SCOPES)
                    self.creds = flow.run_local_server(port=0)
                else:
                    print(f"\nERROR: No credentials found!")
                    print("\nTo use this script, you need EITHER:")
                    print("  Option A: Set environment variables:")
                    print("    export MEMOIR_CLIENT_ID='your_client_id'")
                    print("    export MEMOIR_CLIENT_SECRET='your_client_secret'")
                    print("\n  OR Option B: Use credentials.json file:")
                    print("    1. Go to https://console.cloud.google.com/")
                    print("    2. Create a new project (or select existing)")
                    print("    3. Enable Google Docs API and Google Drive API")
                    print("    4. Create OAuth 2.0 credentials (Desktop app)")
                    print("    5. Download the credentials as 'credentials.json'")
                    print("    6. Place credentials.json in the data/ directory")
                    sys.exit(1)

            # Save the credentials for the next run
            with open(token_path, 'wb') as token:
                pickle.dump(self.creds, token)

        # Build the services
        self.docs_service = build('docs', 'v1', credentials=self.creds)
        self.drive_service = build('drive', 'v3', credentials=self.creds)

        print("✓ Authentication successful")

    def fetch_document(self):
        """Fetch the document content from Google Docs."""
        print(f"\nFetching document {self.document_id}...")

        try:
            # Get the document
            doc = self.docs_service.documents().get(documentId=self.document_id).execute()
            print(f"✓ Document retrieved: {doc.get('title')}")
            return doc
        except HttpError as error:
            print(f'ERROR: {error}')
            sys.exit(1)

    def fetch_comments(self):
        """Fetch comments from the document via Drive API."""
        print("\nFetching comments...")

        try:
            all_comments = []
            page_token = None
            page_num = 1

            # Paginate through all comments
            while True:
                print(f"Fetching page {page_num}...", end='\r')

                # Get comments page
                request_params = {
                    'fileId': self.document_id,
                    'fields': 'comments(id,content,quotedFileContent,anchor,createdTime,author,resolved),nextPageToken',
                    'includeDeleted': False,
                    'pageSize': 100  # Max allowed by API
                }

                if page_token:
                    request_params['pageToken'] = page_token

                results = self.drive_service.comments().list(**request_params).execute()

                # Add comments from this page
                page_comments = results.get('comments', [])
                all_comments.extend(page_comments)

                # Check if there are more pages
                page_token = results.get('nextPageToken')
                if not page_token:
                    break

                page_num += 1

            print()  # New line after progress
            print(f"✓ Found {len(all_comments)} comments across {page_num} page(s)")
            return all_comments

        except HttpError as error:
            print(f'ERROR: {error}')
            sys.exit(1)

    def extract_text_from_element(self, element):
        """Recursively extract text from a document element."""
        text = ''
        if 'textRun' in element:
            text += element['textRun'].get('content', '')
        elif 'paragraph' in element:
            for elem in element['paragraph'].get('elements', []):
                text += self.extract_text_from_element(elem)
        return text

    def get_text_at_index(self, doc, start_index, end_index):
        """Extract text from document at given indices."""
        text = ''
        current_index = 1  # Google Docs uses 1-based indexing

        for element in doc.get('body', {}).get('content', []):
            if 'paragraph' in element:
                para = element['paragraph']
                for elem in para.get('elements', []):
                    if 'textRun' in elem:
                        content = elem['textRun'].get('content', '')
                        elem_start = elem.get('startIndex', current_index)
                        elem_end = elem.get('endIndex', current_index + len(content))

                        # Check if this element overlaps with our range
                        if elem_end > start_index and elem_start < end_index:
                            # Calculate the overlap
                            overlap_start = max(0, start_index - elem_start)
                            overlap_end = min(len(content), end_index - elem_start)
                            text += content[overlap_start:overlap_end]

                        current_index = elem_end
            elif 'table' in element:
                # Handle tables
                current_index = element.get('endIndex', current_index)

        return text

    def export_comments(self, doc, comments, output_file='comments.json'):
        """Export comments with their context to JSON."""
        print(f"\nExporting comments to {output_file}...")

        export_data = {
            'document_title': doc.get('title'),
            'document_id': self.document_id,
            'total_comments': len(comments),
            'comments': []
        }

        for comment in comments:
            comment_data = {
                'id': comment.get('id'),
                'content': comment.get('content'),
                'author': comment.get('author', {}).get('displayName', 'Unknown'),
                'created': comment.get('createdTime'),
                'resolved': comment.get('resolved', False),
                'anchor_text': '',
                'quoted_text': comment.get('quotedFileContent', {}).get('value', '')
            }

            # Try to get the anchor position
            if 'anchor' in comment:
                anchor = comment['anchor']
                # The anchor format varies, try to extract the range
                # This is a simplified version - actual anchor parsing can be complex
                comment_data['anchor'] = anchor

            export_data['comments'].append(comment_data)

        # Save to JSON
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)

        print(f"✓ Exported {len(comments)} comments")

        # Also create a readable markdown version
        md_file = output_file.replace('.json', '.md')
        with open(md_file, 'w') as f:
            f.write(f"# Comments from: {doc.get('title')}\n\n")
            f.write(f"Total comments: {len(comments)}\n\n")
            f.write("---\n\n")

            for i, comment in enumerate(export_data['comments'], 1):
                f.write(f"## Comment {i}\n\n")
                f.write(f"**Author:** {comment['author']}\n\n")
                f.write(f"**Date:** {comment['created']}\n\n")
                f.write(f"**Status:** {'Resolved' if comment['resolved'] else 'Open'}\n\n")

                if comment['quoted_text']:
                    f.write(f"**Quoted text:**\n> {comment['quoted_text']}\n\n")

                f.write(f"**Comment:**\n{comment['content']}\n\n")
                f.write("---\n\n")

        print(f"✓ Created readable version: {md_file}")

        return export_data


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Extract comments from a Google Doc',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract comments from a Google Doc
  %(prog)s --doc-id 1abc123xyz456

  # Extract and save to custom file
  %(prog)s --doc-id 1abc123xyz456 --output my_comments.json

Setup Instructions:
  1. Go to https://console.cloud.google.com/
  2. Create a new project or select existing
  3. Enable Google Docs API and Google Drive API
  4. Create OAuth 2.0 credentials (Desktop app)
  5. Download credentials as 'credentials.json'
  6. Place credentials.json in this directory
  7. Run this script - it will open a browser for authentication

Document ID:
  You can find the document ID in the Google Doc URL:
  https://docs.google.com/document/d/1I5aglDNAqYmdMYojLqwmCLdDzQj8UlPMdAjkviKN9hk/edit
        """
    )

    parser.add_argument('--doc-id', required=True,
                        help='Google Doc ID (from the document URL)')
    parser.add_argument('-o', '--output', default='data/comments.json',
                        help='Output JSON file (default: data/comments.json)')

    args = parser.parse_args()

    # Create extractor
    extractor = CommentExtractor(args.doc_id)

    # Authenticate
    extractor.authenticate()

    # Fetch document and comments
    doc = extractor.fetch_document()
    comments = extractor.fetch_comments()

    # Export
    extractor.export_comments(doc, comments, args.output)

    print("\n✓ Done!")
    print(f"\nNext steps:")
    print(f"1. Review the comments in {args.output.replace('.json', '.md')}")
    print(f"2. Use the JSON file to match comments to your split chapters")


if __name__ == '__main__':
    main()
