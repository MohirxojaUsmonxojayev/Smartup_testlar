# UI Patterns

## Qidiruv Kalitlari

Tags: locator, b-input, grid, modal, biruni, screenshot, list

### Locator Tanlash
Tags: locator, angular
- Qoida: Angular `ng-model` locatorlardan iloji boricha qoch.
- Qoida: Yangi testlarda raw CSS/XPath/`ng-model` locator yozma; avval `page.get_by_role(...)`, `page.get_by_text(...)` yoki label/textga tayangan helper ishlat.
- Afzal locatorlar:
  - `BasePage.fill_textbox_by_label(...)`
  - `BasePage.select_b_input_by_label(...)`
  - `BasePage.expect_b_input_value_by_label(...)`
  - label/text asosidagi local yoki umumiy helper
  - `page.get_by_role(...)`
- Sabab: UI Angular migratsiya/yangilanishlarida semantik locatorlar barqarorroq.

### Form Field Discovery
Tags: form, discovery, checkbox, switch, radio
- Yangi add/edit forma o'rganilganda faqat `input[type=text]`, `textarea`, `select` va `b-input`larni yig'ish yetarli emas.
- Smartup switchlar ko'pincha styled checkbox sifatida chiqadi; `input[type="checkbox"]`, `input[type="radio"]`, ularning label/group texti, `ng-model`, `checked`, `disabled`, `visible` holati alohida yig'ilsin.
- Switch yoqilgandan keyin yangi required maydon paydo bo'lishi mumkin; masalan filial add’da `НДС` (`d.vat_enabled`) yoqilganda `Ставка НДС (%)` (`d.vat_percent`) majburiy input bo'ladi.
- Formani "full" qilishdan oldin field discovery kamida ikki holatni tekshirsin: default state va switch/checkbox yoqilgandan keyingi state.

### b-input
Tags: b-input, locator
- Qoida: `b-input` tanlash uchun umumiy helper ishlatiladi.
- Helperlar:
  - `BasePage.select_b_input_by_label(label, option_text, clear=False, exact=True)`
  - `BasePage.expect_b_input_value_by_label(label, expected_value)`
- Eslatma: ba'zi input value'lar sahifa textiga kirmaydi; input value assert qilish kerak.

### Masked Date/Amount Inputs
Tags: input, mask, date, amount
- Qoida: date/amount mask inputlarda qiymatni almashtirishdan oldin focus + `ControlOrMeta+A` + `Backspace` qiling; faqat `fill(new_value)` ba'zan eski invalid qiymatga append qiladi.
- Testda ishlatish: label/text helperlar inputni label orqali topsin, keyin clear-and-fill patternini bajarsin va `Tab` bilan mask formatini yakunlasin.

### Biruni Confirm
Tags: biruni, confirm, modal
- Preferred: confirm oynasini `page.get_by_role("dialog")` orqali topib, `да` buttonni shu dialog ichida bosing.
- Pattern:
  - `confirm = page.get_by_role("dialog").filter(has=page.get_by_role("button", name="да"))`
  - `expect(confirm).to_be_visible()`
  - `confirm.get_by_role("button", name="да").click()`
  - `confirm.wait_for(state="hidden")`
- Qoida: `да` button har doim confirm modal ichida scope qilinadi.

### Biruni Error
Tags: biruni, error, modal
- Selector: `#biruniAlertExtended`.
- Close button: `#biruniAlertExtended button.close`.
- Qoida: ba'zan `Закрыть` textli button yo'q.
- Qoida: Modal yopilmasa menu/list clicklari intercept bo'lishi mumkin.
- Kelajak flow: error kutish, text tekshirish va modal yopish umumiy helper/flow bo'lishi kerak.

### List va Grid Setting
Tags: list, grid, search, column
- Qoida: Smartup list formalarida kerakli ustun yoki search field ko'rinmasa, grid setting orqali ustun va shu ustun bo'yicha searchni yoqish mumkin.
- Bu pattern barcha listlarda umumiy.
- Testda ishlatish: qo'shilgan elementni listda topish uchun kerakli ustun/search yo'q bo'lsa, avval grid settingdan yoq.

### Screenshot Arxivi
Tags: screenshot, debug, url
- Screenshotlar kelajakdagi visual regression/baseline taqqoslashga tayyor formatda saqlansin.
- Saqlash joylari:
  - `.agents/skills/smartup-guide/references/forms/screenshots/<form-slug>/` — forma bo'yicha doimiy screenshot va metadata arxivi.
  - `test-results/allure-results/` — faqat pytest/Allure failure attachment outputi; forma bilim arxivi sifatida ishlatilmaydi.
  - `test-results/screens/smartup/` — ishlatilmasin, chunki run output tozalanishi mumkin va skill bilim manbasi emas.
- Naming: `<form-slug>__<state>__<viewport>__<stable-id>.png`.
  - Misol: `contract-view__default__desktop-1440x783__contract_code_4986.png`
  - URL asosida saqlash kerak bo'lsa: `<form-slug>__url-<sanitized-url-hash>__<viewport>.png`
- Metadata: har screenshot bilan bir xil arxiv papkasida `.json` saqlansin:
  - URL
  - form slug
  - state
  - viewport
  - code/session id
  - entity id/code/name
  - created_at
  - browser
  - dynamic areas yoki mask kerak bo'lishi mumkin bo'lgan joylar
- Qoida: yangi formaga kirilganda yoki URL/form state sezilarli o'zgarganda skill arxividagi screenshotni yangilab bor.
- Debug tartibi: muammo chiqqanda avval mavjud screenshotlardan qaraladi; kerakli screen yo'q bo'lsa UI ochilib yangi screenshot olinadi.
- Release visual check qo'shilganda current screenshot baseline bilan solishtiriladi; shuning uchun screenshotlar random modal/loader/dropdown ochiq holda emas, barqaror UI state’da olinishi kerak.
