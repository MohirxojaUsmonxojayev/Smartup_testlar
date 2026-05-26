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
cd /Users/mac/Documents/projects/Playwright && \
source .venv/bin/activate && \
pytest tests/smoke/test_smoke_runner.py -v
```

### Bitta test fayl:
```bash
pytest tests/smoke/test_setup/test_<nomi>.py -v
```

### Bitta test funksiya:
```bash
pytest tests/smoke/test_smoke_runner.py::test_<nomi> -v
```

### Allure hisobot ko'rish:
```bash
allure serve test-results/allure-results
```

## Ish tartibi

1. `$ARGUMENTS` bo'sh bo'lsa — to'liq `test_smoke_runner.py` ishga tushir
2. `$ARGUMENTS` fayl nomi bo'lsa — faqat shu faylni ishga tushir
3. `$ARGUMENTS` test nomi bo'lsa — faqat shu testni ishga tushir
4. Natijalarni tahlil qil:
   - **PASSED** testlar sonini ko'rsat
   - **FAILED** testlar bo'lsa — xato xabarini o'qib sababini tushuntir
   - `--maxfail=3` limit urilsa ogohlantir
5. Muvaffaqiyatsiz testlar bo'lsa: `test-results/logs/` papkasidagi log fayllarni o'qi va foydalanuvchiga ko'rsat

## Muhim

- `.venv` ni faollashtirish shart
- `pytest.ini` dagi `testpaths = tests` va `addopts` avtomatik qo'llanadi
- Trace fayllari `test-results/traces/` ga, Allure natijalar `test-results/allure-results/` ga yoziladi

## Test dependency modeli

- User setup testlari ketma-ket va bir-biriga bog'liq: oldingi setup test keyingi setup test uchun kerakli entity yaratadi.
- User setup testlari yaxshi o'tgandan keyin group testlar run qilinadi.
- Group testlar user setup natijalariga bog'liq, lekin boshqa group testlarga bog'liq emas.
- Bir group ichida test yiqilsa, shu groupning qolgan testlari skip qilinadi; keyingi group testlar run bo'lishda davom etadi.
- Run natijasini tahlil qilganda failure setup bosqichidami yoki group bosqichidami aniq ajratib ayt.
- `test_smoke_runner.py` ichidagi mavjud barcha testlar user setup testlari hisoblanadi.
- A-group testlari user setupdan keyin run qilinadi; A-groupning birinchi testi order uchun contract yaratadi.
- A-group testlari `tests/smoke/test_groups/test_A_grup/` papkasida saqlanadi; masalan contract testi `tests/smoke/test_groups/test_A_grup/test_contract.py` ichida.
- Order testlarida product chiqmasa, `test_20_init_balance` orqali balans qo'shib kelish yoki bron qilingan orderlarni `Canceled/Отменен` statusga o'tkazish kerak bo'lishi mumkin.
