# Test Natijalarini Ko'rish va Taqdim Qilish — To'liq Qo'llanma

## Mundarija

1. [Test ishga tushganda nima hosil bo'ladi](#1-test-ishga-tushganda-nima-hosil-boladi)
2. [PASS — Test o'tdi](#2-pass--test-otdi)
3. [FAIL — Test xato berdi](#3-fail--test-xato-berdi)
4. [Screenshot mexanizmi](#4-screenshot-mexanizmi)
5. [Playwright Trace Viewer — qadam-qadam tahlil](#5-playwright-trace-viewer--qadam-qadam-tahlil)
6. [Allure Report — chiroyli hisobot](#6-allure-report--chiroyli-hisobot)
7. [Rahbarimga taqdim qilish](#7-rahbarimga-taqdim-qilish)

---

## 1. Test ishga tushganda nima hosil bo'ladi

Test tugagandan so'ng `test-results/` papkasida quyidagi fayllar paydo bo'ladi:

```
test-results/
├── allure-results/          ← Allure uchun xom ma'lumotlar (JSON, PNG)
│   ├── *-result.json        ← Har bir test natijasi
│   ├── *-container.json     ← Test guruhlash ma'lumotlari
│   ├── *-attachment.png     ← FAIL bo'lganda screenshot
│   ├── *-attachment.txt     ← FAIL bo'lganda URL va sarlavha
│   └── environment.properties ← Server URL, company, brauzer ma'lumotlari
│
├── traces/                  ← Playwright trace fayllar
│   ├── tests_regression_test_auth.py__test_admin_login.zip
│   ├── tests_regression_test_auth.py__test_user_login.zip
│   └── tests_regression_test_check_forms_opening.py__test_check_forms_opening.zip
│
├── logs/                    ← Xato log fayllar (faqat FAIL bo'lganda)
│   └── tests_regression_...py__test_name_YYYYMMDD_HHMMSS.log
│
└── data/
    └── data_store.json      ← Sessiya kodi va testlar orasidagi ma'lumotlar
```

---

## 2. PASS — Test o'tdi

Test muvaffaqiyatli tugaganda terminal shunday ko'rinadi:

```
tests/regression/test_check_forms_opening.py::test_check_forms_opening PASSED [100%]
======================== 1 passed in 237.95s (0:03:57) ========================
```

**PASS bo'lganda nima bor:**

| Narsa | Mavjudmi | Qayerda |
|---|---|---|
| Yakuniy natija | ✓ | Terminal |
| Trace fayl | ✓ | `test-results/traces/*.zip` |
| Allure ma'lumotlari | ✓ | `test-results/allure-results/` |
| Screenshot | — | Faqat FAIL bo'lganda saqlanadi |
| Log fayl | — | Faqat FAIL bo'lganda yaratiladi |

**PASS bo'lganda nima qilsa bo'ladi:**

Allure hisobot yaratib ko'rish (ixtiyoriy, rahbarimga ko'rsatish uchun):
```bash
allure generate test-results/allure-results -o test-results/allure-report --clean
allure open test-results/allure-report
```

---

## 3. FAIL — Test xato berdi

Test xato berganda terminal shunday ko'rinadi:

```
tests/regression/test_check_forms_opening.py::test_check_forms_opening FAILED [100%]
[LOG] Xato logi saqlandi: test-results/logs\..._20260623_152647.log

================================== FAILURES ===================================
__________________________ test_check_forms_opening ___________________________

    playwright._impl._errors.Error: Locator.click: Error: strict mode violation:
    get_by_role("link", name="Закупки", exact=True) resolved to 2 elements:
        1) <a href="...">Закупки</a>  ← menu
        2) <a href="...">Закупки</a>  ← sahifa ichida
```

**FAIL bo'lganda avtomatik saqlanadigan narsalar:**

### 3.1 Screenshot (Allure ga biriktilgan)

`conftest.py` da `pytest_runtest_makereport` hook ishlaydi va:
- Xato bo'lgan paytdagi **sahifaning to'liq screenshotini** oladi
- Sahifaning **URL manzilini** saqlaydi
- Sahifaning **sarlavhasini** saqlaydi
- Bularni Allure reportga biriktiradi

Allure reportda FAIL bo'lgan testni ochsangiz, pastda **"Attachments"** bo'limida ko'rasiz:
```
📎 current-url      → https://app3.greenwhite.uz/xtrade/#/...
📎 page-title       → SmartupERP Trade
📎 screenshot       → [sahifa rasmi]
```

### 3.2 Log fayl

`test-results/logs/` papkasida matn fayl saqlanadi:
```
Test:    tests/regression/test_check_forms_opening.py::test_check_forms_opening
Stage:   call
Time:    2026-06-23 15:26:47

--- Xato tafsiloti ---
playwright._impl._errors.Error: Locator.click: Error: ...
```

Log faylni o'qish:
```bash
# Oxirgi log faylni ko'rish
cat test-results/logs/*.log
```

### 3.3 Trace fayl

Har doim (PASS va FAIL) `test-results/traces/` ga `.zip` fayl saqlanadi. FAIL bo'lganda bu faylda xato yuz bergan qadamgacha barcha harakatlar bor.

---

## 4. Screenshot mexanizmi

Loyihada screenshot 2 xil yo'l bilan ishlaydi:

### 4.1 Avtomatik — FAIL bo'lganda (conftest hook)

```
Test ishlaydi
    ↓
Xato yuz beradi (AssertionError yoki PlaywrightError)
    ↓
conftest.py pytest_runtest_makereport hook ishlaydi
    ↓
page.screenshot(full_page=True) → PNG fayl
    ↓
allure.attach(...) → Allure reportga biriktiradi
    ↓
Allure reportda ko'rish mumkin
```

Bu mexanizm **hech narsa yozmasdan ishlaydi** — siz faqat Allure reportni ochasiz.

### 4.2 Playwright Trace — har doim yoniq

Har bir test uchun `context.tracing.start(screenshots=True, ...)` yoqilgan.
Bu degan ma'no: brauzer har bir harakatni (click, navigation, expect) **videofilm** kabi qayd etadi.

Trace fayl ichida:
- Har bir `page.click()`, `page.navigate()` — vaqt bilan
- O'sha paytdagi sahifa holati (snapshot)
- Network so'rovlari
- Console xabarlari

---

## 5. Playwright Trace Viewer — qadam-qadam tahlil

Trace viewer FAIL bo'lganda xato qaysi qadamda yuz berganini aniq ko'rsatadi.

### 5.1 Trace faylni ochish

```bash
# Oxirgi test uchun trace
playwright show-trace "test-results/traces/tests_regression_test_check_forms_opening.py__test_check_forms_opening.zip"

# Auth testi uchun
playwright show-trace "test-results/traces/tests_regression_test_auth.py__test_admin_login.zip"
```

Buyruq kiritilganda brauzerda **Playwright Trace Viewer** ochiladi.

### 5.2 Trace Viewer'da nima ko'rish mumkin

```
┌─────────────────────────────────────────────────────────┐
│  ACTIONS (chap panel)         │  SAHIFA (o'ng panel)     │
│                               │                          │
│  ▶ page.goto(url)       0.5s │  [Tizimga kirish sahifasi│
│  ▶ fill(email)          0.1s │   ko'rinishi]            │
│  ▶ fill(password)       0.1s │                          │
│  ▶ click(Войти)         2.3s │                          │
│  ▶ expect(heading)      0.8s │                          │
│  ● click(Главное)       ❌   │  [Xato yuz bergan holat] │
│                               │                          │
│  Network  Console  Source     │                          │
└─────────────────────────────────────────────────────────┘
```

**Muhim:** Har bir qadamni bosganingizda o'ng tomonda o'sha vaqtdagi sahifa rasmi ko'rinadi. Xatoli qadam ❌ bilan belgilanadi.

### 5.3 Trace Viewer'da xato qidirish

1. Trace faylni oching
2. Chap panelda pastga suring — xatoli qadam qizil yoki ❌ bilan belgilangan
3. O'sha qadamni bosing
4. O'ng tomonda sahifa rasmini ko'ring
5. Pastdagi "Network" tabida so'rovlarni ko'ring
6. "Console" tabida JavaScript xatolarini ko'ring

---

## 6. Allure Report — chiroyli hisobot

Allure — test natijalarini professional ko'rinishdagi veb-sahifaga aylantiruvchi vosita.

### 6.1 Allure o'rnatilganligini tekshirish

```bash
allure --version
```

O'rnatilmagan bo'lsa:
```bash
# Windows (Scoop orqali)
scoop install allure

# yoki npm orqali
npm install -g allure-commandline
```

### 6.2 Hisobot yaratish va ko'rish

**1-qadam: Test ishga tushing**
```bash
pytest tests/regression/test_check_forms_opening.py -v \
  --url https://app3.greenwhite.uz/xtrade \
  --company-code novatrade \
  --company-password greenwhite
```

**2-qadam: Hisobot yarating**
```bash
allure generate test-results/allure-results -o test-results/allure-report --clean
```

**3-qadam: Hisobotni brauzerda oching**
```bash
allure open test-results/allure-report
```

Brauzerda `http://localhost:PORT` manzilida chiroyli hisobot ochiladi.

### 6.3 Allure hisobotida nima bor

**Overview (bosh sahifa):**
```
┌──────────────────────────────────────────────────────────────┐
│  OVERALL      │  SUITES          │  CATEGORIES              │
│               │                  │                          │
│  ✅ 3 PASSED  │ Regression       │ No defects ✓             │
│  ❌ 0 FAILED  │  └ Auth          │                          │
│               │  └ Formalar...   │                          │
│  Duration: 7m │                  │                          │
└──────────────────────────────────────────────────────────────┘
```

**Test tafsiloti (bosganingizda):**
```
test_check_forms_opening  ✅ PASSED  3m 57s

Epic:    Regression
Feature: Formalar ochilishi
Story:   Barcha bo'limlar

Steps:
  ✅ 1 - Tizimga kirish va filial tanlash        2.1s
  ✅ 2 - [Главное] Организации — 'Создать'       1.8s
  ✅ 3 - [Главное] Пользователи — 'Создать'      1.5s
  ...
  ✅ 138 - [Производство] Движение ТМЦ           1.2s
```

**FAIL bo'lganda test tafsiloti:**
```
test_check_forms_opening  ❌ FAILED  1m 20s

Steps:
  ✅ 1 - Tizimga kirish...
  ✅ 2 - [Главное] Организации...
  ...
  ❌ 40 - [Склад] Закупки — 'Создать'  ← Xato shu yerda

Attachments:
  📎 current-url    → https://app3.greenwhite.uz/xtrade/#/...
  📎 page-title     → SmartupERP Trade
  🖼️ screenshot     → [sahifa rasmi]

Error:
  strict mode violation: get_by_role("link", name="Закупки")
  resolved to 2 elements
```

### 6.4 Allure'dagi muhim sahifalar

| Sahifa | Manzil | Nimani ko'rsatadi |
|---|---|---|
| Overview | `/` | Umumiy statistika, grafik |
| Suites | `/suites` | Bo'limlar bo'yicha testlar |
| Timeline | `/timeline` | Testlar qachon ishlagan |
| Categories | `/categories` | Xato turlari |
| Graphs | `/graphs` | Tendensiyalar |

---

## 7. Rahbarimga taqdim qilish

### 7.1 Eng qulay usul: Allure hisobot

Allure hisobotini HTML papka sifatida saqlasangiz, rahbaringiz brauzerda ochishi mumkin:

```bash
# Hisobot yarating
allure generate test-results/allure-results -o test-results/allure-report --clean
```

`test-results/allure-report/` papkasini arxivga solib yuboring — rahbaringiz arxivni ochib, `index.html` ni brauzerda ochsa hisobotni ko'radi.

> **Muhim:** `index.html` ni to'g'ridan-to'g'ri ochish ishlamaydi (CORS cheklov). Papkani lokal server orqali ochish kerak:
> ```bash
> allure open test-results/allure-report
> # yoki
> python -m http.server 8080 --directory test-results/allure-report
> # keyin: http://localhost:8080
> ```

### 7.2 Qisqa og'zaki hisobot (rahbarimga aytish uchun)

Test yakunlangach terminaldan olinadigan asosiy ma'lumot:

```
pytest tests/regression/ -v --url ... --company-code ... --company-password ...

======================== 3 passed in 427.52s (0:07:07) ========================
```

Rahbarimga aytish uchun:
> "Regression testlari o'tkazildi. Jami 3 ta test, 139 ta qadam tekshirildi.
> Barcha natijalar PASSED — tizimning 137 ta formasi xatosiz ochildi.
> Test vaqti: 7 daqiqa 7 soniya."

### 7.3 FAIL bo'lganda rahbarimga aytish uchun

Terminal chiqishidagi xato xabari + Allure dan screenshot:

> "Test #40 — [Склад] Закупки sahifasida muammo aniqlandi.
> Sahifada 2 ta bir xil nomdagi link mavjud — bu tizim UX muammosi.
> Screenshot biriktirilgan. Dasturchilarga xabar berish kerak."

### 7.4 Taqdimot uchun to'liq ketma-ketlik

```
1. Test ishga tushing:
   pytest tests/regression/ -v --url ... --company-code ... --company-password ...

2. Hisobot yarating:
   allure generate test-results/allure-results -o test-results/allure-report --clean

3. Hisobotni oching:
   allure open test-results/allure-report

4. Brauzerda Overview sahifasini ko'rsating

5. Bitta testni bosib, qadamlarni ko'rsating

6. FAIL bo'lsa — u test ichida screenshot va xato xabarini ko'rsating
```

---

## Tezkor ma'lumotnoma

| Holat | Qaerga qaraladi |
|---|---|
| Test o'tdimi/o'tmadimi? | Terminal → `passed` / `failed` |
| Xato qaysi qadamda? | Terminal → `FAILURES` bo'limi |
| Xato paytidagi sahifa rasmi | Allure → test tafsiloti → Attachments |
| Xato paytidagi URL | Allure → test tafsiloti → Attachments |
| Xato xabari matni | `test-results/logs/*.log` fayli |
| Har bir qadamni ko'rish | `playwright show-trace test-results/traces/*.zip` |
| Rahbarimga hisobot | `allure generate` → `allure open` |

---

## Foydali buyruqlar (bitta joyda)

```bash
# Testlarni ishga tushirish
pytest tests/regression/ -v \
  --url https://app3.greenwhite.uz/xtrade \
  --company-code novatrade \
  --company-password greenwhite

# Allure hisobot yaratish
allure generate test-results/allure-results -o test-results/allure-report --clean

# Allure hisobotni brauzerda ochish
allure open test-results/allure-report

# Trace faylni ochish (xatoni qadam-qadam tahlil)
playwright show-trace "test-results/traces/tests_regression_test_check_forms_opening.py__test_check_forms_opening.zip"

# Xato logini o'qish
cat test-results/logs/*.log

# Faqat bir bo'limni tekshirish
pytest tests/regression/test_check_forms_opening.py -v \
  --url https://app3.greenwhite.uz/xtrade \
  --company-code novatrade \
  --company-password greenwhite
```
