# Пользователи (User) — yaratish, rol va ruxsatlar

User setup 5 ta alohida funksiya: `run_user`, `run_user_attach_form`, `run_role`, `run_role_attach_form`, `run_change_password`.

## Umumiy navigatsiya

```python
switch_filial(page, name=f"filial-pw{code}")
navigate_to(page, tab="Главное", name="Пользователи")
```

## run_user — foydalanuvchi yaratish

**Forma heading:** `Пользователь (создание)`

| Maydon | Locator | Qiymat |
|---|---|---|
| Login | `textbox.nth(2)` | `user-pw{code}` |
| Parol | `#new_password` | `USER_PASS` (hardcode, qoidalarda literal yozilmaydi) |
| Физическое лицо | `BasePage.b_input_by_label("Физическое лицо", value=...)` | `natural_person-pw{code}` |
| Штат | `BasePage.b_input_by_label("Штат", value=...)` | `robot-pw{code}` |

Штат tanlanganida **"Админ"** roli avtomatik ko'rinishi kerak (expect).

`save_and_expect_heading("Пользователи")` → ro'yxatda `natural_person-pw{code}` va `user_email_for(code)` ko'rinadi.

**Login email pattern:** `user-pw{code}@<company_code>` (masalan `user-pw7576@autotest7576`) — `user_email_for(code)` helper orqali.

## run_user_attach_form — formalar ulash

User view → **Формы** link:

| Tab | Harakat |
|---|---|
| Формы | Доступные → checkall → Прикрепить → confirm → нет данных |
| Отчеты | Доступные → checkall → Прикрепить → confirm → нет данных |
| Накладные | wait_for_loader → Доступные → checkall → Прикрепить → confirm → нет данных |
| Внешние системы | wait_for_loader → Доступные → checkall → Прикрепить → confirm → нет данных |

Page size 50→1000 qilinadi (agar 50/ button ko'rinsa). `_attach_available_permissions` helper.

## run_role — Admin rolini sozlash

```
Роли link → "Админ" qatori → Изменить → "Роль (изменение)"
→ barcha ".switch span"[has_text="нет"] switchlarni toggling
→ save_and_expect_heading("Роли", timeout=600_000)
```

**MUHIM — styled switch muammosi:** `.switch span` elementi oddiy `.click()` bilan ishlamasligi mumkin. `_click_role_switch` bir nechta pozitsiya sinab ko'radi (`x = right_edge, center, left`). Bottom-left widget zone (`x<360, y>760`) — o'tkazib yuboriladi (Smartup chat widget).

Save timeout = **600_000** (10 min) — ko'p switch bo'lishi mumkin.

## run_role_attach_form — roliga barcha formalar

```
"Админ" qatori → Просмотреть → Формы link
→ "Доступ ко всем формам" → "Разрешить" → confirm_biruni()
→ wait_for_loader(600_000) → Доступные → нет данных
```

## run_change_password — parolni tasdiqlash

Yangi company'da birinchi login parol o'zgartirish talab qiladi:

```python
login(page, email=user_email_for(code), password=USER_PASS)
expect(page.locator(".alert-icon")).to_be_visible()  # force password change
# current_password, new_password, rewritten_password = USER_PASS
# Подтвердить → confirm_biruni()
```

Parol o'zgartirilmaydi (USER_PASS → USER_PASS), lekin sistem "tasdiqlangan" deb qabul qiladi.

## Test

- `tests/smoke/test_setup/test_user.py` → `run_user`, `run_user_attach_form`, `run_role`, `run_role_attach_form`, `run_change_password`
