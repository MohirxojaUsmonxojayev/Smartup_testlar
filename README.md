# Playwright Smoke Tests — Smartup ERP

Playwright + pytest asosida yozilgan smoke test suite. Allure hisoboti va trace yozish o'rnatilgan.

---

## Talablar

- Python 3.11+
- [Allure CLI](https://allurereport.org/docs/install/) (`brew install allure`)

---

## O'rnatish

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

---

## Muhit o'zgaruvchilari

Credentials `.env` fayldan o'qiladi. `.env` gitga kirmaydi — har kim o'zini yaratadi:

```bash
cp .env.example .env
# keyin .env ni o'z qiymatlari bilan to'ldiradi
```

| O'zgaruvchi    | Tavsif                  |
|----------------|-------------------------|
| `COMPANY_URL`  | Test muhiti manzili     |
| `COMPANY_CODE` | Kompaniya kodi          |
| `COMPANY_PASSWORD` | Admin parol        |
| `USER_PASSWORD` | Test user paroli       |
| `COMPANY_ACTIVATION_CODE` | Yangi companyda license sotib olish uchun activation code (non-production full run uchun kerak bo'lishi mumkin) |

> `.env.example` — xavfsiz namuna fayl, gitda saqlanadi. `.env` — haqiqiy credentials, **gitga kirmaydi**.

---

## Testlarni ishga tushirish

### Tavsiya etilgan — to'liq tsikl (test + allure hisobot)

```bash
python scripts/run_tests.py --url https://app3.greenwhite.uz/xtrade
```

Bu buyruq:
1. Eski natijalarni tozalaydi (history saqlanadi)
2. Smoke runner testlarini o'tkazadi
3. Allure hisobotini yaratadi
4. Productiondan boshqa serverlarda company setupni avtomatik ishlatadi
5. `--open-report` bo'lsa hisobotni brauzerda ochadi

> Non-production serverda yangi company yaratilganda `Лицензии` sahifasi uchun company viewdagi `Активация для лицензии` tabida activation kerak bo'lishi mumkin. Bunday full run uchun `COMPANY_ACTIVATION_CODE=<code>` env qiymatini ham bering.

---

### Cross-platform variantlar

```bash
# Production: company setup skip
python scripts/run_tests.py --url https://smartup.online

# Headless rejimda
python scripts/run_tests.py --url https://app3.greenwhite.uz/xtrade --headless

# Yangi company license aktivatsiyasi bilan (macOS/Linux)
COMPANY_ACTIVATION_CODE=<code> python scripts/run_tests.py --url https://app3.greenwhite.uz/xtrade --headless

# Yangi company license aktivatsiyasi bilan (Windows PowerShell)
$env:COMPANY_ACTIVATION_CODE="<code>"; python scripts/run_tests.py --url https://app3.greenwhite.uz/xtrade --headless

# Regression scope
python scripts/run_tests.py --url https://app3.greenwhite.uz/xtrade --regression

# Testdan keyin eng oxirgi traceni ochish
python scripts/run_tests.py --url https://app3.greenwhite.uz/xtrade --show-trace

# Reportni ochish
python scripts/run_tests.py --url https://app3.greenwhite.uz/xtrade --open-report
```

### Mac/Linux wrapper

```bash
./run_tests.sh --url https://app3.greenwhite.uz/xtrade
```

### Faqat pytest orqali debug qilish

```bash
./.venv/bin/pytest tests/smoke/test_all_runner.py -v
```

---

> **Muhim:** User setup testlari bir-biriga bog'liq — har biri oldingi test yaratgan ma'lumotdan foydalanadi.
> Shuning uchun full smoke uchun **`test_all_runner.py`**, setup uchun esa **`test_setup_runner.py`** ishlatiladi. Oddiy `pytest` yoki directory collection duplicate flowlarni yurgizmasligi uchun default holatda runner bo'lmagan smoke testlar deselect qilinadi; kerak bo'lsa `--include-leaf-tests` ishlatiladi.

---

## Test qamrovi

`tests/smoke/test_all_runner.py` — barcha runnerlarni jamlaydi va mavjud runner fayllarini ketma-ket chaqiradi: user setup, keyin A va B group runnerlar.

`tests/smoke/test_setup/test_setup_runner.py` — user setup testlari **bitta browser sessiyasida** ketma-ket ishlaydi.

Group runnerlar — har bir group boshida user sifatida bir marta login qiladi, group ichidagi testlar shu oynada davom etadi. Group tugaganda yoki failed bo'lganda oyna/context yopiladi; keyingi group yangi oyna va yangi login bilan boshlanadi.

### Setup runner

| # | Test nomi              | Nima tekshiriladi                                     |
|---|------------------------|-------------------------------------------------------|
| 00 | Company               | Non-production serverlarda company yaratish va code saqlash |
| 01 | Authorization         | Login, dashboard yuklanishi                           |
| 02 | Legal Person          | Yuridik shaxs yaratish va qidirish                   |
| 03 | Filial                | Organizatsiya yaratish, valyuta va yuridik shaxs bog'lash |
| 04 | Room                  | Ish zonasi yaratish                                   |
| 05 | Robot                 | Shtat birligini yaratish                              |
| 06 | Natural Person        | Jismoniy shaxs yaratish                               |
| 07 | User                  | Foydalanuvchi yaratish va robot/jismoniy shaxs bog'lash |
| 08 | User Attach Form      | Foydalanuvchiga formalar biriktirish                  |
| 09 | Role                  | Admin roliga barcha ruxsatlar berish                  |
| 10 | Role Attach Form      | Rolga barcha formlarga kirish ruxsatini berish        |
| 11 | Buy License           | Litsenziya sotib olish                                |
| 12 | Attach License        | Foydalanuvchiga litsenziya biriktirish                |
| 13 | Change Password       | Yangi foydalanuvchi parolini o'zgartirish             |
| 14 | Price Type            | Narx turini yaratish                                  |
| 15 | Payment Type          | To'lov turlarini biriktirish                          |
| 16 | Sector                | TMT to'plami (Набор ТМЦ) yaratish                    |
| 17 | Product               | TMT (mahsulot) yaratish                               |
| 18 | Natural Person For Client_1 | Qo'shimcha client uchun jismoniy shaxs yaratish |
| 19 | Room Attachment       | Ish zonasiga kerakli bog'lanishlarni biriktirish      |
| 20 | Init Balance          | Boshlang'ich qoldiq uchun hujjat yaratish             |
| 21 | Balance               | Qoldiq/harakatlar hayot siklini tekshirish            |

### Group runnerlar

| Group | Testlar | Nima tekshiriladi |
|-------|---------|-------------------|
| A | A-01 ... A-05 | Contract yaratish, payment type sharti, contract limit validatsiyasi, order yaratish va edit qilish |
| B | B-01 ... B-02 | Konsignatsiya limiti bilan order yaratish, edit qilish va konsignatsiya summasini bo'lish |

> **Eslatma:** `test_setup_runner.py` user setup runner bo'lib, setup testlari bilan bir papkada turadi.

---

## Test natijalari strukturasi

```
test-results/
├── allure-results/          # pytest tomonidan yoziladigan xom natijalar
│   ├── history/             # Trend grafigi uchun tarix
│   ├── environment.properties
│   ├── executor.json
│   └── categories.json
├── allure-report/           # Allure CLI tomonidan render qilingan HTML
├── data/                    # Runnerlar orasida ishlatiladigan saqlangan code va test ma'lumotlari
│   └── data_store.json
├── playwright/              # pytest-playwright output papkasi
├── traces/                  # Playwright trace fayllari (.zip)
│   ├── smoke_trace.zip      # session_page ishlatgan testlar (to'liq sessiya)
│   └── *.zip                # group/page fixture ishlatgan testlar uchun alohida
└── logs/                    # Muvaffaqiyatsiz testlar uchun log fayllar
    └── *.log
```

---

## Allure hisoboti

### Yaratish va ochish

```bash
# Natijalardan hisobot yaratish
allure generate test-results/allure-results -o test-results/allure-report --clean

# Hisobotni brauzerda ochish
allure open test-results/allure-report
```

### Faqat serve qilish (papkani yaratmasdan)

```bash
allure serve test-results/allure-results
```

---

## Trace Viewer

Test xato bo'lganda Playwright avtomatik `.zip` trace saqlaydi.

### Eng oxirgi traceni ochish

```bash
playwright show-trace $(ls -t test-results/traces/*.zip | head -1)
```

### Muayyan test traceni ochish

```bash
# Fayl nomini ko'rish
ls test-results/traces/

# Kerakli traceni ochish
playwright show-trace test-results/traces/smoke_trace.zip
```

### Trace viewer imkoniyatlari

- **Timeline** — har bir action vaqt bo'yicha
- **Screenshots** — har bir qadam skrinshotlari
- **Network** — barcha tarmoq so'rovlari
- **Console** — brauzer konsol xabarlari
- **Source** — test kodi qaysi qatorda ekanligini ko'rsatadi

---

## Codegen — locator yozishda yordam

Playwright Codegen brauzerda harakatlarni yozib, avtomatik test kodi generatsiya qiladi. Yangi locator topishda ishlatiladi.

### Ishga tushirish

```bash
# COMPANY_URL ga o'tib codegen ochish
playwright codegen https://smartup.online

# Login sahifasidan boshlash
playwright codegen https://smartup.online/login.html
```

### Foydalanish tartibi

1. `playwright codegen <url>` buyrug'ini terminalda ishga tushiring
2. Brauzerda kerakli sahifaga o'ting va amallarni bajaring
3. Hosil bo'lgan kodni o'ng oynadan nusxa olib test fayliga qo'ying
4. Kerak bo'lmagan qatorlarni olib tashlang

> Codegen yozgan locatorlarni to'g'ridan-to'g'ri ishlatmasdan, mavjud `flow_navigate.py`, `flow_authorization.py` patterlariga mos tarzda adaptatsiya qiling.

---

## Foydali buyruqlar

```bash
# Testlarni headless rejimda ishlatish
HEADLESS=1 ./.venv/bin/pytest tests/smoke/test_all_runner.py --headless

# Faqat muvaffaqiyatsiz testlarni qayta ishlatish
./.venv/bin/pytest tests/smoke/test_all_runner.py --lf

# Xato bo'lganda darhol to'xtatish
./.venv/bin/pytest tests/smoke/test_all_runner.py -x

# Verbose + to'liq xato traceback
./.venv/bin/pytest tests/smoke/test_all_runner.py -v --tb=long
```
