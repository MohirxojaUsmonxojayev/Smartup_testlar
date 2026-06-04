# Telegram CI Bot

Telegram bot GitHub Actions workflow `.github/workflows/daily-smoke.yml`ni
ishga tushiradi.

## Bot Flow

Telegramda:

```text
/run
```

Bot server tanlatadi:

```text
[smartup.online]
[app3.greenwhite.uz/xtrade]
```

Keyin scope tanlatadi:

```text
[smoke] [regression]
```

Bot GitHub Actions run boshlaydi. Test jarayonida xabar beradi:

```text
GitHub Actions run boshlandi.
Test davom etyapti... 2 daqiqa bo'ldi
Test hali davom etyapti... 5 daqiqa bo'ldi
Test tugadi: SUCCESS
```

Workflow tugagach `.github/workflows/daily-smoke.yml` ham yakuniy test summary
xabarini Telegramga yuboradi.

## Commands

```text
/run
/servers
/help
```

Company code/password botdan so'ralmaydi. Ular GitHub Actions secrets orqali
olinadi:

```text
SMARTUP_COMPANY_CODE
SMARTUP_COMPANY_PASSWORD
```

## Required Environment Variables

Windows serverda bot uchun kerak:

```text
TELEGRAM_BOT_TOKEN=<telegram bot token>
TELEGRAM_CHAT_ID=<allowed chat id>
GITHUB_PAT=<github personal access token>
```

Optional:

```text
GITHUB_REPOSITORY=turgunovjasur/Playwright
GITHUB_WORKFLOW_FILE=daily-smoke.yml
GITHUB_REF=main
ALLOWED_SERVER_URLS=https://smartup.online,https://app3.greenwhite.uz/xtrade
```

`ALLOWED_SERVER_URLS` faqat shu ikki serverga ruxsat beradi:

```text
https://smartup.online
https://app3.greenwhite.uz/xtrade
```

## GitHub Token Permission

Fine-grained GitHub personal access token yarating.

Repository:

```text
turgunovjasur/Playwright
```

Permission:

```text
Actions: Read and write
```

Tokenni repository fayllariga, Telegramga yoki loglarga yozmang.

## Windows Local Server Run

Repositoryni clone qiling, keyin:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

CMD ishlatsangiz:

```cmd
set TELEGRAM_BOT_TOKEN=telegram_bot_token
set TELEGRAM_CHAT_ID=telegram_chat_id
set GITHUB_PAT=github_pat
set ALLOWED_SERVER_URLS=https://smartup.online,https://app3.greenwhite.uz/xtrade
```

Botni ishga tushirish:

```cmd
powershell -ExecutionPolicy Bypass -File .\scripts\run_telegram_ci_bot.ps1
```

PowerShell oynasi ochiq turishi kerak. Oyna yopilsa bot ham to'xtaydi.
