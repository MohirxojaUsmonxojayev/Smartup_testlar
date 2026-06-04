# Telegram CI Bot

This bot listens for Telegram commands and starts the GitHub Actions workflow
`.github/workflows/daily-smoke.yml` with selected test options.

## Commands

```text
/smoke
/regression
/run scope=smoke server=https://smartup.online target=all
/run scope=regression server=https://smartup.online target=all
/run smoke https://smartup.online
/servers
/help
```

Supported scopes:

```text
smoke
regression
```

Supported targets:

```text
all
setup
group-a
group-b
```

## Required Environment Variables

```text
TELEGRAM_BOT_TOKEN=<telegram bot token>
TELEGRAM_CHAT_ID=<allowed chat id>
GITHUB_TOKEN=<github personal access token>
```

Optional environment variables:

```text
GITHUB_REPOSITORY=turgunovjasur/Playwright
GITHUB_WORKFLOW_FILE=daily-smoke.yml
GITHUB_REF=main
DEFAULT_SERVER_URL=https://smartup.online/
ALLOWED_SERVER_URLS=https://smartup.online
```

Use `TELEGRAM_ALLOWED_CHAT_IDS` instead of `TELEGRAM_CHAT_ID` if multiple chats
are allowed:

```text
TELEGRAM_ALLOWED_CHAT_IDS=123456789,-1001234567890
```

Set `ALLOWED_SERVER_URLS` as a comma-separated allowlist:

```text
ALLOWED_SERVER_URLS=https://smartup.online,https://app3.greenwhite.uz/xtrade
```

Use `ALLOWED_SERVER_URLS=*` only if the bot should accept any server URL.

## GitHub Token Permission

Create a fine-grained GitHub personal access token for this repository with
Actions write permission. Store it as `GITHUB_TOKEN` in the place where the bot
runs.

Do not put this token in repository files or Telegram messages.

## Local Run

```bash
python scripts/telegram_ci_bot.py
```

The bot must keep running. For real use, deploy it to a small always-on service
such as Render, Railway, a VPS, or another worker host.

## Windows Local Server Run

Clone the repository on the Windows server, then install dependencies:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Set environment variables in PowerShell:

```powershell
$env:TELEGRAM_BOT_TOKEN = "<telegram_bot_token>"
$env:TELEGRAM_CHAT_ID = "<telegram_chat_id>"
$env:GITHUB_PAT = "<github_personal_access_token>"
$env:GITHUB_REPOSITORY = "turgunovjasur/Playwright"
$env:GITHUB_WORKFLOW_FILE = "daily-smoke.yml"
$env:GITHUB_REF = "main"
$env:DEFAULT_SERVER_URL = "https://smartup.online/"
$env:ALLOWED_SERVER_URLS = "https://smartup.online"
```

Run the bot:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_telegram_ci_bot.ps1
```

Keep this PowerShell process running. If the Windows server restarts or the
PowerShell window closes, the bot stops.

To allow more than one server:

```powershell
$env:ALLOWED_SERVER_URLS = "https://smartup.online,https://app3.greenwhite.uz/xtrade"
```

Use this only if every server URL should be accepted:

```powershell
$env:ALLOWED_SERVER_URLS = "*"
```
