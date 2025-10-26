# Google API Setup for Comment Extraction

This guide walks you through setting up Google API access to extract comments from your Google Doc.

## Prerequisites

- Python 3.7+ installed
- Google account with access to the document
- Google API libraries installed (already done via requirements.txt)

## Step-by-Step Setup

### 1. Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" (top left)
3. Click "NEW PROJECT"
4. Enter project name: `memoir-comments-extractor`
5. Click "CREATE"
6. Wait for the project to be created, then select it

### 2. Enable Required APIs

1. In the Google Cloud Console, go to **APIs & Services > Library**
2. Search for "Google Docs API"
   - Click on it
   - Click "ENABLE"
3. Go back to the library
4. Search for "Google Drive API"
   - Click on it
   - Click "ENABLE"

### 3. Create OAuth 2.0 Credentials

1. Go to **APIs & Services > Credentials**
2. Click "CREATE CREDENTIALS" at the top
3. Select "OAuth client ID"
4. If prompted to configure consent screen:
   - Click "CONFIGURE CONSENT SCREEN"
   - Select "External" (unless you have a Google Workspace)
   - Click "CREATE"
   - Fill in required fields:
     - App name: `Memoir Comment Extractor`
     - User support email: (your email)
     - Developer contact email: (your email)
   - Click "SAVE AND CONTINUE"
   - On Scopes page, click "SAVE AND CONTINUE" (no need to add scopes)
   - On Test users page, click "ADD USERS" and add your email
   - Click "SAVE AND CONTINUE"
   - Click "BACK TO DASHBOARD"

5. Back in Credentials page, click "CREATE CREDENTIALS" again
6. Select "OAuth client ID"
7. Application type: **Desktop app**
8. Name: `Desktop client 1` (or whatever you prefer)
9. Click "CREATE"
10. Click "DOWNLOAD JSON" on the popup
11. **Rename the downloaded file to `credentials.json`**
12. **Move `credentials.json` to your memoir-split directory**

### 4. Get Your Document ID

1. Open your Google Doc in a browser
2. Look at the URL - it will look like:
   ```
   https://docs.google.com/document/d/1a2b3c4d5e6f7g8h9i0j/edit
   ```
3. The document ID is the long string between `/d/` and `/edit`:
   ```
   1a2b3c4d5e6f7g8h9i0j
   ```
4. Copy this ID - you'll need it to run the extraction script

## Running the Comment Extraction

Once you have `credentials.json` in place:

```bash
# Make the script executable
chmod +x extract_comments.py

# Run it with your document ID
python3 extract_comments.py --doc-id YOUR_DOCUMENT_ID_HERE
```

### First Run

The first time you run the script:
1. A browser window will open
2. Sign in to your Google account (the one with access to the document)
3. You'll see a warning "Google hasn't verified this app"
   - Click "Advanced"
   - Click "Go to Memoir Comment Extractor (unsafe)"
   - This is safe - it's your own app
4. Click "Allow" to grant access to read documents
5. The browser will show "The authentication flow has completed"
6. Close the browser and return to the terminal

The script will save your authentication in `token.pickle`, so you won't need to authenticate again.

## Output Files

The script creates:
- `comments.json` - Structured data with all comments
- `comments.md` - Human-readable markdown version

## Troubleshooting

### "credentials.json not found"
Make sure you:
- Downloaded the credentials file from Google Cloud Console
- Renamed it to exactly `credentials.json`
- Placed it in the memoir-split directory

### "Access denied" or "Permission denied"
Make sure:
- You're signed in with the Google account that owns/has access to the document
- You added your email as a test user in the OAuth consent screen
- The Google Docs API and Google Drive API are enabled

### "Invalid document ID"
Double-check:
- You copied the entire ID from the URL
- It's the part between `/d/` and `/edit`
- No extra spaces or characters

## Security Notes

**Keep these files private:**
- `credentials.json` - Your OAuth client credentials
- `token.pickle` - Your access tokens

**Add to .gitignore:**
```
credentials.json
token.pickle
```

These files give access to your Google account - don't commit them to version control or share them publicly.

## Next Steps

After extracting comments, use `match_comments.py` (coming next) to associate comments with specific chapters in your split files.
