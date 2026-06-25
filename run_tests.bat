@echo off
cd /d "C:\Users\Mohirxoja.Usmonxojay\Desktop\SmartupAuto"
if errorlevel 1 (
    echo [ERROR] Papka topilmadi >> "C:\Users\Mohirxoja.Usmonxojay\Desktop\SmartupAuto\test-results\autorun.log"
    exit /b 1
)

set LOGFILE=C:\Users\Mohirxoja.Usmonxojay\Desktop\SmartupAuto\test-results\autorun.log

if not exist "test-results" mkdir "test-results"

echo. >> "%LOGFILE%"
echo ================================================ >> "%LOGFILE%"
echo  Start: %date% %time% >> "%LOGFILE%"
echo ================================================ >> "%LOGFILE%"

echo ================================================
echo  Start: %date% %time%
echo ================================================

python -m pytest tests/regression/ ^
  --url https://app3.greenwhite.uz/xtrade ^
  --company-code novatrade ^
  --company-password greenwhite ^
  --headless ^
  -v

set PYTEST_EXIT=%errorlevel%

echo. >> "%LOGFILE%"
echo ================================================ >> "%LOGFILE%"
echo  Finish: %date% %time% >> "%LOGFILE%"
echo  Exit: %PYTEST_EXIT% >> "%LOGFILE%"
echo ================================================ >> "%LOGFILE%"

echo ================================================
echo  Finish: %date% %time%
echo  Exit: %PYTEST_EXIT%
echo ================================================

exit /b %PYTEST_EXIT%
