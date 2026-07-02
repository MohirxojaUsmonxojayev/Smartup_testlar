# Scenario 1 Developer Test Cases

Bu hujjat `test_ui_runner.py` ichidagi Scenario 1 UI autotestlari asosida tuzildi. Maqsad: developer uchun autotest ishlaganda bo'ladigan biznes ketma-ketlikni alohida testcase'lar ko'rinishida berish.

Izoh:
- `Dependency` qismi runner ketma-ketligi va test ichidagi real `load_data`/test data ishlatilishiga qarab yozildi.
- `Expected result` qismi unit/integration test yozishda tekshirilishi kerak bo'lgan asosiy natijani ko'rsatadi.
- Manbalar: `tests/ui/...` fayllari va `test_ui_runner.py`.

## 1. Setup va Reference

### TC-REF-001 Create Legal Person
- Source: `tests/ui/test_reference/test_legal_person.py::test_add_legal_person`
- Dependency: yo'q
- Preconditions: admin login ishlashi kerak; `anor/mr/person/legal_person_list` ochilishi kerak.
- Steps:
1. Admin legal person list sahifasiga kiradi.
2. Add forma ochiladi.
3. Legal person ma'lumotlari kiritiladi: name, short name, phone, telegram, email, address, tin, cea, vat code, code, web, barcode, zip code.
4. Save qilinadi.
5. Yangi yozuv code bo'yicha listdan topiladi va view ochiladi.
6. View va card maydonlari kiritilgan qiymatlar bilan solishtiriladi.
- Expected result:
1. Legal person yaratiladi.
2. List va view ichida asosiy atributlar to'g'ri ko'rinadi.
3. `legal_person_cod` saqlanadi.

### TC-SET-002 Create Filial
- Source: `tests/ui/test_order/test_life_cycle.py::test_filial_create`
- Dependency: `TC-REF-001 Create Legal Person`
- Preconditions: base currency `860` mavjud; `legal_person_name` tizimda mavjud.
- Steps:
1. Admin `anor/mr/filial_list` ga kiradi.
2. Filial add forma ochiladi.
3. Filial nomi, base currency va legal person tanlanadi.
4. Save qilinadi.
5. Filial listda qidiriladi va view ochiladi.
6. Filial nomi tekshiriladi.
7. Project checkbox'lari belgilanib save qilinadi.
- Expected result:
1. Filial yaratiladi.
2. Filial nomi view sahifada to'g'ri chiqadi.
3. Project sozlamalari saqlanadi.

### TC-SET-003 Create Room
- Source: `tests/ui/test_order/test_life_cycle.py::test_room_add`
- Dependency: `TC-SET-002 Create Filial`
- Preconditions: filial mavjud va admin shu filialga o'ta olishi kerak.
- Steps:
1. Admin filial kontekstida `trade/trf/room_list` ga kiradi.
2. Add forma ochiladi.
3. Room name kiritiladi.
4. Save qilinadi.
5. Listdan yozuv topilib view ochiladi.
6. Room nomi tekshiriladi.
- Expected result: room yaratiladi va view ichida nomi mos bo'ladi.

### TC-SET-004 Create Robot
- Source: `tests/ui/test_order/test_life_cycle.py::test_robot_add`
- Dependency: `TC-SET-003 Create Room`
- Preconditions: room mavjud; role `Админ` mavjud.
- Steps:
1. Admin filial kontekstida `anor/mrf/robot_list` ga kiradi.
2. Robot add forma ochiladi.
3. Robot name, role va room tanlanadi.
4. Save qilinadi.
5. Listdan yozuv topilib view ochiladi.
6. Robot name tekshiriladi.
- Expected result: robot yaratiladi va room hamda role bilan bog'lanadi.

### TC-SET-005 Create Sub Filial
- Source: `tests/ui/test_order/test_life_cycle.py::test_sub_filial_add`
- Dependency: `TC-SET-004 Create Robot`
- Preconditions: room mavjud.
- Steps:
1. Admin filial kontekstida `anor/mrf/subfilial_list` ga kiradi.
2. Add forma ochiladi.
3. Sub filial name va room tanlanadi.
4. Save qilinadi.
5. List reload qilinib yozuv qidiriladi.
- Expected result: sub filial yaratiladi va room bilan bog'lanadi.

### TC-REF-006 Create Natural Person
- Source: `tests/ui/test_reference/test_natural_person.py::test_natural_person_add`
- Dependency: yo'q
- Preconditions: filial mavjud.
- Steps:
1. Admin filial kontekstida natural person listga kiradi.
2. Add forma ochiladi.
3. Faqat person name kiritiladi.
4. Save qilinadi.
5. Listda topilib view ochiladi.
6. View sarlavhasi tekshiriladi.
- Expected result: natural person yaratiladi.

### TC-SET-007 Create User
- Source: `tests/ui/test_order/test_life_cycle.py::test_user_create`
- Dependency: `TC-SET-004 Create Robot`, `TC-REF-006 Create Natural Person`
- Preconditions: natural person va robot mavjud.
- Steps:
1. Admin filial kontekstida user listga kiradi.
2. Add forma ochiladi.
3. Natural person, password, login va robot tanlanadi.
4. Save qilinadi.
5. Listdan user topilib view ochiladi.
6. Natural person nomi tekshiriladi.
7. View ichida bir nechta formalar attach qilinadi.
- Expected result: user yaratiladi va dastlabki form access'lar biriktiriladi.

### TC-SET-008 Grant Role Permissions
- Source: `tests/ui/test_order/test_life_cycle.py::test_adding_permissions_to_user`
- Dependency: `TC-SET-007 Create User`
- Preconditions: `Админ` roli mavjud.
- Steps:
1. Admin role listga kiradi.
2. `Админ` roli edit qilinadi.
3. Checkbox quantity va permission checkbox'lar tanlanadi.
4. Save qilinadi.
5. Role view ochiladi.
6. Access all form permission beriladi.
- Expected result: role uchun permission'lar to'liq yoqiladi.

### TC-LIC-009 Attach User License
- Source: `tests/ui/test_license/test_license.py::test_add_user_license`
- Dependency: `TC-SET-007 Create User`
- Preconditions: user login ishlashi kerak; admin login ishlashi kerak; license moduli ochilishi kerak.
- Steps:
1. Yangi user bilan login qilinadi.
2. Retry/back orqali login oqimi tekshiriladi.
3. Admin bilan qayta login qilinadi.
4. Alohida oynada `biruni/kl/license_list` ochiladi.
5. License/documents bo'limiga o'tiladi.
6. `ERP users` hujjati tanlanadi.
7. Natural person user license'ga attach qilinadi.
- Expected result: user license biriktiriladi.

### TC-LIC-010 Purchase License
- Source: `tests/ui/test_license/test_license.py::test_add_purchase_license`
- Dependency: `TC-SET-007 Create User`
- Preconditions: payer balance va contract mavjud bo'lishi kerak.
- Steps:
1. Admin license listga kiradi.
2. Purchase bo'limi ochiladi.
3. Payer, contract, begin date va license count bilan purchase qilinadi.
4. Agar purchase talablarini qondirsa modal content yopiladi.
5. Balance qayta o'qilib purchase summasi ayrilgani tekshiriladi.
- Expected result: license purchase bo'ladi va payer balance kamayadi.

### TC-SET-011 Change User Password
- Source: `tests/ui/test_order/test_life_cycle.py::test_user_change_password`
- Dependency: `TC-SET-007 Create User`
- Preconditions: user login bo'lishi va change password oynasi chiqishi kerak.
- Steps:
1. User bilan login qilinadi.
2. Change password forma ochiladi.
3. New, rewritten va current password kiritiladi.
4. Save qilinadi.
- Expected result: password muvaffaqiyatli yangilanadi.

### TC-REF-012 Create Price Type UZB
- Source: `tests/ui/test_reference/test_price_type.py::test_price_type_add_UZB`
- Dependency: `TC-SET-003 Create Room`
- Preconditions: room mavjud.
- Steps:
1. User `anor/mkr/price_type_list` ga kiradi.
2. Add forma ochiladi.
3. Price type name, room va currency `Узбекский сум` tanlanadi.
4. Save qilinadi.
5. View orqali nom tekshiriladi.
6. Qo'shimcha price type turlari attach qilinadi: `Промо`, `Акция`, `Возврат`, `Передача забаланс`, `Обмен`.
- Expected result: UZB price type yaratiladi va qo'shimcha turlar attach qilinadi.

### TC-REF-013 Create Price Type USA
- Source: `tests/ui/test_reference/test_price_type.py::test_price_type_add_USA`
- Dependency: `TC-SET-003 Create Room`, `TC-SET-005 Create Sub Filial`
- Preconditions: room va sub filial mavjud.
- Steps:
1. User price type listga kiradi.
2. Add forma ochiladi.
3. Price type name, room, currency `Доллар США` va sub filial tanlanadi.
4. Save qilinadi.
5. View orqali nom tekshiriladi.
- Expected result: USA price type yaratiladi.

### TC-REF-014 Attach Payment Types
- Source: `tests/ui/test_order/test_life_cycle.py::test_payment_type_add`
- Dependency: yo'q
- Preconditions: payment type attach dialog ishlashi kerak.
- Steps:
1. User `anor/mkr/payment_type_list` ga kiradi.
2. Attach oynasi ochiladi.
3. Barcha payment type checkbox'lari belgilanadi.
4. Oyna yopiladi.
- Expected result: roomlar uchun ishlatiladigan payment type'lar attach holatiga keladi.

### TC-REF-015 Create Sector
- Source: `tests/ui/test_order/test_life_cycle.py::test_sector_add`
- Dependency: `TC-SET-003 Create Room`
- Preconditions: room mavjud.
- Steps:
1. User sector listga kiradi.
2. Add forma ochiladi.
3. Sector name va room tanlanadi.
4. Save qilinadi.
5. View ochilib sector name tekshiriladi.
- Expected result: sector yaratiladi.

### TC-REF-016 Create Product-1 and Set Prices
- Source: `tests/ui/test_reference/test_product.py::test_product_add_as_product_1`
- Dependency: `TC-REF-015 Create Sector`, `TC-REF-012 Create Price Type UZB`, `TC-REF-013 Create Price Type USA`
- Preconditions: sector va ikki valyutadagi price type mavjud.
- Steps:
1. User inventory listga kiradi.
2. Add forma ochiladi.
3. Ixtiyoriy foto qo'shish urinib ko'riladi, xato bo'lsa modal yopiladi.
4. Product name, sector, measurement, goods flag, netto/brutto/litre qiymatlari kiritiladi.
5. Save qilinadi.
6. View orqali product name tekshiriladi.
7. Set price oynasi ochiladi.
8. UZB va USA price type uchun narxlar kiritiladi.
- Expected result: product yaratiladi va ikkala price type bo'yicha narxlar saqlanadi.

### TC-REP-017 Check Price Tag Report
- Source: `tests/ui/test_order/test_life_cycle.py::test_check_price_tag`
- Dependency: `TC-REF-012 Create Price Type UZB`, `TC-REF-016 Create Product-1 and Set Prices`
- Preconditions: product narxi o'rnatilgan bo'lishi kerak.
- Steps:
1. User price type listga kiradi.
2. UZB price type uchun price tag oynasi ochiladi.
3. Product tanlanadi.
4. Price tag report generate qilinadi.
5. `Ценник.xlsx` fayli yuklanganligi tekshiriladi.
- Expected result: price tag report muvaffaqiyatli yuklanadi.

### TC-FIN-018 Add Currency Rate USA
- Source: `tests/ui/test_finance/test_currency.py::test_currency_add_USA`
- Dependency: yo'q
- Preconditions: `Доллар США` currency tizimda mavjud.
- Steps:
1. User currency listga kiradi.
2. `Доллар США` view ochiladi.
3. Rate tab ochilib yangi exchange rate kiritiladi.
4. Save qilinadi.
5. Yangi row ko'rinishi tekshiriladi.
- Expected result: USD kursi qo'shiladi.

### TC-REF-019 Add Margin
- Source: `tests/ui/test_order/test_life_cycle.py::test_margin_add`
- Dependency: yo'q
- Preconditions: margin attach oynasi ishlashi kerak.
- Steps:
1. Admin margin listga kiradi va eski attach holat bo'lsa tozalaydi.
2. User margin listga kiradi.
3. Attach oynasidan yangi margin yaratadi.
4. Margin name, percent value va percent type kiritadi.
5. Save qiladi.
6. Margin attach qilinadi.
- Expected result: margin yaratiladi va roomlar uchun attach bo'ladi.

### TC-REF-020 Create Natural Person Client A
- Source: `tests/ui/test_reference/test_natural_person.py::test_natural_person_client_add_A`
- Dependency: yo'q
- Preconditions: filial mavjud.
- Steps: `TC-REF-006` bilan bir xil, faqat name `client-...-A`.
- Expected result: client A uchun natural person yaratiladi.

### TC-REF-021 Create Natural Person Client B
- Source: `tests/ui/test_reference/test_natural_person.py::test_natural_person_client_add_B`
- Dependency: yo'q
- Steps: `TC-REF-006` bilan bir xil, faqat name `client-...-B`.
- Expected result: client B uchun natural person yaratiladi.

### TC-REF-022 Create Natural Person Client C
- Source: `tests/ui/test_reference/test_natural_person.py::test_natural_person_client_add_C`
- Dependency: yo'q
- Steps: `TC-REF-006` bilan bir xil, faqat name `client-...-C`.
- Expected result: client C uchun natural person yaratiladi.

### TC-REF-023 Create Client A
- Source: `tests/ui/test_reference/test_client.py::test_client_add_A`
- Dependency: `TC-REF-020 Create Natural Person Client A`
- Preconditions: natural person client A mavjud.
- Steps:
1. User client listga kiradi.
2. Add forma ochiladi.
3. Radio tanlanadi va client A name kiritiladi.
4. Save qilinadi.
5. Listdan topilib view ochiladi.
- Expected result: client A yaratiladi.

### TC-REF-024 Create Client B
- Source: `tests/ui/test_reference/test_client.py::test_client_add_B`
- Dependency: `TC-REF-021 Create Natural Person Client B`
- Steps: `TC-REF-023` bilan bir xil, faqat client B.
- Expected result: client B yaratiladi.

### TC-REF-025 Create Client C
- Source: `tests/ui/test_reference/test_client.py::test_client_add_C`
- Dependency: `TC-REF-022 Create Natural Person Client C`
- Steps: `TC-REF-023` bilan bir xil, faqat client C.
- Expected result: client C yaratiladi.

### TC-SET-026 Attach Room Configuration
- Source: `tests/ui/test_order/test_life_cycle.py::test_room_attachment`
- Dependency: `TC-SET-004`, `TC-REF-012`, `TC-REF-013`, `TC-REF-014`, `TC-REF-015`, `TC-REF-019`, `TC-REF-023`, `TC-REF-024`, `TC-REF-025`
- Preconditions: room va barcha attach qilinadigan obyektlar mavjud.
- Steps:
1. User room listga kiradi va kerakli room uchun attachment ochadi.
2. Price type'lar attach qilinadi.
3. Payment type'lar attach qilinadi.
4. Margin type'lar attach qilinadi.
5. Warehouse attach qilinadi.
6. Cash register attach qilinadi.
7. Client A, B, C roomga attach qilinadi.
8. Oyna yopiladi.
- Expected result: room barcha kerakli ma'lumotlar bilan to'liq konfiguratsiya qilinadi.

### TC-WH-027 Initialize Inventory Balance
- Source: `tests/ui/test_order/test_life_cycle.py::test_init_balance`
- Dependency: `TC-SET-026 Attach Room Configuration`, `TC-REF-016 Create Product-1 and Set Prices`
- Preconditions: product va warehouse roomga attach bo'lishi kerak.
- Steps:
1. User init balance listga kiradi.
2. Add forma ochiladi.
3. Balance number, product, card code, quantity va price kiritiladi.
4. Save qilinadi.
5. Yozuv listdan topilib post qilinadi.
6. Balance report orqali product qoldig'i o'qiladi.
- Expected result: boshlang'ich ombor qoldig'i yaratiladi va quantity balansga tushadi.

## 2. Group A - Order with Consignment

### TC-FIN-028 Create Contract Client A UZB
- Source: `tests/ui/test_finance/test_contract.py::test_add_contract_for_client_A_UZB`
- Dependency: `TC-REF-023 Create Client A`, `TC-REF-012 Create Price Type UZB`
- Preconditions: client A mavjud.
- Steps:
1. User contract listga kiradi.
2. Add forma ochiladi.
3. Contract number, contract name, client A, currency `Узбекский сум` va initial amount kiritiladi.
4. Save qilinadi.
5. View ichida contract name va currency tekshiriladi.
- Expected result: client A uchun UZB contract yaratiladi.

### TC-SET-029 Enable Consignment Setting
- Source: `tests/ui/test_order/test_life_cycle.py::test_setting_consignment`
- Dependency: yo'q
- Preconditions: system setting oynasi ochilishi kerak.
- Steps:
1. User `trade/pref/system_setting` ga kiradi.
2. `Заказ` bo'limiga o'tadi.
3. Consignment checkbox yoqiladi.
4. Day limit `90` kiritiladi.
5. Save qilinadi.
- Expected result: consignment setting yoqiladi.

### TC-ORD-030 Create Order with Consignment
- Source: `tests/ui/test_order/test_order.py::test_add_order_with_consignment`
- Dependency: `TC-SET-029`, `TC-FIN-028`
- Preconditions: room, robot, client A, product, warehouse, UZB price type, payment type mavjud.
- Steps:
1. User order listga kiradi va add boshlaydi.
2. Main step'da room, robot va client A tanlanadi.
3. Deal time va delivery date o'qiladi.
4. Product step'da product, warehouse, price type va quantity `15` kiritiladi.
5. Final step'da payment type, consignment day `30`, consignment amount va status `Draft` tanlanadi.
6. Save qilinadi.
7. Listdan client bo'yicha topilib view ochiladi.
8. Order ID saqlanadi va summary maydonlari tekshiriladi.
- Expected result:
1. Consignment order yaratiladi.
2. Status `Draft`, client, room, robot va summa to'g'ri bo'ladi.
3. `order_id_1` saqlanadi.

### TC-REP-031 Check Order List Reports
- Source: `tests/ui/test_order/order_report/test_order_report.py::test_check_report_for_order_list`
- Dependency: `TC-ORD-030 Create Order with Consignment`
- Preconditions: client A uchun order mavjud.
- Steps:
1. User order listga kiradi.
2. Client A order topiladi.
3. Report menyudagi barcha asosiy hisobotlar ketma-ket ochiladi.
4. Har bir report alohida oynada verify qilinadi.
- Expected result: order list reportlari ochiladi va xatoga tushmaydi.

### TC-ORD-032 Edit Consignment Order
- Source: `tests/ui/test_order/test_order_edit.py::test_edit_order_with_consignment`
- Dependency: `TC-ORD-030 Create Order with Consignment`
- Preconditions: `order_id_1` saqlangan bo'lishi kerak.
- Steps:
1. User order listga kiradi.
2. Order ID bo'yicha order edit qilinadi.
3. Product quantity `10` ga o'zgartiriladi.
4. Consignment validation xabari tekshiriladi.
5. Draft status saqlanadi.
6. View ichida consignment tab bo'sh holat tekshiriladi.
7. Order status `New` ga o'tkaziladi.
- Expected result: edit paytida consignment validation ishlaydi va order keyingi statusga o'tadi.

### TC-ORD-033 Copy/Search Filter in Order List
- Source: `tests/ui/test_order/test_order_list.py::test_copy_search_filter_in_order_list`
- Dependency: `TC-ORD-032 Edit Consignment Order`
- Preconditions: consignment order mavjud bo'lishi kerak.
- Steps:
1. Order list ochiladi.
2. Mavjud order bo'yicha copy, search va filter amallari bajariladi.
3. Copy qilingan order view/list ichida tekshiriladi.
4. Yangi order ID saqlanadi.
- Expected result: listdagi copy va filter funksiyalari ishlaydi, `order_id_2` saqlanadi.

### TC-REP-034 Sales Report Constructor
- Source: `tests/ui/test_order/test_order_report.py::test_sales_report_constructor`
- Dependency: `TC-ORD-030 Create Order with Consignment`
- Preconditions: `order_id_1` va `order_id_2` mavjud bo'lishi kerak.
- Steps:
1. User sales report constructorga kiradi.
2. `Заказ` maydoni report row sifatida tanlanadi.
3. Status filter maydoni tozalanadi.
4. Report view qilinadi.
5. Iframe ichidan order ID lar ro'yxati olinadi.
6. `order_id_1` va `order_id_2` report ichida borligi tekshiriladi.
- Expected result: sales report constructor kerakli orderlarni qaytaradi.

### TC-ORD-035 Change Status Draft to Cancelled Flow
- Source: `tests/ui/test_order/test_order_change_status.py::test_order_change_status_from_draft_to_cancelled`
- Dependency: `TC-ORD-033 Copy/Search Filter in Order List`
- Preconditions: `order_id_1` va `order_id_2` mavjud.
- Steps:
1. `order_id_2` uchun status ketma-ket o'zgartiriladi: `New -> Processing -> Pending -> Shipped -> Delivered -> Cancelled`.
2. Har bir oraliq statusdan keyin view orqali status tekshiriladi.
3. `order_id_1` alohida `Archive` statusga o'tkaziladi.
- Expected result: status lifecycle to'liq ishlaydi va har bosqich view da to'g'ri aks etadi.

### TC-REP-036 Check Order History Reports
- Source: `tests/ui/test_order/order_report/test_order_report.py::test_check_report_for_order_history_list`
- Dependency: `TC-ORD-035 Change Status Draft to Cancelled Flow`
- Preconditions: client A order history'da ko'rinishi kerak.
- Steps:
1. User order history listga kiradi.
2. Client A order topiladi.
3. Order history reportlari ketma-ket ochilib verify qilinadi.
- Expected result: order history reportlari ochiladi.

### TC-CASH-037 Add Cashin A
- Source: `tests/ui/test_cashin/test_cashin.py::test_cashin_add_A`
- Dependency: `TC-REF-014 Attach Payment Types`, `TC-REF-023 Create Client A`
- Preconditions: client A uchun qarzdorlik yoki summa aniqlanishi kerak.
- Steps:
1. User cashin listga kiradi.
2. Add forma ochiladi.
3. Cashin number, client A, payment type va cashbox tanlanadi.
4. Tizimdan amount olinadi yoki berilgan summa ishlatiladi.
5. Save qilinadi va close qilinadi.
6. View ichida cashin number tekshiriladi.
7. Cashin post qilinadi.
- Expected result: client A uchun cashin yaratiladi va post bo'ladi.

### TC-CASH-038 Add Offset A
- Source: `tests/ui/test_offset/test_offset.py::test_offset_add_A`
- Dependency: `TC-CASH-037 Add Cashin A`
- Preconditions: client A bo'yicha offset detail mavjud bo'lishi kerak.
- Steps:
1. User offset listga kiradi.
2. Client A detail oynasi ochiladi.
3. Offset action tanlanadi.
4. Offset ichida client balance `0` ekanligi tekshiriladi.
5. Post qilinadi.
- Expected result: client A uchun offset yopiladi va balans nolga teng bo'ladi.

## 3. Group B - Order with Contract

### TC-FIN-039 Create Contract Client B UZB
- Source: `tests/ui/test_finance/test_contract.py::test_add_contract_for_client_B_UZB`
- Dependency: `TC-REF-024 Create Client B`, `TC-REF-012 Create Price Type UZB`
- Steps: `TC-FIN-028` bilan bir xil, faqat client B va initial amount kattaroq.
- Expected result: client B uchun contract yaratiladi.

### TC-ORD-040 Create Order with Contract
- Source: `tests/ui/test_order/test_order.py::test_add_order_with_contract`
- Dependency: `TC-FIN-039 Create Contract Client B UZB`
- Preconditions: contract B, client B, product va room konfiguratsiyasi mavjud.
- Steps:
1. User order addni boshlaydi.
2. Main step'da room, robot, client B va contract B tanlanadi.
3. Product step'da product quantity `101` beriladi.
4. Final step'da payment type va status `Draft` bilan save uriniladi.
5. Contract bo'yicha validation xatosi tekshiriladi.
6. Orqaga qaytib quantity `15` ga tushiriladi.
7. Order qayta save qilinadi.
8. View orqali status, client, room va robot tekshiriladi.
9. `order_id_3` saqlanadi.
- Expected result: contract limiti validation ishlaydi va to'g'ri quantity bilan order yaratiladi.

### TC-ORD-041 Change Status Draft to Archive
- Source: `tests/ui/test_order/test_order_change_status.py::test_change_status_draft_and_archive`
- Dependency: `TC-ORD-040 Create Order with Contract`
- Preconditions: `order_id_3` mavjud.
- Steps:
1. Order view orqali boshlang'ich status `Draft` tekshiriladi.
2. Status `Archive` ga o'tkaziladi.
- Expected result: contract order arxivga o'tkaziladi.

### TC-CASH-042 Add Offset B with Payment
- Source: `tests/ui/test_offset/test_offset.py::test_offset_add_B`
- Dependency: `TC-ORD-041 Change Status Draft to Archive`
- Preconditions: client B bo'yicha payment offset mumkin bo'lishi kerak.
- Steps:
1. User offset detailga kiradi.
2. Payment action tanlanadi.
3. Cashbox tanlanadi.
4. Payment summasi offset ichidan olinadi.
5. Post va confirmation qilinadi.
6. Alohida oynada cashin list ochilib yaratilgan cashin view tekshiriladi.
- Expected result: payment-based offset yaratiladi va cashin summasi offset balance bilan mos bo'ladi.

## 4. Group C - Order with USA Price Type

### TC-FIN-043 Create Contract Client C USA
- Source: `tests/ui/test_finance/test_contract.py::test_add_contract_for_client_C_USA`
- Dependency: `TC-REF-025 Create Client C`, `TC-REF-013 Create Price Type USA`
- Preconditions: sub filial mavjud.
- Steps:
1. User contract listga kiradi.
2. Client C uchun USD contract yaratiladi.
3. Currency `Доллар США`, sub filial va initial amount kiritiladi.
4. View orqali contract name va currency tekshiriladi.
- Expected result: client C uchun USD contract yaratiladi.

### TC-ORD-044 Create Order with USA Price Type
- Source: `tests/ui/test_order/test_order.py::test_add_order_for_price_type_USA`
- Dependency: `TC-FIN-043 Create Contract Client C USA`
- Preconditions: USA price type va margin mavjud.
- Steps:
1. User order addni boshlaydi.
2. Main step'da room, robot va client C tanlanadi.
3. Product step'da product, warehouse, USA price type, quantity `20` va margin kiritiladi.
4. Final step'da payment type va status `New` tanlanadi.
5. Save qilinadi.
6. View orqali status, client, room, robot tekshiriladi.
7. `order_id_4` saqlanadi.
8. File, transaction va attach data oynalari ochilib ko'riladi.
- Expected result: USD order yaratiladi va bog'liq file/transaction/attach ekranlari ishlaydi.

### TC-SET-045 Enable Prepayment
- Source: `tests/ui/test_order/test_life_cycle.py::test_setting_prepayment_on`
- Dependency: yo'q
- Steps:
1. User system settingdagi `Заказ` bo'limiga o'tadi.
2. Prepayment parametri yoqiladi.
3. Save qilinadi.
- Expected result: prepayment nazorati yoqiladi.

### TC-ORD-046 Edit USA Order and Validate Prepayment
- Source: `tests/ui/test_order/test_order_edit.py::test_edit_order_for_price_type_USA`
- Dependency: `TC-SET-045 Enable Prepayment`, `TC-ORD-044 Create Order with USA Price Type`
- Preconditions: `order_id_4` mavjud.
- Steps:
1. Order edit ochiladi.
2. Product UZB price type va quantity `10` bilan yangilanadi.
3. Delivered holatga o'tkazish urinishida prepayment validation xatosi tekshiriladi.
4. Alohida oynada cashin yaratiladi.
5. Order qayta edit qilinadi va half-prepaymentdan kam summa bilan `Processing` saqlanadi.
6. Delivered statusga o'tish urinishi yana xato qaytaradi.
7. Pending, Shipped, Delivered va New o'tishlari sinovdan o'tkaziladi.
8. Oxirida exact prepayment bilan `New` saqlanadi va Delivered ga o'tkaziladi.
9. View ichida final status `Delivered` tekshiriladi.
- Expected result: prepayment qoidalari status o'zgarishlarida to'g'ri ishlaydi.

### TC-SET-047 Disable Prepayment
- Source: `tests/ui/test_order/test_life_cycle.py::test_setting_prepayment_off`
- Dependency: yo'q
- Steps: system setting ichida prepayment flag o'chiriladi va save qilinadi.
- Expected result: prepayment nazorati o'chadi.

### TC-REF-048 Enable Min Order Amount
- Source: `tests/ui/test_reference/test_price_type.py::test_price_type_min_amount_on`
- Dependency: `TC-REF-012 Create Price Type UZB`
- Steps:
1. User UZB price type setting oynasini ochadi.
2. Min amount `100000` kiritadi.
3. Save qiladi.
- Expected result: minimal order summasi yoqiladi.

### TC-ORD-049 Validate Min Order Amount
- Source: `tests/ui/test_order/test_order.py::test_min_order_amount`
- Dependency: `TC-REF-048 Enable Min Order Amount`
- Preconditions: price type min amount yoqilgan bo'lishi kerak.
- Steps:
1. User order yaratish oqimini boshlaydi.
2. Min amountdan past summa bilan order yaratish uriniladi.
3. Validation xatosi tekshiriladi.
- Expected result: minimal summa qoidasi ishlaydi.

### TC-REF-050 Disable Min Order Amount
- Source: `tests/ui/test_reference/test_price_type.py::test_price_type_min_amount_off`
- Dependency: `TC-ORD-049 Validate Min Order Amount`
- Steps:
1. User UZB price type setting oynasini ochadi.
2. Min amount maydoni bo'shatiladi.
3. Save qilinadi.
- Expected result: minimal order summasi cheklovi o'chadi.

## 5. Group D - Order with Sub Filial

### TC-REP-051 Add Invoice Template
- Source: `tests/ui/test_order/order_invoice_report/test_order_invoice_report.py::test_add_template_for_order_invoice_report`
- Dependency: `TC-SET-005 Create Sub Filial`
- Preconditions: excel template fayli `data/test_invoice_report.xlsx` mavjud bo'lishi kerak.
- Steps:
1. Admin template listga kiradi.
2. Add forma ochiladi.
3. Form `Накладная (заказ)` va template name kiritiladi.
4. Excel template upload qilinadi.
5. Save qilinadi.
6. Role attach oynasi ochilib `Админ` roli biriktiriladi.
- Expected result: invoice report template yaratilib rolega attach qilinadi.

### TC-ORD-052 Create Order for Sub Filial
- Source: `tests/ui/test_order/test_order.py::test_add_order_for_sub_filial`
- Dependency: `TC-SET-005 Create Sub Filial`, `TC-FIN-043 Create Contract Client C USA`
- Preconditions: sub filial, contract va USA price type mavjud.
- Steps:
1. User order addni boshlaydi.
2. Main step'da room, robot, client C, sub filial va contract tanlanadi.
3. Product step'da warehouse, USA price type, quantity `10`, margin kiritiladi.
4. Final step'da payment type bilan save qilinadi.
5. View ichida status, project va summa tekshiriladi.
6. `order_id_5` saqlanadi.
- Expected result: sub filial bilan bog'langan order yaratiladi.

### TC-REP-053 Download Invoice Report from Order List
- Source: `tests/ui/test_order/test_order_report.py::test_check_invoice_report_for_order_list`
- Dependency: `TC-REP-051 Add Invoice Template`, `TC-ORD-052 Create Order for Sub Filial`
- Preconditions: template va client C order mavjud.
- Steps:
1. User order listga kiradi.
2. Client C order topiladi.
3. Invoice report template tanlanadi.
4. Excel fayl yuklab olinadi.
- Expected result: `Test_invoice_report.xlsx` muvaffaqiyatli yuklanadi.

### TC-ORD-054 Change Status New to Cancelled
- Source: `tests/ui/test_order/test_order_change_status.py::test_change_status_new_and_cancelled`
- Dependency: `TC-ORD-052 Create Order for Sub Filial`
- Preconditions: `order_id_5` mavjud.
- Steps:
1. View orqali boshlang'ich status `New` tekshiriladi.
2. Status `Cancelled` ga o'tkaziladi.
- Expected result: sub filial order bekor qilinadi.

## 6. Group I - Order with Action

### TC-REF-055 Create Action Cash Money
- Source: `tests/ui/test_reference/test_action.py::test_add_action_cash_money`
- Dependency: `TC-SET-026 Attach Room Configuration`
- Preconditions: room, warehouse, payment type va product mavjud.
- Steps:
1. User action listga kiradi.
2. Add forma ochiladi.
3. Sana oralig'i, room, warehouse, payment type `Наличные деньги` va required flag kiritiladi.
4. Keyingi step'da product, bonus product, quantity va kind `Скидка` kiritiladi.
5. Save qilinadi va view orqali action name tekshiriladi.
- Expected result: cash money aksiyasi yaratiladi.

### TC-REF-056 Create Action Terminal
- Source: `tests/ui/test_reference/test_action.py::test_add_action_terminal`
- Dependency: `TC-SET-026 Attach Room Configuration`
- Preconditions: terminal payment type mavjud bo'lishi kerak.
- Steps: `TC-REF-055` bilan bir xil, faqat payment type `Терминал` va bonus quantity boshqacha.
- Expected result: terminal aksiyasi yaratiladi.

### TC-ORD-057 Create Order for Action
- Source: `tests/ui/test_order/test_order.py::test_add_order_for_action`
- Dependency: `TC-REF-055`, `TC-REF-056`
- Preconditions: action'lar aktiv holatda bo'lishi kerak.
- Steps:
1. User order addni boshlaydi.
2. Main step'da room, robot, client C va sub filial tanlanadi.
3. Product step'da aksiya mos mahsulot va quantity kiritiladi.
4. Final step'da order summa va action ta'siri tekshiriladi.
5. Save qilinadi.
6. View orqali status, client, room, project va summa tekshiriladi.
7. `order_id_6` saqlanadi.
- Expected result: aksiya qo'llangan order yaratiladi.

### TC-ORD-058 Edit Action Order
- Source: `tests/ui/test_order/test_order_edit.py::test_edit_order_for_action`
- Dependency: `TC-ORD-057 Create Order for Action`
- Preconditions: `order_id_6` mavjud.
- Steps:
1. Order edit ochiladi.
2. Quantity `8` ga o'zgartiriladi.
3. Final total amount olinadi.
4. Save qilinadi.
5. View ichida status, client, room, project va summa tekshiriladi.
- Expected result: order summary yangi quantity bo'yicha qayta hisoblanadi.

### TC-ORD-059 Change Status New to Delivered
- Source: `tests/ui/test_order/test_order_change_status.py::test_change_status_draft_and_delivered`
- Dependency: `TC-ORD-058 Edit Action Order`
- Preconditions: `order_id_6` mavjud.
- Steps:
1. View orqali boshlang'ich status `New` tekshiriladi.
2. Status `Delivered` ga o'tkaziladi.
3. View orqali delivered status tekshiriladi.
- Expected result: action order delivered holatga o'tadi.

### TC-ORD-060 Return Delivered Order
- Source: `tests/ui/test_order/test_order_return.py::test_order_return`
- Dependency: `TC-ORD-059 Change Status New to Delivered`
- Preconditions: `order_id_6` delivered holatda bo'lishi kerak.
- Steps:
1. Delivered order return oqimi ishga tushiriladi.
2. Order ID bo'yicha return yaratiladi.
3. Return natijasi view/list orqali tekshiriladi.
- Expected result: delivered order uchun return yaratiladi.

## 7. Purchase, Supplier, Warehouse

### TC-REF-061 Create Legal Person for Supplier
- Source: `tests/ui/test_reference/test_legal_person.py::test_add_legal_person_by_supplier`
- Dependency: yo'q
- Preconditions: user login ishlashi kerak.
- Steps:
1. User legal person listga kiradi.
2. Add forma ochiladi.
3. Supplier name, short name, room va code bilan save qilinadi.
4. View ichida nom va code tekshiriladi.
- Expected result: supplier uchun legal person yaratiladi.

### TC-WH-062 Create Supplier
- Source: `tests/ui/test_warehouse/test_supplier.py::test_add_supplier`
- Dependency: `TC-REF-061 Create Legal Person for Supplier`
- Preconditions: supplier legal person va product mavjud.
- Steps:
1. User supplier listga kiradi.
2. Add forma ochiladi.
3. Supplier person tanlanadi.
4. Save qilinadi.
5. View ichida supplier name tekshiriladi.
6. Bind product oynasi ochilib product attach qilinadi.
- Expected result: supplier yaratiladi va product biriktiriladi.

### TC-REF-063 Create Product-2 and Set Prices
- Source: `tests/ui/test_reference/test_product.py::test_product_add_as_product_2`
- Dependency: `TC-REF-015`, `TC-REF-012`, `TC-REF-013`
- Preconditions: supplier mavjud.
- Steps: `TC-REF-016` bilan bir xil, faqat product-2 va supplier tanlanadi.
- Expected result: supplierga bog'langan ikkinchi product yaratiladi.

### TC-PUR-064 Create Purchase
- Source: `tests/ui/test_purchase/test_purchase.py::test_add_purchase`
- Dependency: `TC-WH-062 Create Supplier`, `TC-REF-063 Create Product-2 and Set Prices`
- Preconditions: supplier va product mavjud.
- Steps:
1. User purchase listga kiradi.
2. Add oqimi boshlanadi.
3. Supplier tanlanadi.
4. Product, quantity `10` va price kiritiladi.
5. Purchase number generatsiya qilinib save qilinadi.
6. View, post, transaction va report tekshiriladi.
7. `purchase_number_1` saqlanadi.
- Expected result: purchase yaratiladi, post qilinadi, report va transaction ochiladi.

### TC-PUR-065 Create Extra Cost
- Source: `tests/ui/test_purchase/test_extra_cost.py::test_add_extra_cost`
- Dependency: `TC-PUR-064 Create Purchase`
- Preconditions: `purchase_number_1` mavjud.
- Steps:
1. User extra cost listga kiradi.
2. Expense article, corr template va amount bilan extra cost yaratiladi.
3. Note text bilan save qilinadi.
4. View va post tekshiriladi.
5. Separate/share amali `purchase_number_1` ga qo'llanadi.
6. Alohida oynada purchase transaction va report tekshiriladi.
- Expected result: extra cost yaratiladi va purchase ga taqsimlanadi.

### TC-PUR-066 Create Purchase with Extra Cost Sum
- Source: `tests/ui/test_purchase/test_purchase.py::test_add_purchase_with_extra_cost_sum`
- Dependency: `TC-PUR-064 Create Purchase`, `TC-PUR-065 Create Extra Cost`
- Preconditions: extra cost oqimi ishlashi kerak.
- Steps:
1. Purchase add extra cost flag bilan boshlanadi.
2. Supplier va product kiritiladi.
3. Extra cost modal ochiladi.
4. Expense article, corr template, amount va note kiritilib affects price flag tanlanadi.
5. Calc extra cost qilinadi.
6. Purchase number generatsiya qilinib save qilinadi.
7. View, post, transaction va report tekshiriladi.
8. `purchase_number_2` saqlanadi.
- Expected result: extra cost summasi purchase narxiga qo'shilgan purchase yaratiladi.

### TC-PUR-067 Create Purchase with Extra Cost Quantity
- Source: `tests/ui/test_purchase/test_purchase.py::test_add_purchase_with_extra_cost_quantity`
- Dependency: `TC-PUR-064 Create Purchase`, `TC-PUR-065 Create Extra Cost`
- Preconditions: product-1 va product-2 mavjud.
- Steps:
1. Purchase add extra cost flag bilan boshlanadi.
2. Ikki xil product turli quantity bilan qo'shiladi.
3. Extra cost modal method `Q` bilan ishlatiladi.
4. Calc qilinadi va save qilinadi.
5. Post, transaction va report tekshiriladi.
6. Report ichida har mahsulotga taqsimlangan final summa hisob-kitob bilan solishtiriladi.
7. `purchase_number_3` saqlanadi.
- Expected result: extra cost quantity ulushi bo'yicha to'g'ri taqsimlanadi.

### TC-PUR-068 Create Purchase with Extra Cost Weight Brutto
- Source: `tests/ui/test_purchase/test_purchase.py::test_add_purchase_with_extra_cost_weight_brutto`
- Dependency: `TC-PUR-064 Create Purchase`, `TC-PUR-065 Create Extra Cost`
- Preconditions: product brutto weight qiymatlari mavjud.
- Steps:
1. Purchase add extra cost flag bilan boshlanadi.
2. Ikki product qo'shiladi.
3. Extra cost method brutto weight bo'yicha taqsimlanadi.
4. Save, post, transaction va report tekshiriladi.
5. `purchase_number_4` saqlanadi.
- Expected result: extra cost brutto weight bo'yicha taqsimlanadi.

### TC-INP-069 Create Input
- Source: `tests/ui/test_input/test_input.py::test_add_input`
- Dependency: `TC-PUR-064 Create Purchase`
- Preconditions: `purchase_number_1` mavjud.
- Steps:
1. User input listga kiradi.
2. Input number va warehouse bilan input yaratiladi.
3. Purchase number tanlanadi va quantity `10` kiritiladi.
4. Save qilinadi.
5. View, status, transaction va report tekshiriladi.
6. `input_number_1` saqlanadi.
- Expected result: purchase asosida warehouse input yaratiladi.

### TC-INP-070 Create Input with Extra Cost
- Source: `tests/ui/test_input/test_input.py::test_add_input_with_extra_cost`
- Dependency: `TC-PUR-066 Create Purchase with Extra Cost Sum`
- Preconditions: `purchase_number_2` mavjud.
- Steps:
1. Input extra cost flag bilan yaratiladi.
2. Purchase number `purchase_number_2` tanlanadi.
3. Extra cost modal method `V` bilan ishlatiladi.
4. Calc extra cost qilinadi va save qilinadi.
5. View, status, transaction va report tekshiriladi.
6. `input_number_2` saqlanadi.
- Expected result: input ichida extra cost qayta hisoblanadi.

### TC-PUR-071 Create Purchase for Return to Supplier
- Source: `tests/ui/test_return_supplier/test_return_supplier.py::test_add_purchase_to_supplier`
- Dependency: `TC-PUR-064 Create Purchase`
- Steps: purchase oqimi qayta ishlatiladi va `purchase_number_5` saqlanadi.
- Expected result: return supplier uchun alohida purchase yaratiladi.

### TC-PUR-072 Return to Supplier
- Source: `tests/ui/test_return_supplier/test_return_supplier.py::test_return_to_supplier`
- Dependency: `TC-PUR-071 Create Purchase for Return to Supplier`
- Preconditions: `purchase_number_5` mavjud.
- Steps:
1. User return listga kiradi.
2. Purchase number tanlanadi.
3. Return number va warehouse kiritiladi.
4. Purchase, supplier va currency auto-filled qiymatlar tekshiriladi.
5. Product, quantity `10` va percent value kiritiladi.
6. Save qilinadi.
7. View ichida purchase, currency, supplier, warehouse va total amount tekshiriladi.
8. Transaction oynasi ochilib verify qilinadi.
- Expected result: supplierga qaytarish hujjati yaratiladi.

### TC-WH-073 Create Warehouse
- Source: `tests/ui/test_warehouse/test_warehouse.py::test_add_warehouse`
- Dependency: `TC-SET-003 Create Room`
- Preconditions: room mavjud.
- Steps:
1. User warehouse listga kiradi.
2. Add forma ochiladi.
3. New warehouse name va type `Minor` tanlanadi.
4. Type topilmasa, yangi warehouse type yaratiladi.
5. Room tanlanib save qilinadi.
6. View orqali warehouse name tekshiriladi.
- Expected result: ikkilamchi warehouse yaratiladi.

### TC-WH-074 Internal Movement
- Source: `tests/ui/test_movement/test_movement.py::test_add_internal_movement`
- Dependency: `TC-WH-073 Create Warehouse`
- Preconditions: asosiy va minor warehouse hamda product qoldig'i mavjud.
- Steps:
1. User movement listga kiradi.
2. From warehouse, to warehouse va movement number kiritiladi.
3. Product va quantity `10` kiritiladi.
4. Save qilinadi.
5. View ichida movement number tekshiriladi.
6. Status post qilinadi.
7. Target warehouse balansida quantity tekshiriladi.
- Expected result: ichki ko'chirishdan keyin minor warehouse balansi oshadi.

### TC-WH-075 Create Write Off
- Source: `tests/ui/test_writeoff/test_writeoff.py::test_add_write_off`
- Dependency: `TC-REF-016 Create Product-1 and Set Prices`
- Preconditions: warehouse va product balansi mavjud.
- Steps:
1. User writeoff listga kiradi.
2. Add forma ochiladi.
3. Writeoff number, warehouse va reason kiritiladi.
4. Select step'da product va quantity `10` tanlanadi.
5. Save qilinadi.
6. View ichida asosiy info tekshiriladi.
7. Eski balans o'qiladi.
8. Status `В сборке` va keyin `Проведено` ga o'tkaziladi.
9. Yangi balans tekshiriladi.
10. Expense oynasi ochilib total sum va expense article bilan xarajat yaratiladi.
11. View ichida `Расходы` bo'limi tekshiriladi.
- Expected result: write off balansni kamaytiradi va expense yozuvi yaratiladi.

### TC-REP-076 Check Write Off Constructor Report
- Source: `tests/ui/test_writeoff/test_writeoff.py::test_check_constructor_report_write_off`
- Dependency: `TC-WH-075 Create Write Off`
- Steps:
1. User writeoff MBI report constructorga kiradi.
2. Date, writeoff, warehouse, currency va product field'lari report row ga qo'shiladi.
3. View bosiladi.
4. Iframe ichida report qiymatlari o'qiladi.
- Expected result: writeoff report constructor ma'lumot qaytaradi.

### TC-WH-077 Create Stocktaking
- Source: `tests/ui/test_stocktaking/test_stocktaking.py::test_add_stocktaking`
- Dependency: `TC-REF-016 Create Product-1 and Set Prices`, `TC-REF-063 Create Product-2 and Set Prices`
- Preconditions: warehouse va ikki mahsulot mavjud.
- Steps:
1. User stocktaking listga kiradi.
2. Add forma ochiladi.
3. Stocktaking number, warehouse, reason va note kiritiladi.
4. Select orqali product-1 tanlanadi.
5. Product-2 qo'lda ortiqcha qoldiq sifatida qo'shiladi.
6. Yozuv edit qilinadi.
7. View ichida warehouse, excess, minority va creation date tekshiriladi.
8. Transaction tekshiriladi.
9. Complete qilinadi.
10. Complete summary va TMZ bo'limi tekshiriladi.
- Expected result: inventarizatsiya excess/minority summalari bilan yakunlanadi.

### TC-FIN-078 Payment to Suppliers
- Source: `tests/ui/test_payment_to_suppliers/test_payment_to_suppliers.py::test_payment_to_suppliers`
- Dependency: `TC-WH-062 Create Supplier`, `TC-REF-014 Attach Payment Types`
- Preconditions: supplier bo'yicha to'lov qilish uchun balans bo'lishi kerak.
- Steps:
1. User cashout listga kiradi.
2. Add forma ochiladi.
3. Cashout number kiritilib vaqt olinadi.
4. Supplier va payment type tanlanadi, currency `Узбекский сум` ekanligi tekshiriladi.
5. Cash register tanlanadi va available balance olinadi.
6. Amount sifatida shu balance kiritilib save qilinadi.
7. View ichida main info va audit history tekshiriladi.
8. Post qilinadi.
9. Transaction tekshiriladi.
- Expected result: supplier payment hujjati yaratiladi va post bo'ladi.

## 8. Integration va Reportlar

### TC-INT-079 Check CisLink Report
- Source: `tests/ui/test_rep/integration/cislink/test_cislink.py::test_check_report_cis_link`
- Dependency: `TC-REF-012 Create Price Type UZB`
- Preconditions: filial va price type mavjud.
- Steps:
1. Admin CisLink sahifasiga kiradi.
2. Setting ochiladi.
3. Identification code, person group, product group, filial va price type kiritiladi.
4. Save qilinadi.
5. Generate qilinadi va zip fayl yuklanishi tekshiriladi.
- Expected result: `cislink.zip` yaratiladi.

### TC-INT-080 Check Integration Three Report
- Source: `tests/ui/test_rep/integration/integration_three/test_integration_three.py::test_check_report_integration_three`
- Dependency: yo'q
- Steps:
1. Admin integration three sahifasiga kiradi.
2. Setting ochilib save qilinadi.
3. Sana kiritilib generate qilinadi.
4. Iframe ichida uchta report document tekshiriladi.
- Expected result: integration three report content ochiladi.

### TC-INT-081 Check Integration Two Exchange Files
- Source: `tests/ui/test_rep/integration/integration_two/test_integration_two.py::test_check_report_integration_two`
- Dependency: `TC-REF-012 Create Price Type UZB`
- Preconditions: price type mavjud.
- Steps:
1. Admin integration two sahifasiga kiradi.
2. Setting ochiladi va company id, user name, url, price type, checkbox konfiguratsiyasi saqlanadi.
3. Exchange mode 1 uchun `import_order.xml` generate qilinadi.
4. Error modal tekshiriladi.
5. Exchange mode 2 uchun `export_order.xml` generate qilinadi.
6. Exchange mode 3 uchun `import_order_status.xml` generate qilinadi.
7. Exchange mode 5 uchun `export_input.xml` generate qilinadi.
- Expected result: barcha kerakli XML fayllar generatsiya qilinadi.

### TC-INT-082 Check Optimum Report
- Source: `tests/ui/test_rep/integration/optimum/test_optimum.py::test_check_report_optimum`
- Dependency: `TC-SET-002 Create Filial`
- Preconditions: filial mavjud.
- Steps:
1. Admin optimum sahifasiga kiradi.
2. Product group va prefix sozlamalari kiritilib save qilinadi.
3. Generate qilinadi va `optimum.zip` tekshiriladi.
4. All filial checkbox tanlanadi, filial belgilanadi.
5. Generate qayta qilinadi.
- Expected result: optimum report ikkala holatda ham generatsiya qilinadi.

### TC-INT-083 Check Sales Work Report
- Source: `tests/ui/test_rep/integration/saleswork/test_saleswork.py::test_check_report_sales_work`
- Dependency: yo'q
- Steps:
1. Admin sales work sahifasiga kiradi.
2. Template listdan yangi template yaratiladi.
3. Product group bilan save qilinadi.
4. Sales work sahifasida tanlangan template nomi tekshiriladi.
5. Generate qilinadi va `sales_work.zip` yuklanadi.
- Expected result: sales work template yaratiladi va report chiqadi.

### TC-INT-084 Check Spot 2D Report
- Source: `tests/ui/test_rep/integration/spot/test_spot.py::test_check_report_spot_2d`
- Dependency: yo'q
- Steps:
1. Admin spot sahifasiga kiradi.
2. Template oynasi orqali yangi spot template yaratiladi.
3. Product group biriktiriladi.
4. Preferences tozalanadi.
5. Run qilinadi va `Spot2D.zip` yuklanadi.
- Expected result: Spot 2D integratsiya fayli generatsiya qilinadi.

## Qisqa Dependency Zanjiri

Asosiy setup zanjiri:
1. Legal Person
2. Filial
3. Room
4. Robot
5. Sub Filial
6. Natural Person
7. User
8. Permissions / Licenses / Password
9. Price Type / Sector / Product / Margin / Clients
10. Room Attachment
11. Init Balance

Shundan keyin order, purchase, warehouse va integration testlari ishlaydi.
