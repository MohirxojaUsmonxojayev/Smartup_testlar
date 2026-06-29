## Token tejash qoidalari [MAJBURIY]

### Har qanday vazifadan OLDIN:
1. Vazifani o'qib, **kerakli fayllarni** aniqla — barchasini emas
2. Agar 3+ faylga tegadigan bo'lsa → `/plan` rejimida reja ko'rsat, tasdiqlashimni kut
3. Faylni to'liq o'qima — faqat kerakli qatorlarni o'qi (`Read(file.py, 10, 80)`)

### Sessiya davomida:
- Kontekst 40%+ to'lganda `/compact` taklif qil
- Bir vazifa tugagach, keyingisi boshlanishidan oldin so'ra:
  "Yangi mavzu — `/clear` bilan yangi sessiya ochaymi?"
- Bir faylni ikki marta o'qima — keshdan foydalanish

### Model tanlash (o'zing qaror qil):
- Kichik tuzatish / savol → Haiku
- Oddiy kod / refaktoring → Sonnet
- Arxitektura / murakkab tahlil → Opus
Foydalanuvchiga qaysi model ishlatilayotganini ayt.

### Nima QILMA:
- Butun papkani skanerlama — faqat so'ralgan fayllar
- Log, migration, __pycache__, .lock fayllarini o'qima
- Bir xato uchun 3+ marta urinma — 2 ta urinishdan keyin to'xta va tushuntir
- Keraksiz tushuntirma yozma — faqat so'ralgan natija

### Sifatni saqlash:
- Vazifaning MOHIYATINI hech qachon yo'qotma
- Agar token tejash vazifaga zarar bersa → tejamkorlikni qo'y, vazifani bajar
- Har doim tugallangan, ishlaydigan kod ber
# Claude uchun Ko'rsatmalar — Playwright Loyihasi

## Bilim Bazasi — `skills/` (Yagona Ishonchli Manba)

Barcha skilllar va Smartup domain bilimlari uchun **yagona source of truth** — repo root'idagi `skills/`. `.claude/skills/` (Claude Code) va `.agents/skills/` (Codex) — shu papkaga `../../skills/<name>` symlink qiluvchi entry-point'lar; ikkalasi ham aslida bir xil `skills/` faylini o'qiydi va yozadi, shuning uchun data bo'linmaydi. Doim `skills/` ni manba deb bil:

- **O'qish:** Smartup sahifa, forma, contract, order, locator, modal, grid yoki UI xatti-harakati ustida ishlashdan oldin avval `skills/smartup-guide/SKILL.md` ni (index) o'qi, so'ng kerakli `references/...` yoki forma uchun `references/forms/<slug>.md` dossierini o'qi.
- **Yozish:** Yangi biznes qoida, UI xatti-harakati, locator yoki xato sababi topilsa — uni `skills/smartup-guide/` ichidagi mos reference yoki form dossier fayliga yoz (boshqa joyga emas). Forma screenshotlari `skills/smartup-guide/references/forms/screenshots/<slug>/` ichida arxivlanadi.
- `smartup-guide` Skill tool ro'yxatida bo'lmasligi mumkin — shunda ham yuqoridagi fayllarni to'g'ridan-to'g'ri Read bilan o'qi.
- **Yangi skill qo'shish:** papkani `skills/<name>/` ichida yarat, so'ng ikkala entry-point'da symlink qo'sh — `.claude/skills/<name> -> ../../skills/<name>` va `.agents/skills/<name> -> ../../skills/<name>`.

## Avtomatik O'rganish

Foydalanuvchi quyidagi narsalarni aytganda `/learn` skillini **o'zing, so'ralmay** ishlat:

- UI yoki ilovaning qanday ishlashini tushuntirsa
- Xato sababini o'zi topib aytsa
- Avvalgi yechim noto'g'ri ekanligi ma'lum bo'lsa
- Loyihaga xos qoida yoki pattern ko'rsatsa

Maqsad: har suhbatda bir xil xatoni takrorlamaslik.

## Loyiha Haqida

- Framework: Playwright + pytest (Python)
- Test turi: Smoke testlar — `tests/smoke/`
- User setup runner: `tests/smoke/test_setup/test_setup_runner.py` — setup testlarini ketma-ket ishlatadi
- All runner: `tests/smoke/test_all_runner.py` — barcha runner fayllarini ketma-ket jamlab ishlatadi
- Full script: `run_tests.sh` — `test_all_runner.py` ni Allure bilan ishlatadi
- `code` fixture: session uchun unikal 6 xonali son, runner da yangi, yakka testda `data_store.json` dan o'qiladi
- `.env` ishlatilmaydi; runnerda `--url` majburiy
- Mavjud company: `--url <server_url> --company-code <code> --company-password <password>`
- Yangi company: `--url <server_url> --create-company`; yangi company admin paroli kod ichidagi default qiymat
- User password test ichida hardcode, lekin qoida fayllarida literal qiymat yozilmaydi
