# SmartupAuto Regression Tests — Windows Task Scheduler setup
# Har kuni 00:00, 06:00, 12:00, 18:00 da avtomatik ishga tushiradi
# Administrator sifatida ishga tushiring!

$taskName = "SmartupAuto Regression Tests"
$batFile  = "C:\Users\Mohirxoja.Usmonxojay\Desktop\SmartupAuto\run_tests.bat"
$xmlFile  = "$env:TEMP\smartupauto_task.xml"

$sid = ([System.Security.Principal.WindowsIdentity]::GetCurrent()).User.Value

$xml = @"
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>SmartupAuto regression testlar — har 6 soatda: 00:00, 06:00, 12:00, 18:00</Description>
  </RegistrationInfo>
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>2026-06-25T00:00:00</StartBoundary>
      <Enabled>true</Enabled>
      <Repetition>
        <Interval>PT6H</Interval>
        <StopAtDurationEnd>false</StopAtDurationEnd>
      </Repetition>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>$sid</UserId>
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <ExecutionTimeLimit>PT3H</ExecutionTimeLimit>
    <StartWhenAvailable>true</StartWhenAvailable>
    <Enabled>true</Enabled>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>cmd.exe</Command>
      <Arguments>/c "$batFile"</Arguments>
    </Exec>
  </Actions>
</Task>
"@

$xml | Out-File -FilePath $xmlFile -Encoding Unicode

schtasks /delete /tn $taskName /f 2>$null

$out = schtasks /create /tn $taskName /xml $xmlFile /f 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "Task muvaffaqiyatli yaratildi!" -ForegroundColor Green
    Write-Host "  Jadval  : 00:00, 06:00, 12:00, 18:00 (har kuni)" -ForegroundColor Cyan
    Write-Host "  Buyruq  : $batFile" -ForegroundColor Cyan
} else {
    Write-Host "Xatolik: $out" -ForegroundColor Red
    Write-Host "ESLATMA: Administrator PowerShell dan ishga tushiring!" -ForegroundColor Yellow
}

Remove-Item $xmlFile -ErrorAction SilentlyContinue

# ── playwright_original eski task ni o'chirish ────────────────────────────────
Write-Host ""
Write-Host "Eski 'Playwright Autotests' task o'chirilmoqda..." -ForegroundColor Yellow
$delOut = schtasks /delete /tn "Playwright Autotests" /f 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  'Playwright Autotests' muvaffaqiyatli o'chirildi." -ForegroundColor Green
} else {
    Write-Host "  'Playwright Autotests' o'chirishda xato (yoki mavjud emas): $delOut" -ForegroundColor Gray
}

# ── Quvvat sozlamalari ────────────────────────────────────────────────────────
Write-Host ""
Write-Host "Quvvat sozlamalari o'rnatilmoqda..." -ForegroundColor Yellow
powercfg /change standby-timeout-ac 0
powercfg /change monitor-timeout-ac 0
powercfg /change standby-timeout-dc 0
powercfg /setacvalueindex SCHEME_CURRENT SUB_BUTTONS LIDACTION 0
powercfg /setdcvalueindex SCHEME_CURRENT SUB_BUTTONS LIDACTION 0
powercfg /setactive SCHEME_CURRENT
Write-Host "  Uyqu  : o'chirildi" -ForegroundColor Cyan
Write-Host "  Ekran : o'chirilmaydi" -ForegroundColor Cyan
