# TC-ZAKUPKA-001: Закупка yaratish (to'liq flow)

## Meta

| Maydon | Qiymat |
|--------|--------|
| **Suite** | Склад / Закупки |
| **Priority** | Critical |
| **Type** | Functional (E2E Flow) |
| **Automation** | `tests/regression/test_zakupka_flow.py::test_create_zakupka` |
| **Status** | Active |

## Maqsad

Foydalanuvchi (moxir@novatrade) tomonidan yetkazib beruvchidan
tovar zakup qilish operatsiyasini boshidan oxirigacha tekshiradi:
navigatsiya → yaratish ustasi → yetkazib beruvchi tanlash →
tovar qo'shish → проведение.

## Pre-conditions

- Server: `https://app3.greenwhite.uz/xtrade`
- Company: `novatrade`
- Foydalanuvchi: `moxir@novatrade` (parol: `1`)
- Filial: `NovaTrade - Toshkent Filiali`
- Yetkazib beruvchi `NovaWater` (Юридическое лицо) tizimda mavjud
- Tovar `NovaCola 0.5L` ombordan mavjud

---

## Test qadamlari

| # | Harakat | Kutilgan natija |
|---|---------|----------------|
| **1** | `moxir@novatrade` / `1` bilan tizimga kirish, `NovaTrade - Toshkent Filiali` filialini tanlash | Dashboard ko'rinadi, filial sarlavhada aks etadi |
| **2** | Menyu: `Склад` → `Закупки` (exact) | Закупки ro'yxati sahifasi ochiladi, `#anor288-button-add` ko'rinadi |
| **3** | Asboblar panelida `Создать` dropdown ochish | Dropdown menyusi ko'rinadi: "Создать", "Создать закупку через faktura.uz" |
| **4** | Dropdown dan `Создать` (exact) ni bosish | Закупка yaratish ustasi (wizard) ochiladi, **0-qadam** (yetkazib beruvchi tanlash) ko'rinadi |
| **5** | Yetkazib beruvchi: `step0` formasida `NovaWater` ni tanlash (тип: Юридическое лицо) | `NovaWater` tanlab qo'yiladi, forma to'g'ri to'ldirilgan |
| **6** | `Далее` tugmasini bosish | Ustaning **1-qadami** ochiladi — tovar ro'yxati va qidiruv maydoni |
| **7** | `#anor289` dagi qidiruv maydoniga click, `NovaCola 0.5L` ni tanlash | `NovaCola 0.5L` qatorsiga qo'shiladi |
| **8** | `Miqdor (quantity)` maydoniga `5` kiritish | Miqdor `5` bo'ladi |
| **9** | `Narx (price)` maydoniga `4000` kiritish | Narx `4000`, jami `20 000` bo'ladi |
| **10** | `Далее` tugmasini bosish | Ustaning **2-qadami** (tasdiqlash) ochiladi, jami summa ko'rinadi |
| **11** | `Провести` tugmasini bosish | Tasdiqlash dialogi chiqadi: "Провести?" |
| **12** | Dialogda `да` ni bosish | Dialog yopiladi, закупка провести qilinadi, ro'yxatga qaytiladi |
| **13** | Yaratilgan закупка ro'yxatda ko'rinishini tekshirish | Yangi zakупка status: **Проведен** holida ro'yxatda ko'rinadi |

---

## Post-conditions

- Tizimda yangi `Закупка` hujjati `Проведен` statusida mavjud
- Omborda `NovaCola 0.5L` uchun `5` ta qo'shilgan
- Yetkazib beruvchi `NovaWater` bilan qarzdorlik hosil bo'lgan

---

## Bog'liq test holatlari

| TC ID | Nomi | Bog'liqlik |
|-------|------|-----------|
| TC-ORDER-001 | Order yaratish | Ushbu закупka tomonidan toʻldirilgan ombordan sotiladi |
| TC-PAYMENT-001 | Qarzdorlikni so'ndirish | NovaWater bilan Взаиморасчет |

---

## Xatolar (muammo chiqqanda qarang)

| Qadam | Ehtimoliy muammo | Yechim |
|-------|-----------------|--------|
| 3 | Dropdown ochilmaydi | `#anor288-button-add` ID o'zgargan — codegen bilan qayta tekshir |
| 5 | `NovaWater` ko'rinmaydi | `step0` forma Angular yoki eski? URL dagi `/a2/` ni tekshir |
| 7 | Qidiruv maydoni (`#anor289`) bo'sh | ID o'zgargan bo'lishi mumkin — playwright mcp bilan locator ol |
| 11 | `Провести` bosilmaydi | Forma validatsiyasi — miqdor yoki narx maydonlari to'ldirilganmi? |
