# Smoke Runner Setup Chain

## Qidiruv Kalitlari

Tags: smoke, setup, runner, dependency, data-store, license, balance, tmc, room, user

### 2026-05-25 Run Natijasi
Tags: smoke, run-result, sandbox
- Buyruq: `./.venv/bin/pytest tests/smoke/test_smoke_runner.py -v --tb=short`
- Natija: 21 passed, 0 failed, umumiy vaqt 196.22s.
- Session code: `1384`; `test_01_authorization` `test-results/data/data_store.json` ichidagi `code` qiymatini yangiladi.
- `data_store.json` ichidagi A-group `contract_*` va `order_id` qiymatlari bu runnerda yangilanmadi; ular avvalgi run code qiymatlariga tegishli bo'lishi mumkin.
- Trace: `test-results/traces/smoke_trace.zip` saqlandi.
- Eslatma: sandbox ichida Chromium Crashpad permission xatosi bilan browser ochilmadi; sandboxdan tashqarida xuddi shu runner passed bo'ldi.

### Runner Qoidasi
Tags: smoke, setup, dependency, data-store
- `tests/smoke/test_smoke_runner.py` ichidagi testlar bitta `session_page` bilan ketma-ket ishlaydi; UI state va login holati testlar orasida saqlanadi.
- `code` fixture full runnerda yangi random 4 xonali qiymat beradi; yakka testlarda `test-results/data/data_store.json` dan o'qiladi.
- `test_01_authorization` `save_data("code", code)` orqali yangi code ni keyingi yakka/debug testlar uchun saqlaydi.
- Smoke runner `data_store.json` ni tozalab qayta yaratmaydi; faqat `code` yozadi. Shu sabab group testlardan qolgan eski `contract_*` yoki `order_id` qiymatlarini smoke setupning hozirgi code qiymati bilan bir xil deb qabul qilmaslik kerak.
- Setup zanjiri buzilsa keyingi testlar ham precondition yo'qligi sabab yiqilishi mumkin; yakka testdan oldin to'liq runner yoki mos precondition ma'lumotlari kerak.

### Entity Naming
Tags: smoke, entity, naming
- Legal person: `cod_lg_pw{code}` / `legal_person-pw{code}`.
- Filial/organization: `filial-pw{code}`; yuridik shaxs `cod_lg_pw{code}` ga ulanadi.
- Room/work zone: `code_room_pw{code}` / `room-pw{code}`.
- Robot/staff: `code_robot-pw{code}` / `robot-pw{code}`.
- Employee natural person: `natural_person-pw{code}`.
- User: `user-pw{code}{COMPANY_CODE}`; password `USER_PASSWORD`.
- Price type: `code_price_type_uzb_pw{code}` / `Price Type UZB-pw{code}`.
- Sector/TMC set: `code_sector_pw{code}` / `sector-pw{code}`.
- Product/TMC: `code_product-pw{code}` / `product-pw{code}`; price `7000`.
- Client natural person: `natural_client-pw{code}`.
- Init balance document number: `{code}`; quantity `100`, price `5000`, expected posting sum `500 000`.

## Testlar Tartibi Va Vazifasi

### 01 Authorization
Tags: authorization, data-store
- Fayl/flow: `tests/smoke/test_smoke_runner.py`, `tests/smoke/flows/flow_authorization.py`.
- Nima qiladi: admin sifatida login qiladi va `Trade` dashboard headingini kutadi.
- Nima saqlaydi: session `code` qiymatini `data_store.json` ga yozadi.

### 02 Legal Person
Tags: legal-person, setup
- Fayl: `tests/smoke/test_setup/test_legal_person.py`.
- Navigation: `Справочники` -> `Юридические лица`.
- Nima yaratadi: `cod_lg_pw{code}` kodli, `legal_person-pw{code}` nomli yuridik shaxs.
- Tekshiruv: ro'yxatda code va nom search orqali ko'rinadi; save uchun `#biruniConfirm` modalida `да` bosiladi.

### 03 Filial
Tags: filial, organization, legal-person
- Fayl: `tests/smoke/test_setup/test_filial.py`.
- Navigation: `Главное` -> `Организации`.
- Nima yaratadi: `filial-pw{code}` tashkilot/filial.
- Bog'lanish: valyuta `Узбекский сум`, yuridik shaxs `cod_lg_pw{code}`.
- Tekshiruv: ro'yxatda filial va legal person code ko'rinadi; keyin sahifa reload va loader kutish bor.

### 04 Room
Tags: room, filial, work-zone
- Fayl: `tests/smoke/test_setup/test_room.py`.
- Precondition: `switch_filial(page, name=f"filial-pw{code}")`.
- Navigation: `Справочники` -> `Рабочие зоны`.
- Nima yaratadi: `code_room_pw{code}` / `room-pw{code}` ish zonasi.
- Tekshiruv: saqlagandan keyin `Рабочие зоны` ro'yxatida code va nom ko'rinadi.

### 05 Robot
Tags: robot, staff, room
- Fayl: `tests/smoke/test_setup/test_robot.py`.
- Navigation: `Справочники` -> `Штат`.
- Nima yaratadi: `code_robot-pw{code}` / `robot-pw{code}` xodim.
- Bog'lanish: `Админ` tanlanadi va `room-pw{code}` ish zonasi ulanadi.

### 06 Natural Person
Tags: natural-person, employee
- Fayl: `tests/smoke/test_setup/test_natural_person.py`.
- Precondition: `filial-pw{code}` filialiga o'tadi.
- Navigation: `Справочники` -> `Физические лица`.
- Nima yaratadi: xodim uchun `natural_person-pw{code}` jismoniy shaxs.
- Tekshiruv: save confirmdan keyin ro'yxatda nom ko'rinadi.

### 07 User
Tags: user, robot, natural-person
- Fayl: `tests/smoke/test_setup/test_user.py`.
- Navigation: `Главное` -> `Пользователи`.
- Nima yaratadi: `user-pw{code}{COMPANY_CODE}` loginli user.
- Bog'lanish: `robot-pw{code}` va `natural_person-pw{code}` ulanadi; password `USER_PASSWORD`.
- Tekshiruv: user ro'yxatida natural person va login ko'rinadi.

### 08 User Attach Form
Tags: user, permissions, forms
- Fayl: `tests/smoke/test_setup/test_user.py`.
- Nima qiladi: user view ichida `Формы` sahifasini ochib `Формы`, `Отчеты`, `Накладные`, `Внешние системы` tablaridagi mavjud elementlarni userga ulaydi.
- Muhim pattern: page size `1000` qilinadi, `BasePage.click_js()` orqali birinchi checkbox/select all bosiladi, `#biruniConfirm` orqali tasdiqlanadi.
- Tekshiruv: har bo'limda `Доступные` ro'yxati `нет данных` bo'lishi kerak.

### 09 Role
Tags: role, permissions
- Fayl: `tests/smoke/test_setup/test_user.py`.
- Navigation: `Пользователи` sahifasidan `Роли`.
- Nima qiladi: `Админ` rolini edit qilib, `.switch span` ichidagi barcha `нет` switchlarni yoqadi.
- Muhim pattern: onboarding launcher JS orqali yashiriladi; saqlashdan keyin loader 600s gacha kutiladi.

### 10 Role Attach Form
Tags: role, forms, permissions
- Fayl: `tests/smoke/test_setup/test_user.py`.
- Nima qiladi: `Админ` rol viewidagi `Формы` bo'limida `Доступ ко всем формам` -> `Разрешить` qiladi.
- Tekshiruv: `Доступные` ro'yxati `нет данных` bo'ladi.

### 11 Buy License
Tags: license, admin, balance
- Fayl: `tests/smoke/test_setup/test_license.py`.
- Nima qiladi: logout qilib admin sifatida qayta kiradi, `Администрирование` filialiga o'tadi, `Главное` -> `Лицензии` sahifasida balans musbatligini tekshiradi va `Smartup ERP` uchun 1 ta license sotib oladi.
- Kerakli ma'lumotlar: payer `AUTOTEST GWS`, contract `Договор № bn от 01.01.2025`, begin date today.
- Log: balans musbat bo'lsa `Balans musbat — Success`, sotib olinsa `Litsenziya olindi`.

### 12 Attach License
Tags: license, user
- Fayl: `tests/smoke/test_setup/test_license.py`.
- Nima qiladi: `Лицензии и документы` ichida `ERP users` license ochiladi, mavjud attached users bo'lsa ajratiladi, `natural_person-pw{code}` userga ulanadi.
- Muhim pattern: `PlaywrightTimeoutError` orqali `нет данных` bo'lmasa hammasini select qilib `Открепить` qiladi.

### 13 Change Password
Tags: user, password
- Fayl: `tests/smoke/test_setup/test_user.py`.
- Nima qiladi: yangi `user-pw{code}{COMPANY_CODE}` login bilan kiradi; majburiy password change alert chiqishini kutadi.
- Amaliyot: current/new/rewrite password maydonlariga `USER_PASSWORD` kiritib `Подтвердить` va confirm `да` bosadi.

### 14 Price Type
Tags: price-type, room, nps
- Fayl: `tests/smoke/test_setup/test_price_type.py`.
- Nima qiladi: NPS Survey modal chiqsa 10 ball bilan yuboradi; `Справочники` -> `Цены` sahifasida UZB price type yaratadi.
- Bog'lanish: `room-pw{code}` ish zonasi ulanadi; `Цена продажи` ko'rinishi tekshiriladi.
- Tekshiruv: `Price Type UZB-pw{code}` searchdan keyin ro'yxatda ko'rinadi.

### 15 Payment Type
Tags: payment-type, room-attachment
- Fayl: `tests/smoke/test_setup/test_payment_type.py`.
- Nima qiladi: `Цены` -> `Типы оплат` ichida `Прикрепление` orqali barcha 4 payment typeni tizimga ulaydi.
- Tekshiruv: `Наличные деньги`, `Перечисление`, `Терминал`, `Чековая книжка` ro'yxatda ko'rinadi.

### 16 Sector
Tags: tmc, sector, room
- Fayl: `tests/smoke/test_setup/test_sector.py`.
- Nima yaratadi: `Наборы ТМЦ` ichida `code_sector_pw{code}` / `sector-pw{code}` TMC to'plami.
- Bog'lanish: `room-pw{code}` tanlanadi.

### 17 Product
Tags: tmc, product, price
- Fayl: `tests/smoke/test_setup/test_product.py`.
- Nima yaratadi: `ТМЦ` ichida `code_product-pw{code}` / `product-pw{code}` mahsulot.
- Bog'lanish: measure `шт`, product type `Товар`, sahifada `sector-pw{code}` ko'rinishi precondition sifatida tekshiriladi.
- Qo'shimcha: `Установить цены` orqali gridga `7000` narx yozib saqlaydi.

### 18 Natural Person For Client 1
Tags: natural-person, client
- Fayl: `tests/smoke/test_setup/test_natural_person.py`.
- Nima yaratadi: `natural_client-pw{code}` jismoniy shaxs, `Клиент` belgisi yoqiladi.
- Tekshiruv: avval `Физические лица`, keyin `Клиенты` ro'yxatida ko'rinadi.

### 19 Room Attachment
Tags: room, payment-type, warehouse, cashbox, client
- Fayl: `tests/smoke/test_setup/test_room.py`.
- Nima qiladi: yangi user sifatida kirib `room-pw{code}` ish zonasi `Прикрепление` sahifasiga kiradi.
- Bog'lanishlar: 4 payment type, 1 warehouse, 1 cashbox va `natural_client-pw{code}` client ish zonasiga ulanadi.
- Tekshiruv: payment/warehouse/cashbox available listlari `нет данных`; client attached listida `natural_client-pw{code}` ko'rinadi.

### 20 Init Balance
Tags: inventory, init-balance, product
- Fayl: `tests/smoke/test_life_cycle/init_balance.py`.
- Nima qiladi: `authorization_user(page, code)` bilan user sifatida kiradi, `Склад` -> `Ввод начальных остатков ТМЦ` sahifasida boshlang'ich qoldiq hujjati yaratadi.
- Hujjat: number `{code}`, product `code_product-pw{code}`, quantity `100`, price `5000`.
- Tekshiruv: hujjat o'tkazilgandan keyin `Проводки` popupida `100` va `500 000` borligi tekshiriladi.

### 21 Balance
Tags: inventory, balance, product
- Fayl: `tests/smoke/test_life_cycle/balance.py`.
- Navigation: `Склад` -> `Остатки ТМЦ`.
- Tekshiruv: qoldiq sahifasida `code_product-pw{code}` ko'rinadi.
