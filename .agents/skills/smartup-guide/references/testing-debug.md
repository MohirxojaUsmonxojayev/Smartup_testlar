# Testing And Debug

## Qidiruv Kalitlari

Tags: debug, data-store, setup, screenshot, dependency, smoke, regression

### Code Fixture
Tags: code, data-store
- Session `code` setupda yaratiladi.
- Entity nomlari uchun ishlatiladi:
  - `natural_client-pw{code}`
  - `room-pw{code}`
  - `robot-pw{code}`
  - `product-pw{code}`
- Yakka testlarda `code` `test-results/data/data_store.json` dan olinadi.

### Debug Iteratsiyada Precondition Qayta Yaratilmaydi
Tags: debug, data-store, precondition
- Qoida: Test yozish/debug iteratsiyasi paytida precondition entity allaqachon yaratilgan va `data_store.json` ga saqlangan bo'lsa, uni qayta yaratish shart emas.
- Misol: contract code/name mavjud bo'lsa, order testdagi xatoni tekshirish uchun mavjud contractdan foydalan.
- Faqat real chain verification kerak bo'lsa yoki data yo'q bo'lsa precondition test qayta run qilinadi.

### Fresh Database Assumption
Tags: fresh-db, setup, group, data
- Qoida: Yangi testlar har doim yangi server/baza holatida ham ishlashi kerak; lokal debug rerunlari yaratgan mavjud dataga suyanib test yozma.
- Cleanup/cancel qadamlari faqat mavjud data bo'lsa ishlasin; data yo'q bo'lsa no-op bo'lib, test yangi record yaratib davom etsin.
- Testga kerakli entity setup runner yoki shu group ichida yaratilishi kerak; sahifada oldindan record bor deb hisoblama.
- Fresh DB default sozlamalari ham hisobga olinsin: testga kerak bo'lgan feature setting default o'chirilgan bo'lsa, test uni idempotent yoqib keyin asosiy flowga o'tsin.
- Order edit case yozish/debug paytida test yiqilib yarim holat qolsa, keyingi urinishdan oldin shu clientning active orderlarini `Отменен` qilib product bookingni tozala; aks holda edit logikasi eski data bilan buziladi.
- Kelajakda kamaytirib edit qilinadigan order preconditioni minimal quantity bilan yaratilmasin; masalan konsignatsiya edit testi uchun create bosqichida 5 dona yaratilib, editda 4 donaga tushiriladi.

### Masked Input Replace
Tags: debug, input, date, amount, mask
- Smartup date/amount mask inputlarida invalid qiymatdan keyin oddiy `fill()` eski qiymatni almashtirmay ustiga qo'shib yuborishi mumkin.
- Test helper avval inputni focus qilib `ControlOrMeta+A` va `Backspace` bilan tozalasin, keyin yangi value yozib `Tab` bossin.

### Smoke Va Regression
Tags: smoke, regression
- Smoke: forma minimal yurishi uchun majburiy maydonlar va minimal harakatlar.
- Regression: formaning barcha muhim imkoniyatlari, qo'shimcha sozlamalar va kengroq tekshiruvlar.

### Setup Va Group Model
Tags: setup, group, dependency
- `test_smoke_runner.py` ichidagi mavjud testlar user setup testlari.
- Setup testlari ketma-ket va bir-biriga bog'liq.
- Smoke runner bo'yicha har bir test vazifasi va entity naming xaritasi `references/smoke-runner.md` ichida saqlanadi.
- Group testlar user setup natijalariga bog'liq, lekin boshqa grouplarga bog'liq emas.
- Group ichidagi testlar bir-biriga bog'liq bo'lishi mumkin; shu groupda bitta test failed bo'lsa, shu groupning keyingi testlari skip qilinadi.
- Bir group failed bo'lishi boshqa grouplarga ta'sir qilmasin: A failed bo'lsa B/C/D... group testlari run bo'lishi kerak.
- Group testlar boshqa groupning `data_store` keylari, UI state yoki yaratilgan biznes recordlariga suyanmasin; faqat user_setup va o'z group prefixidagi data ishlatilsin.
- Full run mexanizmida user_setup failed bo'lsa barcha group testlar skip qilinadi; user_setup passed bo'lsa group failed statuslari group marker/prefix bo'yicha alohida yuritiladi.
- Grouplar orasida browser/page state leak bo'lmasligi uchun group runnerlar alohida page/context bilan ishlashi yoki har test fresh page ochishi kerak.
- A-group testlari `tests/smoke/test_groups/test_A_grup/` ichida.

### Screenshot Debug Workflow
Tags: screenshot, debug
- Yangi Smartup formaga kirilganda yoki URL/form state o'zgarganda screenshot saqla.
- Saqlash joyi: `test-results/screens/smartup/current/`.
- Naming: `<form-slug>__<state>__<viewport>__<stable-id>.png`.
- Har screenshot uchun `test-results/screens/smartup/meta/` ichida bir xil nomdagi `.json` metadata saqla.
- Screenshotlar kelajakdagi release visual regression uchun baseline/current taqqoslashga tayyor bo'lishi kerak.
- Muammo bo'lsa:
  - avval mavjud screenshotni tekshir
  - yo'q bo'lsa formani ochib screenshot ol
  - keyin locator/test flow yoz

### Xato Case Va Dublikat Kod
Tags: review, duplicate, testcase
- Test yozish, migratsiya yoki debug paytida xato testcase, noto'g'ri flow, ortiqcha murakkablik yoki dublikat kod ko'rinsa, foydalanuvchiga alohida xabar ber.
- Takrorlanadigan UI harakatlar flow/helperga chiqariladi.

### Ish Yakuni Knowledge Capture
Tags: summary, knowledge-capture, dossier
- Har bir Smartup/test vazifasi yakunida bajarilgan ish xulosasi mos skill reference fayllarga yoziladi.
- Agar ish aniq forma bilan bog'liq bo'lsa, avval `references/forms/<form-slug>.md` yangilanadi.
- Agar ish umumiy biznes qoida bo'lsa, `contracts.md` yoki `orders.md` yangilanadi.
- Agar ish locator/modal/grid/screenshot pattern bilan bog'liq bo'lsa, `ui-patterns.md` yangilanadi.
- Xulosa ichida quyilar tartibli bo'lsin: nima qilindi, qaysi fayllar/flowlar tegdi, qanday biznes/UI qoida o'rganildi, screenshot path, known issue yoki keyingi risk.
