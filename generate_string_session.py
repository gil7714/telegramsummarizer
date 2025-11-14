#!/usr/bin/env python3
"""
Generate a Telegram StringSession for GitHub Actions automation.
Run this once to get your session string for GitHub Secrets.
"""

import os
import sys
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

async def generate_string_session():
    """Generate a StringSession for use in GitHub Actions."""
    api_id = os.getenv('TELEGRAM_API_ID')
    api_hash = os.getenv('TELEGRAM_API_HASH')
    phone = os.getenv('TELEGRAM_PHONE')
    
    if not api_id or not api_hash or not phone:
        print("❌ Missing Telegram credentials!")
        print("Please set: TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE")
        sys.exit(1)
    
    print("🔑 Generating Telegram StringSession for automation...")
    print()
    
    client = TelegramClient(StringSession(), int(api_id), api_hash)
    
    await client.connect()
    
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        print(f"📱 Verification code sent to {phone}")
        code = input("Enter the code you received: ")
        
        try:
            await client.sign_in(phone, code)
        except Exception as e:
            print(f"❌ Error: {e}")
            if "password" in str(e).lower():
                password = input("Enter your 2FA password: ")
                await client.sign_in(password=password)
    
    session_string = client.session.save()
    
    print()
    print("=" * 80)
    print("✅ StringSession generated successfully!")
    print("=" * 80)
    print()
    print("Copy the string below and save it as TELEGRAM_SESSION in GitHub Secrets:")
    print()
    print(session_string)
    print()
    print("=" * 80)
    print()
    print("Next steps for GitHub Actions automation:")
    print("1. Go to your GitHub repository")
    print("2. Go to Settings > Secrets and variables > Actions")
    print("3. Add these secrets:")
    print(f"   - TELEGRAM_API_ID = {api_id}")
    print(f"   - TELEGRAM_API_HASH = {api_hash}")
    print(f"   - TELEGRAM_SESSION = {session_string[:20]}...{session_string[-20:]}")
    print("   - OPENAI_API_KEY = (your OpenAI API key)")
    print()
    
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(generate_string_session())
