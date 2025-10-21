import asyncio
import requests
from dotenv import load_dotenv
load_dotenv()
import os
from telegram import Bot

async def test_producthunt():
    print('Testing Product Hunt API...')
    query = '''
    query TodayPosts($perPage: Int!) {
      posts(order: RANKING, postedAfter: null, postedBefore: null, first: $perPage) {
        edges {
          node {
            name
            tagline
            url
            votesCount
          }
        }
      }
    }
    '''
    headers = {"Authorization": f"Bearer {os.getenv('PH_TOKEN')}", "Content-Type": "application/json"}
    try:
        res = requests.post(
            "https://api.producthunt.com/v2/api/graphql",
            json={"query": query, "variables": {"perPage": 3}},
            headers=headers,
            timeout=30
        )
        data = res.json().get("data", {}).get("posts", {}).get("edges", [])
        if data:
            print(f"✅ Product Hunt API working! Found {len(data)} products")
            for i, p in enumerate(data[:2]):
                print(f"  {i+1}. {p['node']['name']} - {p['node']['tagline']}")
        else:
            print("❌ No data from Product Hunt API")
    except Exception as e:
        print(f"❌ Product Hunt error: {e}")

async def test_telegram():
    print('Testing Telegram...')
    bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
    try:
        await bot.send_message(chat_id=os.getenv('TELEGRAM_CHAT_ID'), text="🤖 Bot test successful!")
        print("✅ Telegram working!")
    except Exception as e:
        print(f"❌ Telegram error: {e}")

async def main():
    await test_producthunt()
    await test_telegram()

if __name__ == "__main__":
    asyncio.run(main())
