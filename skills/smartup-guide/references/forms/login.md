## Login Form

### Default Login Snapshot
Tags: login, auth, screenshot, locator
- URL pattern: `<company_url>/login.html`; odatiy server uchun `https://smartup.online/login.html`.
- Screenshot: `skills/smartup-guide/references/forms/screenshots/login/login__default__desktop-1440x900__20260610-151534.png`.
- UI holati: markazda Smartup login kartasi, yuqorida til selector (`Язык: РУС`), maydonlar `Логин@компания` va `Пароль`, asosiy tugma `ВОЙТИ`, linklar `Забыли пароль?` va `Войти через номер телефона`.
- Test locatorlari: `page.get_by_placeholder("Логин@компания")`, `page.get_by_role("textbox", name="Пароль")`, `page.get_by_role("button", name="Войти")`.
- Debug note: snapshot credential kiritmasdan, faqat default login sahifasi yuklangandan keyin olindi.
