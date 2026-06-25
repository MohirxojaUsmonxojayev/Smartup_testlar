# SmartupAuto — To'liq Bilimlar Bazasi

> Oxirgi yangilanish: 2026-06-24
> Saqlovchi: Claude Code (avtomatik)

Bu hujjat SmartupERP (xtrade) tizimidagi barcha modullar, formalar, test qamrovi va
loyiha arxitekturasi haqida yagona ma'lumotnoma sifatida yaratilgan. Har bir yangi
sessiyada bu faylni o'qib ishga kirishish tavsiya etiladi.

---

## 1. TIZIM HAQIDA UMUMIY MA'LUMOT

### 1.1 Server va muhit

| Parametr | Qiymat |
|---|---|
| Asosiy server | `https://app3.greenwhite.uz/xtrade` |
| Kompaniya kodi | `novatrade` |
| Kompaniya admin email | `admin@novatrade` |
| Test foydalanuvchi | `moxir@novatrade` |
| Filial | `NovaTrade - Toshkent Filiali` |

### 1.2 Frontend texnologiya

- **Framework:** AngularJS SPA (Single Page Application)
- **Custom elementlar:** `b-page`, `b-grid`, `b-input` — Smartup o'zining UI komponentlari
- **Menyu tuzilmasi:** yuqori navigatsion bar — har bir modul alohida menyu elementi
- **Locator strategiyasi:**
  - Odatda: `page.get_by_role("link", name="ModulNomi").click()` → sahifaga kiriladi
  - Muqobil: `page.get_by_role("button", name="ModulNomi").click()` — ba'zi modullar `<button>` sifatida render bo'ladi
  - Bir xil nomli linklar bo'lganda: `page.locator("#kt_header_menu").get_by_role("link", name="...").click()`
  - Bir nechta bir xil nomli element bo'lganda: `.nth(0)`, `.nth(2)`, `.first`

### 1.3 Test tekshirish mantiqi

Har bir forma uchun test quyidagini tekshiradi:
- Sahifa muvaffaqiyatli ochiladimi (timeout yo'q)
- Sahifada kutilgan tugma/matn ko'rinadimi

**Kutilgan elementlar (tipik):**

| Holat | Tekshiruv | Misol |
|---|---|---|
| Ro'yxat sahifasi | `b-page` → `"Создать"` | Ko'pchilik modullar |
| Jadval sahifasi | `b-grid` → ustun nomi | Омborlar, hisobotlar |
| Hisobot sahifasi | `b-page` → `"Параметры"` | Moliya hisobotlari |
| Ko'rish sahifasi | `b-page` → `"Просмотреть"` | Konstruktorlar |
| Maxsus sahifa | Boshqa locator | Har xil |

---

## 2. MODULLAR VA FORMALAR RO'YXATI

**Jami: 9 modul, 219 forma, 220 qadam (1 ta login + 219 ta forma)**

| # | Modul | Formalar soni |
|---|---|---|
| 1 | Главное | 11 |
| 2 | Продажа | 24 |
| 3 | Склад | 37 |
| 4 | Финансы | 41 |
| 5 | Кадры и зарплата | 10 |
| 6 | Производство | 14 |
| 7 | Справочники | 36 |
| 8 | Торговый маркетинг | 36 |
| 9 | Оборудование | 10 |

---

## 3. HAR BIR MODUL BATAFSIL

### 3.1 Главное (Asosiy) — 11 ta forma

Tizimning umumiy sozlamalari va boshqaruv bo'limi.

| Qadam | Forma nomi | Biznes maqsadi | Kutilgan element |
|---|---|---|---|
| 2 | Организации | Kompaniyalar/filiallar ro'yxati va yaratish | `b-page` → Создать |
| 3 | Пользователи | Tizim foydalanuvchilarini boshqarish | `b-page` → Создать |
| 4 | Проекты | Loyihalar boshqaruvi | `b-page` → Создать |
| 5 | Шаблоны накладных | Hisob-faktura shablonlari | `b-page` → Добавить |
| 6 | Настройки системы | Tizim konfiguratsiyasi | `b-page` → Сохранить |
| 7 | История изменений | Audit log — tizimda qilingan o'zgarishlar | `b-page` → Параметры |
| 8 | Шаги визита | Savdo vakili vizitining bosqichlari | `b-grid` → Роль |
| 9 | Настройки интеграции со сторонним ПО | Uchinchi tomon tizimlar bilan integratsiya | `form` → Сохранить |
| 10 | Объекты | Biznes ob'ektlar (locator: `button` + `menuitem`) | `b-grid` → Объект |
| 11 | Динамичные поля | Formalar uchun qo'shimcha dinamik maydonlar | `b-page` → Создать |
| 12 | Отчeты | Umumiy hisobotlar ro'yxati | `b-page` → Дополнительно |

**Eslatma:** Объекты formasiga kirish uchun `page.get_by_role("button", name="Главное").click()` → `page.get_by_role("menuitem", name="Объекты")` ishlatiladi (link emas, button).

---

### 3.2 Продажа (Savdo) — 24 ta forma

Savdo vakillarining ish jarayonlari: vizitlar, buyurtmalar, to'lovlar, hisobotlar.

| Qadam | Forma nomi | Biznes maqsadi | Kutilgan element |
|---|---|---|---|
| 13 | Визиты | Savdo vakili mijoz vizitlari jurnali | `heading` → Визиты |
| 14 | Архив визитов | Yopilgan vizitlar arxivi | `heading` → Архив визитов |
| 15 | Отслеживание пользователей | Foydalanuvchilar joylashuvini kuzatish | `complementary` → Обновить |
| 16 | Отслеживание мобильных представителей | Mobil vakilllarni real vaqt kuzatish | `trade-lib-tph-user-tracking` → Обновить |
| 17 | Планирование визитов | Vizitlar jadvalini rejalashtirish | `b-page` → Импорт |
| 18 | Планы | Savdo rejalari | `#kt_content` → Планы |
| 19 | Отслеживание оборудования | Reklama jihozlari joylashuvini kuzatish | `b-page` → Архивировать успешные |
| 20 | Фото- и видеоотчеты | Vizit davomida tushirilgan media | `b-page` → Применить |
| 21 | Заказы | Mijozlardan buyurtmalar (locator: `#trade81-button-add`) | `#trade81-button-add` → Создать |
| 22 | Архив заказов | Yopilgan buyurtmalar arxivi | `#kt_content` → Архив заказов |
| 23 | Отмененные заказы | Bekor qilingan buyurtmalar | `heading` → Отмененные заказы |
| 24 | Возвраты | Mijozlardan qaytarilgan tovarlar | `b-page` → Создать |
| 25 | Взаиморасчеты с клиентами | Mijozlar bilan o'zaro hisob-kitob | `b-page` → Взаиморасчет |
| 26 | Лиды | Potentsial mijozlar (leads) | `b-page` → Создать |
| 27 | Дашборд | Umumiy savdo dashboard | `b-page` → Сформировать |
| 28 | Дашборд по продажам | Savdo ko'rsatkichlari dashboard | `b-page` → Сформировать |
| 29 | Конструктор отчетов по продажам | Savdo hisobotlari quruvchisi | `b-page` → Параметры |
| 30 | Общий отчет по продажам (организации) | Tashkilotlar bo'yicha umumiy savdo hisoboti | `b-page` → Параметры |
| 31 | Задолженность покупателей по срокам задолженности | Xaridorlar qarzi muddat bo'yicha | `b-page` → Параметры |
| 32 | Расчет бонуса за оплату долга | Qarz to'lash uchun bonus hisoblash | `b-page` → Параметры |
| 33 | Коммерческий дашборд | Tijorat ko'rsatkichlari (locator: `smt-dropdown-button`) | `smt-dropdown-button` → Экспорт |
| 34 | Конструктор отчётов по визитам | Vizitlar hisobotlari quruvchisi (locator: button+menuitem) | `b-page` → Просмотр |
| 35 | Отчет по визитам | Vizitlar bo'yicha hisobot | `b-page` → Параметры |
| 36 | Анализ маршрута | Savdo vakili marshrutini tahlil | `b-page` → Параметры |

**Eslatma:** Отслеживание мобильных представителей va Конструктор отчётов по визитам uchun `page.get_by_role("button", name="Продажа").click()` → `page.get_by_role("menuitem", name="...")` ishlatiladi.

---

### 3.3 Склад (Ombor) — 37 ta forma

Ombor boshqaruvi: kirim, chiqim, ko'chirish, inventarizatsiya, hisobotlar.

| Qadam | Forma nomi | Biznes maqsadi | Kutilgan element |
|---|---|---|---|
| 37 | Ввод начальных остатков ТМЦ | Tovar-moddiy qiymatlar boshlang'ich qoldig'ini kiritish | `b-page` → Создать |
| 38 | Запросы на закупку | Xarid so'rovlari | `b-page` → Создать |
| 39 | Заказы на закупку | Xarid buyurtmalari | `b-page` → Создать |
| 40 | Закупки | Xaridlar jurnali (locator: `#anor288-button-add`) | `#anor288-button-add` → Создать |
| 41 | Дополнительные расходы | Qo'shimcha xarajatlar | `b-page` → Создать |
| 42 | Поступления ТМЦ на склад | Omborga TMZ kelishi (locator: `#anor113-button-add`) | `#anor113-button-add` → Создать |
| 43 | Возвраты поставщику | Ta'minotchiga qaytarish | `b-page` → Создать |
| 44 | Списания | TMZ hisobdan chiqarish | `b-page` → Создать |
| 45 | Инвентаризации | Ombor inventarizatsiyasi | `b-page` → Создать |
| 46 | Переоценки себестоимости ТМЦ | TMZ tannarxini qayta baholash | `b-page` → Создать |
| 47 | Взаиморасчеты с поставщиками | Ta'minotchilar bilan o'zaro hisob-kitob | `b-page` → Взаиморасчет |
| 48 | Пересчет приходных цен | Kirim narxlarini qayta hisoblash | `b-page` → Скорректировать |
| 49 | Прогноз для закупки | Xarid uchun prognoz | `b-page` → Создать |
| 50 | Запросы на внутр. перемещения | Ichki ko'chirish so'rovlari | `b-page` → Создать |
| 51 | Внутренние перемещения | Ombor ichida tovar ko'chirish (locator: `#anor132-button-add`) | `#anor132-button-add` → Создать |
| 52 | Запросы на межорг. перемещ.: отправка | Tashkilotlararo ko'chirish so'rovi (jo'natish) | `b-page` → Создать |
| 53 | Запросы на межорг. перемещ.: прием | Tashkilotlararo ko'chirish so'rovi (qabul) | `heading` → Запросы на межорг. перемещ.: прием |
| 54 | Межорг. перемещения: отправка | Tashkilotlararo jo'natish | `b-page` → Создать |
| 55 | Межорг. перемещения: прием | Tashkilotlararo qabul | `#kt_content` → Межорг. перемещения: прием |
| 56 | Архив межорг. перемещений | Yopilgan tashkilotlararo ko'chirmalar arxivi | `heading` → Архив межорг. перемещений |
| 57 | Отмененные межорг. перемещения | Bekor qilingan tashkilotlararo ko'chirmalar | `heading` → Отмененные межорг. перемещения |
| 58 | Поставщики | Ta'minotchilar ma'lumotnoması | `b-page` → Создать |
| 59 | Автотранспорт | Transport vositalari | `b-page` → Создать |
| 60 | Склады | Omborlar ro'yxati | `b-page` → Создать |
| 61 | Остатки ТМЦ | Tovar qoldiqlari (locator: `t` elementi) | `t` → Детали |
| 62 | Логистика | Logistika boshqaruvi (locator: `smt-data-table`) | `smt-data-table` → Создать |
| 63 | Рекламное оборудование | Reklama jihozlari (locator: button+menuitem) | `heading` → Рекламное оборудование |
| 64 | Материальный отчет | Moddiy hisobot | `b-page` → Параметры |
| 65 | Общий отчет по складам | Omborlar bo'yicha umumiy hisobot | `b-page` → Параметры |
| 66 | Конструктор отчетов по внутр. перемещениям | Ichki ko'chirmalar hisobotlari quruvchisi | `b-page` → Параметры |
| 67 | Конструктор отчетов по запросам на закуп | Xarid so'rovlari hisobotlari quruvchisi | `b-page` → Просмотр |
| 68 | Конструктор отчетов по закупкам | Xaridlar hisobotlari quruvchisi | `b-page` → Просмотреть |
| 69 | Конструктор отчетов по поступлениям | Kirimlar hisobotlari quruvchisi | `b-page` → Просмотреть |
| 70 | Конструктор отчетов по списанию | Hisobdan chiqarish hisobotlari quruvchisi | `b-page` → Просмотреть |
| 71 | Конструктор отчетов по запросам на межорг. перемещения | Tashkilotlararo ko'chirish so'rovlari quruvchisi | `b-page` → Просмотреть |
| 72 | Конструктор отчетов по межорг. перемещениям | Tashkilotlararo ko'chirmalar hisobotlari quruvchisi | `b-page` → Просмотреть |
| 73 | Отчёт по отгрузкам и оплатам | Jo'natmalar va to'lovlar hisoboti | `b-page` → Параметры |

**Eslatma:** Рекламное оборудование uchun `page.get_by_role("button", name="Склад").click()` → `page.get_by_role("menuitem", name="Рекламное оборудование")` ishlatiladi.

---

### 3.4 Финансы (Moliya) — 41 ta forma

Moliyaviy operatsiyalar: kassa, bank, to'lovlar, buxgalteriya, hisobotlar.

| Qadam | Forma nomi | Biznes maqsadi | Kutilgan element |
|---|---|---|---|
| 74 | Кассовые документы | Kassa operatsiyalari | `b-page` → Создать |
| 75 | Банковские выписки | Bank ko'chirma hisobotlari | `b-page` → Создать |
| 76 | Документы чековой книжки | Chek daftari hujjatlari | `b-page` → Создать |
| 77 | Платежные поручения | To'lov topshiriqnomalari | `b-page` → Создать |
| 78 | Платежные требования | To'lov talabnomalari | `b-page` → Создать |
| 79 | Ручные операции | Qo'lda kiritilgan moliyaviy operatsiyalar | `b-page` → Создать |
| 80 | Переоценки валют | Valyuta qayta baholash | `b-page` → Создать |
| 81 | Уставный капитал | Ustav kapitali | `b-page` → Создать |
| 82 | Взаиморасчеты | Umumiy o'zaro hisob-kitoblar | `b-page` → Создать |
| 83 | Перекидка аванса клиентов / поставщиков | Avans mablag'larini ko'chirish | `b-page` → Создать |
| 84 | Оплаты от клиентов | Mijozlardan to'lovlar | `b-page` → Создать |
| 85 | Оплаты поставщикам | Ta'minotchilarga to'lovlar | `b-page` → Создать |
| 86 | Запросы об оплате | To'lov so'rovlari | `heading` → Запросы об оплате |
| 87 | Мои заявки | Foydalanuvchining o'z to'lov arizalari | `b-page` → Создать |
| 88 | Согласование | To'lovlarni tasdiqlash jarayoni | `heading` → Согласование |
| 89 | Оплаты (реестр) | To'lovlar reestri (`.nth(2)` — uchinchi link) | `heading` → Оплаты |
| 90 | Документооборот | Hujjat aylanmasi | `heading` → Документооборот |
| 91 | Валюты | Valyutalar ma'lumotnoması | `b-page` → Создать |
| 92 | План счетов | Hisoblar rejasi (chart of accounts) | `b-page` → Создать |
| 93 | Виды операций | Operatsiya turlari | `b-page` → Создать |
| 94 | Договоры | Shartnomalar | `b-page` → Создать |
| 95 | Статьи доходов | Daromad moddalari | `b-page` → Прикрепление |
| 96 | Статьи расходов | Xarajat moddalari | `b-page` → Прикрепление |
| 97 | Дашборд по финансам | Moliya dashboard | `b-page` → Аналитика по счету |
| 98 | Конструктор отчетов по финансам | Moliya hisobotlari quruvchisi | `b-page` → Просмотреть |
| 99 | Акт-сверки | Muhammasala akti | `b-page` → Параметры |
| 100 | Оборотно-сальдовая ведомость | Aylanma-qoldiq xisoboti (exact) | `b-page` → Параметры |
| 101 | Оборотно-сальдовая ведомость(BETA) | Beta aylanma-qoldiq vedomosti | `b-page` → Закрыть |
| 102 | Оборотно-сальдовая ведомость по счету | Hisob bo'yicha aylanma-qoldiq | `b-page` → Параметры |
| 103 | Проводки счетов | Hisob yozuvlari | `b-page` → Параметры |
| 104 | Карточка счета | Hisob kartochkasi | `b-page` → Параметры |
| 105 | Анализ счета | Hisob tahlili | `b-page` → Параметры |
| 106 | Прибыль и убыток (P&L) | Foyda va zarar hisoboti | `b-page` → Параметры |
| 107 | Отчет о прибылях и убытках (БЕТА) | Beta foyda-zarar hisoboti | `b-page` → Закрыть |
| 108 | Отчет о движении денежных средств (БЕТА) | Beta pul oqimi hisoboti | `b-page` → Закрыть |
| 109 | Денежный поток | Pul oqimi | `b-page` → Параметры |
| 110 | Оплаты (отчет) | To'lovlar hisoboti (`.nth(3)` — to'rtinchi link) | `b-page` → Параметры |
| 111 | Отчет по должникам | Qarzdorlar hisoboti | `b-page` → Параметры |
| 112 | Обороты по контрагентам | Kontragentlar bo'yicha aylanmalar | `b-page` → Параметры |
| 113 | Бухгалтерский баланс | Buxgalteriya balansi | `b-page` → Просмотреть |
| 114 | Журнал документов | Hujjatlar jurnali | `heading` → Журнал документов |

**Muhim locator eslatmasi:** "Оплаты" nomi bir necha marta takrorlanadi. Reestр uchun `.nth(2)`, hisobot uchun `.nth(3)` ishlatiladi.

---

### 3.5 Кадры и зарплата (HR va ish haqi) — 10 ta forma

Xodimlarni boshqarish va ish haqi hisoblash.

| Qadam | Forma nomi | Biznes maqsadi | Kutilgan element |
|---|---|---|---|
| 115 | Расчеты зарплаты | Ish haqi hisoblash | `b-page` → Создать |
| 116 | Выплаты | Ish haqi to'lovlari | `b-page` → Создать |
| 117 | Бонусная система | Bonus tizimi | `b-page` → Создать |
| 118 | Сотрудники | Xodimlar ma'lumotnoması | `b-page` → Создать |
| 119 | Отделы | Bo'limlar/departamentlar | `b-page` → Создать |
| 120 | Должности | Lavozimlar | `b-page` → Создать |
| 121 | Виды начислений | Hisoblash turlari | `b-page` → Создать |
| 122 | Виды удержаний | Ushlab qolish turlari | `b-page` → Создать |
| 123 | Виды выплат | To'lov turlari | `b-page` → Создать |
| 124 | Отчёт по начислениям и выплатам персоналу | Xodimlarga to'lov hisoboti | `b-page` → Параметры |

---

### 3.6 Производство (Ishlab chiqarish) — 14 ta forma

Ishlab chiqarish jarayonlari: rejalashtirish, markировка, texnologik operatsiyalar.

| Qadam | Forma nomi | Biznes maqsadi | Kutilgan element |
|---|---|---|---|
| 125 | Журнал план производства | Ishlab chiqarish rejalari jurnali | `b-page` → Создать |
| 126 | План производства | Ishlab chiqarish rejasi (exact, `#kt_header_menu`) | `b-page` → Создать |
| 127 | Технологические операции | Texnologik operatsiyalar | `b-page` → Создать |
| 128 | Заказы кодов маркировки | Markirovka kodlari buyurtmalari | `b-page` → Создать |
| 129 | Отчет о нанесении | Markirovka tatbiq etish hisoboti | `b-page` → Создать |
| 130 | Заказ на производство | Ishlab chiqarish buyurtmasi | `b-page` → Создать |
| 131 | Производственные задания | Ishlab chiqarish vazifalari | `heading` → Производственные задания |
| 132 | Ввод производственных остатков ТМЦ | Ishlab chiqarish TMZ qoldig'ini kiritish | `heading` → Ввод производственных остатков ТМЦ |
| 133 | Спецификация | Mahsulot spetsifikatsiyasi | `b-page` → Создать |
| 134 | Ресурсы/доп.затраты | Resurslar va qo'shimcha xarajatlar | `b-page` → Создать |
| 135 | Технологическая карта | Texnologik xarita | `b-page` → Создать |
| 136 | Оборудование | Ishlab chiqarish jihozlari (`.first` — birinchi link) | `b-page` → Добавить |
| 137 | Обеспечение производства | Ishlab chiqarishni ta'minlash | `b-page` → Параметры |
| 138 | Движение ТМЦ в производстве | Ishlab chiqarishdagi TMZ harakati | `b-page` → Параметры |

**Muhim locator eslatmasi:** "Оборудование" nomi ham bu modulda, ham alohida `Оборудование` modulida mavjud. Bu modulda `.first` ishlatiladi.

---

### 3.7 Справочники (Ma'lumotnoмalar) — 36 ta forma

Tizimning asosiy ma'lumotlar bazasi: tovarlar, narxlar, mijozlar, xodimlar va boshqa.

| Qadam | Forma nomi | Biznes maqsadi | Kutilgan element |
|---|---|---|---|
| 139 | ТМЦ | Tovar-moddiy qiymatlar (locator: `#anor50-button-text-add`) | `#anor50-button-text-add` → Создать |
| 140 | Цены | Narxlar (locator: `#anor182-button-add`) | `#anor182-button-add` → Создать |
| 141 | Услуги | Xizmatlar (locator: `#anor50-button-add`) | `#anor50-button-add` → Создать |
| 142 | Скидки/наценки | Chegirma va ustama narxlar | `b-grid` → Название |
| 143 | Производители | Ishlab chiqaruvchilar | `b-page` → Создать |
| 144 | Типы фото-отчетов | Foto-hisobot turlari | `b-page` → Прикрепление |
| 145 | Типы видео-отчетов | Video-hisobot turlari | `b-page` → Прикрепление |
| 146 | Комментарии | Izohlar ma'lumotnoması | `b-page` → Прикрепление |
| 148 | Опросники | So'rovnomalar (exact, step 148) | `b-page` → Прикрепление |
| 149 | Регионы | Mintaqalar | `b-page` → Создать |
| 150 | Вопросы двойного визита | Ikki tomonlama vizit savollari | `b-page` → Создать |
| 151 | Опросники двойных визитов | Ikki tomonlama vizit so'rovnomalari | `b-page` → Создать |
| 152 | Презентации | Taqdimotlar | `b-page` → Создать |
| 153 | Продавцы | Sotuvchilar | `b-grid` → Название |
| 154 | Физические лица | Jismoniy shaxslar | `b-page` → Создать |
| 155 | Юридические лица | Yuridik shaxslar | `b-page` → Создать |
| 156 | Отделы | Bo'limlar (Справочники ichida) | `b-page` → Создать |
| 157 | Должности | Lavozimlar (Справочники ichida) | `b-page` → Создать |
| 158 | Рабочие зоны | Ish zonalari (hududiy) | `b-page` → Создать |
| 159 | Штат | Shtat jadvali | `b-page` → Создать |
| 160 | Клиенты | Mijozlar ma'lumotnoması | `b-page` → Создать |
| 161 | Уведомления | Bildirishnomalar | `b-page` → Создать |
| 162 | Акции | Aksiyalar (locator: `#anor717-button-add`) | `#anor717-button-add` → Создать |
| 163 | Нагрузки | Yuklamalar (locator: `#anor723-button-add`) | `#anor723-button-add` → Создать |
| 164 | Рекомендации | Tavsiyalar | `b-page` → Создать |
| 165 | Правила ограничений | Cheklash qoidalari | `b-page` → Создать |
| 166 | Продуктовая корзина | Mahsulot savati | `b-page` → Создать |
| 167 | Сеты ТМЦ | TMZ to'plamlari | `b-page` → Создать |
| 168 | Лимитирование ТМЦ | TMZ limitlari | `b-page` → Создать |
| 169 | Вопросы категоризации | Kategoriyalash savollari | `b-page` → Создать |
| 170 | Категоризация физических лиц | Jismoniy shaxslar kategoriyalash | `b-grid` → Название |
| 171 | Категоризация юридических лиц | Yuridik shaxslar kategoriyalash | `b-grid` → Название |
| 172 | Результат категоризации | Kategoriyalash natijalari | `b-grid` → Пользователь |
| 173 | Отчет по результату категоризации | Kategoriyalash natijasi hisoboti | `b-page` → Просмотреть |
| 174 | Публикация в бот | Telegram bot e'lonlari | `b-page` → Добавить |
| 175 | Минимальные обязательные ассортименты | Minimal majburiy assortiment (Справочники) | `b-page` → Создать |

**Eslatma:** Qadam 147 raqami ko'rinmaydi — Справочники bo'limida ketma-ketlikda tushib qolgan. Bu xato emas — test kodida ham 148-dan davom etadi.

---

### 3.8 Торговый маркетинг (Savdo marketingi) — 36 ta forma

Merchandayzing, KPI tizimi, assortiment, planogramma, raqobatchilar tahlili va hisobotlar.

| Qadam | Forma nomi | Biznes maqsadi | Kutilgan element |
|---|---|---|---|
| 176 | Настройки мерчандайзинга | Merchandayzing sozlamalari | `b-page` → Создать |
| 177 | Мерчандайзинг | Merchandayzing jurnali (exact) | `b-grid` → Пользователь |
| 178 | КПЭ по штатам | Shtat bo'yicha KPI | `b-page` → Создать |
| 179 | КПЭ по рабочим зонам | Ish zonalari bo'yicha KPI | `b-page` → Создать |
| 180 | КПЭ по характеристикам ТМЦ | TMZ xususiyatlari bo'yicha KPI (`#kt_header_menu`) | `b-page` → Создать |
| 181 | КПЭ по ТМЦ | TMZ bo'yicha KPI (`#kt_header_menu`) | `b-page` → Создать |
| 182 | КПЭ по клиентам | Mijozlar bo'yicha KPI (`#kt_header_menu`) | `b-page` → Создать |
| 183 | КПЭ клиентов по ТМЦ | Mijozlar TMZ bo'yicha KPI (`#kt_header_menu`) | `b-page` → Создать |
| 184 | КПЭ клиентов по характеристикам ТМЦ | Mijozlar TMZ xususiyatlari bo'yicha KPI (`#kt_header_menu`) | `b-page` → Создать |
| 185 | КПЭ на категорию клиентов по характеристикам ТМЦ | Mijoz kategoriyasi TMZ xususiyatlari KPI (`#kt_header_menu`) | `b-page` → Создать |
| 186 | Шаблон КПЭ | KPI shabloni | `b-page` → Сохранить |
| 187 | Настройки бонуса | Bonus sozlamalari | `b-page` → Создать |
| 188 | Дашборд по КПЭ | KPI dashboard | `b-page` → Сформировать |
| 189 | Настройка характеристики | Xususiyat sozlamalari | `b-page` → Создать |
| 190 | Минимальные обязательные ассортименты | Minimal majburiy assortiment (TM) | `b-page` → Создать |
| 191 | Ассортименты | Assortimentlar (exact) | `b-page` → Создать |
| 192 | Планограммы | Planogrammalar | `b-page` → Прикрепление |
| 193 | POS-материалы | POS materiallar | `b-page` → Прикрепление |
| 194 | Причины несоответствия | Muvofiqsizlik sabablari | `b-page` → Прикрепление |
| 195 | Конкуренты | Raqobatchilar | `b-page` → Прикрепление |
| 196 | Шаблон отчета по опросам | So'rov hisoboti shabloni | `b-page` → Создать |
| 197 | Продукты конкурентов | Raqobatchilar mahsulotlari | `b-grid` → Название |
| 198 | Статусы мерчандайзинга | Merchandayzing statuslari | `b-page` → Прикрепление |
| 199 | Отчет по доле на полке | Javon ulushi hisoboti | `b-page` → Параметры |
| 200 | Отчет по ассортиментам | Assortiment hisoboti | `b-page` → Параметры |
| 201 | Отчет по планограмме | Planogramma hisoboti | `b-page` → Параметры |
| 202 | Отчет по ценам на полке | Javon narxlari hisoboti | `b-page` → Параметры |
| 203 | Отчет по POS-материалам | POS materiallar hisoboti | `b-page` → Параметры |
| 204 | Сводный отчет по мерчандайзингу | Yig'ma merchandayzing hisoboti | `b-page` → Параметры |
| 205 | Отчет об отсутствии или несоответствии | Yo'qlik yoki muvofiqsizlik hisoboti | `b-page` → Параметры |
| 206 | Отчет анализа цен | Narx tahlili hisoboti | `b-page` → Параметры |
| 207 | Отчет по мерчандайзингу | Merchandayzing hisoboti (exact) | `b-page` → Начало периода |
| 208 | Экспорт фото и видео отчетов по визитам | Vizit foto/video eksporti | `b-page` → Параметры |
| 209 | Отчет по ценникам конкурентов | Raqobatchilar narx hisoboti | `b-page` → Сформировать |
| 210 | Отчет по статусам мерчандайзинга | Merchandayzing statuslari hisoboti | `b-page` → Сформировать |
| 211 | Конструктор отчетов по долям на полках | Javon ulushi hisobotlari quruvchisi | `b-page` → Просмотр |

**Muhim locator eslatmasi:** КПЭ formalarining ko'pchiligi uchun `page.locator("#kt_header_menu").get_by_role("link", name="...")` ishlatiladi — chunki menyu elementlari ambiguos (bir xil nom boshqa joyda ham bor).

---

### 3.9 Оборудование (Jihozlar) — 10 ta forma

Savdo nuqtalari uchun reklama va ishlab chiqarish jihozlarini boshqarish.

| Qadam | Forma nomi | Biznes maqsadi | Kutilgan element |
|---|---|---|---|
| 212 | Заявки на оборудование | Jihozlar bo'yicha arizalar | `b-page` → Установить |
| 213 | Заявки на перемещения | Ko'chirish arizalari | `b-page` → Создать |
| 214 | Межорг. перемещение оборудования: отправка | Tashkilotlararo jihozlar jo'natmasi | `b-page` → Создать |
| 215 | Межорг. перемещение оборудования: прием | Tashkilotlararo jihozlar qabuli | `b-grid` → Вид перемещения |
| 216 | Заявки на ремонт | Ta'mirlash arizalari | `b-grid` → Номер заявки |
| 217 | Неисправности оборудования | Jihozlar nosozliklari (menyu nomi: "Неисправности оборудовния" — typo!) | `b-page` → Прикрепление |
| 218 | Конструктор отчетов по заявкам на оборудование | Jihozlar arizalari hisobotlari quruvchisi | `b-page` → Просмотреть |
| 219 | Цели для рекламного оборудования | Reklama jihozlari maqsadlari | `b-page` → Создать |
| 220 | Остатки по рекламному оборудованию | Reklama jihozlari qoldiqlari | `b-grid` → Оборудование |
| 221 | Характеристики оборудования | Jihozlar xususiyatlari | `b-page` → Создать |

**Muhim eslatma:** "Неисправности оборудования" formasining menyu linki `"Неисправности оборудовния"` — "а" harfi tushib qolgan (typo tizimda). Test ham shu yozuv bilan ishlaydi.

---

## 4. TEST STSENARIYLAR XARITASI

### 4.1 Mavjud test fayllar

| Fayl | Test funksiya | Qadam soni | Maqsadi |
|---|---|---|---|
| `tests/regression/test_auth.py` | `test_admin_login` | 2 | Admin kirishi + filial tanlash |
| `tests/regression/test_auth.py` | `test_user_login` | 2 | Foydalanuvchi kirishi + filial tanlash |
| `tests/regression/test_check_forms_opening.py` | `test_check_forms_opening` | 220 | 219 ta forma ochilishini tekshirish |

### 4.2 Login foydalanuvchilari

| Tur | Login | Parol manba | Filial |
|---|---|---|---|
| Admin | `admin@novatrade` | `--company-password` (greenwhite) | NovaTrade - Toshkent Filiali |
| Foydalanuvchi | `moxir@novatrade` | hardcode `"1"` | NovaTrade - Toshkent Filiali |

`test_check_forms_opening` → `run_user_login` chaqiradi (moxir@novatrade bilan kiradi).

### 4.3 Forma tekshiruv strategiyasi

Har bir forma uchun test:
1. Modul linkini bosadi
2. Forma/sahifa linkini bosadi
3. Kutilgan element ko'rinishini tekshiradi (120 soniya timeout)

Tekshiruv muvaffaqiyatli bo'lsa: step PASSED, davom etiladi.
Tekshiruv muvaffaqiyatsiz bo'lsa: step FAILED, test butunlay to'xtaydi.

### 4.4 Allure hisobot tuzilmasi

```
Epic:   Regression
Feature: Formalar ochilishi
Story:  Barcha bo'limlar
```

---

## 5. NOMA'LUM / TAHLIL KERAK FORMALAR

### 5.1 Qadam raqami tushib qolganlar

| Holat | Tafsilot |
|---|---|
| Qadam 147 yo'q | Справочники bo'limida 146-dan 148-ga o'tiladi. Menyu'da shu raqamdagi forma yo'q yoki o'chirilgan. |

### 5.2 Typo-lar (tizimda xato yozuvlar)

| Forma | Muammo | Qanday ishlashini |
|---|---|---|
| Неисправности оборудования | Menyu linki `"Неисправности оборудовния"` — "а" yo'q | Test ham shu yozuv bilan ishlaydi, o'zgartirmaslik kerak |

### 5.3 Noaniq locatorlar (ehtiyotkorlik kerak)

| Forma | Sabab | Yechim |
|---|---|---|
| Оплаты (reestр) | "Оплаты" nomi 4 joyda uchrаydi | `.nth(2)` — uchinchi link |
| Оплаты (hisobot) | "Оплаты" nomi 4 joyda uchrаydi | `.nth(3)` — to'rtinchi link |
| Оборудование (Производство) | Ikkita "Оборудование" linki bor | `.first` — birinchi link |
| КПЭ formalar | Navigatsion menyuda bir xil nomlar | `#kt_header_menu` locator orqali aniqlashtirish |

### 5.4 Biznes logikasi hali tushunilmagan formalar

Quyidagi formalar texnik jihatdan testdan o'tadi, lekin biznes maqsadi to'liq aniqlanmagan:

- **Шаги визита** — vizit bosqichlari qanday sozlanadi?
- **Динамичные поля** — qaysi formlarga qo'shimcha maydonlar qo'shilishi mumkin?
- **Прогноз для закупки** — prognoz qanday algoritmda hisoblanadi?
- **Обеспечение производства** — qanday ma'lumotlar tahlil qilinadi?
- **Планограммы / POS-материалы** — fayllar qanday tarkibda bo'lishi kerak?

---

## 6. LOYIHA TEXNIK ARXITEKTURASI

### 6.1 Fayl tuzilmasi

```
SmartupAuto/
├── .env                              ← Telegram token/chat_id (gitignored)
├── CLAUDE.md                         ← Claude Code ko'rsatmalari
├── pytest.ini                        ← pytest konfiguratsiyasi
├── requirements.txt                  ← Python kutubxonalar
├── run_tests.bat                     ← Regression testlarni headless ishlatish
├── run_tests.sh                      ← Linux/Mac variant
├── start_bot.bat                     ← Telegram botni terminal'da ishlatish
├── start_bot_hidden.ps1              ← Telegram botni fon rejimda ishlatish
├── stop_bot.bat                      ← Bot jarayonini to'xtatish
├── setup_scheduler.ps1               ← Windows Task Scheduler o'rnatish
│
├── utils/
│   ├── telegram_sender.py            ← Telegram API HTTP POST (faqat requests)
│   ├── telegram_reporter.py          ← pytest plugin: natijalarni Telegram'ga
│   ├── telegram_bot.py               ← Long-polling bot: /run tugmasi
│   └── logger.py                     ← Test log yozish
│
├── tests/regression/
│   ├── conftest.py                   ← Fixtures, pytest hooks, TelegramReporter
│   ├── test_auth.py                  ← Login testlari
│   ├── test_check_forms_opening.py   ← 219 forma tekshiruvi
│   ├── AUTORUN_GUIDE.md              ← Avtorun va bot qo'llanmasi
│   ├── COMMANDS.md                   ← Ishlatish buyruqlari
│   └── flows/
│       ├── flow_authorization.py     ← Kirish oqimi
│       └── flow_navigate.py          ← Navigatsiya (filial tanlash)
│
├── docs/
│   └── KNOWLEDGE_BASE.md             ← Bu fayl
│
└── test-results/
    ├── autorun.log                   ← run_tests.bat logi
    ├── bot.pid                       ← Bot jarayon ID
    ├── bot_out.log / bot_err.log     ← Bot loglar
    ├── allure-results/               ← Allure xom ma'lumotlar
    ├── allure-report/                ← Allure HTML hisoboti
    ├── traces/                       ← Playwright trace .zip
    │   └── regression_trace.zip      ← Har run yangilanadi
    ├── logs/                         ← FAIL bo'lganda xato loglari
    └── data/
        └── data_store.json           ← Sessiyalararo ma'lumot saqlash
```

### 6.2 Asosiy conftest fixtures

| Fixture | Scope | Maqsadi |
|---|---|---|
| `session_browser` | session | Butun sessiya uchun bitta Chromium |
| `session_context` | session | Trace yoziladi, sessiya oxirida `regression_trace.zip` |
| `session_page` | session | Barcha sessiya testlari uchun yagona sahifa |
| `browser` | function | Har bir test uchun alohida browser |
| `page` | function | Har bir test uchun yangi sahifa + trace |
| `code` | session | Unikal 6 raqamli sessiya kodi |
| `save_data` / `load_data` | session | JSON orqali testlar orasida ma'lumot uzatish |

### 6.3 Avtorun tizimi

| Komponent | Vazifasi |
|---|---|
| Windows Task Scheduler | Har 6 soatda (00:00/06:00/12:00/18:00) `run_tests.bat` ishlatadi |
| `run_tests.bat` | headless regression testlarni ishlatadi, `autorun.log`'a yozadi |
| `TelegramReporter` pytest plugin | Test boshida va oxirida Telegram'ga xabar yuboradi |
| `telegram_bot.py` | `/run` buyruqi yoki "Run Tests Now" tugmasi orqali qo'lda ishlatish |

### 6.4 Telegram bot buyruqlari

| Buyruq | Kimga | Natija |
|---|---|---|
| `/start` | Faqat admin | Boshqaruv paneli (inline keyboard) |
| `/run` | Faqat admin | Boshqaruv paneli |
| `/id` | Hamma | Telegram ID ko'rsatadi |
| "Run Tests Now" tugmasi | Faqat admin | `run_tests.bat` subprocess sifatida ishga tushadi |

---

## 7. ISHLATISH QOIDALARI (Assisstent uchun)

### 7.1 Yangi forma qo'shish qoidasi

Yangi forma testi qo'shishda:
1. Qadam raqamini davom ettir (hozir max: 221)
2. `run_check_forms_opening` funksiyasiga step qo'sh
3. `test_check_forms_opening` docstring'idagi sana va raqamlarni yangiyla
4. `COMMANDS.md` va bu KNOWLEDGE_BASE.md ni yangiyla

### 7.2 Locator strategiyasi (xatolardan saqlaning)

- **`b-page` vs `heading`:** Ro'yxat sahifalari `b-page`, modal/panel sahifalar `heading` ishlatadi
- **`button` vs `link`:** Ba'zi menyu elementlari `button` sifatida render bo'ladi — test ishlamasa shuни tekshiring
- **`#kt_header_menu`:** Bir xil nomdagi linklar bo'lganda menyu containerini aniqlashtiring
- **`.nth(N)`:** Bir xil nomli bir nechta link bo'lganda indeks orqali tanlang

### 7.3 Xato topilganda tekshirish tartibi

1. Playwright Trace Viewer → `test-results/traces/regression_trace.zip`
2. Allure hisoboti → `allure open test-results/allure-report`
3. Xato logi → `test-results/logs/`
4. Bot logi → `test-results/bot_err.log`

### 7.4 Tizim cheklovlari

- **Trace fayllar:** Har run yangilanadi, oldingi overwrite bo'ladi
- **Bot parallel:** Bir vaqtda faqat bitta test run bo'lishi mumkin (`_is_running()` tekshiruvi)
- **Admin ruxsati:** Bot buyruqlari faqat `TELEGRAM_CHAT_ID` egasiga ishlaydi
- **`.env` gitignore:** Token va chat_id hech qachon git'ga tushmasligi kerak
