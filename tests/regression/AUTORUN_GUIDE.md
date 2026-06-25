# Regression Testlar — Avtorun va Telegram Bot Qo'llanmasi

---

## 1-BOSQICH TEKSHIRUV NATIJALARI

### Eski loyiha (`playwright_original`) holati

| Tekshiruv | Natija | Izoh |
|---|---|---|
| Telegram bot yuborish kodi hali mavjudmi? | ✅ Mavjud | O'chirilmagan — `utils/telegram_reporter.py`, `telegram_sender.py` bor |
| Cron job / scheduler aktivmi? | ✅ O'chirildi | `"Playwright Autotests"` Task Scheduler o'chirildi |
| Asosiy test logikasi buzilganmi? | ✅ Buzilmagan | `conftest.py`, fixtures, flow'lar to'liq ishlaydi |
| Import yoki dependency singanmi? | ✅ Sog'lom | `conftest OK` — barcha importlar ishlaydi |

> **Xulosa:** Eski loyiha to'liq sog'lom. Faqat avtorun o'chirildi. Eski loyihaning o'z bot kodi o'chirilmagan, lekin endi Task Scheduler bo'lmagani uchun avtomatik ishlamaydi.

---

### Yangi loyiha (`SmartupAuto`) holati

| Tekshiruv | Natija | Izoh |
|---|---|---|
| Token va chat_id konfiguratsiyasi | ✅ To'g'ri | `.env` faylda `TELEGRAM_BOT_TOKEN` va `TELEGRAM_CHAT_ID` mavjud |
| Bot xabar yuborish funksiyasi | ✅ Tayyor | `utils/telegram_sender.py` — `requests` orqali ishlaydi |
| Cron job / scheduler qo'shilganmi? | ✅ Qo'shildi | Windows Task Scheduler — `"SmartupAuto Regression Tests"` |
| Scheduler 4 marta ishga tushadimi? | ✅ Ha | 00:00 / 06:00 / 12:00 / 18:00 — har 6 soatda |
| Regression testlar scheduler tomonidan chaqiriladimi? | ✅ Ha | `run_tests.bat` → `pytest tests/regression/` |
| Test natijasi bot orqali yuboriladimi? | ✅ Ha | `TelegramReporter` plugin session boshida va oxirida yuboradi |
| Log va screenshot funksiyalari ishlayaptimi? | ✅ To'liq | `pytest_runtest_makereport` + `pytest_runtest_logreport` hooks barcha |
| Entry point mavjudmi? | ✅ Mavjud | `run_tests.bat` (avtorun), `start_bot.bat` (bot) |

---

## Loyiha Arxitekturasi

```
SmartupAuto/
├── .env                            ← Telegram token va chat_id (gitignore'da)
├── run_tests.bat                   ← AVTORUN entry point: testlarni headless ishlatadi
├── start_bot.bat                   ← BOT entry point: Telegram botni ishga tushiradi
├── setup_scheduler.ps1             ← Windows Task Scheduler o'rnatish (bir marta)
│
├── utils/
│   ├── telegram_sender.py          ← Telegram API ga HTTP POST (faqat requests)
│   ├── telegram_reporter.py        ← pytest plugin: session start/end Telegram'ga
│   └── telegram_bot.py             ← Long-polling bot: /run tugmasi → test ishlatadi
│
└── tests/regression/
    ├── conftest.py                 ← TelegramReporter registered + log/screenshot hooks
    ├── test_auth.py                ← Login testi
    └── test_check_forms_opening.py ← 219 ta forma tekshiruvi (asosiy)
```

### Har bir fayl nima qiladi

| Fayl | Vazifasi |
|---|---|
| `utils/telegram_sender.py` | `.env` dan token o'qiydi, Telegram'ga xabar yuboradi. 4000 belgidan uzun xabarni avtomatik bo'ladi. |
| `utils/telegram_reporter.py` | pytest plugin. Test session boshlananda "🚀 Testlar boshlandi", tugaganda "✅/❌ NATIJALAR" xabari yuboradi. |
| `utils/telegram_bot.py` | Telegram long-polling boti. `/start`, `/run` buyruqlari va "Run Tests Now" tugmasiga javob beradi. Tugma bosilganda `run_tests.bat` subprocess sifatida ishga tushiradi. |
| `run_tests.bat` | `pytest tests/regression/` ni `--headless` va barcha kerakli parametrlar bilan ishlatadi. Log yozadi. |
| `start_bot.bat` | `utils/telegram_bot.py` ni ishga tushiradi. Fon jarayon emas — terminal ochiq turishi kerak. |
| `setup_scheduler.ps1` | Windows Task Scheduler'ga "SmartupAuto Regression Tests" taskini qo'shadi. Eski "Playwright Autotests" taskini o'chiradi. |
| `tests/regression/conftest.py` | `TelegramReporter` pluginni ro'yxatga oladi. FAIL bo'lganda screenshot va log saqlaydi (avvalgi funksiyalar saqlab qolindi). |

---

## Eski Loyihadan Ko'chirilgan Narsalar

| Narsa | Eski loyiha | Yangi loyiha | Yaxshilanishlar |
|---|---|---|---|
| `telegram_sender.py` | `utils/telegram_sender.py` | `utils/telegram_sender.py` | O'zgarishsiz — sifatli kod |
| `telegram_reporter.py` | pytest plugin, `--server` flag ishlatgan | pytest plugin, `--url` / `COMPANY_URL` ishlatadi | SmartupAuto conftest bilan mos |
| `telegram_bot.py` | `python-telegram-bot` kutubxona (async) | Faqat `requests` (sync, sodda) | Yangi dependency yo'q |
| `run_tests.bat` | Online + Xtrade ikkala server uchun | Faqat xtrade, regression papkasi | Aniqroq, oddiy |
| `setup_scheduler.ps1` | Faqat yangi task yaratardi | Yangi task yaratadi + eskini o'chiradi | Ikki ish bir joyda |

---

## Avtorun Jadvali

```
Har kuni:
  00:00  →  run_tests.bat ishga tushadi
  06:00  →  run_tests.bat ishga tushadi
  12:00  →  run_tests.bat ishga tushadi
  18:00  →  run_tests.bat ishga tushadi

Har run davomiyligi: ~5-8 daqiqa (219 forma)
```

**Task Scheduler holati tekshirish:**
```powershell
schtasks /query /tn "SmartupAuto Regression Tests" /fo LIST
```

**Qo'lda bir marta ishga tushirish:**
```powershell
schtasks /run /tn "SmartupAuto Regression Tests"
```

---

## Telegram Bot Sozlamasi

### Token va chat_id qayerda?

```
SmartupAuto/.env
```
```env
TELEGRAM_BOT_TOKEN=<bot_token>
TELEGRAM_CHAT_ID=<sizning_telegram_id>
```

`.env` faylni hech qachon git'ga yubormang — `.gitignore`'da allaqachon mavjud.

### Chat_id ni qanday bilib olish?

Bot ishga tushirilgandan so'ng `/id` buyrug'ini yuboring:
```
Sizning Telegram ID: 6847971883
Bot admin ID: 6847971883
Mos keladi: ✅ HA
```

### Faqat ADMIN (TELEGRAM_CHAT_ID egasi) quyidagilarni bajarа oladi:
- `🚀 Run Tests Now` tugmasini bosish
- `/run` buyrug'ini ishlatish

---

## Ishga Tushirish Ko'rsatmasi

### Birinchi marta o'rnatish (bir marta, admin PowerShell)

```powershell
# Administrator sifatida PowerShell oching
Set-ExecutionPolicy Bypass -Scope Process -Force
C:\Users\Mohirxoja.Usmonxojay\Desktop\SmartupAuto\setup_scheduler.ps1
```

Bu bajaradi:
1. "SmartupAuto Regression Tests" Task Scheduler taskini yaratadi (00:00/06:00/12:00/18:00)
2. Eski "Playwright Autotests" taskini o'chiradi
3. Kompyuter uyquga ketmasligi uchun quvvat sozlamalarini o'rnatadi

---

### Telegram botni ishga tushirish

**Variant 1 — Qo'lda (test uchun):**
```bat
C:\Users\Mohirxoja.Usmonxojay\Desktop\SmartupAuto\start_bot.bat
```
Terminal yopilmasligi kerak.

**Variant 2 — Windows ishga tushganda avtomatik:**
1. `start_bot.bat` ga shortcut yarating
2. `Win+R` → `shell:startup` → shortcut'ni u yerga tashlang

---

### Testlarni qo'lda ishlatish

```bat
# Barcha regression testlar (headless)
C:\Users\Mohirxoja.Usmonxojay\Desktop\SmartupAuto\run_tests.bat

# Faqat forma tekshiruvi (terminal orqali)
cd C:\Users\Mohirxoja.Usmonxojay\Desktop\SmartupAuto
python -m pytest tests/regression/test_check_forms_opening.py -v ^
  --url https://app3.greenwhite.uz/xtrade ^
  --company-code novatrade ^
  --company-password greenwhite
```

---

## Muhit O'zgaruvchilari (Environment Variables)

| O'zgaruvchi | Qayerda belgilanadi | Maqsadi |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | `.env` fayli | Bot tokeni |
| `TELEGRAM_CHAT_ID` | `.env` fayli | Admin telegram ID |
| `COMPANY_URL` | `conftest.py` (`--url` dan) | Server manzili (TelegramReporter uchun) |
| `COMPANY_CODE` | `conftest.py` (`--company-code` dan) | Kompaniya kodi |
| `COMPANY_PASSWORD` | `conftest.py` (`--company-password` dan) | Kompaniya paroli |
| `HEADLESS` | `run_tests.bat` (`--headless` orqali) | Headless rejim |

---

## Test Natijasi Telegram'da Qanday Ko'rinadi

**Test boshlananda:**
```
🚀 Testlar boshlandi
🌐 Server: https://app3.greenwhite.uz/xtrade
🕐 2026-06-25 00:00:12
```

**Test muvaffaqiyatli tugaganda:**
```
📊 REGRESSION TEST — ✅ MUVAFFAQIYATLI
🌐 https://app3.greenwhite.uz/xtrade
📅 2026-06-25 00:07:43
⏱ 7m 31s
📦 Jami: 2  |  ✅ 2  |  ❌ 0  |  ⚠️ 0

📋 test_auth — ✅ PASSED
📋 test_check_forms_opening — ✅ PASSED
```

**Test xato berganda:**
```
📊 REGRESSION TEST — ❌ XATOLIKLAR BOR
⏱ 3m 15s
📦 Jami: 2  |  ✅ 1  |  ❌ 1  |  ⚠️ 0

📋 test_auth — ✅ PASSED
📋 test_check_forms_opening — ❌ FAILED
   └ AssertionError: Expected to contain 'Создать'...
```

---

## Muammolarni Bartaraf Etish

### Bot xabar yubormayapti

**Sababi:** `.env` fayl yo'q yoki token/chat_id noto'g'ri.
```bat
# Tekshirish:
python -c "from utils.telegram_sender import send_telegram; print(send_telegram('Test xabar'))"
```
`True` chiqsa — ishlaydi. `False` chiqsa — `.env` faylni tekshiring.

---

### Task Scheduler ishlamayapti

**Sababi:** Kompyuter o'chirilgan yoki foydalanuvchi tizimga kirmagan.

Task Scheduler faqat foydalanuvchi tizimga kirgan paytda ishlaydi (`InteractiveToken`).

```powershell
# Holat tekshirish:
schtasks /query /tn "SmartupAuto Regression Tests" /fo LIST

# Qo'lda ishga tushirish:
schtasks /run /tn "SmartupAuto Regression Tests"
```

---

### "Testlar allaqachon ishlamoqda" xabari

**Sababi:** Bot tugma bosilganda oldingi run hali tugamagan.
Taxminan 8 daqiqa kutib, qayta bosing.

---

### `--url` majburiy xatosi

**Sababi:** `run_tests.bat` ichida `--url` ko'rsatilgan, lekin yo'l noto'g'ri.
`run_tests.bat` faylini oching va `--url`, `--company-code`, `--company-password` qiymatlarini tekshiring.

---

### Log fayllar qayerda?

```
SmartupAuto/
└── test-results/
    ├── autorun.log          ← run_tests.bat log (har run yoziladi)
    ├── allure-results/      ← Allure xom ma'lumotlar
    ├── traces/              ← Playwright trace .zip fayllar
    └── logs/                ← FAIL bo'lganda test xato loglari
```

---

## Hozirgi Holat

- ✅ **SmartupAuto** — avtorun YOQILGAN (00:00 / 06:00 / 12:00 / 18:00)
- ✅ **playwright_original** — avtorun O'CHIRILGAN
- ✅ **Telegram bot** — `start_bot.bat` orqali ishga tayyor
- ✅ **219 ta forma** — test_check_forms_opening.py da PASSED
