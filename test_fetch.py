import os
import sys
from datetime import datetime, timezone
from telethon import TelegramClient
import asyncio

async def test_fetch(group_username_or_id):
    api_id = os.getenv('TELEGRAM_API_ID')
    api_hash = os.getenv('TELEGRAM_API_HASH')
    phone = os.getenv('TELEGRAM_PHONE')
    
    print("🔐 Authenticating with Telegram...")
    
    client = TelegramClient('session_name', int(api_id), api_hash)
    await client.connect()
    
    if not await client.is_user_authorized():
        print("❌ Not authorized!")
        client.disconnect()
        return
    
    print("✅ Authenticated!")
    print(f"\n📥 Fetching last 50 messages from: {group_username_or_id}\n")
    print("=" * 80)
    
    message_count = 0
    
    try:
        async for message in client.iter_messages(group_username_or_id, limit=50):
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
            time_str = message.date.strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"[{time_str}] {sender_name}:")
            print(f"  {msg_text[:100]}{'...' if len(msg_text) > 100 else ''}")
            print("-" * 80)
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print(f"\n📊 Total messages fetched: {message_count}")
    client.disconnect()
    print("✅ Done!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_fetch.py @groupname")
        sys.exit(1)
    
    asyncio.run(test_fetch(sys.argv[1]))
