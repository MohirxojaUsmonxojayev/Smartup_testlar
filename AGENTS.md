# Codex uchun Ko'rsatmalar — Playwright Loyihasi

## Bilim Bazasi — `skills/` (Yagona Ishonchli Manba)

Barcha skilllar va Smartup domain bilimlari uchun **yagona source of truth** — repo root'idagi `skills/`. `.agents/skills/` (Codex) va `.claude/skills/` (Claude Code) — shu papkaga `../../skills/<name>` symlink qiluvchi entry-point'lar; ikkalasi ham aslida bir xil `skills/` faylini o'qiydi va yozadi, shuning uchun data bo'linmaydi.

- **O'qish/Yozish:** Smartup bilimlari uchun `skills/smartup-guide/SKILL.md` (index) dan boshla; yangi bilim topilsa shu papkadagi mos `references/...` yoki `references/forms/<slug>.md` ga yoz. Forma screenshotlari `skills/smartup-guide/references/forms/screenshots/<slug>/` ichida.
- **Yangi skill qo'shish:** papkani `skills/<name>/` ichida yarat, so'ng ikkala entry-point'da symlink qo'sh — `.agents/skills/<name> -> ../../skills/<name>` va `.claude/skills/<name> -> ../../skills/<name>`.

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
- `code` fixture: session uchun unikal 4 xonali son, runner da yangi, yakka testda `data_store.json` dan o'qiladi
- `.env` ishlatilmaydi; runnerda `--url` majburiy
- Mavjud company: `--url <server_url> --company-code <code> --company-password <password>`
- Yangi company: `--url <server_url> --create-company`; yangi company admin paroli kod ichidagi default qiymat
- User password test ichida hardcode, lekin qoida fayllarida literal qiymat yozilmaydi

## Ruxsatlar

- Escalation/ruxsat kerak bo'lsa, xavfsiz va qayta ishlatiladigan holatda doim `prefix_rule` taklif qil.
- Uzun `python -c $'...'` debug buyruqlari o'rniga workspace ichidagi vaqtinchalik yoki mavjud scriptni `./.venv/bin/python path/to/script.py` ko'rinishida ishlat.
