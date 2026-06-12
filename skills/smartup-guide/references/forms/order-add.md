# Order Add Wizard (order+add / order+edit)

3 qadamli order yaratish/o'zgartirish wizard'i. MCP bilan jonli tekshirilgan
(`autotest@smartup.online`, `user-pw{code}`, 2026-06-12).

## URL / Navigation
- Navigation: `Продажа > Заказы` → `Создать` (yoki list `flow_order_list(page, add=True)`).
- URL: `*/anor/mdeal/order/order+add` (yangi), `*/anor/mdeal/order/order+edit` (edit).
- Content heading: `Заказ (создание)` / `Заказ (изменение)`.
- Qadamlar tugmasi: `#anor279-button-next_step` (step 1-2 da "ДАЛЕЕ", oxirgi stepda "СОХРАНИТЬ"),
  orqaga `#anor279-button-prev_step`. Save tugmasida `fa-save` ikonka bor →
  `get_by_role("button", name="Сохранить", exact=True)` 0 element topadi; `exact_button=False` kerak.

## anor279 Modul ID
- Order wizard moduli ID = **`anor279`** (autotest deploymentida barqaror; A-group order testlari ham shu bilan o'tadi).
- Bu Smartup modul/forma kodi — boshqa deployment/versiyada **boshqacha bo'lishi mumkin**. Agar order add
  locatorlari to'satdan butunlay topilmasa, birinchi navbatda `anor279` prefiksining hali to'g'riligini tekshir
  (`document.querySelectorAll('[id^="anor279"]')`).
- ID prefiksida nomuvofiqlik bor: ba'zi step-1 elementlari `anor279-input-...`, product step esa
  `anor279_input-...` (underscore). Payment type wrapper id'da typo: `anor279-inpu-b_input-payment_type`
  (shuning uchun payment type label orqali tanlanadi, id orqali emas).

## Step 1 — Main page
- Stabil id'li date inputlar: `#anor279-input-deal_time` (`d.deal_time`),
  `#anor279-input-delivery_date` (`d.delivery_date`). Date inputlarda `min`/`max` atribut **yo'q**.
- b-input wrapperlari (`div`, ichida `input[placeholder="Поиск..."]`):
  - `#anor279-input-b_input-room_name` — label "Рабочая зона*", `d.room_name`
  - `#anor279-input-b_input-robot_name` — label "Штат*", `d.robot_name`
  - `#anor279-input-b_input-person_name` — label "Клиент*", `d.person_name`
  - `#anor279-input-b_input-subfilial_name` — label "Проект", `d.subfilial_name`
  - `#anor279-input-b_input-contract_name` — label "Договор", `d.contract_name`
- **Auto-fill**: user-pw{code} bilan kirilganda room/robot/client default qiymatlari avtomatik to'ladi
  (room-pw{code} / robot-pw{code} / natural_client-pw{code}). `check_form=True` shuni `expect(...).to_have_value(...)`
  bilan tekshiradi (auto-retry — timing barqaror).
- b-input search role: input placeholder "Поиск..." → `get_by_role("textbox", name="Поиск")` (substring match) ishlaydi.
- Date labellar list/forma textida: "Дата заказа" (deal_time), "Дата отгрузки" (delivery_date) — B-group shu label orqali o'qiydi.

## Step 2 — Product page
- Product b-input: `#anor279_input-b_input-product_name_goods0` (tag `b-input`, underscore!).
- Product grid: `#anor279_input-b_pg_grid-goods_items` (tag `b-pg-grid`).
- Quantity input: `#anor279_input-b_pg_col-quantity_0` (`item.quantity`) — **product tanlanmaguncha mavjud emas**,
  qator yaratilgach paydo bo'ladi.
- **Product dropdown (flaky bo'lgan joy):**
  - Search bosilganda b-input ichida `.hint` ochiladi: `.hint-header` (Название/Цена/Остаток ustunlari) + `.hint-item` qatorlar.
  - Option matni **kombinatsiyalangan**: `"product-pw{code}  Основной склад  Price Type ...  7 000"` —
    product nomi **alohida text node emas**. Shuning uchun `page.get_by_text(product)` page-wide bo'lib bir nechta
    elementga tushadi va dropdown ochilishini kutmaydi → flaky.
  - **To'g'ri pattern** (`flow_order_product_page`):
    ```python
    product_input = page.locator("#anor279_input-b_input-product_name_goods0")
    search = product_input.get_by_role("textbox", name="Поиск")
    search.click(); search.fill(product)
    option = product_input.locator(".hint-item").filter(has_text=product).first
    expect(option).to_be_visible(); option.click()
    expect(product_input.locator("input").first).to_have_value(product)
    ```
  - `.hint-item` ni bosish to'g'ridan-to'g'ri qatorni tanlaydi (name cell ichiga emas).

## Step 3 — Final page
- Payment type b-input: `d.payment_type_name`, label "Тип оплаты" → `select_b_input_by_label("Тип оплаты", ...)` (label orqali, id'da typo bor).
- Status ui-select: `#anor279-ui_select-status` (div), ichida "Select box activate" (`.ui-select-toggle`),
  optionlar `.ui-select-choices-row-inner`. Default "Новый".
- Save: `#anor279-button-next_step` matni "СОХРАНИТЬ" (`nextStep()`), `save_and_expect_heading(..., exact_button=False)`.

### Konsignatsiya kartasi (consignment enabled bo'lsa)
- Faqat `Главное > Настройки системы > Заказ` da `Разрешить выдачу консигнации` yoqilgan bo'lsa ko'rinadi.
- Inputlar: `item.consignment_date` (label "Дата оплаты по консигнации", placeholder "Выбрать дату"),
  `item.consignment_amount` (label "Сумма консигнации"). `+` qo'shish: `button[ng-click="addConsignment()"]`.
- **30 kunlik limit qayerda (MUHIM):**
  - Limit DOM textida YOKI date input atributida (`max`) **ko'rinmaydi**.
  - Faqat AngularJS scope'da: **`q.consignment_day_limit`** = "30". (`q.consignment_allow`="Y", `q.total_amount`=5×narx.)
  - **`d.max_consignment_date` degan field YO'Q** — max sana client-side hisoblanadi (delivery_date + limit), scope'da saqlanmaydi.
    (Eski orders.md notasi `d.max_consignment_date` deb yozgan edi — bu noto'g'ri.)
  - Scope'ni o'qish: `item.consignment_date` inputidan `angular.element(el).scope()` olib, `$parent` zanjirida `q.consignment_day_limit` qidiriladi (`order_helpers._consignment_day_limit`).
- **Eski flaky bug**: `_consignment_limit_state` page'dan o'qimasdan `"30"` + `datetime.today()+30` qaytarardi; bu
  `delivery_date+30` bilan solishtirilib, `today != delivery_date` bo'lganda (timezone/midnight/auto-inc delivery)
  AssertionError berardi. Tuzatildi: limit `q.consignment_day_limit` dan o'qiladi, max sana esa formadagi haqiqiy
  `delivery_date` + limit dan hisoblanadi.

## Ishlatiladigan flow/helper/test fayllari
- Flowlar: `tests/smoke/flows/flow_order/flow_order_add.py` (main/product/final), `flow_order_list.py` (list/add/find_row/view/edit/status).
- B-group consignment: `tests/smoke/test_groups/test_B_grup/order_helpers.py`.
- A-group order: `tests/smoke/test_groups/test_A_grup/test_order.py`.

## Known issues / debug notes
- Product chiqmasligi → balans/booking; orders.md "Product Chiqmasa" bo'limiga qara.
- `anor279` prefiksi deploymentga bog'liq — locator butunlay topilmasa avval shuni tekshir.
