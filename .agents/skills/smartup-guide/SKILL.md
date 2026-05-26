---
name: smartup-guide
description: Smartup ilovasiga xos biznes bilimlar, UI joylashuvlari, contract/order flowlari, locator kuzatuvlari va test yozishda ishlatiladigan domain qoidalari. Smartup sahifalari, formalar, contract, order, payment type, modal, navigation yoki loyiha UI xatti-harakati haqida ishlaganda foydalan.
---

# Smartup Guide

Bu skill Smartup bo'yicha bilimlarni tez topish uchun index vazifasini bajaradi. Batafsil bilimlar `references/` ichida domainlarga bo'lingan.

## Qidirish Tartibi

1. User so'rovidagi domainni aniqlash: contract, order, list/grid, Biruni error, setup/debug.
2. Agar so'rov aniq forma haqida bo'lsa, avval `references/forms/<form-slug>.md` dossier faylini o'qi.
3. Keyin kerak bo'lsa quyidagi domain reference fayllardan faqat keraklisini o'qi.
4. Agar kerakli bilim topilmasa, UI/test/trace orqali aniqlab, tegishli form dossier yoki reference faylga qisqa va tagli qilib qo'sh.

## Reference Xarita

- Forma dossierlari: [references/forms/](references/forms/)
- Contract va contract shartlari: [references/contracts.md](references/contracts.md)
- Order biznes qoidalari va flowlar: [references/orders.md](references/orders.md)
- Smoke runner setup zanjiri: [references/smoke-runner.md](references/smoke-runner.md)
- Smartup UI, locator, modal, grid patternlari: [references/ui-patterns.md](references/ui-patterns.md)
- Test setup, debug va screenshot arxivi: [references/testing-debug.md](references/testing-debug.md)

## Form Dossier Qoidasi

Har bir muhim forma uchun bitta dossier fayl bo'lsin:

```text
references/forms/<form-slug>.md
```

Dossier ichida shu mavzu bo'yicha bir harakatda kerak bo'ladigan ma'lumotlar turadi:

- URL pattern va navigation
- screenshot pathlari
- visual regression uchun baseline/current screenshot state nomlari va metadata
- asosiy locatorlar
- ishlatiladigan flow/helper/test fayllari
- related business rules
- known issues/debug notes

Misol: contract view haqida so'ralganda avval [references/forms/contract-view.md](references/forms/contract-view.md) o'qiladi.

## Bilim Qo'shish Formati

Yangi bilim tegishli faylga quyidagi formatda qo'shilsin:

```markdown
### <qisqa mavzu>
Tags: contract, order, payment-type, grid, error, setup, locator
- <qayerda>: <sahifa yoki flow>
- <qoida>: <biznes/UI xatti-harakati>
- <testda ishlatish>: <qanday assert yoki flow kerak>
```

## Asosiy Eslatma

- Smartup bo'yicha yangi biznes qoida, UI xatti-harakati, xato sababi yoki locator topilsa, shu skillning mos reference fayliga yoz.
- Dublikat kod, noto'g'ri testcase yoki flowga ajratilishi kerak bo'lgan takrorlanish ko'rinsa, foydalanuvchiga alohida xabar ber.
- Har bir Smartup/test vazifasi yakunida bajarilgan ish xulosasi, o'rganilgan biznes/UI bilimlar, muhim locatorlar, screenshot pathlari va debug notes mos form dossier yoki reference faylga tartibli yozib qo'yilsin.
