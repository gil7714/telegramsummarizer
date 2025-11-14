import os
import sys
from datetime import datetime, timedelta, timezone
from telethon import TelegramClient
from telethon.tl.types import Channel, Chat
import asyncio

async def fetch_yesterday_messages(group_username_or_id):
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
    
    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    yesterday_start = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_end = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    client = TelegramClient('session_name', int(api_id), api_hash)
    await client.connect()
    
    if not await client.is_user_authorized():
        print("❌ Not authorized! You need to authenticate first.")
        print("This requires interactive authentication (entering a code from Telegram).")
        print("Please run: python authenticate.py")
        client.disconnect()
        return
    
    print("✅ Authenticated successfully!")
    
    await fetch_and_display_messages(client, group_username_or_id, yesterday_start, yesterday_end)
    
    client.disconnect()

async def fetch_and_display_messages(client, group_username_or_id, yesterday_start, yesterday_end):
    print(f"\n📥 Fetching messages from: {group_username_or_id}")
    print(f"📅 Date range: {yesterday_start.strftime('%Y-%m-%d %H:%M')} to {yesterday_end.strftime('%Y-%m-%d %H:%M')}")
    
    messages = []
    message_count = 0
    
    try:
        async for message in client.iter_messages(
            group_username_or_id,
            offset_date=yesterday_end,
            reverse=True,
            limit=None
        ):
            if message.date < yesterday_start:
                break
            if message.date > yesterday_end:
                continue
                
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
    
    print(f"\n📊 Found {message_count} messages from yesterday\n")
    print("=" * 80)
    
    for msg in messages:
        time_str = msg['date'].strftime('%H:%M:%S')
        print(f"[{time_str}] {msg['sender']}:")
        print(f"  {msg['text']}")
        print("-" * 80)
    
    print("\n✅ Done!")

def main():
    group = None
    
    if len(sys.argv) >= 2:
        group = sys.argv[1]
    elif os.getenv('TELEGRAM_GROUP'):
        group = os.getenv('TELEGRAM_GROUP')
    else:
        print("📋 Usage: python main.py <group_username_or_id>")
        print("\nExamples:")
        print("  python main.py @publicgroupname")
        print("  python main.py -1001234567890")
        print("\nOr set TELEGRAM_GROUP environment variable:")
        print("  export TELEGRAM_GROUP=@publicgroupname")
        print("  python main.py")
        print("\nTo find a group ID:")
        print("  1. Forward a message from the group to @userinfobot on Telegram")
        print("  2. It will show you the chat ID")
        sys.exit(1)
    
    asyncio.run(fetch_yesterday_messages(group))

if __name__ == "__main__":
    main()
