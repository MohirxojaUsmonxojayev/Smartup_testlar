---
name: run-smoke
description: Smoke testlarni ishga tushirish va natijalarni ko'rsatish. "testlarni ishga tushir", "smoke run", "pytest ishga tushir" so'ralganda ishlatiladi.
allowed-tools: Bash, Read, Glob
---

# Smoke Testlarni Ishga Tushirish

Argument: `$ARGUMENTS` (test nomi, fayl yoki bo'sh)

## Qaysi buyruqni ishlating

### Barcha smoke testlar (to'liq run):
```bash
python scripts/run_tests.py --url <server_url> --company-code <company_code> --company-password <company_password>
```

Headless run:
```bash
python scripts/run_tests.py --url <server_url> --company-code <company_code> --company-password <company_password> --headless
```

Regression:
```bash
python scripts/run_tests.py --url <server_url> --company-code <company_code> --company-password <company_password> --regression
```

Yangi company yaratish:
```bash
python scripts/run_tests.py --url <server_url> --create-company --head-email <head_email> --head-password <head_password>
```

Debug uchun setup yoki group:
```bash
python scripts/run_tests.py setup --url <server_url> --company-code <company_code> --company-password <company_password>
python scripts/run_tests.py group-a --url <server_url> --company-code <company_code> --company-password <company_password>
python scripts/run_tests.py group-b --url <server_url> --company-code <company_code> --company-password <company_password>
python scripts/run_tests.py group-c --url <server_url> --company-code <company_code> --company-password <company_password>
python scripts/run_tests.py group-report --url <server_url> --company-code <company_code> --company-password <company_password>
```

Browser ochilishi kerak bo'lsa `HEADLESS=1` yoki `--headless` ishlatma; `--headless` berilsa browser ko'rinmasligi to'g'ri holat.

### Bitta test fayl:
```bash
pytest tests/smoke/test_setup/test_<nomi>.py -v
```

### Bitta test funksiya:
```bash
pytest tests/smoke/test_setup/test_setup_runner.py::test_<nomi> -v
```

### Allure hisobot ko'rish:
```bash
allure serve test-results/allure-results
```

## Ish tartibi

1. `$ARGUMENTS` bo'sh bo'lsa — to'liq `python scripts/run_tests.py --url <server_url> --company-code <code> --company-password <password>` yoki `--create-company --head-email <email> --head-password <password>` bilan ishga tushir
2. `$ARGUMENTS` fayl nomi bo'lsa — faqat shu faylni ishga tushir
3. `$ARGUMENTS` test nomi bo'lsa — faqat shu testni ishga tushir
4. Natijalarni tahlil qil:
   - **PASSED** testlar sonini ko'rsat
   - **FAILED** testlar bo'lsa — xato xabarini o'qib sababini tushuntir
   - `--maxfail=3` limit urilsa ogohlantir
5. Muvaffaqiyatsiz testlar bo'lsa: `test-results/logs/` papkasidagi log fayllarni o'qi va foydalanuvchiga ko'rsat

## Muhim

- Asosiy runner cross-platform: `python scripts/run_tests.py --url <server_url> --company-code <code> --company-password <password>`; Mac/Linux uchun `./run_tests.sh ...` wrapper ham bor.
- `.env` ishlatilmaydi; `--url` majburiy.
- Mavjud company bilan run qilish uchun `--company-code` va `--company-password` majburiy.
- Yangi company yaratish uchun `--create-company`, `--head-email` va `--head-password` majburiy.
- `--create-company` bilan `--company-code` va `--company-password` berilmaydi; company code test ichida `autotest<code>` ko'rinishida yaratiladi.
- Company setupda Security tabdagi `Политика лицензирования`ni off qilish kerak bo'lsa `--create-company --head-email <email> --head-password <password> --disable-license-policy` ishlatiladi.
- `--disable-license-policy` ishlatilsa `Buy License` va `Attach License` qadamlari o'tkazib yuboriladi.
- `scripts/run_tests.py` default scope `smoke`; `--regression` berilsa pytestga `--scope regression` uzatiladi.
- Bevosita pytest runlarda scope shunday beriladi: `./.venv/bin/pytest tests/smoke/test_setup/test_setup_runner.py::test_02_legal_person --scope=regression`.
- Scope faqat bitta testga xos emas; all/setup/group runnerlar orqali butun suitega uzatiladigan global mode.
- Smoke natijasini tahlil qilganda minimal path ishlaganini tekshir; regression natijasini tahlil qilganda add form full to'ldirilgani, list check va view check bajarilganini alohida ko'r.
- `pytest.ini` dagi `testpaths = tests` va `addopts` avtomatik qo'llanadi
- Trace fayllari `test-results/traces/` ga, Allure natijalar `test-results/allure-results/` ga yoziladi
- `scripts/run_tests.py` report/trace viewerlarni faqat `--open-report` yoki `--show-trace` bo'lsa ochadi.
- Directory/default collectionda runner bo'lmagan smoke testlar duplicate flow bo'lmasligi uchun deselect qilinadi; kerak bo'lsa `--include-leaf-tests` ishlatiladi.

## Loyiha Xususiyatlari

### Telegram CI bot
- Telegram CI botda bir vaqtning o'zida faqat bitta test run faol bo'ladi; run tugaguncha yangi `/run` bloklanadi.
- Telegram CI workflow har soat `00` daqiqada avtomatik smoke run qiladi.
- Telegram CI progress xabari bitta edit-in-place message bo'ladi: `Test boshlandi`, `<Scope> scope tanlangan`, status, `Hozir`, `Passed` ro'yxati va failed bo'lsa `Group/Runner test/Ichki test/Step/Error turi`; workflow final xabar yuborgandan keyin progress message o'chiriladi.
- Telegram CI progress eventlari real-time ko'rinishi uchun GitHub Actions pytestni `-s` bilan, progress wrapperni esa `python -u` bilan ishlatadi; aks holda pytest stdout capture sabab progress xabar `browser o'rnatildi`da qolib ketishi mumkin.
- Telegram CI final xabarida `test-results/data/data_store.json` ichidagi `code` va tanlangan company code asosida `User login: user-pw<code>@<company>` ko'rsatiladi; password xabarga chiqarilmaydi.
- Telegram CI bot GitHub run statusini olishdagi vaqtinchalik network/API xatolarini retry qiladi; faqat ketma-ket 5 marta status olinmasa Telegramga xato yuboradi.

## Test dependency modeli

- User setup testlari ketma-ket va bir-biriga bog'liq: oldingi setup test keyingi setup test uchun kerakli entity yaratadi.
- User setup testlari yaxshi o'tgandan keyin group testlar run qilinadi.
- Group testlar user setup natijalariga bog'liq, lekin boshqa group testlarga bog'liq emas.
- Bir group ichida test yiqilsa, shu groupning qolgan testlari skip qilinadi; keyingi group testlar run bo'lishda davom etadi.
- Run natijasini tahlil qilganda failure setup bosqichidami yoki group bosqichidami aniq ajratib ayt.
- `tests/smoke/test_setup/test_setup_runner.py` ichidagi mavjud barcha testlar user setup testlari hisoblanadi.
- A-group testlari user setupdan keyin run qilinadi; A-groupning birinchi testi order uchun contract yaratadi.
- A-group testlari `tests/smoke/test_groups/test_A_grup/` papkasida saqlanadi; masalan contract testi `tests/smoke/test_groups/test_A_grup/test_contract.py` ichida.
- Order testlarida product chiqmasa, `test_20_init_balance` orqali balans qo'shib kelish yoki bron qilingan orderlarni `Canceled/Отменен` statusga o'tkazish kerak bo'lishi mumkin.
