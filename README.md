# 🤖 Daily Product Hunt Bot

每天自动抓取 Product Hunt 前10名产品，用 OpenAI 总结并推送到 Telegram。

## 📋 功能

- ✅ 自动获取 Product Hunt 今日前10名产品
- ✅ 使用 OpenAI 生成中文总结（支持备用方案）
- ✅ 自动推送到 Telegram 频道
- ✅ 支持 GitHub Actions 每日自动运行

## 🚀 本地运行

### 方法1：命令行运行

```bash
# 进入项目目录
cd "c:\Users\elondust\Desktop\Cursor Projects\Producthunt\daily-product-bot"

# 运行机器人
py main.py
```

### 方法2：双击运行

直接双击 `run_bot.bat` 文件即可运行机器人。

### 方法3：在 Cursor 中运行

1. 打开 `main.py` 文件
2. 按 **F5** 或点击右上角的运行按钮
3. 或者在终端中运行 `py main.py`

## 📝 环境要求

### Python 包
```bash
pip install -r requirements.txt
```

### 必需的 API 密钥
在 `.env` 文件中配置：

```
OPENAI_API_KEY=你的OpenAI密钥
TELEGRAM_BOT_TOKEN=你的Telegram机器人Token
TELEGRAM_CHAT_ID=你的Telegram频道ID
PH_TOKEN=你的ProductHunt令牌
```

## 🔧 配置说明

### 获取 API 密钥

1. **OpenAI API Key**
   - 访问 https://platform.openai.com/api-keys
   - 创建新的 API 密钥

2. **Telegram Bot Token**
   - 在 Telegram 中找到 @BotFather
   - 发送 `/newbot` 创建机器人
   - 获取 Bot Token

3. **Telegram Chat ID**
   - 将机器人添加到频道
   - 使用 @userinfobot 获取 Chat ID

4. **Product Hunt Token**
   - 访问 https://api.producthunt.com/v2/oauth/applications
   - 创建应用获取访问令牌

## ⚙️ GitHub Actions 自动运行

### 设置步骤

1. 将代码推送到 GitHub 仓库
2. 在仓库设置中添加 Secrets：
   - `OPENAI_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
   - `PH_TOKEN`
3. 机器人将每天 UTC 1:00（北京时间 9:00）自动运行

### 手动触发

在 GitHub 仓库的 Actions 页面，可以手动触发运行。

## 📊 运行流程

```
1. 🔍 获取 Product Hunt 数据
   ↓
2. 🤖 使用 OpenAI 生成总结
   ↓
3. 📱 发送到 Telegram
   ↓
4. ✅ 完成
```

## ⚠️ 注意事项

- **OpenAI 配额**：如果 OpenAI API 配额用完，机器人会自动使用备用方案，直接显示产品信息
- **网络访问**：需要能访问 Product Hunt、OpenAI 和 Telegram API
- **频率限制**：建议不要频繁运行，遵守 API 使用限制

## 🐛 故障排除

### 问题：环境变量未加载
**解决方案**：确保 `.env` 文件存在且格式正确

### 问题：Telegram 发送失败
**解决方案**：
- 检查 Bot Token 是否正确
- 确认机器人已添加到频道
- 检查 Chat ID 是否正确

### 问题：Product Hunt API 错误
**解决方案**：
- 检查 PH_TOKEN 是否有效
- 确认网络可以访问 Product Hunt API

### 问题：显示乱码
**解决方案**：已在代码中添加 UTF-8 编码支持，应该不会出现此问题

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

Made with ❤️ by Your Name
