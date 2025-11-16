# How to Extract June Cross's Comments from Google Drive

**Document ID Found:** `1I5aglDNAqYmdMYojLqwmCLdDzQj8UlPMdAjkviKN9hk`

---

## Issue

The comment extraction script requires Google OAuth credentials to access the Google Doc via the API. Currently, no credentials file exists in the `data/` directory.

---

## Option 1: Set Up Google API Access (Recommended for Automation)

### Steps:

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/

2. **Create or Select a Project**
   - Create a new project or use an existing one

3. **Enable Required APIs**
   - Enable "Google Docs API"
   - Enable "Google Drive API"

4. **Create OAuth 2.0 Credentials**
   - Go to "Credentials" in the left sidebar
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: "Desktop app"
   - Name it something like "Memoir Comment Extractor"
   - Click "Create"

5. **Download Credentials**
   - Click the download button (⬇) next to your new OAuth client
   - This downloads a JSON file

6. **Install Credentials**
   - Rename the downloaded file to `credentials.json`
   - Move it to: `/Users/derrickburns/Documents/claude-assisted/memoir-split/data/credentials.json`

7. **Run the Extraction Script**
   ```bash
   cd /Users/derrickburns/Documents/claude-assisted/memoir-split
   python3 scripts/extract_comments.py --doc-id $MEMOIR_DOCUMENT_ID
   ```

8. **First-Time Authentication**
   - A browser window will open
   - Sign in with your Google account (the one with access to the memoir doc)
   - Grant permissions
   - The script will save a token for future use

9. **Review Results**
   - Comments will be saved to `comments.json` and `comments.md`
   - Run the matcher: `python3 scripts/match_comments_improved.py`
   - Review: `comment_matches_improved.md`

---

## Option 2: Manual Export (Quick but One-Time)

If you don't want to set up API access:

1. **Open the Google Doc**
   - Go to: https://docs.google.com/document/d/1I5aglDNAqYmdMYojLqwmCLdDzQj8UlPMdAjkviKN9hk/edit

2. **Open Comment History**
   - Click the comments icon (💬) in the top-right
   - Click "Comment history" or view all comments

3. **Export Comments Manually**
   - Copy June Cross's comments into a text document
   - Organize by chapter/section if possible
   - Save as `june_cross_feedback.md` in the `docs-analysis/` folder

4. **Share with Claude**
   - Paste the organized feedback
   - I'll analyze it and incorporate into `claude.md`

---

## Option 3: Share Key Themes (Fastest)

If you've already reviewed June Cross's comments, you can just tell me:

**What are the main themes of her feedback?**
- Writing issues she identified?
- Structural problems?
- Voice concerns?
- Specific chapters with issues?
- Patterns she noticed?

I'll incorporate her perspective into the editing guidelines and apply fixes accordingly.

---

## What Happens After Extraction

Once comments are extracted (by any method), I will:

1. **Analyze June Cross's feedback patterns**
   - Identify recurring themes
   - Note specific technical issues
   - Understand her editorial perspective

2. **Update `claude.md`**
   - Add section: "June Cross's Editorial Priorities"
   - Incorporate her concerns into editing checklist
   - Create guidelines based on her feedback

3. **Apply Fixes**
   - Address issues she identified
   - Revise chapters based on her comments
   - Maintain your authentic voice while fixing problems

4. **Track Progress**
   - Document which comments have been addressed
   - Create summary of changes made in response to her feedback

---

## Recommended Approach

**For ongoing work:** Set up API access (Option 1) so you can extract updated comments anytime

**For immediate progress:** Share key themes (Option 3) so I can start incorporating her perspective now

**For complete record:** Do both - share themes now, set up API later for complete extraction

---

## Current Status

✅ Document ID identified: `1I5aglDNAqYmdMYojLqwmCLdDzQj8UlPMdAjkviKN9hk`
✅ Data directory created: `data/`
⏸️ Waiting for: Google OAuth credentials OR manual feedback sharing

**Next step:** Choose which option works best for you and let me know the key themes of June's feedback.
