# Plan: Deploy Telegram Fashion Bot

## Task Description
Deploy the Tokopedia Fashion Bot (a Python Telegram bot using polling mode) to the cloud in the simplest way possible.

## Objective
Get the bot running 24/7 on a cloud platform with minimal configuration and cost.

## Problem Statement
The current bot runs locally using `uv run python -m src.bot` with polling mode. It needs to be deployed to a hosting platform that:
- Supports long-running Python processes (polling bots)
- Can handle environment variables securely
- Has minimal setup complexity
- Is cost-effective (preferably free tier)

## Solution Approach

**Cloudflare is NOT recommended** for this use case because:
1. Workers have a 30-second CPU timeout - polling bots need to run continuously
2. Python support on CF Workers is experimental (Pyodide)
3. Would require refactoring the entire bot to webhook mode

**Recommended: Railway.app** - The simplest deployment option:
- Native Python support
- Just push code + add env vars
- Free tier (500 hours/month = ~20 days continuous)
- Supports long-running processes
- Simple GitHub integration

**Alternative: Render.com** - Also simple but free tier has limitations (sleeps after 15 mins).

## Relevant Files

- `src/bot.py` - Main bot entry point that needs to run continuously
- `src/config.py` - Configuration loading (env vars)
- `src/gemini_analyzer.py` - Gemini AI integration
- `pyproject.toml` - Dependencies
- `.env` - Environment variables (GEMINI_API_KEY, TELEGRAM_BOT_API)
- `beach-party-tokopedia-looks.json` - Reference data file

### New Files to Create

- `Procfile` - Tells Railway how to start the app
- `.gitignore` - Ensure .env is not committed (if not exists)

## Step by Step Tasks

### 1. Create Procfile for Railway
- Create a `Procfile` in the project root
- Content: `worker: python -m src.bot`
- This tells Railway to run the bot as a worker process

### 2. Update .gitignore
- Ensure `.env` is in `.gitignore`
- Ensure `.venv/` is in `.gitignore`
- Ensure `__pycache__/` is in `.gitignore`

### 3. Create requirements.txt (Railway compatibility)
- While Railway supports pyproject.toml, having requirements.txt ensures compatibility
- Run: `uv pip compile pyproject.toml -o requirements.txt`

### 4. Push to GitHub
- Create a new GitHub repository (if not exists)
- Push the code: `git add . && git commit -m "Prepare for Railway deployment" && git push`

### 5. Deploy on Railway
- Go to railway.app and sign up/login with GitHub
- Click "New Project" → "Deploy from GitHub repo"
- Select the repository
- Railway will auto-detect Python and Procfile
- Add environment variables in Railway dashboard:
  - `GEMINI_API_KEY` = your key
  - `TELEGRAM_BOT_API` = your bot token
- Click Deploy

### 6. Verify Deployment
- Check Railway logs for "Bot is ready! Starting polling..."
- Test the bot on Telegram by sending a photo

## Acceptance Criteria
- [ ] Bot runs continuously on Railway
- [ ] Bot responds to /start command
- [ ] Bot analyzes photos and returns Tokopedia links
- [ ] Environment variables are securely configured
- [ ] No secrets in source code

## Validation Commands
Execute these commands to validate the task is complete:

- `curl -s https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getMe` - Verify bot is accessible
- Send a test photo to the bot on Telegram and confirm it responds with analysis

## Notes

### Environment Variables Required
```
GEMINI_API_KEY=your_gemini_api_key
TELEGRAM_BOT_API=your_telegram_bot_token
```

### Railway Pricing
- Free tier: 500 hours/month (~20 days of continuous running)
- Hobby plan: $5/month for unlimited hours
- For 24/7 operation, you'll need the Hobby plan after free hours run out

### Alternative: Convert to Webhook Mode (for Cloudflare)
If you prefer Cloudflare in the future, the bot would need to be refactored to:
1. Use webhook mode instead of polling
2. Add a web server (Flask/FastAPI)
3. Convert to Cloudflare Workers Python (experimental)
4. Set up webhook URL with Telegram

This is significantly more complex and not recommended for simplicity.
