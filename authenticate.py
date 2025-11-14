import os
import sys
from telethon import TelegramClient
import asyncio

async def authenticate():
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
    
    print("🔐 Starting Telegram authentication...")
    print(f"📱 Phone: {phone}")
    print("\n⚠️  IMPORTANT:")
    print("  1. Telegram will send a login code to your phone")
    print("  2. You'll need to enter it when prompted")
    print("  3. This only needs to be done once\n")
    
    client = TelegramClient('session_name', int(api_id), api_hash)
    
    await client.start(
        phone=phone,
        code_callback=lambda: input('Enter the code you received: '),
        password_callback=lambda: input('Enter your 2FA password (if enabled): ')
    )
    
    print("\n✅ Authentication successful!")
    print("✅ Session file created!")
    print("\nYou can now run: python main.py @bulletproofscale")
    
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(authenticate())
