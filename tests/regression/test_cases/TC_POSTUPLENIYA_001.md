# TC-POSTUPLENIYA-001: Поступления ТМЦ — закуп tovarlarni omborga tushirish

## Meta

| Maydon | Qiymat |
|--------|--------|
| **Suite** | Склад / Поступления ТМЦ на склад |
| **Priority** | Critical |
| **Type** | Functional (E2E Flow) |
| **Automation** | `tests/regression/test_postupleniya_flow.py::test_postupleniya_tmc` |
| **Status** | Active |
| **Depends on** | TC-ZAKUPKA-001 |

## Maqsad

Закуп qilingan tovarlarni «Поступления ТМЦ на склад» moduli orqali
omborga (Основной склад) tushirish operatsiyasini to'liq tekshiradi:
navigatsiya → yaratish ustasi → ombor tanlash → закупka ulash →
tovarlarni qo'shish → завершение.

## Pre-conditions

- Server: `https://app3.greenwhite.uz/xtrade`
- Company: `novatrade`
- Foydalanuvchi: `moxir@novatrade` (parol: `1`)
- Filial: `NovaTrade - Toshkent Filiali`
- Ombor `Основной склад` tizimda mavjud
- **TC-ZAKUPKA-001 muvaffaqiyatli o'tgan** — «Проведен» statusdagi закупka mavjud

---

## Test qadamlari

| # | Assertion | Harakat | Kutilgan natija |
|---|-----------|---------|----------------|
| **1** | HARD | `moxir@novatrade` / `1` bilan kirish, filial tanlash | Dashboard ko'rinadi |
| **2** | HARD + soft | Склад → Поступления ТМЦ на склад | Sahifa ochiladi; `#anor113-button-add` ko'rinadi |
| **3** | HARD | `#anor113-button-add` — `Создать` bosish | Yaratish ustasi (wizard) ochiladi, **0-qadam** |
| **4** | HARD | Qidiruv maydonida `Основной склад` topib tanlash | Ombor tanlanadi |
| **5** | HARD | `Далее` bosish | **1-qadam** ochiladi — закупka ulash |
| **6** | HARD | `Поиск закупки` maydoniga bosish → dropdown dan birinchi aktiv yozuv tanlash | Закупka tanlanadi |
| **7** | HARD | Tovar qo'shish tugmasi (`button.nth(4)`) bosish | Закупka tovarlar ro'yxatga qo'shiladi |
| **8** | HARD | `Далее` bosish | **2-qadam** ochiladi — yakunlash |
| **9** | HARD | `Select box activate` → `Завершено` tanlash | Status `Завершено` bo'ladi |
| **10** | HARD | `Завершить` bosish | Tasdiqlash dialogi chiqadi |
| **11** | HARD | `да` bosish | Dialog yopiladi, поступление yakunlanadi |
| **12** | soft | `#anor113-button-add` ko'rinishini tekshirish | Ro'yxatga qaytilgan |

> **HARD** — muvaffaqiyatsiz bo'lsa test to'xtatiladi + screenshot olinadi  
> **soft** — muvaffaqiyatsiz bo'lsa screenshot olinadi, test davom etadi

---

## Post-conditions

- Omborda (`Основной склад`) `NovaCola 0.5L` uchun `5` ta qo'shilgan
- Поступление hujjati `Завершен` statusida ro'yxatda ko'rinadi
- Закупka bilan bog'liq Взаиморасчет (qarzdorlik) hosil bo'lgan

---

## Bog'liq test holatlari

| TC ID | Nomi | Bog'liqlik |
|-------|------|-----------|
| TC-ZAKUPKA-001 | Закупка yaratish | **Pre-condition** — avval o'tishi shart |
| TC-PAYMENT-001 | Qarzdorlikni so'ndirish | Ushbu поступление orqali hosil bo'lgan qarzdorlik |

---

## Xatolar (muammo chiqqanda qarang)

| Qadam | Ehtimoliy muammo | Yechim |
|-------|-----------------|--------|
| 6 | `Поиск закупки` dropdown bo'sh | TC-ZAKUPKA-001 o'tmagan; avval закупka qilib ko'r |
| 6 | `.hint-item.ng-scope.active` topilmadi | Angular versiya o'zgardi — playwright mcp bilan locator ol |
| 7 | `button.nth(4)` noto'g'ri tugma bosdi | Sahifadagi tugmalar soni o'zgardi — codegen bilan qayta tekshir |
| 9 | `Select box activate` topilmadi | Label atributi o'zgardi — `get_by_text("Статус")` bilan sinab ko'r |
