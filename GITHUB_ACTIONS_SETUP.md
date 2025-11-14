# GitHub Actions Automation Setup

This guide will help you set up daily automated summaries delivered to your Telegram.

## Prerequisites

- A GitHub account
- Your Telegram summaries working locally (you've already done this ✅)
- An OpenAI API key (get one at https://platform.openai.com/api-keys)

## Step 1: Generate Your Telegram Session String

Run this command in the Replit Shell:

```bash
python generate_string_session.py
```

This will:
1. Authenticate with Telegram (you may need to enter a code)
2. Generate a session string
3. Display the string to copy

**Copy the session string** - you'll need it for GitHub Secrets.

## Step 2: Push Your Code to GitHub

If you haven't already:

```bash
git init
git add .
git commit -m "Initial commit - Telegram summarizer"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

## Step 3: Add GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** > **Secrets and variables** > **Actions**
3. Click **New repository secret** and add these 4 secrets:

| Secret Name | Value | Where to Find |
|------------|-------|---------------|
| `TELEGRAM_API_ID` | Your API ID | Replit Secrets (already set) |
| `TELEGRAM_API_HASH` | Your API hash | Replit Secrets (already set) |
| `TELEGRAM_SESSION` | Session string from Step 1 | Output from generate_string_session.py |
| `OPENAI_API_KEY` | Your OpenAI API key | https://platform.openai.com/api-keys |

## Step 4: Configure the Schedule

Edit `.github/workflows/daily-summary.yml`:

```yaml
on:
  schedule:
    # Runs daily at 9:00 AM UTC - adjust to your timezone
    - cron: '0 9 * * *'
```

**Time zone converter:**
- 9:00 AM EST = `'0 14 * * *'`
- 9:00 AM PST = `'0 17 * * *'`
- 6:00 AM UTC = `'0 6 * * *'`

Also update the group name in line 39:
```yaml
python summarize.py @bulletproofscale 1 --deliver telegram
```

Change `@bulletproofscale` to your group name.

## Step 5: Test It

You can manually trigger the workflow to test it:

1. Go to your GitHub repository
2. Click **Actions** tab
3. Click **Daily Telegram Summary** workflow
4. Click **Run workflow** > **Run workflow**
5. Wait a minute and check your Telegram Saved Messages!

## Step 6: Enable Automation

That's it! GitHub Actions will now run daily at your scheduled time and send summaries to your Telegram.

## Optional: Add Webhook or Email Delivery

To also send to webhooks or email, edit the workflow:

```yaml
run: |
  python summarize.py @bulletproofscale 1 --deliver telegram,webhook \
    --webhook-url https://your-webhook-url
```

Or add `SUMMARY_WEBHOOK_URL` to GitHub Secrets and use:
```yaml
env:
  SUMMARY_WEBHOOK_URL: ${{ secrets.SUMMARY_WEBHOOK_URL }}
run: |
  python summarize.py @bulletproofscale 1 --deliver telegram,webhook
```

## Troubleshooting

### Workflow fails with "Not authorized"
- Regenerate your session string with `python generate_string_session.py`
- Update the `TELEGRAM_SESSION` secret in GitHub

### No summary received
- Check the Actions tab for error logs
- Verify all 4 secrets are set correctly
- Make sure the group name is correct

### OpenAI errors
- Verify your `OPENAI_API_KEY` is valid and has credits
- Check https://platform.openai.com/usage

## Cost Estimate

- **GitHub Actions**: Free (2,000 minutes/month for free tier)
- **OpenAI API**: ~$0.01-0.05 per summary (depending on message count)
- **Telegram**: Free

**Monthly cost**: $0.30-1.50 for daily summaries (OpenAI only)
