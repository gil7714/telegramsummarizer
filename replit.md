# Telegram Group Message Fetcher

## Overview
Automated system that fetches messages from Telegram groups you're in (without needing admin access or bot permissions). Uses your personal Telegram account via the Telegram Client API (MTProto).

**Current State**: Phase 3 Complete ✅ - Message fetching, AI summarization, AND automated delivery!

## Recent Changes
- **2025-11-14**: Phase 3 Complete - Automated Delivery Working!
  - ✅ Created modular delivery system (delivery/ module)
  - ✅ Telegram DM delivery - sends summaries to your Saved Messages
  - ✅ Webhook delivery - POST summaries to Make/Zapier/n8n/etc
  - ✅ Email delivery support (SMTP)
  - ✅ Support for multiple simultaneous delivery methods
  - ✅ Phase 2: AI Summarization with GPT-4o
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

**Phase 3: Automated Delivery** ✅
- **delivery/**: Modular delivery system
  - Telegram DM - sends to your Saved Messages
  - Webhook - POST to Make/Zapier/n8n/custom endpoints
  - Email - SMTP delivery support
  - Multiple delivery methods can run simultaneously
  - Simple command-line flags to control delivery

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

#### Option 1: AI Summary to Console (Default) 🖥️

**Get AI summary of yesterday's messages:**
```bash
python summarize.py @bulletproofscale
```

**Get AI summary of today's messages:**
```bash
python summarize.py @bulletproofscale 0
```

**Get AI summary from 2 days ago:**
```bash
python summarize.py @bulletproofscale 2
```

#### Option 2: Automated Delivery 📬

**Send to your Telegram DM (Saved Messages):**
```bash
python summarize.py @bulletproofscale --deliver telegram
```

**Send to a webhook (Make/Zapier/n8n):**
```bash
python summarize.py @bulletproofscale --deliver webhook --webhook-url https://your-webhook-url
```

**Send via email:**
```bash
python summarize.py @bulletproofscale --deliver email --email-to you@example.com
```

**Multiple delivery methods at once:**
```bash
python summarize.py @bulletproofscale --deliver telegram,webhook
```

#### Option 3: Raw Messages (for reference)

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

## Delivery Configuration

### Environment Variables (Optional)

For webhook delivery:
- `SUMMARY_WEBHOOK_URL` - Default webhook URL for automatic delivery

For email delivery:
- `SUMMARY_EMAIL_TO` - Default recipient email address
- `SMTP_HOST` - SMTP server hostname (e.g., smtp.gmail.com)
- `SMTP_PORT` - SMTP server port (default: 587)
- `SMTP_USER` - SMTP username/email
- `SMTP_PASS` - SMTP password or app-specific password
- `SMTP_FROM` - Sender email address (optional, defaults to SMTP_USER)

You can also pass these as command-line arguments instead of environment variables.

### Phase 4: Daily Automation ✅
**GitHub Actions** - Free, reliable, automated daily summaries
- Runs automatically every day at your chosen time
- No network restrictions (webhooks work!)
- Zero ongoing maintenance
- See `GITHUB_ACTIONS_SETUP.md` for setup instructions

**Setup Summary:**
1. Run `python generate_string_session.py` to get your session string
2. Push code to GitHub
3. Add 4 secrets to GitHub repository
4. Done! Daily summaries automatically delivered to Telegram

## Next Steps

You now have a complete automated Telegram summarizer! Optional enhancements:
- Add more Telegram groups to monitor
- Customize the schedule (morning vs evening)
- Add webhook integration to Make/Zapier
- Set up email delivery for backup copies

## Files
- `main.py` - Fetch and display raw messages
- `summarize.py` - Fetch messages and generate AI summary with delivery options (Phase 2 & 3) ✅
- `delivery/__init__.py` - Modular delivery system for Telegram DM, webhooks, email (Phase 3) ✅
- `authenticate.py` - One-time authentication script (local use)
- `generate_string_session.py` - Generate session string for GitHub Actions (Phase 4) ✅
- `.github/workflows/daily-summary.yml` - GitHub Actions automation workflow (Phase 4) ✅
- `GITHUB_ACTIONS_SETUP.md` - Complete setup guide for daily automation
- `requirements.txt` - Python dependencies for GitHub Actions
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
