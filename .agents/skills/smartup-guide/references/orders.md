# Orders

## Qidiruv Kalitlari

Tags: order, order-add, order-list, order-view, product, payment-type, contract-limit

### Order Navigation
Tags: order, navigation
- Qayerda: `Продажа > Заказы`.
- URLlar:
  - list: `*/order_list`
  - add: `*/order+add`
  - view: `*/order_view`
- Testda ishlatish: list heading `Заказы`, add content `Заказ (создание)`, view content `Заказ / Просмотр`.

### Mavjud Order Flowlar
Tags: order, flow
- Qayerda: `tests/smoke/flows/flow_order/`.
- Flowlar:
  - `flow_order_list(page, add=True/find_row/view/edit/status)`
  - `flow_order_main_page(...)`
  - `flow_order_product_page(...)`
  - `flow_order_final_page(...)`
  - `flow_order_view(page, get_value=...)`
- Qoida: Order testlari ko'p yoziladi; takrorlanadigan order harakatlari flowga chiqariladi.

### Minimal Order Setup Entitylar
Tags: order, setup
- Client: `natural_client-pw{code}`
- Room: `room-pw{code}`
- Robot: `robot-pw{code}`
- Product: `product-pw{code}`
- Default payment type: `Наличные деньги`
- Default status: `Черновик`

### Contract Limit Order Case
Tags: order, contract, limit, error
- Qoida: 500000 contract bilan quantity `100` product order summasi `700 000` bo'ladi.
- Expected: save paytida Biruni error chiqadi, order add formadan chiqib ketmaydi.
- Davomiy smoke: shu test ichida order listga qaytib quantity `1` bilan `7 000` order saqlanishi tekshiriladi.
- View assert: contract, client, product, payment type, status va summa.
- Muhim: limit testda quantity'ni mavjud stockga qarab kamaytirib yuborma; bu test maqsadini buzadi. Agar stock yetmasa, preconditionni tuzat: yangi initial balance qo'sh yoki bron qilingan orderlarni `Canceled/Отменен` statusga o'tkaz.
- Debug/re-run paytida contract oldin ishlatilgan bo'lsa, qoldiq `500000` bo'lmasligi mumkin; error assertda exact qoldiqni hard-code qilma, lekin `сумма заказа = 700000` va limit error borligini tekshir.

### Contract + Payment Type Order Case
Tags: order, contract, payment-type, auto-fill
- Qoida: Contract `Типы оплат = Перечисление` bilan yaratilsa, order final sahifasida `Тип оплаты` auto-fill `Перечисление`.
- Qoida: User `Тип оплаты` ni boshqa qiymatga o'zgartirishi mumkin; save validation payment typega emas, contract sum limitga bog'liq.
- Testda ishlatish: auto-fill uchun input value tekshir. Keyin optional ravishda payment type o'zgartirilib ham save ishlashi tekshirilishi mumkin.

### Order Edit Save As New
Tags: order, edit, a-group, status
- Qayerda: A-group `A-05` testi `A-04` yaratgan active orderni edit qiladi.
- Qoida: edit flowda yangi row/mahsulot qo'shilmaydi; main va product sahifalarida faqat `Далее` bosiladi.
- Qoida: final sahifada mavjud qiymatlar tekshirilib, order statusi `Новый` qilib saqlanadi.
- Testda ishlatish: edit main/product/final sahifalaridagi room, robot, client, contract, product, warehouse, price type, quantity, payment type va total qiymatlarini tekshir; save'dan keyin viewda order id saqlanganini va status `Новый` bo'lganini assert qil.

### Consignment Order Case
Tags: order, consignment, settings, view
- Qayerda: `Главное > Настройки системы > Заказ`.
- Sozlama: `Разрешить выдачу консигнации` switchi va `Лимит консигнации (в днях)` inputi label text orqali topiladi; testda raw `ng-model` locator ishlatilmaydi.
- Fresh DB qoida: konsignatsiya default o'chirilgan bo'ladi; B-group konsignatsiya testi order yaratishdan oldin shu settingni yoqib, limitni `30` qilib saqlashi kerak.
- Qoida: limit `30` saqlansa, order add final/3-formasida `Дата оплаты по консигнации` va `Сумма консигнации` kartasi ko'rinadi.
- Create test maqsadi keyingi edit case uchun precondition ham yaratadi: quantity `5`, total/konsignatsiya `35 000` bo'lsin; quantity `1` bilan keyingi testda totalni kamaytirib bo'lmaydi.
- Testda ishlatish: final formadagi Angular state `q.consignment_day_limit == "30"` va `d.max_consignment_date == delivery_date + 30 days` bo'lishi kerak.
- View assert: order viewda visible `Консигнация` textini bosib, visible text orqali consignment date va `35 000` summa tekshiriladi.
- B-group test fayli: `tests/smoke/test_groups/test_B_grup/test_order.py`.

### Consignment Edit And Split Case
Tags: order, consignment, edit, validation, split
- Precondition: `test_b_group_create_order_with_consignment_limit` 5 dona order yaratgan bo'lishi kerak; debug rerun oldidan shu clientning active orderlari `Отменен` qilinadi.
- Qoida: 5 dona (`35 000`) konsignatsiyali order editda quantity `4` ga tushirilsa total `28 000` bo'ladi; eski konsignatsiya totaldan katta qolsa `H02-ANOR279-006 — Ошибка` va `Общая сумма консигнаций не должна быть больше суммы заказа` chiqadi.
- UI xatti-harakati: bu error product qadamidan final qadamga o'tishda chiqadi va `Дата оплаты по консигнации` / `Сумма консигнации` inputlari clear bo'ladi.
- Limit qoida: delivery date + 31 kun kabi 30 kunlik limitdan katta konsignatsiya sanasi save confirm ochmaydi; valid max sana delivery date + 30 kun.
- Split qoida: konsignatsiya sectionidagi `+` orqali ikkinchi row qo'shiladi; 4 dona order uchun `14 000 + 14 000` qilib ikki sanaga bo'lib save qilinadi.
- View assert: `Консигнация` tabida ikkala sana va ikkita `14 000` summa ko'rinishi kerak.
- Data: create test `b_group_consignment_order_id`ni order view URLidagi `deal_id`dan saqlaydi, edit test esa stable topish uchun client keydan ham foydalanadi.

### Product Chiqmasa
Tags: order, product, balance, booking, setup
- Problem: order product qadamida tovar/product chiqmayapti.
- Sabablar: zaxira/balans yo'q yoki product bron qilingan orderlarda band.
- Fresh DB qoida: yangi server/bazada oldingi orderlar bo'lmaydi; order cleanup/cancel qadamiga testning majburiy preconditioni sifatida qaramang.
- Asosiy yechim: mavjud ishlayotgan testni o'zgartirma; agar `order_list`da oldin yaratilgan orderlar bo'lsa, yangi order testlaridan oldin ularning statusini `Canceled/Отменен` ga o'tkaz.
- Birinchi run holati: oldin yaratilgan order bo'lmasa cleanup qadam no-op bo'lishi kerak; order mavjudligini precondition sifatida qabul qilma.
- Order statusini o'zgartirish uchun yangi DOM cleanup/helper yozma; mavjud `flow_order_list(page, find_row=..., status="Отменен")` flowidan foydalan.
- `flow_open_order_list`dan keyin order grid hali yuklanmagan bo'lishi mumkin; count/search qilishdan oldin heading/create button yoki page body visible text orqali list tayyorligini kut.
- Order list grid textlari `get_by_text(..., exact=True)` bilan topilmasligi mumkin; cleanupda client text body ichida bor-yo'qligini tekshir, keyin mavjud `flow_order_list(..., status="Отменен")` bilan birinchi active rowni cancel qil.
- Agar cancellation mumkin bo'lmasa, order listdan productni band qilib turgan orderlarni o'chirish mumkin.
- Faqat order listdan tozalash imkoni bo'lmasa: setupdagi `test_20_init_balance` orqali balans qo'shib kel.
- Test/debug uchun initial balance flow qo'shish oxirgi variant; u mavjud ishlayotgan testlarga ulanmasligi kerak.

### Order ID
Tags: order, view, data-store
- Qayerda: order view.
- Locator: `ИД заказа` label textidan yaqin view value olinadi; yangi testlarda raw XPath yozilmaydi.
- Data: keyingi testlar uchun `a_group_order_id` yoki casega xos key bilan `data_store.json` ga saqla.

### Order List Накладные Reports
Tags: order, invoice, report, b-group, locator
- Qayerda: `Продажа > Заказы` listida kerakli row ochilgandan keyin row menu ichidagi `Накладные` dropdown; order view ichida emas.
- Locator: bitta order uchun row-level button `#trade81-button-report_one`. Reportni ochish uchun `a.dropdown-item` markaziga emas, option nomi yozilgan `span[ng-click*="reportOne"]` yoki `span[ng-click*="chequeOne"]` elementiga click qilish kerak.
- Qoida: `Счет-фактура с наценкой` va `Экспортировать заказ` dropdownda ko'rinadi, lekin HTML report popup sikliga qo'shilmaydi; ularni visible option sifatida tekshir.
- B-group case: B-02 draft orderni listda qoldiradi; B-03 shu sessiyadan foydalanib `Накладные` optionlarini tekshiradi va asosiy reportlarda client/product/summa/order id ko'rinishini assert qiladi.
