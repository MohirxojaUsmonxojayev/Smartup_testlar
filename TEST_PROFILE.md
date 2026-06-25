# SmartupERP — Test Profil Bilim Bazasi

**Kompaniya nomi:** NovaTrade Distribution Co  
**Tarmoq:** Oziq-ovqat va iste'mol tovarlari distribyusiyasi (FMCG)  
**Hudud:** Toshkent, O'zbekiston  
**Valyuta:** O'zbek so'mi (UZS)

> Bu fayl SmartupERP tizimida test muhitini yaratish uchun zarur bo'lgan barcha
> biznes ma'lumotlarini o'z ichiga oladi. Har bir bo'lim sherigingizning testlari
> qanday nom va kod formatidan foydalanishini ko'rsatadi.

---

## 1. KOMPANIYA (Company)

Sherigingizning testi `--create-company` flagi bilan yangi company yaratadi.
Sizning testingizda esa **mavjud company** bilan ishlaysiz (`--company-code` + `--company-password`).

| Maydon           | Qiymat                        |
|------------------|-------------------------------|
| **Kod sервера**  | `novatrade`                   |
| **Nomi**         | `NovaTrade Distribution Co`   |
| **Til**          | Русский                        |
| **Markировка**   | UZ Marking                    |
| **План счетов**  | UZ COA                        |
| **Банки**        | UZ BANK                       |
| **Products**     | trade (+ barcha child modullari yoqilgan) |

### Yoqiladigan Trade modullari:
- Call center, Equipment, Finance - Main, Finance - Advanced
- HR and Payroll, Image Recognition, Main, Manufacturing
- Marking, Sales - Main, Sales - Advanced, Store, Telegram
- Trade Marketing, Uzbekistan Module, Warehouse - Main, Warehouse - Advanced

### Admin login ma'lumotlari:
| Maydon     | Qiymat                          |
|------------|---------------------------------|
| **Email**  | `admin@novatrade`               |
| **Parol**  | *(test parolingizni yozing)*    |

---

## 2. YURIDIK SHAXS (Legal Person)

### 2.1 Asosiy yuridik shaxs (Kompaniya o'zi)

| Maydon             | Qiymat                                          |
|--------------------|-------------------------------------------------|
| **Kod**            | `novatrade_legal`                               |
| **To'liq nomi**    | `NovaTrade Distribution Co LLC`                 |
| **Qisqa nomi**     | `NovaTrade Dist Co`                             |
| **INN/TIN**        | `307456123`                                     |
| **Telefon**        | `998971234567`                                  |
| **Email**          | `info@novatrade.uz`                             |
| **Telegram**       | `@novatrade_official`                           |
| **Veb-sayt**       | `https://novatrade.uz`                          |
| **Mintaqa**        | город Ташкент                                   |
| **Manzil**         | `Toshkent sh., Yunusobod tumani, Amir Temur ko'chasi 108`  |
| **Pochta manzili** | `Toshkent sh., Yunusobod tumani, Amir Temur ko'chasi 108`  |
| **Pochta indeksi** | `100084`                                        |
| **CEA kodi**       | `62010`                                         |
| **QQS kodi**       | `320045678901`                                  |
| **Shtrix-kod**     | `4690046123456`                                 |
| **GPS**            | `41.2994958,69.2400734,12`                      |
| **Holati**         | Активный                                        |

#### Bank hisob raqami:
| Maydon            | Qiymat                                                    |
|-------------------|-----------------------------------------------------------|
| **Hisob nomi**    | `Asosiy hisob raqam - NovaTrade`                          |
| **MFO**           | `00001`                                                   |
| **Bank nomi**     | `Центр расчетов Центрального банка по г. Ташкенту`        |
| **Hisob raqam**   | `20208000456789012345`                                    |
| **Valyuta**       | Узбекский сум                                             |
| **Asosiy?**       | Да (belgilangan)                                          |

#### Rahbar ma'lumotlari (Руководящие должности):
| Lavozim           | F.I.Sh.                              | INN            |
|-------------------|--------------------------------------|----------------|
| **Direktor**      | Karimov Jasur Abdullayevich          | `41234567890123` |
| **Bosh hisobchi** | Yusupova Malika Rashidovna           | —              |

### 2.2 Egasi — alohida yuridik shaxs (Собственник)

| Maydon          | Qiymat                                      |
|-----------------|---------------------------------------------|
| **Kod**         | `novatrade_owner`                           |
| **Nomi**        | `NovaTrade Holding Group LLC`               |
| **Qisqa nomi**  | `NovaTrade Holding`                         |
| **INN**         | `308123456`                                 |
| **Holati**      | Активный                                    |

---

## 3. JISMONIY SHAXSLAR (Natural Persons)

Tizimda jismoniy shaxslar uch maqsadda ishlatiladi:
1. **Xodim** — Штат va Foydalanuvchi uchun
2. **Mijoz** — Клиент sifatida ro'yxatga olinadi
3. **Direktor** — Yuridik shaxsga biriktiriladi

### 3.1 Xodimlar (Hodimlar)

| # | F.I.Sh.                          | Kod                      | Rol            | Telefon        | Email                        |
|---|----------------------------------|--------------------------|----------------|----------------|------------------------------|
| 1 | Toshmatov Sardor Hamidovich      | `emp_sardor_novatrade`   | Savdo menejeri | `998901112233` | `sardor@novatrade.uz`        |
| 2 | Nazarova Dilnoza Baxtiyor qizi   | `emp_dilnoza_novatrade`  | Ombor boshqaruvchisi | `998902223344` | `dilnoza@novatrade.uz` |
| 3 | Rajabov Ulugbek Sobirovich       | `emp_ulugbek_novatrade`  | Kassir         | `998903334455` | `ulugbek@novatrade.uz`       |
| 4 | Xolmatova Feruza Aliyevna        | `emp_feruza_novatrade`   | Hisobchi       | `998904445566` | `feruza@novatrade.uz`        |
| 5 | Mirzayev Bobur Komilovich        | `emp_bobur_novatrade`    | Direktor       | `998905556677` | `bobur@novatrade.uz`         |

#### Umumiy xodim paroli (test uchun):
```
Parol: Test@12345
```

### 3.2 Mijozlar (Клиенты — Natural Person)

| # | F.I.Sh.                        | Kod                        | Telefon        | Holat    |
|---|--------------------------------|----------------------------|----------------|----------|
| 1 | Abdullayev Sherzod Rustamovich | `client_sherzod_nova`      | `998911234567` | Клиент ✓ |
| 2 | Qodirov Otabek Mansurovich     | `client_otabek_nova`       | `998912345678` | Клиент ✓ |
| 3 | Yusupova Zulfiya Hamidovna     | `client_zulfiya_nova`      | `998913456789` | Клиент ✓ |
| 4 | Rahimov Jamshid Bahromovich    | `client_jamshid_nova`      | `998914567890` | Клиент ✓ |

> **Eslatma:** Mijozlar `test_natural_person.py::run_natural_person_for_client_1` ga o'xshash
> yaratiladi — forma to'ldirganda **"Клиент" checkbox** belgilanadi.

---

## 4. FILIAL / TASHKILOT (Организация)

| Maydon              | Qiymat                      |
|---------------------|-----------------------------|
| **Nomi**            | `NovaTrade - Toshkent Filiali` |
| **Valyuta**         | Узбекский сум               |
| **Yuridik shaxs**   | `novatrade_legal` (NovaTrade Distribution Co LLC) |
| **Vaqt zonasi**     | `(+05:00) Ташкент` / `Asia/Tashkent` |
| **Buyurtma raqami** | *(avtomatik — code raqamidan)* |
| **QQS foizi**       | `12`                        |
| **QQS yoqilgan?**   | Да                          |
| **Aktsiz yoqilgan?**| Да                          |
| **Holati**          | Активный                    |

---

## 5. ISH ZONASI (Рабочая зона / Room)

| Maydon   | Qiymat                          |
|----------|---------------------------------|
| **Kod**  | `room_tashkent_nova`            |
| **Nomi** | `NovaTrade - Toshkent Savdo Zonasi` |
| **Holati** | Активный                      |

### Ish zonasiga biriktirilgan resurslar:
| Resurs turi        | Biriktirilganlar                              |
|--------------------|-----------------------------------------------|
| **To'lov turlari** | Наличные деньги, Перечисление, Терминал, Чековая книжка |
| **Omborlar**       | `NovaTrade - Asosiy Ombor`                    |
| **Kassalar**       | `NovaTrade - Asosiy Kassa`                    |
| **Mijozlar**       | `client_sherzod_nova` (va boshqalar)          |
| **Narx turlari**   | `Price Type UZB - NovaTrade`, Акция           |

---

## 6. TMC TO'PLAMI / SEKTOR (Набор ТМЦ / Sector)

| Maydon          | Qiymat                          |
|-----------------|---------------------------------|
| **Kod**         | `sector_nova_main`              |
| **Nomi**        | `NovaTrade - Asosiy Tovarlar`   |
| **Ish zonasi**  | `NovaTrade - Toshkent Savdo Zonasi` |

---

## 7. TOVARLAR / TMC (Товарно-материальные ценности)

| # | Nomi                             | Kod                        | O'lchov | Turi   | Narxi (UZS) | Sektori              |
|---|----------------------------------|----------------------------|---------|--------|-------------|----------------------|
| 1 | NovaCola 0.5L                    | `sku_novacola_05`          | шт      | Товар  | 5 000       | NovaTrade - Asosiy   |
| 2 | NovaCola 1.5L                    | `sku_novacola_15`          | шт      | Товар  | 8 500       | NovaTrade - Asosiy   |
| 3 | NovaJuice Olcha 1L               | `sku_novajuice_olcha`      | шт      | Товар  | 12 000      | NovaTrade - Asosiy   |
| 4 | NovaSnack Chips 100g             | `sku_novasnack_chips`      | шт      | Товар  | 7 000       | NovaTrade - Asosiy   |
| 5 | NovaWater Still 1L               | `sku_novawater_still`      | шт      | Товар  | 3 500       | NovaTrade - Asosiy   |
| 6 | NovaWater Sparkling 1L           | `sku_novawater_spark`      | шт      | Товар  | 4 000       | NovaTrade - Asosiy   |
| 7 | NovaMilk 1L                      | `sku_novamilk_1l`          | шт      | Товар  | 9 000       | NovaTrade - Asosiy   |
| 8 | NovaTea Classic 100 paket        | `sku_novatea_classic`      | шт      | Товар  | 18 000      | NovaTrade - Asosiy   |

---

## 8. NARX TURLARI (Типы цен)

| # | Nomi                          | Kod                        | Ish zonasi                  | Tur           |
|---|-------------------------------|----------------------------|-----------------------------|---------------|
| 1 | Price Type UZB - NovaTrade    | `price_uzb_nova`           | NovaTrade - Toshkent Zonasi | Цена продажи  |
| 2 | Акция                         | *(katalogdan tanlanadi)*   | NovaTrade - Toshkent Zonasi | Акция chegirma|

---

## 9. TO'LOV TURLARI (Типы оплат)

Tizimda 4 ta standart to'lov turi mavjud bo'lib, hammasi biriktiriladi:

| # | Nomi               | Izoh                          |
|---|--------------------|-------------------------------|
| 1 | Наличные деньги    | Naqd pul                      |
| 2 | Перечисление       | Bank o'tkazmasi               |
| 3 | Терминал           | POS-terminal (karta)          |
| 4 | Чековая книжка     | Chek daftarchasi              |

---

## 10. SHTAT (Штат / Robot)

Shtat — bu tizimda xodimning lavozimi va ish zonasini biriktiruvchi yozuv.

| # | Shtat kodi                  | Shtat nomi                 | Rol    | Ish zonasi               |
|---|-----------------------------|----------------------------|--------|--------------------------|
| 1 | `robot_menejer_nova`        | NovaTrade - Savdo Menejeri | Админ  | NovaTrade - Toshkent Zonasi |
| 2 | `robot_ombor_nova`          | NovaTrade - Omborchi       | Админ  | NovaTrade - Toshkent Zonasi |
| 3 | `robot_kassir_nova`         | NovaTrade - Kassir         | Админ  | NovaTrade - Toshkent Zonasi |

---

## 11. FOYDALANUVCHILAR (Пользователи)

| # | Login (email)                         | Parol       | Biriktirilgan shaxs       | Shtat                    |
|---|---------------------------------------|-------------|---------------------------|--------------------------|
| 1 | `user_sardor@novatrade`               | `Test@12345`| Toshmatov Sardor          | NovaTrade - Savdo Menejeri |
| 2 | `user_dilnoza@novatrade`              | `Test@12345`| Nazarova Dilnoza          | NovaTrade - Omborchi     |
| 3 | `user_ulugbek@novatrade`              | `Test@12345`| Rajabov Ulugbek           | NovaTrade - Kassir       |

> **Eslatma:** Foydalanuvchi yaratilgandan so'ng unga barcha formalar,
> hisobotlar va nakladnoylar biriktiriladi (`test_user.py::run_user_attach_form` kabi).

---

## 12. ROL VA RUXSATLAR (Роли)

| Rol nomi | Ruxsatlar                                   |
|----------|---------------------------------------------|
| **Админ** | Barcha switch'lar yoqilgan (test_user.py::run_role) |

> Har bir yangi foydalanuvchi uchun **Barcha formalarga ruxsat berish** (`Доступ ко всем формам`) amalga oshiriladi.

---

## 13. BUYURTMA YARATISH (Заказ)

Buyurtma yaratish uchun minimal kerakli ma'lumotlar:

| Maydon              | Qiymat                                       |
|---------------------|----------------------------------------------|
| **Filial**          | NovaTrade - Toshkent Filiali                 |
| **Ish zonasi**      | NovaTrade - Toshkent Savdo Zonasi            |
| **Mijoz**           | Abdullayev Sherzod (yoki boshqa client)      |
| **Tovar**           | NovaCola 0.5L × 10 dona                     |
| **Narx turi**       | Price Type UZB - NovaTrade                  |
| **To'lov turi**     | Наличные деньги                              |

### Oddiy buyurtma stsenariysi:
1. `user_sardor@novatrade` sifatida kiriladi
2. Savdo → Buyurtmalar → Создать
3. Mijoz tanlanadi: `client_sherzod_nova`
4. Tovar qo'shiladi: NovaCola 0.5L, 10 dona, narxi 5 000 UZS
5. To'lov: Наличные деньги
6. Saqlash va tasdiqlash

---

## 14. TEST ISHGA TUSHIRISH BUYRUG'I

### Mavjud company bilan (sizning asosiy holatiz):
```bash
pytest tests/ \
  --url https://app.smartup.uz/xtrade \
  --company-code novatrade \
  --company-password YourPassword123
```

### Yangi company yaratib (to'liq setup):
```bash
pytest tests/smoke/test_setup/ \
  --url https://app.smartup.uz/xtrade \
  --create-company \
  --head-email head_admin@smartup.uz \
  --head-password HeadPassword123
```

### Faqat bitta test fayli:
```bash
pytest tests/smoke/test_setup/test_product.py \
  --url https://app.smartup.uz/xtrade \
  --company-code novatrade \
  --company-password YourPassword123 \
  --reuse-code \
  --include-leaf-tests
```

### Headless rejimda (CI/CD uchun):
```bash
pytest tests/ \
  --url https://app.smartup.uz/xtrade \
  --company-code novatrade \
  --company-password YourPassword123 \
  --headless
```

---

## 15. TESTLAR KETMA-KETLIGI (Setup tartibi)

Sherigingizning `test_setup_runner.py` faylidagi tartib:

```
1.  test_company.py          → Kompaniya yaratish (faqat --create-company bilan)
2.  test_legal_person.py     → Yuridik shaxs yaratish
3.  test_filial.py           → Filial (tashkilot) yaratish
4.  test_natural_person.py   → Xodim uchun jismoniy shaxs
                               Mijoz uchun jismoniy shaxs
5.  test_payment_type.py     → To'lov turlarini ulash
6.  test_price_type.py       → Narx turi yaratish
7.  test_room.py             → Ish zonasi yaratish
                               Ish zonasiga resurslar ulash
8.  test_sector.py           → TMC to'plami (sektor) yaratish
9.  test_product.py          → Tovar yaratish va narx belgilash
10. test_robot.py            → Shtat yaratish
11. test_user.py             → Foydalanuvchi yaratish
                               Foydalanuvchiga formalar ulash
                               Admin roli sozlash
                               Parol o'zgartirish
```

> **Muhim:** Har bir qadam oldingi qadam natijalari (nomlar, kodlar)ga bog'liq.
> Tartibni buzmaslik kerak.

---

## 16. BIZNES QOIDALAR

### Kompaniyaga xos qoidalar:
- Barcha narxlar O'zbek so'mida (UZS)
- QQS stavkasi: **12%**
- Aktsiz: **yoqilgan**
- Vaqt zonasi: **Asia/Tashkent (+05:00)**
- Mintaqa: **город Ташкент**

### Buyurtma qoidalari:
- Tovar omborda bo'lishi shart (boshlanish balansi kerak)
- Buyurtma yaratish uchun foydalanuvchida `Savdo` ruxsati bo'lishi kerak
- Aksiya narxi faqat ish zonasiga "Акция" narx turi biriktirilganda ishlaydi

### Foydalanuvchi qoidalari:
- Login format: `username@company_code` (masalan: `admin@novatrade`)
- Yangi foydalanuvchi birinchi kirishda parol o'zgartirishi shart
- Foydalanuvchiga shtat, jismoniy shaxs va formalar biriktirilishi kerak

---

## 17. MUHIM ESLATMALAR

- `code` — bu tasodifiy 6 raqamli son (masalan `482931`). Sherigingizning testlari
  barcha nomlarni `name-pw{code}` formatida yaratadi. Siz real nomlar ishlatasiz.
- Sessiya timeout bo'lganda tizim `#closing-session` overlay chiqaradi —
  `flow_authorization.py::install_session_keepalive` bu holatni avtomatik hal qiladi.
- Testlar `test-results/data/data_store.json` faylga ma'lumot saqlaydi — keyingi
  testlar shu fayldan o'qiydi (`load_data` fixture orqali).
- Allure hisobotlar `test-results/allure-results/` papkasida saqlanadi.
