@echo off
setlocal

cd /d "%~dp0"

.venv\Scripts\python.exe scripts\telegram_ci_bot.py

exit /b %ERRORLEVEL%
