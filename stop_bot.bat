@echo off
set PIDFILE=C:\Users\Mohirxoja.Usmonxojay\Desktop\SmartupAuto\test-results\bot.pid

if not exist "%PIDFILE%" (
    echo Bot ishlamayapdi.
    pause
    exit /b 0
)

set /p BOT_PID=<"%PIDFILE%"
echo Bot to'xtatilmoqda (PID: %BOT_PID%)...
taskkill /PID %BOT_PID% /F >nul 2>&1
del "%PIDFILE%" >nul 2>&1
echo Bot to'xtatildi.
pause
