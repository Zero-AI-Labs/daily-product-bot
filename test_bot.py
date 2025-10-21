import asyncio
import requests
from dotenv import load_dotenv
import os
from telegram import Bot
from openai import OpenAI

async def test_all():
    print("🧪 开始测试所有功能...")
    
    # 加载环境变量
    load_dotenv()
    
    # 获取环境变量
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    PH_TOKEN = os.getenv("PH_TOKEN")
    
    print(f"✅ 环境变量加载完成")
    print(f"   - OpenAI API Key: {'已设置' if OPENAI_API_KEY else '未设置'}")
    print(f"   - Telegram Bot Token: {'已设置' if TELEGRAM_BOT_TOKEN else '未设置'}")
    print(f"   - Telegram Chat ID: {TELEGRAM_CHAT_ID}")
    print(f"   - PH Token: {'已设置' if PH_TOKEN else '未设置'}")
    
    # 测试 Product Hunt API
    print("\n🔍 测试 Product Hunt API...")
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
    
    headers = {"Authorization": f"Bearer {PH_TOKEN}", "Content-Type": "application/json"}
    try:
        res = requests.post(
            "https://api.producthunt.com/v2/api/graphql",
            json={"query": query, "variables": {"perPage": 3}},
            headers=headers,
            timeout=30
        )
        
        if res.status_code == 200:
            data = res.json().get("data", {}).get("posts", {}).get("edges", [])
            print(f"✅ Product Hunt API 连接成功！获取到 {len(data)} 个产品")
            for i, p in enumerate(data[:2]):
                print(f"   {i+1}. {p['node']['name']} - {p['node']['tagline']}")
        else:
            print(f"❌ Product Hunt API 错误: {res.status_code}")
            
    except Exception as e:
        print(f"❌ Product Hunt API 连接失败: {e}")
    
    # 测试 Telegram
    print("\n📱 测试 Telegram...")
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    try:
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID, 
            text="🤖 机器人测试消息 - 如果你看到这条消息，说明 Telegram 连接正常！"
        )
        print("✅ Telegram 连接成功！")
    except Exception as e:
        print(f"❌ Telegram 连接失败: {e}")
    
    # 测试 OpenAI (如果配额足够)
    print("\n🤖 测试 OpenAI...")
    client = OpenAI(api_key=OPENAI_API_KEY)
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say hello in Chinese"}],
            max_tokens=10
        )
        print("✅ OpenAI 连接成功！")
        print(f"   回复: {completion.choices[0].message.content}")
    except Exception as e:
        print(f"❌ OpenAI 连接失败: {e}")
        if "quota" in str(e).lower():
            print("   💡 提示: 这可能是 OpenAI API 配额问题，但机器人仍然可以运行（会使用备用方案）")
    
    print("\n🎉 测试完成！")

if __name__ == "__main__":
    asyncio.run(test_all())
