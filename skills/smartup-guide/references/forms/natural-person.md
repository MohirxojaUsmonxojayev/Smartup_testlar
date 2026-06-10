# Natural Person Add Form

## URL Va Navigation

### Natural person add
Tags: natural-person, setup, form, navigation
- Navigation: `Справочники` -> `Физические лица` -> `Создать`.
- URL pattern: `/anor/mr/person/natural_person+add`.
- Test fayli: `tests/smoke/test_setup/test_natural_person.py`.
- Runner: `tests/smoke/test_setup/test_setup_runner.py`, step `06 - Natural Person` va `18 - Natural Person For Client 1`.

## Test Arxitekturasi

### Alohida natural person flow
Tags: natural-person, legal-person, regression, helper
- Natural Person alohida entity test hisoblanadi; uning qiymat yaratish, add forma to'ldirish, save, list assert helperlari `tests/smoke/test_setup/test_natural_person.py` ichida turadi.
- Legal Person regressionda `Руководитель` uchun natural person kerak bo'lsa, `natural_person_values` va `create_natural_person_record` import qilinadi; natural person locator/fill/assert logikasi Legal Person ichida dublikat qilinmaydi.
- Kelajakda natural person list/view bo'yicha qo'shimcha testlar shu fayldagi helperlarga tayanadi.

## Field Bilimlari

### Natural person add fields
Tags: natural-person, input, regression
- Smoke branch: majburiy `d.first_name` (`Имя *`) va `d.code` to'ldiriladi; xodim uchun ko'rinadigan nom `natural_person-pw{code}`, client uchun `natural_client-pw{code}` bo'lib qolishi kerak, chunki keyingi user/contract/order flowlar shu matnni exact qidiradi.
- Regression branch: smoke maydonlariga qo'shimcha `d.birthday`, `d.passport_series`, `d.passport_digits`, `Регион`, `d.address`, `d.post_address`, `d.main_phone`, `d.tin`, `d.telegram`, `d.email`, `d.web` to'ldiriladi.
- `Регион` legal persondagi kabi b-tree search (`_$bTree.searchValue`); avval input click/focus qilinadi, keyin `Ташкент` qidirilib hint ichidagi exact text/label yoki `.jstree-anchor` orqali `город Ташкент`/`Ташкент` optioni tanlanadi.
- Client case'da `Клиент` belgisi yoqiladi va save qilingandan keyin `Клиенты` listida ham ko'rinishi tekshiriladi.

## List Va View Tekshiruv

### Natural person list
Tags: natural-person, list, grid, assert
- Default list gridda `Название`, `Пол`, `Дата рождения`, `Группа`, `Категория`, `Статус` ko'rinadi; `Код` default ko'rinmaydi.
- Test global searchda code bo'yicha filter qilishi mumkin, lekin row assert ko'rinadigan nom (`natural_person-pw{code}`, `natural_client-pw{code}` yoki director F.I.O.) va `Активный` statusni tekshiradi.
- View tugmasi: row tanlangandan keyin `Просмотр`.

### Natural person view
Tags: natural-person, view, assert
- View URL pattern: `/anor/mr/person/natural_person_view`.
- View heading bilan tab heading birga chiqishi mumkin; heading assertda `get_by_role("heading").filter(has_text="Физическое лицо (просмотр)")` ishlatiladi.
- Smoke view assert hozir yaratilgan person name va `Активный` statusini tekshiradi; regression view assert qo'shimcha `code`, `birthday`, `email`, `address`, `post_address` qiymatlarini ham tekshiradi.
- `natural_client-pw{code}` case uchun person viewdan keyin `Клиенты` listida ham client nomi borligi tekshiriladi.

## Debug Notes

### 2026-06-02 list/view verification
Tags: natural-person, client, list, view, run-result
- `test_01_authorization` + `test_03_filial` + `test_06_natural_person` + `test_18_natural_person_for_client_1 --reuse-code --headless -s` passed: 4 passed in 27.74s.
- Run code: `5535`; natural person va natural client list/view assertlari o'tdi.
