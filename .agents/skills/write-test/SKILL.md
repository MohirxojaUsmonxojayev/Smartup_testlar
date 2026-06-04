---
name: write-test
description: Yangi Playwright + pytest smoke test yozish. Foydalanuvchi yangi test, test funksiya yoki test fayl yaratmoqchi bo'lganda ishlatiladi.
---

# Yangi Test Yozish

Quyidagi qoidalarga qat'iy rioya qil:

## 1. Loyiha strukturasini tushun

- Testlar: `tests/smoke/test_setup/` yoki `tests/smoke/test_life_cycle/`
- Flowlar: `tests/smoke/flows/`
- User setup runner: `tests/smoke/test_setup/test_setup_runner.py`
- Group runnerlar: `tests/smoke/test_groups/test_<X>_grup/test_<x>_group_runner.py`
- All runner: `tests/smoke/test_all_runner.py`
- Fixtures: `tests/smoke/conftest.py`

## 2. Test fayl shabloni

```python
import allure
from playwright.sync_api import Page

pytestmark = [allure.epic("Smoke"), allure.feature("<Feature nomi>"), allure.story("<Story nomi>")]

@allure.title("<Test nomi>")
def test_<nomi>(session_page: Page, code: str, save_data, load_data, logger):
    with allure.step("1 - <Qadam nomi>"):
        # amal
        pass
    with allure.step("2 - <Qadam nomi>"):
        # assert
        pass
```

## 3. Qoidalar

- **Fixtures**: `session_page`, `code`, `save_data`, `load_data`, `logger` — conftest.py dan keladi, import qilma
- **Allure**: har bir test `@allure.title()` va `with allure.step()` bilan bo'lishi SHART
- **Locator**: `page.locator()` ishlatilsin, `page.find_element()` EMAS
- **Assert**: `expect(locator).to_be_visible()` ishlatilsin, Python `assert` EMAS
- **Timeout**: DEFAULT_TIMEOUT (10s) yetarli; kerak bo'lsa `page.wait_for_timeout()` emas, `expect(...).to_be_visible()` kutish
- **Session data**: `save_data("key", value)` va `load_data("key")` orqali ma'lumot almashing
- **`code`**: har bir test uchun unikal identifikator, nom sifatida ishlating

## 4. Runner ga qo'shish

Yangi user setup testi yozilgandan keyin `tests/smoke/test_setup/test_setup_runner.py` ga import va `@allure.title` bilan qo'sh:

```python
from tests.smoke.test_setup.test_<nomi> import test_<nomi> as run_<nomi>

@allure.title("XX - <Nomi>")
def test_XX_<nomi>(session_page: Page, code):
    run_<nomi>(session_page, code)
```

## 5. Loyiha Xususiyatlari

### .env va dinamik qiymatlar
- `.env` da Python f-string **ishlamaydi**: `TEST_USER_EMAIL=f"user-pw{code}@autotest"` — xato
- Dinamik email va shunga o'xshash qiymatlar test/flow ichida f-string bilan quriladi:
  ```python
  user_email = f"user-pw{code}{COMPANY_CODE}"
  ```

### code fixture
- `pytest.mark.user_setup` runner orqali ishlaganda: yangi `random.randint(1000, 9999)` yaratadi
- Yakka test ishlaganda: `test-results/data/data_store.json` dan `"code"` kalitini o'qiydi
- Agar `data_store.json` bo'lmasa: `pytest.exit()` bilan aniq xato beradi

### authorization_user
- `authorization_user(page, code)` — `code` parametrni qabul qiladi
- Email ichida quriladi: `f"user-pw{code}{COMPANY_CODE}"`

### Selenium migratsiya source fayli
- Foydalanuvchi Selenium test kodini rootdagi `for_migratsiya.py` fayliga qo'yadi; migratsiya so'ralganda shu fayldan o'qib Playwright + pytest smoke testga o'tkaz, UI da run qilib xatolarini tuzat.
- Migratsiya qilingan Playwright kodni ham `for_migratsiya.py` faylining davomiga yoz; runnerga yoki test flowga avtomatik qo'shma, foydalanuvchi tekshirib o'zi ko'chiradi.
- Migratsiyada foydalanuvchi `run_tests.sh` oldin run qilinganini aytsa, user setup tayyor deb hisobla; user bilan login qil va `code` qiymatini `test-results/data/data_store.json` dan ol.
- Agar foydalanuvchi Playwright codegen pytest kodini bersa, Seleniumdan taxminiy migratsiya qilma; codegen kodini asos qilib olib loyiha fixture, Allure step, `code`, `authorization_user`, helper flow va locator patternlariga moslab ber.
- Codegen kodini moslashda har bir ochilgan sahifa, forma yoki view uchun `expect(...)` bilan ochilganini tasdiqla; mavjud login/navbar flowlari bo'lsa, codegen qatorlari o'rniga o'shalarni ishlat.
- Umumiy test ma'lumotlarini ajratish uchun random ishlatma, `code` fixture qiymatini ishlat; bu test boshida generatsiya bo'ladi va butun sessiya davomida saqlanadi.
- `code` fixture umumiy entity nomlari va testlarni ajratish uchun ishlatiladi; agar formaning o'z `code`/`number` maydoni keyingi testlarda kerak bo'lsa, alohida `contract_code_{random_son}` kabi qiymat generatsiya qil, listda aynan shu qiymat bilan hozir yaratilgan recordni top, test muvaffaqiyatli tugaganda `save_data` orqali `data_store.json` ga saqla.
- Contract add formasida generated `contract_code_{random_son}` qiymati `Код` inputiga yoziladi; `Номер` inputi bilan almashtirib yuborma.
- Dinamik test qiymatlarini test boshida alohida o'zgaruvchiga yig'ib olma; kerakli joyida `f"...{code}"` ko'rinishida yoz.
- Barcha testlarda qayta ishlatiladigan umumiy helperlar, masalan `b-input` tanlash, local test helper emas `utils/base_page.py` ichidagi `BasePage` methodi bo'lsin.
- `input[ng-model=...]` kabi Angularga bog'langan locatorlardan iloji boricha foydalanma; label/role/text asosidagi `BasePage.fill_textbox_by_label`, `BasePage.select_b_input_by_label`, `page.get_by_role(...)` kabi locatorlarni afzal ko'r.
- Smoke UI testlarda form inputlarini to'ldirish, switch/radio/checkbox/button bosish uchun `page.evaluate()` ishlatma; real user action bo'lgan `locator.click()`, `locator.fill()`, `locator.press()` va `expect(...)` ishlat. `page.evaluate()` faqat o'qish/diagnostika yoki haqiqiy user flowga ta'sir qilmaydigan yordamchi holatlarda ishlatiladi.
- Test nomi, Allure title va step nomlari professional, sodda va test maqsadini darhol tushuntiradigan bo'lsin.
- Har bir test boshida docstringda testcase qadamlarini yoz; docstringdagi qadamlar test ichidagi `with allure.step(...)` bo'limlari bilan mantiqan mos kelsin.
- Add form testlarida birinchi navbatda `Код` inputini qidir va recordni listda code bo'yicha top; agar `Код` inputi bo'lmasa keyin nom/name bo'yicha yur.
- Add formadagi barcha majburiy `*` inputlarni albatta to'ldir.
- Test add qilgan har bir element list formada ham, view formada ham ko'ringanini tekshirishi shart.
- Agar qo'shilgan elementni list formadan topish uchun kerakli ustun yoki search yo'q bo'lsa, grid settingdan kerakli ustunni va shu ustun bo'yicha searchni yoq; Smartup listlarida bu umumiy pattern.
- Add formaga kiritiladigan nom, kompaniya, shaxs, manzil kabi biznes qiymatlarni mantiqan `Faker` bilan generatsiya qil; testda qidirish/bog'lash oson bo'lishi uchun kerakli joyda `code` yoki saqlangan entity code qo'shimchasini saqla.
- Smartup test yozish jarayonida yangi formaga kirilganda yoki URL/form state o'zgarganda screenshotni `.agents/skills/smartup-guide/references/forms/screenshots/<form-slug>/` ichiga saqla; `test-results/screens/smartup/` forma arxivi uchun ishlatilmasin.

### Smoke va Regression farqi
- Smoke testlarda forma minimal yurishi uchun kerak bo'lgan majburiy maydonlar va minimal harakatlar bajariladi; maqsad forma ishlashini tez tekshirish.
- Regression testlarda formaning barcha imkoniyatlari qamrab olinadi: mavjud barcha muhim inputlar to'ldiriladi, qo'shimcha sozlamalar/holatlar ishlatiladi va kengroq tekshiruvlar yoziladi.
- Bu loyihada smoke/regression scope global arxitektura: `scripts/run_tests.py` default `smoke`, `--regression` yoki `--scope=regression` esa pytest `--scope` ga uzatiladi; `test_scope` fixture runner va biznes `run_*` funksiyalarga beriladi.
- Yangi test yozganda alohida smoke test va alohida regression test yaratma; bitta biznes `run_*` funksiyada `scope: str = "smoke"` parametr bo'lsin.
- Runner wrapperlar `test_scope` fixture qabul qilib `run_*(..., scope=test_scope)` chaqirsin; group/setup chain funksiyalari ham `scope` qabul qilib ichki `run_*` funksiyalarga uzatsin.
- Smoke branch minimal: real formani saqlash uchun kerakli majburiy maydonlar, keyingi testlarga kerak data-store keylari, save, listdagi asosiy `code/name/status` check.
- Regression branch full: forma ichidagi real mavjud barcha muhim inputlar, checkbox/switchlar, tablar va modal/quick-addlar browserda ko'rib aniqlanadi; Faker bilan real nom/manzil/shaxs qiymatlari to'ldiriladi; add qilingan data list va viewda tekshiriladi.
- Foydalanuvchi “shu testni regression qilamiz” desa, bu avtomatik ravishda add formani full to'ldirish, list check, view check, viewdagi mos card/tab/module holatlarini check qilish degani.
- Fieldlarni taxmin qilma. Har yangi regression forma uchun avval browserda add/view ochib screenshot/field state ol, screenshotlarni `smartup-guide/references/forms/screenshots/<form-slug>/` ichiga arxivla va forma bilimini `smartup-guide/references/forms/<form-slug>.md` ga yoz.
- Regression-only qiymatlar `data_store.json` da eski runlardan qolib ketmasin: smoke branch ularni `None`/null qilib tozalasin, regression branch esa view/list assert uchun kerak hamma muhim qiymatlarni saqlasin.
- Scope bilan yozilgan testni yakunda ikki mode bilan tekshir: smoke minimal path, regression full path. Cross-platform runnerda `python scripts/run_tests.py --url <server_url>` va `python scripts/run_tests.py --url <server_url> --regression` ishlatiladi.

### Setup va Group test dependency modeli
- Yangi testlar har doim yangi server/baza holatida ham ishlashi kerak; lokal debugda oldingi rerunlardan data ko'paygan bo'lsa ham, testni mavjud dataga suyanib yozma.
- Fresh bazada feature settinglar default o'chirilgan bo'lishi mumkin; testga kerak bo'lgan settingni mavjud holatga suyanmay, idempotent tarzda yoqib/sozlab keyin asosiy flowga o't.
- User setup testlari bir-biriga bog'liq: oldingi setup test keyingi setup test uchun kerakli ma'lumot yoki entity yaratadi; setup ichida test yiqilsa keyingi setup test yura olmasligi mumkin.
- User setup testlari muvaffaqiyatli o'tgandan keyin group testlar boshlanadi: masalan `A group`, `B group` va boshqa guruhlar.
- Har bir group test user setup natijalariga bog'liq, lekin boshqa group testlarga bog'liq emas.
- Bir group ichida test yiqilsa, shu groupning qolgan testlari skip qilinadi; keyingi group testlari esa run bo'lishda davom etadi.
- Group testlar boshqa group yaratgan data yoki statega suyanmasin; A failed bo'lsa ham B, C, D... group testlari user_setup natijalaridan mustaqil run bo'lishi kerak.
- Har bir group ichki dependency uchun o'z data_store key prefixidan foydalansin (`a_group_*`, `b_group_*`, `c_group_*`), boshqa group prefixlarini o'qimasin.
- Group runnerlar `tests/smoke/test_groups/test_<X>_grup/test_<x>_group_runner.py` ko'rinishida bo'lsin; group ichidagi tartib wrapper test nomlari orqali `X-01`, `X-02` tarzida aniq berilsin.
- Har yangi group runner qo'shilganda `tests/smoke/test_all_runner.py` ichidagi import/listga ham qo'shilsin; full run faqat shu all runner orqali yuradi.
- `tests/smoke/test_all_runner.py` individual testlarni qayta e'lon qilmaydi; u user setup runner va group runner fayllarini setup -> A -> B -> ... tartibida ketma-ket chaqiradigan umumiy runner bo'lsin.
- Mexanizm pytest hook/marker orqali bo'lsin: `pytest.mark.user_setup` setup chain uchun, `pytest.mark.smoke_group("A")` kabi markerlar group chain uchun ishlatiladi.
- Bitta group testi failed bo'lsa faqat shu groupning keyingi testlari skip qilinadi, boshqa group markerlari skip qilinmaydi; user_setup failed bo'lsa barcha group testlar skip qilinadi.
- Grouplar bir-birining browser/page holatini meros qilib olmasin: full runnerda har group `group_page` bilan alohida oyna oladi, alohida group runner faylida esa testlar `group_user_page` bilan bitta module-scoped oyna va bitta loginni bo'lishadi.
- Har bir group runner ichida `*_GROUP_TEST_SCENARIO` constant bo'lsin; unda shu groupdagi testcaselar jamlangan biznes ssenariy yozilsin va `run_*_group_chain` boshida `allure.dynamic.description(...)` orqali reportga berilsin.
- Group ichidagi `run_*` funksiyalarda `login=True` default bo'lsin; group chain yoki group runner wrapperlari boshida bir marta login qilib, ichki chaqiruvlarga `login=False` bersin.
- Group test ichida cleanup yoki oldingi recordlarni cancel qilish faqat optional bo'lsin: data topilmasa no-op bo'lib, test yangi record yaratib davom etishi kerak.
- Yangi test yozishda u setup bosqichigami yoki qaysi mustaqil groupga tegishli ekanini aniq ajrat.
- `tests/smoke/test_setup/test_setup_runner.py` ichidagi mavjud barcha testlar user setup testlari hisoblanadi; runner setup testlari bilan bir papkada turadi va ular yozib bo'lingan.
- Endi A-group testlari boshlanmoqda; A-groupning birinchi testi order uchun contract yaratish testi.
- A-group testlari `tests/smoke/test_groups/test_A_grup/` papkasiga yozib boriladi; masalan contract testi `tests/smoke/test_groups/test_A_grup/test_contract.py` ichida saqlanadi.
- A-group contract testida `a_group_contract_code` bilan birga `a_group_contract_name` ham `data_store.json` ga saqlanadi; order formasidagi `Договор` maydoni contract code emas, contract name bilan tanlanadi.
- Order testlari ko'p yozilishi kutiladi; yangi order case yozishda avval `tests/smoke/flows/flow_order/` ichidagi mavjud flowlardan foydalan, takrorlanadigan order harakatlari paydo bo'lsa ularni test ichida qoldirmay alohida order flowga ajrat.
- Test yozish, migratsiya yoki debug paytida xato testcase, noto'g'ri flow, ortiqcha murakkablik yoki dublikat kod ko'rinsa, foydalanuvchiga alohida xabar ber va tavsiya qilingan tuzatishni qisqa tushuntir.
- Contract add formasida contractni turli shartlar bilan yaratish mumkin; masalan `Типы оплат` sharti keyingi order testlarida alohida case sifatida tekshirilishi mumkin. Bunday holatlarda contract yaratish flowi parametrli bo'lsin va order test shu shart bilan yaratilgan contractni ishlatsin.
- Contract + `Типы оплат` case'ida `Тип оплаты` orderda auto-fill bo'lishini tekshir; user uni o'zgartirsa ham order ishlashi kerak, faqat contract sum limit tekshiriladi.
- Contract valyutasi order productlarini filterlaydi; boshqa valyutali contractga almashtirilsa, oldin tanlangan productlar o'chishi kutiladi.

## 6. Ish tartibi

1. Avval `$ARGUMENTS` bo'yicha kerakli fayllarni o'qi
2. Mavjud o'xshash testni o'rganib shablon chiqar
3. Yangi test yoz
4. Agar bu Selenium migratsiyasi bo'lsa, migrated kodni `for_migratsiya.py` davomiga yoz va runnerga avtomatik qo'shma
5. Oddiy yangi test bo'lsa, runner ga qo'sh
6. Foydalanuvchiga qaysi fayllarga nima qo'shilganini ko'rsat
