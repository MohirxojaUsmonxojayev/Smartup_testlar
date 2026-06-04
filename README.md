# Playwright Smoke Tests — Smartup ERP

Playwright + pytest asosida yozilgan smoke test suite. Allure hisoboti va trace yozish o'rnatilgan.

---

## Mundarija

- [Tezkor boshlash](#tezkor-boshlash)
  - [Loyihani klon qilish](#loyihani-klon-qilish)
  - [Tizim talablarini tekshirish](#tizim-talablarini-tekshirish)
  - [Virtual muhit yaratish va aktivlashtirish](#virtual-muhit)
  - [Python paketlarini o'rnatish](#python-paketlari)
  - [Chromium brauzerini o'rnatish](#chromium)
  - [Test credentiallarini tayyorlash](#test-credentiallari)
  - [Testlarni ishga tushirish va hisobotni ochish](#testlarni-ishga-tushirish)
- [Talablar](#talablar)
- [O'rnatish](#ornatish)
- [Testlarni Run Qilish](#testlarni-run-qilish)
  - [Majburiy Tanlov](#majburiy-tanlov)
  - [Eng Ko'p Ishlatiladigan Buyruqlar](#eng-kop-ishlatiladigan-buyruqlar)
  - [Targetlar](#targetlar)
  - [Mac/Linux Wrapper](#mac-linux-wrapper)
  - [Pytest Orqali Debug](#pytest-orqali-debug)
- [Test qamrovi](#test-qamrovi)
  - [Setup runner](#setup-runner)
  - [Group runnerlar](#group-runnerlar)
- [Test natijalari strukturasi](#test-natijalari)
- [Allure hisoboti](#allure-hisoboti)
  - [Yaratish va ochish](#allure-yaratish-ochish)
  - [Faqat serve qilish](#allure-serve)
- [Trace Viewer](#trace-viewer)
  - [Eng oxirgi traceni ochish](#eng-oxirgi-trace)
  - [Muayyan test traceni ochish](#muayyan-trace)
  - [Trace viewer imkoniyatlari](#trace-imkoniyatlari)
- [Codegen](#codegen)
  - [Ishga tushirish](#codegen-ishga-tushirish)
  - [Foydalanish tartibi](#codegen-foydalanish)
- [Foydali buyruqlar](#foydali-buyruqlar)

---

## <a id="tezkor-boshlash"></a>🚀 Tezkor boshlash — gitdan klon qilgandan hisobot olgungacha

Loyihani yangi olgan odam quyidagi qadamlarni **ketma-ket** bajaradi. Buyruqlar **macOS, Linux va Windows** uchun alohida berilgan — o'z tizimingizdagi varianti bo'yicha yuring. Oxirida testlar ishga tushadi va Allure hisoboti brauzerda ochiladi.

### <a id="loyihani-klon-qilish"></a>1. Loyihani klon qilish

Barcha tizimlarda bir xil:

```bash
git clone https://github.com/turgunovjasur/Playwright.git
cd Playwright
```

### <a id="tizim-talablarini-tekshirish"></a>2. Tizim talablarini tekshirish

**macOS / Linux:**
```bash
python3 --version      # 3.11+ bo'lishi kerak
allure --version
```

**Windows (PowerShell):**
```powershell
python --version       # 3.11+ bo'lishi kerak
allure --version
```

Allure CLI yo'q bo'lsa (barchasi uchun Java JDK 8+ ham kerak):

| Tizim   | O'rnatish buyrug'i |
|---------|--------------------|
| macOS   | `brew install allure` |
| Linux   | `brew install allure` yoki [scoop/manual](https://allurereport.org/docs/install/) |
| Windows | `scoop install allure` yoki `choco install allure-commandline` ([qo'llanma](https://allurereport.org/docs/install/)) |

> Python yo'q bo'lsa → https://www.python.org/downloads/ (Windowsda o'rnatishda **"Add Python to PATH"** ni belgilang).

### <a id="virtual-muhit"></a>3. Virtual muhit yaratish va aktivlashtirish

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

> Windows PowerShell'da script ishga tushmasa (execution policy xatosi), bir marta:
> `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`

### <a id="python-paketlari"></a>4. Python paketlarini o'rnatish

Virtual muhit aktiv bo'lgach, barcha tizimda bir xil:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### <a id="chromium"></a>5. Chromium brauzerini o'rnatish

```bash
python -m playwright install chromium
```

> Linuxda birinchi marta tizim kutubxonalari yetishmasa: `python -m playwright install-deps chromium` (sudo so'rashi mumkin).

### <a id="test-credentiallari"></a>6. Test credentiallarini tayyorlash

`.env` ishlatilmaydi. Test run qilishda `--url` har doim majburiy, keyin ikki mode'dan biri tanlanadi:

- Mavjud company bilan: `--company-code` va `--company-password`
- Yangi company bilan: `--create-company`

### <a id="testlarni-ishga-tushirish"></a>7. Testlarni ishga tushirish va hisobotni ochish

Barcha tizimda bir xil (cross-platform Python runner):

```bash
python scripts/run_tests.py --url <server_url> --company-code <company_code> --company-password <company_password> --open-report
```

macOS / Linuxda qisqa wrapper ham bor:

```bash
./run_tests.sh --url <server_url> --company-code <company_code> --company-password <company_password> --open-report
```

Bu bitta buyruq: eski natijalarni tozalaydi → smoke testlarni o'tkazadi → Allure hisobotini yaratadi → brauzerda ochadi.

> Yangi company yaratish kerak bo'lsa `--create-company` ishlating. Yangi company admin paroli kod ichida belgilangan default qiymat bo'ladi.

✅ Tayyor — hisobot brauzerda ochiladi. Keyinroq hisobotni qayta ochish uchun: `allure open test-results/allure-report`.

---

## <a id="talablar"></a>Talablar

- Python 3.11+
- [Allure CLI](https://allurereport.org/docs/install/) (`brew install allure`)

---

## <a id="ornatish"></a>O'rnatish

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

---

## <a id="testlarni-run-qilish"></a>Testlarni Run Qilish

Asosiy runner:

```bash
python scripts/run_tests.py [target] --url <server_url> [company mode] [options]
```

Bu buyruq macOS, Linux va Windowsda ishlaydi. `.env` ishlatilmaydi.

### <a id="majburiy-tanlov"></a>Majburiy Tanlov

Har bir run uchun `--url` majburiy. Keyin ikki company mode'dan bittasi tanlanadi:

| Mode | Buyruq | Nima bo'ladi |
|------|--------|--------------|
| Mavjud company | `--company-code <code> --company-password <password>` | Company yaratilmaydi, testlar berilgan company bilan ishlaydi |
| Yangi company | `--create-company` | Suite boshida `00 - Company` ishlaydi, yangi company yaratiladi |

Qoidalar:

- `--create-company` bilan `--company-code` va `--company-password` berilmaydi.
- `--create-company` mode'da yangi company admin password kod ichida belgilangan default qiymat bo'ladi.
- Test user password ham kod ichida belgilangan.
- `--disable-license-policy` faqat `--create-company` bilan ishlaydi.
- `--disable-license-policy` berilsa company viewda `Политика лицензирования` off qilinadi va license testlari skip bo'ladi.
- `--disable-license-policy` berilmasa license policy off qilinmaydi va license testlari skip qilinmaydi.

### <a id="eng-kop-ishlatiladigan-buyruqlar"></a>Eng Ko'p Ishlatiladigan Buyruqlar

Mavjud company bilan full smoke:

```bash
python scripts/run_tests.py --url <server_url> --company-code <company_code> --company-password <company_password>
```

Yangi company yaratib full smoke:

```bash
python scripts/run_tests.py --url <server_url> --create-company
```

Yangi company yaratib, license policy off qilish:

```bash
python scripts/run_tests.py --url <server_url> --create-company --disable-license-policy
```

Reportni testdan keyin ochish:

```bash
python scripts/run_tests.py --url <server_url> --company-code <company_code> --company-password <company_password> --open-report
```

Headless rejim:

```bash
python scripts/run_tests.py --url <server_url> --company-code <company_code> --company-password <company_password> --headless
```

Regression scope:

```bash
python scripts/run_tests.py --url <server_url> --company-code <company_code> --company-password <company_password> --regression
```

Trace viewer ochish:

```bash
python scripts/run_tests.py --url <server_url> --company-code <company_code> --company-password <company_password> --show-trace
```

Buyruqni ishga tushirmasdan ko'rish:

```bash
python scripts/run_tests.py --url <server_url> --create-company --disable-license-policy --dry-run
```

### <a id="targetlar"></a>Targetlar

Default target `all`, ya'ni full suite.

| Target | Buyruq namunasi | Nima ishlaydi |
|--------|------------------|---------------|
| `all` | `python scripts/run_tests.py --url <url> --company-code <code> --company-password <pass>` | Setup + A group + B group |
| `setup` | `python scripts/run_tests.py setup --url <url> --company-code <code> --company-password <pass>` | Faqat user setup |
| `company` | `python scripts/run_tests.py company --url <url> --create-company` | Faqat company yaratish testi |
| `group-a` | `python scripts/run_tests.py group-a --url <url> --company-code <code> --company-password <pass>` | Faqat A group |
| `group-b` | `python scripts/run_tests.py group-b --url <url> --company-code <code> --company-password <pass>` | Faqat B group |

`--create-company` faqat `all`, `setup`, `company` targetlari bilan ishlatiladi. `group-a` yoki `group-b` uchun avval mavjud company va setup data kerak.

### <a id="mac-linux-wrapper"></a>Mac/Linux Wrapper

macOS va Linuxda `./run_tests.sh` ham ishlaydi, argumentlar `python scripts/run_tests.py` bilan bir xil:

```bash
./run_tests.sh --url <server_url> --company-code <company_code> --company-password <company_password>
```

### <a id="pytest-orqali-debug"></a>Pytest Orqali Debug

Asosiy run uchun `scripts/run_tests.py` ishlatish tavsiya qilinadi. Debug uchun to'g'ridan-to'g'ri pytest yuritish mumkin:

```bash
./.venv/bin/pytest tests/smoke/test_all_runner.py --new-code --url <server_url> --company-code <company_code> --company-password <company_password> -v
```

Yangi company bilan:

```bash
./.venv/bin/pytest tests/smoke/test_all_runner.py --new-code --url <server_url> --create-company -v
```

---

> **Muhim:** User setup testlari bir-biriga bog'liq — har biri oldingi test yaratgan ma'lumotdan foydalanadi.
> Shuning uchun full smoke uchun **`test_all_runner.py`**, setup uchun esa **`test_setup_runner.py`** ishlatiladi. Oddiy `pytest` yoki directory collection duplicate flowlarni yurgizmasligi uchun default holatda runner bo'lmagan smoke testlar deselect qilinadi; kerak bo'lsa `--include-leaf-tests` ishlatiladi.

---

## <a id="test-qamrovi"></a>Test qamrovi

`tests/smoke/test_all_runner.py` — barcha runnerlarni jamlaydi va mavjud runner fayllarini ketma-ket chaqiradi: user setup, keyin A va B group runnerlar.

`tests/smoke/test_setup/test_setup_runner.py` — user setup testlari **bitta browser sessiyasida** ketma-ket ishlaydi.

Group runnerlar — har bir group boshida user sifatida bir marta login qiladi, group ichidagi testlar shu oynada davom etadi. Group tugaganda yoki failed bo'lganda oyna/context yopiladi; keyingi group yangi oyna va yangi login bilan boshlanadi.

### <a id="setup-runner"></a>Setup runner

| # | Test nomi              | Nima tekshiriladi                                     |
|---|------------------------|-------------------------------------------------------|
| 00 | Company               | `--create-company` bilan company yaratish va code saqlash |
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

### <a id="group-runnerlar"></a>Group runnerlar

| Group | Testlar | Nima tekshiriladi |
|-------|---------|-------------------|
| A | A-01 ... A-05 | Contract yaratish, payment type sharti, contract limit validatsiyasi, order yaratish va edit qilish |
| B | B-01 ... B-02 | Konsignatsiya limiti bilan order yaratish, edit qilish va konsignatsiya summasini bo'lish |

> **Eslatma:** `test_setup_runner.py` user setup runner bo'lib, setup testlari bilan bir papkada turadi.

---

## <a id="test-natijalari"></a>Test natijalari strukturasi

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

## <a id="allure-hisoboti"></a>Allure hisoboti

### <a id="allure-yaratish-ochish"></a>Yaratish va ochish

```bash
# Natijalardan hisobot yaratish
allure generate test-results/allure-results -o test-results/allure-report --clean

# Hisobotni brauzerda ochish
allure open test-results/allure-report
```

### <a id="allure-serve"></a>Faqat serve qilish (papkani yaratmasdan)

```bash
allure serve test-results/allure-results
```

---

## <a id="trace-viewer"></a>Trace Viewer

Test xato bo'lganda Playwright avtomatik `.zip` trace saqlaydi.

### <a id="eng-oxirgi-trace"></a>Eng oxirgi traceni ochish

```bash
playwright show-trace $(ls -t test-results/traces/*.zip | head -1)
```

### <a id="muayyan-trace"></a>Muayyan test traceni ochish

```bash
# Fayl nomini ko'rish
ls test-results/traces/

# Kerakli traceni ochish
playwright show-trace test-results/traces/smoke_trace.zip
```

### <a id="trace-imkoniyatlari"></a>Trace viewer imkoniyatlari

- **Timeline** — har bir action vaqt bo'yicha
- **Screenshots** — har bir qadam skrinshotlari
- **Network** — barcha tarmoq so'rovlari
- **Console** — brauzer konsol xabarlari
- **Source** — test kodi qaysi qatorda ekanligini ko'rsatadi

---

## <a id="codegen"></a>Codegen — locator yozishda yordam

Playwright Codegen brauzerda harakatlarni yozib, avtomatik test kodi generatsiya qiladi. Yangi locator topishda ishlatiladi.

### <a id="codegen-ishga-tushirish"></a>Ishga tushirish

```bash
# URL ga o'tib codegen ochish
playwright codegen <server_url>

# Login sahifasidan boshlash
playwright codegen <server_url>/login.html
```

### <a id="codegen-foydalanish"></a>Foydalanish tartibi

1. `playwright codegen <url>` buyrug'ini terminalda ishga tushiring
2. Brauzerda kerakli sahifaga o'ting va amallarni bajaring
3. Hosil bo'lgan kodni o'ng oynadan nusxa olib test fayliga qo'ying
4. Kerak bo'lmagan qatorlarni olib tashlang

> Codegen yozgan locatorlarni to'g'ridan-to'g'ri ishlatmasdan, mavjud `flow_navigate.py`, `flow_authorization.py` patterlariga mos tarzda adaptatsiya qiling.

---

## <a id="foydali-buyruqlar"></a>Foydali buyruqlar

```bash
# Testlarni headless rejimda ishlatish
python scripts/run_tests.py --url <server_url> --company-code <company_code> --company-password <company_password> --headless

# Faqat muvaffaqiyatsiz testlarni qayta ishlatish
./.venv/bin/pytest tests/smoke/test_all_runner.py --reuse-code --url <server_url> --company-code <company_code> --company-password <company_password> --lf

# Xato bo'lganda darhol to'xtatish
./.venv/bin/pytest tests/smoke/test_all_runner.py --new-code --url <server_url> --company-code <company_code> --company-password <company_password> -x

# Verbose + to'liq xato traceback
./.venv/bin/pytest tests/smoke/test_all_runner.py --new-code --url <server_url> --company-code <company_code> --company-password <company_password> -v --tb=long
```
