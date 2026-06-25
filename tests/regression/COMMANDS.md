# Regression testlarni ishga tushirish buyruqlari

playwright codegen --target python https://app3.greenwhite.uz/xtrade/login.html

## Qo'shimcha flaglar

| Flag | Izoh |
|---|---|
| `-v` | Har bir test nomi va natijasi alohida ko'rsatiladi |
| `-s` | `print()` va logger chiqishlarini terminalda ko'rsatadi |
| `--headless` | Brauzer ko'rinmaydi, fonda ishlaydi (tezroq) |
| `--reuse-code` | Oldingi sessiyada saqlangan `code` ni ishlatadi (yakka test debug qilganda) |
| `--new-code` | Yangi `code` yaratadi va `data_store.json` ga saqlaydi |
| `--scope regression` | Test scope ni belgilaydi (default: regression) |

---

## Asosiy parametrlar (har doim kerak)

```
--url https://app3.greenwhite.uz/xtrade
--company-code novatrade
--company-password greenwhite
```

---

## Testlar

### Auth — Login va filial tanlash

**Barcha auth testlari (admin + user):**
```bash
pytest tests/regression/test_auth.py -v --url https://app3.greenwhite.uz/xtrade --company-code novatrade --company-password greenwhite
```

**Faqat admin login:**
```bash
pytest tests/regression/test_auth.py::test_admin_login -v --url https://app3.greenwhite.uz/xtrade --company-code novatrade --company-password greenwhite
```

**Faqat user login:**
```bash
pytest tests/regression/test_auth.py::test_user_login -v --url https://app3.greenwhite.uz/xtrade --company-code novatrade --company-password greenwhite
```

---

### Barcha bo'limlar — formalar ochilishi (Главное + Продажа + Склад + Финансы + Кадры и зарплата + Производство + Справочники + Торговый маркетинг + Оборудование)

**Barcha formalarni tekshirish (219 ta forma, 220 qadam):**
```bash
pytest tests/regression/test_check_forms_opening.py -v --url https://app3.greenwhite.uz/xtrade --company-code novatrade --company-password greenwhite
```

---

## Barcha regression testlarni ishga tushirish

```bash
pytest tests/regression/ -v --url https://app3.greenwhite.uz/xtrade --company-code novatrade --company-password greenwhite
```
