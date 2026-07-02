# Лицензии — sotib olish va ulash

Litsenziya 2 ta alohida funksiya: `run_buy_license` va `run_attach_license`.

## Skip sharti

`DISABLE_LICENSE_POLICY` env var = `1/true/yes/on` bo'lsa — **ikkala funksiya ham o'tkazib yuboriladi** (allure attach bilan). `--disable-license-policy` flag berilganda shu env set qilinadi.

## run_buy_license — sotib olish

**Admin (head) sifatida Администрирование filialida:**

```
logout (agar sessiya ochiq bo'lsa)
→ authorization(page)  — admin login
→ switch_filial("Администрирование")
→ navigate_to(tab="Главное", name="Лицензии")
→ expect heading "Лицензии"
```

**Balans tekshiruvi:** `p.text-success[ng-if="q.balance > 0"]` — 5s timeout; musbat bo'lmasa fail.

**Sotib olish form:**
- Покупка link (agar ko'rinmasa)
- Payer: `AUTOTEST GWS` (ng_model="purchase.payer.name")
- Kontrakt: `Договор № bn от 01.01.2025` (ng_model="purchase.contract_name")
- Sana: today (ng_model="purchase.begin_date")

**Litsenziya qatorlari:**
- `Smartup ERP: Базовый пользователь (Обязательный)` — **majburiy**, agar mavjud bo'lsa 5 dona (`editable_quantity=False`)
- `Smartup ERP: Базовый пользователь ... За пользователя` — har doim 1 dona

Har bir qatorda: miqdor → `Купить` → `Я ознакомился...` → `Да` → wait_for_loader.

## run_attach_license — foydalanuvchiga ulash

**Лицензии и документы** link (admin sahifasida):

```
→ "ERP users" qatorini bosish
→ "Прикрепить пользователей" button
→ "Прикрепленные пользователи" heading
→ agar biriktirilgan bor: checkall → "Открепить" → confirm → "нет данных"
→ "Доступные" button → wait_for_loader(120_000)
→ Поиск: natural_person-pw{code}
→ qatorni bosish → "Прикрепить" → confirm_biruni() → "Закрыть"
```

## Muhim

- `run_attach_license` `run_buy_license` bilan ketma-ket chaqiriladi (runner'da)
- wait_for_loader timeout = **120_000** (2 min) — litsenziya yuklanishi sekin bo'lishi mumkin
- Agar company'da Политика лицензирования o'chirilgan (`company.md`) — bu step skip qilinadi

## Test

- `tests/smoke/test_setup/test_license.py` → `run_buy_license`, `run_attach_license`
