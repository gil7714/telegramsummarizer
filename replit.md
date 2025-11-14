# Telegram Group Message Fetcher

## Overview
Automated system that fetches messages from Telegram groups you're in (without needing admin access or bot permissions) and provides daily summaries. Uses your personal Telegram account via the Telegram Client API (MTProto).

**Current State**: Phase 1 - Basic message fetching and display functionality implemented.

## Recent Changes
- **2024-11-14**: Initial setup complete
  - Installed Telethon library for Telegram API access
  - Created main.py script with message fetching functionality
  - Added support for both command-line arguments and environment variables
  - Configured Telegram API credentials (TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE)
  - Added session file exclusions to .gitignore

## Project Architecture

### Current Implementation (Phase 1)
- **main.py**: Core script that:
  - Authenticates using your Telegram account
  - Fetches all messages from yesterday (00:00 to 23:59)
  - Displays messages with timestamps and sender names
  - Handles both text messages and media indicators

### Dependencies
- Python 3.11
- Telethon 1.42.0 (Telegram MTProto client library)

### How It Works
1. Uses your personal Telegram API credentials to authenticate
2. Creates a persistent session (saved locally in `session_name.session`)
3. Connects to Telegram as your account (not a bot)
4. Retrieves all messages from a specified group for yesterday
5. Prints them to console with timestamps

## How to Use

### First Time Setup
You've already completed this:
- Created Telegram app at https://my.telegram.org/apps
- Obtained API_ID and API_HASH
- Added credentials to Replit Secrets

### Running the Script

**Option 1: Using command-line argument**
```bash
python main.py @yourgroupname
```
or
```bash
python main.py -1001234567890
```

**Option 2: Using environment variable**
1. Add a new secret in Replit called `TELEGRAM_GROUP` with your group username or ID
2. Run: `python main.py`

### Finding Group Username or ID
1. Forward a message from the group to @userinfobot on Telegram
2. The bot will show you the chat ID
3. Use that ID (including the minus sign if present)

### First Run Authentication
- The first time you run the script, Telegram will send a login code to your phone
- Enter the code when prompted
- After first authentication, a session file is created and you won't need to login again

## Next Phases

### Phase 2: AI Summarization (Not Yet Implemented)
- Integrate with GPT-4 or another AI model
- Generate intelligent summaries of daily messages
- Extract key points, action items, and important discussions

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
- `main.py` - Main script for fetching messages
- `pyproject.toml` - Python project configuration
- `uv.lock` - Dependency lock file
- `.gitignore` - Excludes session files and Python artifacts

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
