# Акция (Aksiya / Promotion) formasi

Smartup'da aksiya = **Акция** (chegirma/bonus kampaniyasi). Mijoz buyurtmada shart bajarsa, bonus (skidka % yoki bonus tovar) oladi.

## Navigatsiya

- Menyu: **Справочники → Маркетинг → Акции** (`navigate_to(page, tab="Справочники", name="Акции")`)
- Ro'yxat URL: `#/<session>/anor/mcg/action_list`
- Qo'shish URL: `#/<session>/anor/mcg/action+add` ("Создать" tugmasi)
- Product tanlash (Показать все): `#/<session>/anor/mcg/action_product_list` — "Акция (подбор)" modali (Доступные/Выбранные). Lekin oddiy holatda inline dropdown'dan to'g'ridan-to'g'ri tanlash yetarli.

## Tuzilma — 2 bosqichli wizard

Forma 2 tab/bosqich: **Главное** va **Условия**. Pastda "Далее" → "Завершить". "Завершить" bosilganda **"Сохранить?"** biruni confirm modali chiqadi → **да** (`#biruniConfirm button: да`). Saqlangach `Акции` ro'yxatiga qaytadi.

### 1) Главное (asosiy) — majburiy maydonlar (*)

Forma moduli barqaror: `#anor718-input-...`; ro'yxat grid moduli `#anor717-input-b_grid-table`.

- **Название*** — `#anor718-input-text-name` ichidagi textbox (ng-model `d.name`)
- **Дата начала*** / **Срок действия*** — `#anor718-input-b_input-start_date` / `...-end_date` (default: bugun → +20 kun)
- **Рабочие зоны*** — `#anor718-input-b_input-rooms` (Поиск); ish zonasi `room-pw{code}`
- **Бонусный склад*** — `#anor718-input-b_input-bonus_warehouse` (Поиск); default ombor `Основной склад`
- **Тип акции** — shart asosi: `Кол-во` (default), `Сумма`, `Вес`, `Кол-во кейс`, `Смешанный`. Select ng-model `d.calc_kind` turidagi ui-select.
- Ixtiyoriy: Тип цены, Типы оплат, Склады, Характеристика клиентов, Обязательная; Статус (`Активный`), Бонусы за заказ va h.k.

### 2) Условия (shartlar) — Условие / Бонус (barqaror ng-model selektorlar)

- **Условие** (trigger): Тип условия = `[ng-model="rule.rule_kind"]` (`Обычный`). Default qator **"Все ТМЦ"**.
  - Мин. значение = `input[ng-model="rule.main_value"]`
  - Макс. значение = `input[ng-model="rule.extra_value"]`
  - МТКП = `input[ng-model="rule.required_count"]` (default 1)
  - Shart productini qidirish: `input[ng-model="d['selected_rule_name_' + condition_index + rule_index]"]` (Поиск)
- **Бонус** (mijoz nima oladi): **Тип бонуса** = `[ng-model="bonus.bonus_kind"]` → `Кол-во` yoki **`Скидка`**.
  - `Скидка` tanlansa, bonus product qatorida ustun **Значение(%)** bo'ladi.
  - Bonus product qidirish: `#bonus_products input[placeholder="Поиск..."]` → inline dropdown'dan `product-pw{code}` tanlanadi (yoki "Показать все" modali).
  - Chegirma foizi: `input[ng-model="product.value"]`

## "10 ta productga 10% skidka" talqini va flow (tasdiqlangan)

Bu kompaniyada odatda 1 ta product (`product-pw{code}`) bo'ladi, shuning uchun "10 ta product" = **miqdor** deb talqin qilinadi:

- Тип акции = **Кол-во**
- Условие "Все ТМЦ": `rule.main_value` = **10** (10 dona olinganda ishga tushadi)
- Бонус: `bonus.bonus_kind` = **Скидка**, ТМЦ = `product-pw{code}`, `product.value` = **10**
- Ro'yxatda: `Скидка 10% ... | Кол-во | Активный`
- Screenshot: `skills/smartup-guide/references/forms/screenshots/action/action__list-created__desktop-1200x660__20260610.png`

## Login / data eslatma

- Aksiya user profil bilan yaratiladi: `user-pw{code}@<company>`, parol USER_PASS. `code` va konkret qiymatlar `data_store.json` dan olinadi (dossierга literal yozilmaydi).
- Test: `tests/smoke/test_groups/test_C_grup/` (C-group), leaf `run_c_group_create_action(...)`.
