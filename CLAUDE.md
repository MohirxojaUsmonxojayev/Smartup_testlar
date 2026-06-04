# Claude uchun Ko'rsatmalar — Playwright Loyihasi

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
- `.env`: `COMPANY_URL`, `COMPANY_CODE`, `COMPANY_PASSWORD`, `USER_PASSWORD`
