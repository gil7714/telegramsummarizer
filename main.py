import os
import sys
from datetime import datetime, timedelta, timezone
from telethon import TelegramClient
from telethon.tl.types import Channel, Chat
import asyncio

async def fetch_messages(group_username_or_id, days_ago=0):
    api_id = os.getenv('TELEGRAM_API_ID')
    api_hash = os.getenv('TELEGRAM_API_HASH')
    phone = os.getenv('TELEGRAM_PHONE')
    
    if not api_id or not api_hash or not phone:
        print("❌ Missing credentials!")
        print("Please set the following environment variables:")
        print("  - TELEGRAM_API_ID")
        print("  - TELEGRAM_API_HASH")
        print("  - TELEGRAM_PHONE")
        sys.exit(1)
    
    print("🔐 Authenticating with Telegram...")
    
    target_day = datetime.now(timezone.utc) - timedelta(days=days_ago)
    day_start = target_day.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = target_day.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    client = TelegramClient('session_name', int(api_id), api_hash)
    await client.connect()
    
    if not await client.is_user_authorized():
        print("❌ Not authorized! You need to authenticate first.")
        print("This requires interactive authentication (entering a code from Telegram).")
        print("Please run: python authenticate.py")
        client.disconnect()
        return
    
    print("✅ Authenticated successfully!")
    
    await fetch_and_display_messages(client, group_username_or_id, day_start, day_end)
    
    client.disconnect()

async def fetch_and_display_messages(client, group_username_or_id, day_start, day_end):
    print(f"\n📥 Fetching messages from: {group_username_or_id}")
    print(f"📅 Date range: {day_start.strftime('%Y-%m-%d %H:%M')} to {day_end.strftime('%Y-%m-%d %H:%M')}")
    
    messages = []
    message_count = 0
    
    try:
        async for message in client.iter_messages(
            group_username_or_id,
            limit=None
        ):
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
                'id': message.id,
                'date': message.date,
                'sender': sender_name,
                'text': msg_text
            })
    
    except Exception as e:
        print(f"❌ Error fetching messages: {e}")
        return
    
    day_label = "today" if (datetime.now(timezone.utc).date() == day_start.date()) else day_start.strftime('%Y-%m-%d')
    print(f"\n📊 Found {message_count} messages from {day_label}\n")
    print("=" * 80)
    
    for msg in messages:
        time_str = msg['date'].strftime('%H:%M:%S')
        print(f"[{time_str}] {msg['sender']}:")
        print(f"  {msg['text']}")
        print("-" * 80)
    
    print("\n✅ Done!")

def main():
    group = None
    days_ago = 1
    
    if len(sys.argv) >= 2:
        group = sys.argv[1]
    elif os.getenv('TELEGRAM_GROUP'):
        group = os.getenv('TELEGRAM_GROUP')
    else:
        print("📋 Usage: python main.py <group_username_or_id> [days_ago]")
        print("\nExamples:")
        print("  python main.py @bulletproofscale          # Yesterday's messages")
        print("  python main.py @bulletproofscale 0        # Today's messages")
        print("  python main.py @bulletproofscale 2        # Messages from 2 days ago")
        print("\nOr set TELEGRAM_GROUP environment variable:")
        print("  export TELEGRAM_GROUP=@publicgroupname")
        print("  python main.py")
        print("\nTo find a group ID:")
        print("  1. Forward a message from the group to @userinfobot on Telegram")
        print("  2. It will show you the chat ID")
        sys.exit(1)
    
    if len(sys.argv) >= 3:
        try:
            days_ago = int(sys.argv[2])
        except ValueError:
            print("❌ Error: days_ago must be a number (0 for today, 1 for yesterday, etc.)")
            sys.exit(1)
    
    asyncio.run(fetch_messages(group, days_ago))

if __name__ == "__main__":
    main()
