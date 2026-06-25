# Telegram botni ko'rinmas fon rejimda ishlatadi
# Administrator shart emas

$ProjectDir = "C:\Users\Mohirxoja.Usmonxojay\Desktop\SmartupAuto"
$PidFile    = "$ProjectDir\test-results\bot.pid"
$LogFile    = "$ProjectDir\test-results\bot.log"

# Eski jarayon hali ishlamoqdami?
if (Test-Path $PidFile) {
    $oldPid = Get-Content $PidFile -ErrorAction SilentlyContinue
    if ($oldPid) {
        $proc = Get-Process -Id $oldPid -ErrorAction SilentlyContinue
        if ($proc) {
            Write-Host "Bot allaqachon ishlamoqda (PID: $oldPid)" -ForegroundColor Yellow
            Write-Host "To'xtatish uchun: stop_bot.bat" -ForegroundColor Gray
            exit 0
        }
    }
}

if (-not (Test-Path "$ProjectDir\test-results")) {
    New-Item -ItemType Directory -Path "$ProjectDir\test-results" | Out-Null
}

# Botni ko'rinmas oynada ishga tushirish
$proc = Start-Process -FilePath "python" `
    -ArgumentList "$ProjectDir\utils\telegram_bot.py" `
    -WorkingDirectory $ProjectDir `
    -WindowStyle Hidden `
    -RedirectStandardOutput "$ProjectDir\test-results\bot_out.log" `
    -RedirectStandardError $LogFile `
    -PassThru

$proc.Id | Out-File -FilePath $PidFile -Encoding utf8

Write-Host "Bot ishga tushirildi!" -ForegroundColor Green
Write-Host "  PID     : $($proc.Id)" -ForegroundColor Cyan
Write-Host "  Log fayl: $LogFile" -ForegroundColor Cyan
Write-Host "  To'xtatish: stop_bot.bat" -ForegroundColor Cyan
Write-Host ""
Write-Host "Telegram'da /start yoki /run yuboring." -ForegroundColor White
