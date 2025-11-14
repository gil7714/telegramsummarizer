#!/usr/bin/env python3
"""
AI-powered Telegram message summarizer.
Fetches messages from a specified day and generates an intelligent summary.
Supports delivery via Telegram DM, webhook, or email.
"""

import os
import sys
import argparse
from datetime import datetime, timedelta, timezone
from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio
from openai import OpenAI
from delivery import deliver_summary

async def fetch_messages_for_summary(group_username_or_id, days_ago=0):
    """Fetch messages from Telegram for summarization. Returns (messages, day_label, client)."""
    api_id = os.getenv('TELEGRAM_API_ID')
    api_hash = os.getenv('TELEGRAM_API_HASH')
    phone = os.getenv('TELEGRAM_PHONE')
    session_string = os.getenv('TELEGRAM_SESSION')
    
    if not api_id or not api_hash:
        print("❌ Missing Telegram credentials!")
        print("Please set: TELEGRAM_API_ID, TELEGRAM_API_HASH")
        sys.exit(1)
    
    if not session_string and not phone:
        print("❌ Missing authentication!")
        print("Please set either: TELEGRAM_SESSION (for automation) or TELEGRAM_PHONE (for local use)")
        sys.exit(1)
    
    print("🔐 Authenticating with Telegram...")
    
    target_day = datetime.now(timezone.utc) - timedelta(days=days_ago)
    day_start = target_day.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = target_day.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    if session_string:
        client = TelegramClient(StringSession(session_string), int(api_id), api_hash)
    else:
        client = TelegramClient('session_name', int(api_id), api_hash)
    
    await client.connect()
    
    if not await client.is_user_authorized():
        print("❌ Not authorized! Please run: python authenticate.py")
        await client.disconnect()
        return None, None, None
    
    print("✅ Authenticated!")
    print(f"\n📥 Fetching messages from: {group_username_or_id}")
    print(f"📅 Date range: {day_start.strftime('%Y-%m-%d %H:%M')} to {day_end.strftime('%Y-%m-%d %H:%M')}")
    
    messages = []
    message_count = 0
    
    try:
        async for message in client.iter_messages(group_username_or_id, limit=None):
            if message.date > day_end:
                continue
            if message.date < day_start:
                break
                
            message_count += 1
            
            sender_name = "Unknown"
            if message.sender:
                if hasattr(message.sender, 'first_name'):
                    sender_name = message.sender.first_name or "Unknown"
                    if hasattr(message.sender, 'last_name') and message.sender.last_name:
                        sender_name += f" {message.sender.last_name}"
                elif hasattr(message.sender, 'title'):
                    sender_name = message.sender.title
            
            msg_text = message.text or "[Media/Sticker/Other]"
            
            messages.append({
                'time': message.date.strftime('%H:%M:%S'),
                'sender': sender_name,
                'text': msg_text
            })
    
    except Exception as e:
        print(f"❌ Error fetching messages: {e}")
        await client.disconnect()
        return None, None, None
    
    day_label = "today" if (datetime.now(timezone.utc).date() == day_start.date()) else day_start.strftime('%Y-%m-%d')
    print(f"✅ Fetched {message_count} messages from {day_label}\n")
    
    return messages, day_label, client

def create_summary_prompt(messages, day_label, group_name):
    """Create the prompt for AI summarization."""
    messages_text = "\n".join([
        f"[{msg['time']}] {msg['sender']}: {msg['text']}"
        for msg in reversed(messages)
    ])
    
    prompt = f"""You are analyzing messages from a Telegram group "{group_name}" from {day_label}.

Please analyze these messages and provide:

1. **Executive Summary** (2-3 sentences): The most important takeaways from today's discussion
2. **Key Topics Discussed**: Main themes and subjects that came up
3. **Notable Insights**: Specific strategies, tips, advice, or valuable information shared
4. **Action Items**: Any recommendations, tools, resources, or next steps mentioned
5. **Important People/Mentions**: Key contributors and what they shared

Here are the messages (oldest to newest):

{messages_text}

Please be concise but thorough. Focus on actionable insights and the most valuable information shared in the conversation."""
    
    return prompt

def generate_summary(messages, day_label, group_name):
    """Generate AI summary using OpenAI."""
    if not messages:
        print("❌ No messages to summarize!")
        return None
    
    print("🤖 Generating AI summary with GPT-4o...\n")
    
    api_key = os.getenv('AI_INTEGRATIONS_OPENAI_API_KEY')
    base_url = os.getenv('AI_INTEGRATIONS_OPENAI_BASE_URL')
    
    if not api_key or not base_url:
        print("❌ Missing OpenAI integration credentials!")
        print(f"API Key present: {bool(api_key)}")
        print(f"Base URL present: {bool(base_url)}")
        print("\nPlease ensure the Replit AI Integration is properly set up.")
        return None
    
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    
    prompt = create_summary_prompt(messages, day_label, group_name)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert at analyzing group conversations and extracting the most valuable and actionable insights from discussions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        summary = response.choices[0].message.content
        return summary
    
    except Exception as e:
        print(f"❌ Error generating summary: {e}")
        return None

async def main():
    parser = argparse.ArgumentParser(
        description='AI-powered Telegram message summarizer with delivery options',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python summarize.py @bulletproofscale                    # Yesterday's summary (console)
  python summarize.py @bulletproofscale 0                  # Today's summary (console)
  python summarize.py @bulletproofscale --deliver telegram # Send to your Telegram DM
  python summarize.py @bulletproofscale --deliver webhook  # POST to webhook
  python summarize.py @bulletproofscale --deliver telegram,webhook  # Multiple delivery methods
  
Environment Variables:
  SUMMARY_WEBHOOK_URL   - Default webhook URL
  SUMMARY_EMAIL_TO      - Default email recipient
  SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS - Email configuration
        """
    )
    
    parser.add_argument('group', help='Telegram group username (e.g., @bulletproofscale) or ID')
    parser.add_argument('days_ago', nargs='?', type=int, default=1,
                       help='Days ago to summarize (0=today, 1=yesterday, default: 1)')
    parser.add_argument('--deliver', '-d', type=str,
                       help='Delivery methods (comma-separated): telegram, webhook, email')
    parser.add_argument('--webhook-url', type=str,
                       help='Webhook URL (overrides SUMMARY_WEBHOOK_URL)')
    parser.add_argument('--email-to', type=str,
                       help='Email recipient (overrides SUMMARY_EMAIL_TO)')
    
    args = parser.parse_args()
    
    messages, day_label, client = await fetch_messages_for_summary(args.group, args.days_ago)
    
    if messages is None:
        if client:
            await client.disconnect()
        sys.exit(1)
    
    if len(messages) == 0:
        print(f"No messages found for {day_label}")
        if client:
            await client.disconnect()
        sys.exit(0)
    
    summary = generate_summary(messages, day_label, args.group)
    
    if not summary:
        print("❌ Failed to generate summary")
        if client:
            await client.disconnect()
        sys.exit(1)
    
    print("=" * 80)
    print(f"📊 SUMMARY - {day_label.upper()}")
    print("=" * 80)
    print()
    print(summary)
    print()
    print("=" * 80)
    print(f"✅ Summary complete! ({len(messages)} messages analyzed)")
    
    if args.deliver:
        print()
        delivery_methods = [m.strip() for m in args.deliver.split(',')]
        results = await deliver_summary(
            summary=summary,
            group_name=args.group,
            day_label=day_label,
            delivery_methods=delivery_methods,
            telegram_client=client,
            webhook_url=args.webhook_url,
            email_to=args.email_to
        )
        
        success_count = sum(1 for success in results.values() if success)
        total_count = len(results)
        print(f"\n📬 Delivery: {success_count}/{total_count} successful")
    
    if client:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
