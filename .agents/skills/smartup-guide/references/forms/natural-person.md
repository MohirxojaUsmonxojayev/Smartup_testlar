# Natural Person Add Form

## URL Va Navigation

### Natural person add
Tags: natural-person, setup, form, navigation
- Navigation: `Справочники` -> `Физические лица` -> `Создать`.
- URL pattern: `/anor/mr/person/natural_person+add`.
- Test fayli: `tests/smoke/test_setup/test_natural_person.py`.
- Runner: `tests/smoke/test_setup/test_setup_runner.py`, step `06 - Natural Person` va `18 - Natural Person For Client 1`.

## List Va View Tekshiruv

### Natural person list
Tags: natural-person, list, grid, assert
- Default list gridda `Название`, `Пол`, `Дата рождения`, `Группа`, `Категория`, `Статус` ko'rinadi; `Код` default ko'rinmaydi.
- Shu sabab test list rowni person name (`natural_person-pw{code}` yoki `natural_client-pw{code}`) orqali topadi va row ichida `Активный` statusni tekshiradi.
- View tugmasi: row tanlangandan keyin `Просмотр`.

### Natural person view
Tags: natural-person, view, assert
- View URL pattern: `/anor/mr/person/natural_person_view`.
- View heading bilan tab heading birga chiqishi mumkin; heading assertda `get_by_role("heading").filter(has_text="Физическое лицо (просмотр)")` ishlatiladi.
- Smoke view assert hozir yaratilgan person name va `Активный` statusini tekshiradi.
- `natural_client-pw{code}` case uchun person viewdan keyin `Клиенты` listida ham client nomi borligi tekshiriladi.

## Debug Notes

### 2026-06-02 list/view verification
Tags: natural-person, client, list, view, run-result
- `test_01_authorization` + `test_03_filial` + `test_06_natural_person` + `test_18_natural_person_for_client_1 --reuse-code --headless -s` passed: 4 passed in 27.74s.
- Run code: `5535`; natural person va natural client list/view assertlari o'tdi.
