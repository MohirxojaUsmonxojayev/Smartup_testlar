# Test Arxitekturasi Optimizatsiya Rejasi

Ushbu hujjat Playwright + pytest smoke suite tekshiruvida topilgan kamchiliklarni phase'larga bo'lib tartiblaydi. Maqsad: testlarni kamroq flaky, oson debug qilinadigan, kengaytirishga tayyor va aniq boshqariladigan holatga olib kelish.

## Phase 1: Runner va Test Arxitekturasini Tozalash

**Prioritet:** Yuqori  
**Maqsad:** pytest collection, runner va biznes qadamlar aralashib ketmasin.

### Muammolar

- `test_smoke_runner.py` va `test_a_group_runner.py` boshqa `test_*.py` fayllardagi test funksiyalarni import qilib chaqiryapti.
- Bir xil biznes flow pytest tomonidan alohida test sifatida ham, runner ichida ham collect bo'ladi.
- Allure history, failure diagnosis, retry va fixture lifecycle chalkashadi.

### Ishlar

- Test ichidagi biznes qadamlarni `tests/smoke/flows/` yoki yangi `tests/smoke/steps/` modullariga ko'chirish.
- Runnerlar faqat oddiy step/flow funksiyalarni chaqirsin, `test_...` funksiyalarni emas.
- `test_setup/`, `test_life_cycle/`, `test_groups/` ichidagi test fayllar entrypoint sifatida qolsin.
- A-group runner uchun ham shu patternni qo'llash.

### Kutilgan natija

- `pytest --collect-only` natijasi aniq va dublikat ma'noli testlarsiz bo'ladi.
- Har bir testning Allure history va failure sababi aniqroq ko'rinadi.
- Yangi group qo'shish osonlashadi.

## Phase 2: Run Boshqaruvini Standartlash

**Prioritet:** Yuqori  
**Maqsad:** setup, group va full smoke run aniq boshqarilsin.

### Muammolar

- `run_tests.sh` hozir to'liq smoke emas, faqat A-group runnerni ishlatyapti.
- README va skilllarda `test_smoke_runner.py` asosiy runner deyilgan, script esa boshqa runnerni yurityapti.
- `code` fixture faqat `test_smoke_runner.py` ni full run deb taniydi.

### Ishlar

- `run_tests.sh` ni rejimlarga ajratish:
  - `setup`: faqat user/setup runner.
  - `group-a`: faqat A-group.
  - `all`: avval setup, keyin group testlar.
- `code` fixture uchun aniq boshqaruv qo'shish:
  - `--new-code` CLI option yoki pytest marker.
  - `--reuse-code` yoki default single-test rejimi.
- `README.md`, `run-smoke` skill va `write-test` skilldagi run qoidalarini bir xil qilish.

### Kutilgan natija

- Testni qanday yuritish kerakligi bitta standartga tushadi.
- A-group eski yoki noto'g'ri `data_store.json` ga tasodifan bog'lanib qolmaydi.
- Debug paytida setup va group failure aniq ajraladi.

## Phase 3: Fixture va State Modelini Mustahkamlash

**Prioritet:** Yuqori  
**Maqsad:** `session_page`, `data_store.json` va test state nazorat ostida bo'lsin.

### Muammolar

- Bitta `session_page` faildan keyin keyingi testlarga modal, lock screen yoki noto'g'ri URL qoldirishi mumkin.
- `data_store.json` buzilsa yoki eski bo'lsa testlar noto'g'ri precondition bilan yuradi.
- `save_data` / `load_data` schema yoki required key tekshiruvi yo'q.

### Ishlar

- Har runner testi boshida `clean_state_guard(page)` helper qo'shish:
  - `#biruniConfirm` ochiq bo'lsa yopish.
  - extended alert/NPS/session lock holatini tekshirish.
  - kerakli dashboard yoki expected page statega qaytarish.
- `data_store` helperni kuchaytirish:
  - required key bo'lmasa aniq `AssertionError`.
  - JSON buzilgan bo'lsa aniq xabar.
  - run metadata: `code`, `created_at`, `runner`, `environment`.
- Group test boshlanishida kerakli setup keylarni validate qilish.

### Kutilgan natija

- Domino effect kamayadi.
- Precondition xatolari locator timeoutga aylanib ketmaydi.
- Debug va rerun tezlashadi.

## Phase 4: Locator va Helperlarni Barqarorlashtirish

**Prioritet:** O'rta-Yuqori  
**Maqsad:** UI ozgina o'zgarsa testlar keraksiz sinmasin.

### Muammolar

- `.nth()`, `.first`, `get_by_text()` va Angular `ng-model` locatorlari ko'p.
- JS `evaluate()` clicklar mavjud.
- `page.wait_for_timeout(150)` ishlatilgan.

### Ishlar

- Asosiy form inputlar uchun label/role asosidagi `BasePage` methodlarini standart qilish:
  - `fill_textbox_by_label`
  - `select_b_input_by_label`
  - `expect_b_input_value_by_label`
- JS clicklarni nomlangan helperlarga yig'ish va faqat zarur joyda ishlatish.
- `wait_for_timeout` o'rniga locator state yoki qiymat o'zgarishini kutish.
- Grid row tanlash uchun reusable helper yozish:
  - row text topish.
  - search ishlatish.
  - row count/visibility assert qilish.
- Confirmation modal uchun bitta helper yozish:
  - text assert.
  - opacity `1` kutish.
  - `да` buttonni modal ichida bosish.
  - hidden state kutish.

### Kutilgan natija

- Locator flakiness kamayadi.
- Testlar o'qilishi yaxshilanadi.
- Yangi test yozishda bir xil pattern ishlatiladi.

## Phase 5: Logger, Report va Debug Qatlamini Yaxshilash

**Prioritet:** O'rta  
**Maqsad:** test yiqilganda sababni tez topish.

### Muammolar

- `logger.fail()` testni fail qilmaydi, faqat log yozadi.
- `run_tests.sh` har doim Allure report va trace viewer ochadi.
- Logs/traces retention siyosati yo'q.

### Ishlar

- `logger.fail()` uchun `raise_error=True` yoki `pytest.fail()` qo'llash.
- Failure hookda qo'shimcha attachlar:
  - current URL.
  - page title.
  - active element info.
  - `data_store.json` snapshot.
- `run_tests.sh` uchun optional flaglar:
  - `OPEN_REPORT=1`
  - `SHOW_TRACE=1`
  - `HEADLESS=1`
- Eski `logs` va `traces` uchun cleanup:
  - oxirgi N ta runni saqlash.
  - katta fayllarni tozalash.

### Kutilgan natija

- False pass holatlari kamayadi.
- CI yoki headless run noqulayliksiz ishlaydi.
- Failure analysis tezlashadi.

## Phase 6: Skill va Dokumentatsiyani Sinxronlash

**Prioritet:** O'rta  
**Maqsad:** agentlar va odamlar bir xil qoida bilan ishlasin.

### Muammolar

- `.agents/skills` va `.claude/skills` fayllari farq qiladi.
- `smartup-guide` faqat `.agents/skills` ichida bor.
- README `.env` nomlari bilan real `.env.example` nomlari mos emas.

### Ishlar

- Bitta canonical skill source tanlash.
- Skill sync script yoki qoida qo'shish.
- README env jadvalini real qiymatlarga moslash:
  - `COMPANY_URL`
  - `COMPANY_CODE`
  - `COMPANY_PASSWORD`
  - `USER_PASSWORD`
- `write-test`, `run-smoke`, `debug-test`, `review-test` skilllarini yangi runner modeli bilan yangilash.

### Kutilgan natija

- Codex/Claude/odam bir xil arxitektura qoidalariga amal qiladi.
- Yangi test yozishda eski patternlar qaytmaydi.
- Onboarding osonlashadi.

## Phase 7: Test Dizayni va Qamrovni Tartibga Solish

**Prioritet:** O'rta  
**Maqsad:** smoke, setup va group testlar aniq maqsadga ega bo'lsin.

### Muammolar

- Setup testlar, lifecycle testlar va group testlar orasidagi chegara to'liq formalashmagan.
- Ba'zi testlarda biznes scenario juda katta bitta test ichida turibdi.
- Group ichida failure bo'lsa qolgan testlarni skip qilish qoidasi skillda yozilgan, lekin kodda majburiy emas.

### Ishlar

- Test turlarini aniq belgilash:
  - setup: user/company/environment tayyorlash.
  - group: mustaqil biznes scenario.
  - lifecycle: end-to-end entity lifecycle.
- Group dependency manager yoki marker qo'shish.
- Katta testlarni kichik, aniq maqsadli testlarga ajratish, lekin setup costni hisobga olish.
- Har group boshida precondition validate qilish.

### Kutilgan natija

- Qaysi test nima uchun borligi aniq bo'ladi.
- Failure blast radius kamayadi.
- Yangi B/C group qo'shish osonlashadi.

## Tavsiya Qilingan Tartib

1. Phase 1: runner import anti-patternini yo'qotish.
2. Phase 2: `run_tests.sh` va `code` fixture boshqaruvini tuzatish.
3. Phase 3: state guard va `data_store` validation.
4. Phase 4: eng flaky locator/helperlarni refactor qilish.
5. Phase 5: logger/report/debugni kuchaytirish.
6. Phase 6: skills va README sinxronlash.
7. Phase 7: qamrov va group dependency modelini formalash.

## Minimal Birinchi Sprint

Quyidagi ishlar birinchi sprint uchun eng katta foyda beradi:

- `test_smoke_runner.py` import qilayotgan test funksiyalarni step/flow funksiyalarga ajratish.
- `test_a_group_runner.py` uchun ham shu refactorni qilish.
- `run_tests.sh` ga `setup`, `group-a`, `all` rejimlarini qo'shish.
- `code` fixturega `--new-code` option qo'shish.
- `logger.fail()` testni fail qiladigan qilish.
- `confirm_modal()` helper yozib, eng ko'p ishlatilgan joylarda qo'llash.

## Umumiy Baho

Suite ishlay oladigan holatda va foydali qatlamlar bor: Allure, trace, flowlar, `BasePage`, `data_store`. Asosiy muammo test entrypoint, runner va reusable biznes qadamlar chegarasi aralashganida. Avval shu chegarani tozalash kerak, keyingi optimizatsiyalar shundan keyin ancha osonlashadi.
