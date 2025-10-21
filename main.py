# -*- coding: utf-8 -*-
import os
import sys
import requests
import asyncio
from dotenv import load_dotenv
from telegram import Bot
from openai import OpenAI
from datetime import datetime, timezone

# 设置控制台编码为 UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# 加载环境变量
load_dotenv()

# 获取 API 密钥
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
PH_TOKEN = os.getenv("PH_TOKEN")

# ========== 📢 多频道推送配置 ==========
# 支持推送到多个 Telegram 频道
# 格式：在 .env 文件中用逗号分隔多个 Chat ID
# 例如：TELEGRAM_CHAT_ID=-123456789,-987654321,-111222333
TELEGRAM_CHAT_IDS = [
    chat_id.strip() 
    for chat_id in TELEGRAM_CHAT_ID.split(',') 
    if chat_id.strip()
] if TELEGRAM_CHAT_ID else []
# =======================================

# 初始化客户端
bot = Bot(token=TELEGRAM_BOT_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

def fetch_producthunt_top10():
    """获取 Product Hunt 前10名产品"""
    print("🔍 正在获取 Product Hunt 数据...")
    
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
    
    headers = {
        "Authorization": f"Bearer {PH_TOKEN}", 
        "Content-Type": "application/json"
    }
    
    try:
        res = requests.post(
            "https://api.producthunt.com/v2/api/graphql",
            json={"query": query, "variables": {"perPage": 10}},
            headers=headers,
            timeout=30
        )
        
        if res.status_code == 200:
            data = res.json().get("data", {}).get("posts", {}).get("edges", [])
            products = []
            for p in data:
                products.append({
                    "name": p["node"]["name"],
                    "tagline": p["node"]["tagline"], 
                    "url": p["node"]["url"],
                    "votes": p["node"]["votesCount"]
                })
            print(f"✅ 成功获取 {len(products)} 个产品")
            return products
        else:
            print(f"❌ Product Hunt API 错误: {res.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ 获取 Product Hunt 数据失败: {e}")
        return []

def summarize_with_openai(products):
    """使用 OpenAI 总结产品信息"""
    print("🤖 正在使用 OpenAI 生成总结...")
    
    if not products:
        return "今天没有找到 Product Hunt 产品数据。"
    
    # 构建产品列表文本
    text = "\n".join([
        f"{i+1}. {p['name']} — {p['tagline']} ({p['votes']} votes)"
        for i, p in enumerate(products)
    ])
    
    # 构建严格格式的 prompt
    prompt = f"""你是一个专业的产品分析助手。请严格按照以下格式总结 Product Hunt 产品：

【重要要求 - 必须处理所有产品】：
- 必须为列表中的每一个产品都生成总结
- 不能遗漏任何产品
- 必须按照产品在列表中的顺序进行编号

【格式要求 - 必须严格遵守】：
每个产品必须包含：
1. 产品编号和名称（格式：数字. 产品名 - 英文标语）
2. 三个要点，每个要点一行，以 "- " 开头
3. 要点用中文，简洁清晰

【输出示例】：
1. Meku - AI Web App and Site Builder:
- 利用人工智能技术，轻松建立网站
- 提供丰富的模板和设计选项
- 突出智能建站的便捷和创新

2. Open SaaS 2.0 - 免费、开源的 SaaS 起步工具包:
- 开放源代码，免费使用
- 提供强大功能，助力SaaS创业者
- 强调开源和自由的创新精神

【要点撰写规则】：
- 第1点：产品的核心功能或主要特点
- 第2点：产品提供的价值或优势
- 第3点：产品的创新点或核心价值

【待总结的产品列表 - 共{len(products)}个产品，必须全部处理】：
{text}

【最终要求】：
请为上述列表中的每一个产品都生成总结，按照1-{len(products)}的顺序编号，不要遗漏任何产品。严格按照上述格式输出，不要添加其他内容："""
    
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个严格遵守格式要求的产品分析助手。你必须完全按照用户指定的格式输出，不能有任何偏差。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3500,
            temperature=0.3
        )
        summary = completion.choices[0].message.content
        
        # 🔍 调试信息：查看 OpenAI 返回的详细信息
        print("✅ OpenAI 总结生成成功")
        print(f"📊 返回内容长度: {len(summary)} 字符")
        print(f"📊 使用的 tokens: {completion.usage.total_tokens} (prompt: {completion.usage.prompt_tokens}, completion: {completion.usage.completion_tokens})")
        print(f"📊 finish_reason: {completion.choices[0].finish_reason}")
        print("\n" + "="*50)
        print("📝 OpenAI 实际返回的内容：")
        print("="*50)
        print(summary)
        print("="*50 + "\n")
        
        # 检查是否被截断
        if completion.choices[0].finish_reason == "length":
            print("⚠️  警告：OpenAI 输出因 token 限制被截断！")
        
        return summary
        
    except Exception as e:
        print(f"❌ OpenAI 总结失败: {e}")
        # 如果 OpenAI 失败，返回简单格式
        return f"🚀 Product Hunt 今日热门产品：\n\n{text}\n\n(OpenAI 服务暂时不可用，显示原始数据)"

async def send_to_telegram(message):
    """发送消息到 Telegram（支持多个频道）"""
    print(f"📱 正在发送消息到 {len(TELEGRAM_CHAT_IDS)} 个 Telegram 频道...")
    
    success_count = 0
    fail_count = 0
    
    for chat_id in TELEGRAM_CHAT_IDS:
        try:
            await bot.send_message(
                chat_id=chat_id, 
                text=message, 
                disable_web_page_preview=True
            )
            print(f"  ✅ 发送成功 → {chat_id}")
            success_count += 1
        except Exception as e:
            print(f"  ❌ 发送失败 → {chat_id}: {e}")
            fail_count += 1
    
    print(f"📊 发送完成：成功 {success_count} 个，失败 {fail_count} 个")

async def main():
    """主函数"""
    print("🚀 开始运行 Daily Product Bot...")
    print("=" * 50)
    
    # 步骤1: 获取 Product Hunt 数据
    products = fetch_producthunt_top10()
    
    if not products:
        error_msg = "❌ 今天没有获取到 Product Hunt 数据，请检查网络连接和 API 配置。"
        await send_to_telegram(error_msg)
        return
    
    # 步骤2: 生成 AI 总结
    summary = summarize_with_openai(products)
    
    # 步骤3: 构建最终消息
    today = datetime.now(timezone.utc).strftime('%Y年%m月%d日')
    msg = f"🚀 Product Hunt 今日热门产品 ({today})\n\n{summary}\n\n— Daily Product Bot 🤖"
    
    # 步骤4: 发送到 Telegram
    await send_to_telegram(msg)
    
    print("=" * 50)
    print("✅ 机器人运行完成！")

if __name__ == "__main__":
    print("🤖 Daily Product Bot 启动中...")
    asyncio.run(main())