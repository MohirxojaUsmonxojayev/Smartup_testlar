@echo off
cd /d "C:\Users\Mohirxoja.Usmonxojay\Desktop\SmartupAuto"
if errorlevel 1 (
    echo [ERROR] Papka topilmadi
    pause
    exit /b 1
)
echo Telegram bot ishga tushmoqda...
echo Toxtatish uchun Ctrl+C bosing
echo.
python utils\telegram_bot.py
pause
