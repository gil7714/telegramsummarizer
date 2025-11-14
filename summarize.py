#!/usr/bin/env python3
"""
AI-powered Telegram message summarizer.
Fetches messages from a specified day and generates an intelligent summary.
"""

import os
import sys
from datetime import datetime, timedelta, timezone
from telethon import TelegramClient
import asyncio
from openai import OpenAI

async def fetch_messages_for_summary(group_username_or_id, days_ago=0):
    """Fetch messages from Telegram for summarization."""
    api_id = os.getenv('TELEGRAM_API_ID')
    api_hash = os.getenv('TELEGRAM_API_HASH')
    phone = os.getenv('TELEGRAM_PHONE')
    
    if not api_id or not api_hash or not phone:
        print("❌ Missing Telegram credentials!")
        print("Please set: TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE")
        sys.exit(1)
    
    print("🔐 Authenticating with Telegram...")
    
    target_day = datetime.now(timezone.utc) - timedelta(days=days_ago)
    day_start = target_day.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = target_day.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    client = TelegramClient('session_name', int(api_id), api_hash)
    await client.connect()
    
    if not await client.is_user_authorized():
        print("❌ Not authorized! Please run: python authenticate.py")
        client.disconnect()
        return None, None
    
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
        client.disconnect()
        return None, None
    
    client.disconnect()
    
    day_label = "today" if (datetime.now(timezone.utc).date() == day_start.date()) else day_start.strftime('%Y-%m-%d')
    print(f"✅ Fetched {message_count} messages from {day_label}\n")
    
    return messages, day_label

def create_summary_prompt(messages, day_label):
    """Create the prompt for AI summarization."""
    messages_text = "\n".join([
        f"[{msg['time']}] {msg['sender']}: {msg['text']}"
        for msg in reversed(messages)
    ])
    
    prompt = f"""You are analyzing messages from a Telegram group called "Bulletproof Scaling" from {day_label}.

This is a high-level marketing, scaling, and business strategy group. Please provide:

1. **Executive Summary** (2-3 sentences): The most important takeaways
2. **Key Topics Discussed**: Main themes and subjects covered
3. **Notable Insights**: Specific strategies, tips, or valuable information shared
4. **Action Items**: Any recommendations, tools, or resources mentioned
5. **Important People/Mentions**: Key contributors and what they shared

Here are the messages (oldest to newest):

{messages_text}

Please be concise but thorough. Focus on actionable insights and strategic value."""
    
    return prompt

def generate_summary(messages, day_label):
    """Generate AI summary using OpenAI."""
    if not messages:
        print("❌ No messages to summarize!")
        return None
    
    print("🤖 Generating AI summary with GPT-4o...\n")
    
    client = OpenAI(
        api_key=os.getenv('AI_INTEGRATIONS_OPENAI_API_KEY'),
        base_url=os.getenv('AI_INTEGRATIONS_OPENAI_BASE_URL')
    )
    
    prompt = create_summary_prompt(messages, day_label)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert at analyzing business and marketing discussions and extracting actionable insights."},
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
    if len(sys.argv) < 2:
        print("📋 Usage: python summarize.py <group_username_or_id> [days_ago]")
        print("\nExamples:")
        print("  python summarize.py @bulletproofscale          # Summarize yesterday's messages")
        print("  python summarize.py @bulletproofscale 0        # Summarize today's messages")
        print("  python summarize.py @bulletproofscale 2        # Summarize messages from 2 days ago")
        sys.exit(1)
    
    group = sys.argv[1]
    days_ago = 1
    
    if len(sys.argv) >= 3:
        try:
            days_ago = int(sys.argv[2])
        except ValueError:
            print("❌ Error: days_ago must be a number (0 for today, 1 for yesterday, etc.)")
            sys.exit(1)
    
    messages, day_label = await fetch_messages_for_summary(group, days_ago)
    
    if messages is None:
        sys.exit(1)
    
    if len(messages) == 0:
        print(f"No messages found for {day_label}")
        sys.exit(0)
    
    summary = generate_summary(messages, day_label)
    
    if summary:
        print("=" * 80)
        print(f"📊 SUMMARY - {day_label.upper()}")
        print("=" * 80)
        print()
        print(summary)
        print()
        print("=" * 80)
        print(f"✅ Summary complete! ({len(messages)} messages analyzed)")
    else:
        print("❌ Failed to generate summary")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
