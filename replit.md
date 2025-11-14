# Telegram Group Message Fetcher

## Overview
Automated system that fetches messages from Telegram groups you're in (without needing admin access or bot permissions). Uses your personal Telegram account via the Telegram Client API (MTProto).

**Current State**: Phase 2 Complete ✅ - Fully functional message fetching AND AI-powered summarization!

## Recent Changes
- **2025-11-14**: Phase 2 Complete - AI Summarization Working!
  - ✅ Integrated OpenAI GPT-4o via Replit AI Integrations (no API key needed)
  - ✅ Created summarize.py for intelligent message summarization
  - ✅ Successfully tested with 448 messages - generates excellent summaries
  - ✅ Extracts key topics, insights, action items, and important contributors
  - ✅ Phase 1: Message fetching fully functional
  - ✅ Telegram authentication persisted via session file

## Project Architecture

### Current Implementation ✅

**Phase 1: Message Fetching**
- **main.py**: Raw message display
  - Authenticates using your Telegram account (session persisted)
  - Fetches ALL messages from any specified day (no limits)
  - Displays messages with timestamps and sender names
  - Handles text messages and indicates media/stickers
  - Flexible day selection: today, yesterday, or X days ago

**Phase 2: AI Summarization** ✅
- **summarize.py**: Intelligent AI-powered summaries
  - Fetches messages from specified day
  - Sends to GPT-4o for analysis
  - Generates executive summary, key topics, notable insights
  - Extracts action items and highlights important contributors
  - Perfect for daily digests of active groups

### Dependencies
- Python 3.11
- Telethon 1.42.0 (Telegram MTProto client library)
- OpenAI 2.8.0 (AI summarization via Replit AI Integrations)

### How It Works
1. Uses your personal Telegram API credentials to authenticate
2. Creates a persistent session (saved locally in `session_name.session`)
3. Connects to Telegram as your account (not a bot)
4. Retrieves all messages from a specified group for yesterday
5. Prints them to console with timestamps

## How to Use

### ✅ Already Set Up
- Telegram app credentials configured
- Authentication completed (session file created)
- Tested with @bulletproofscale group

### Running the Scripts

Open the **Shell** tab in Replit and use these commands:

#### Option 1: AI Summary (Recommended) 🤖

**Get AI summary of today's messages:**
```bash
python summarize.py @bulletproofscale 0
```

**Get AI summary of yesterday's messages (default):**
```bash
python summarize.py @bulletproofscale
```

**Get AI summary from 2 days ago:**
```bash
python summarize.py @bulletproofscale 2
```

#### Option 2: Raw Messages (for reference)

**View today's raw messages:**
```bash
python main.py @bulletproofscale 0
```

**View yesterday's raw messages:**
```bash
python main.py @bulletproofscale 1
```

**Any other group:**
```bash
python summarize.py @yourgroupname 0
```

### Finding Group Username or ID
1. Forward a message from the group to @userinfobot on Telegram
2. The bot will show you the chat ID
3. Use that ID (including the minus sign if present)

### Authentication Status
- ✅ Already authenticated - session file exists
- You won't need to login again unless the session expires
- If session expires, the script will tell you and you'll need to authenticate again

## Next Phases

### Phase 3: Delivery Options (Not Yet Implemented)
- Send summary to your Telegram DMs
- Post to Make/Zapier webhook
- Email delivery
- Slack integration
- Discord integration

### Phase 4: Automation (Not Yet Implemented)
- Set up daily scheduled runs
- Options: GitHub Actions, Replit cron, or cloud VPS
- Fully automated daily summaries

## Files
- `main.py` - Fetch and display raw messages
- `summarize.py` - Fetch messages and generate AI summary (Phase 2) ✅
- `authenticate.py` - One-time authentication script
- `pyproject.toml` - Python project configuration
- `uv.lock` - Dependency lock file
- `.gitignore` - Excludes session files and Python artifacts
- `session_name.session` - Telegram session (gitignored)

## Security Notes
- Session files contain authentication tokens - they are gitignored
- API credentials are stored in Replit Secrets (environment variables)
- Never commit or share your session files, API credentials, or phone number

## Troubleshooting

### "Missing credentials" error
Make sure these secrets are set in Replit:
- TELEGRAM_API_ID
- TELEGRAM_API_HASH
- TELEGRAM_PHONE

### "TELEGRAM_GROUP not set" error
Either:
- Pass the group as a command-line argument: `python main.py @groupname`
- Or add TELEGRAM_GROUP to Replit Secrets

### "FloodWaitError"
Telegram has rate limits. Wait a few minutes and try again.

### "ChatAdminRequiredError"
This happens if the group is private and restricts non-admin message access. Try a different group.
