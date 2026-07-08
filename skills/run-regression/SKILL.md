---
name: run-regression
description: Regression testlarni ishga tushirish. "regression run", "regression testlarni ishga tushir", "regression tekshir" so'ralganda ishlatiladi.
allowed-tools: Bash, Read, PowerShell
---

# Regression Testlarni Ishga Tushirish

Argument: `$ARGUMENTS` (test nomi, target yoki bo'sh)

## Mavjud targetlar

| Target | Fayl | Izoh |
|---|---|---|
| `regression` | `tests/regression/` | Barcha regression testlar |
| `regression-forms` | `tests/regression/test_check_forms_opening.py` | Faqat forma ochilish testi |
| `regression-auth` | `tests/regression/test_auth.py` | Faqat autentifikatsiya testi |

## Buyruqlar

### Barcha regression testlar:
```bash
python scripts/run_tests.py regression --url https://app3.greenwhite.uz/xtrade --company-code moxir@novatrade --company-password 1
```

### Faqat forma testi:
```bash
python scripts/run_tests.py regression-forms --url https://app3.greenwhite.uz/xtrade --company-code moxir@novatrade --company-password 1
```

### Faqat auth testi:
```bash
python scripts/run_tests.py regression-auth --url https://app3.greenwhite.uz/xtrade --company-code moxir@novatrade --company-password 1
```

### Headless rejimda:
```bash
python scripts/run_tests.py regression --url https://app3.greenwhite.uz/xtrade --company-code moxir@novatrade --company-password 1 --headless
```

## Ish tartibi

1. `$ARGUMENTS` bo'sh bo'lsa — `regression` (barcha) target ishga tushir
2. `$ARGUMENTS` da `forms` so'zi bo'lsa — `regression-forms` ishga tushir
3. `$ARGUMENTS` da `auth` so'zi bo'lsa — `regression-auth` ishga tushir
4. Buyruqni **background**da ishga tushir (uzoq vaqt ketadi)
5. Natija kelgach tahlil qil:
   - **PASSED** sonini ko'rsat
   - **FAILED** bo'lsa — `test-results/logs/` dan xato o'qi va sababini tushuntir
   - Davomiylikni (vaqtni) ko'rsat

## Muhim

- Server: `https://app3.greenwhite.uz/xtrade`
- Company: `moxir@novatrade`, parol: `1`
- Regression testlar smoke testlarga bog'liq emas — mustaqil run bo'ladi
- `regression-forms` testi barcha formalar ochilishini tekshiradi (~4-5 daqiqa)
- `regression-auth` testi login/logout stsenariylarini tekshiradi
- Allure report: `test-results/allure-report/`
