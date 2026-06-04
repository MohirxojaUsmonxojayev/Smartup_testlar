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
python scripts/run_tests.py --url https://app3.greenwhite.uz/xtrade
```

Headless run:
```bash
python scripts/run_tests.py --url https://app3.greenwhite.uz/xtrade --headless
```

Regression:
```bash
python scripts/run_tests.py --url https://app3.greenwhite.uz/xtrade --regression
```

Production:
```bash
python scripts/run_tests.py --url https://smartup.online
```

Debug uchun setup yoki group:
```bash
python scripts/run_tests.py setup --url https://app3.greenwhite.uz/xtrade
python scripts/run_tests.py group-a --url https://app3.greenwhite.uz/xtrade
python scripts/run_tests.py group-b --url https://app3.greenwhite.uz/xtrade
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

1. `$ARGUMENTS` bo'sh bo'lsa — to'liq `python scripts/run_tests.py --url <server_url>` ishga tushir
2. `$ARGUMENTS` fayl nomi bo'lsa — faqat shu faylni ishga tushir
3. `$ARGUMENTS` test nomi bo'lsa — faqat shu testni ishga tushir
4. Natijalarni tahlil qil:
   - **PASSED** testlar sonini ko'rsat
   - **FAILED** testlar bo'lsa — xato xabarini o'qib sababini tushuntir
   - `--maxfail=3` limit urilsa ogohlantir
5. Muvaffaqiyatsiz testlar bo'lsa: `test-results/logs/` papkasidagi log fayllarni o'qi va foydalanuvchiga ko'rsat

## Muhim

- Asosiy runner cross-platform: `python scripts/run_tests.py --url <server_url>`; Mac/Linux uchun `./run_tests.sh --url <server_url>` wrapper ham bor.
- Non-production `COMPANY_URL` bo'lsa company setup default ishlaydi; `https://smartup.online` productionda skip bo'ladi.
- Non-productionda yangi company license xaridi uchun company `Активация для лицензии` tabida aktivatsiya qilinishi kerak; activation code bo'lsa buyruqqa `COMPANY_ACTIVATION_CODE=<code>` env qiymatini qo'sh.
- `scripts/run_tests.py` default scope `smoke`; `--regression` berilsa pytestga `--scope regression` uzatiladi.
- Bevosita pytest runlarda scope shunday beriladi: `./.venv/bin/pytest tests/smoke/test_setup/test_setup_runner.py::test_02_legal_person --scope=regression`.
- Scope faqat bitta testga xos emas; all/setup/group runnerlar orqali butun suitega uzatiladigan global mode.
- Smoke natijasini tahlil qilganda minimal path ishlaganini tekshir; regression natijasini tahlil qilganda add form full to'ldirilgani, list check va view check bajarilganini alohida ko'r.
- `pytest.ini` dagi `testpaths = tests` va `addopts` avtomatik qo'llanadi
- Trace fayllari `test-results/traces/` ga, Allure natijalar `test-results/allure-results/` ga yoziladi
- `scripts/run_tests.py` report/trace viewerlarni faqat `--open-report` yoki `--show-trace` bo'lsa ochadi.
- Directory/default collectionda runner bo'lmagan smoke testlar duplicate flow bo'lmasligi uchun deselect qilinadi; kerak bo'lsa `--include-leaf-tests` ishlatiladi.

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
