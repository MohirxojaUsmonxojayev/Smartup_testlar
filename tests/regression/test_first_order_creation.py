import re

import allure
from playwright.sync_api import Page, expect

from tests.regression.test_auth import run_user_login
from utils.soft_assert import SoftAssert

pytestmark = [
    allure.epic("Regression"),
    allure.feature("E2E Flow"),
    allure.story("Закупка → Поступления ТМЦ → Заказ → Архив"),
]

TEST_NAME      = "test_first_order_creation"
SUPPLIER_NAME  = "NovaWater"
PRODUCT_NAME   = "NovaCola 0.5L"
QUANTITY       = "5"
PRICE          = "4000"
WAREHOUSE_NAME = "Основной склад"
STAFF_NAME     = "NovaTrade - TP"
CLIENT_NAME    = "Abdullayev Sherzod Rustamovich"
PAYMENT_TYPE   = "Наличные деньги"

# Xato xabarlari uchun prefiks qoliplari
_ZAKUPKA   = "[Закупки]"
_POSTUPL   = "[Поступления ТМЦ]"
_OSTATKI   = "[Остатки ТМЦ]"
_ORDER     = "[Заказы]"
_NEXT_STEP = f"→ keyingi qadamga o'tib bo'lmadi → {TEST_NAME} MUVAFFAQIYATSIZ"


# ----------------------------------------------------------------------------------------------------------------------

@allure.title("Birinchi buyurtma: Закупка → Поступления ТМЦ (складga tushirish)")
def test_first_order_creation(page: Page, soft: SoftAssert) -> None:
    """
    To'liq E2E flow — login bir marta, qadamlar ketma-ket:
      1. Login + filial tanlash
      ── ЗАКУПКИ QADAMI ──────────────────────────────────────
      2. Склад → Закупки navigatsiya
      3. Yaratish dropdown → Создать
      4. Yetkazib beruvchi: NovaWater
      5. Tovar: NovaCola 0.5L, miqdor=5, narx=4000
      6. Провести + да
      ── ПОСТУПЛЕНИЯ ТМЦ QADAMI ──────────────────────────────
      7. Склад → Поступления ТМЦ на склад
      8. Создать → Основной склад → закупka ulash → tovar qo'shish
      9. Статус: Завершено → Завершить + да

    Qoidalar:
      - Har bir ACTION qadam hard_check: xato → screenshot + test to'xtaydi
      - Har bir TEKSHIRUV (expect) qadam check: xato → screenshot + davom etadi
      - Закупки qadamidagi hard_check xabarida Поступления ТМЦ o'tkazilgani aytiladi
    """

    # ══════════════════════════════════════════════════════════════════════
    # LOGIN
    # ══════════════════════════════════════════════════════════════════════

    with allure.step("1 - Tizimga kirish va filial tanlash"):
        try:
            run_user_login(page)
        except Exception as e:
            soft.hard_check(False,
                f"❌ Login muvaffaqiyatsiz {_NEXT_STEP} | {type(e).__name__}: {e}")

    # ══════════════════════════════════════════════════════════════════════
    # ЗАКУПКИ QADAMI
    # ══════════════════════════════════════════════════════════════════════

    with allure.step("2 - [Закупки] Склад → Закупки ga o'tish"):
        try:
            page.get_by_role("link", name="Склад").click()
            page.locator("#kt_header_menu").get_by_role(
                "link", name="Закупки", exact=True
            ).click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_ZAKUPKA} navigatsiya muvaffaqiyatsiz {_NEXT_STEP} | {type(e).__name__}: {e}")
        try:
            expect(page.locator("#anor288-button-add")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False, f"❌ {_ZAKUPKA} 'Создать' tugmasi ko'rinmaydi | {type(e).__name__}")

    with allure.step("3 - [Закупки] 'Создать' dropdown ochish"):
        try:
            page.locator("div").filter(
                has_text="Создать Создать закупку через faktura.uz Отчет 0"
            ).nth(5).click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_ZAKUPKA} dropdown trigger topilmadi {_NEXT_STEP} | {type(e).__name__}: {e}")

    with allure.step("4 - [Закупки] Dropdown dan 'Создать' ni tanlash"):
        try:
            page.get_by_role("button", name="Создать", exact=True).click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_ZAKUPKA} wizard ochilmadi {_NEXT_STEP} | {type(e).__name__}: {e}")

    with allure.step(f"5 - [Закупки] Yetkazib beruvchi '{SUPPLIER_NAME}' ni tanlash"):
        try:
            page.get_by_text(
                "Поставщик Юридическое лицоФизическое лицоПоставщикСотрудник * Показать все"
            ).click()
            page.locator('form[name="step0"]').get_by_text(SUPPLIER_NAME).click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_ZAKUPKA} step0: '{SUPPLIER_NAME}' topilmadi {_NEXT_STEP} | {type(e).__name__}: {e}")

    with allure.step("6 - [Закупки] 'Далее' — tovar qo'shish qadamiga"):
        try:
            page.get_by_role("button", name="Далее").click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_ZAKUPKA} step0→step1 'Далее' topilmadi {_NEXT_STEP} | {type(e).__name__}: {e}")

    with allure.step(f"7 - [Закупки] '{PRODUCT_NAME}' qidirish va tanlash"):
        try:
            page.locator("#anor289-input-binput-fastsearchquery-G-0").get_by_role(
                "textbox", name="Поиск"
            ).click()
            page.get_by_text(PRODUCT_NAME).click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_ZAKUPKA} step1: '{PRODUCT_NAME}' topilmadi {_NEXT_STEP} | {type(e).__name__}: {e}")

    with allure.step(f"8 - [Закупки] Miqdor = {QUANTITY}"):
        try:
            qty = page.locator("#anor289-input-text-quantity-G-0")
            qty.click()
            qty.fill(QUANTITY)
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_ZAKUPKA} step1: Miqdor maydoni topilmadi {_NEXT_STEP} | {type(e).__name__}: {e}")

    with allure.step(f"9 - [Закупки] Narx = {PRICE}"):
        try:
            price = page.locator("#anor289-input-text-price-G-0")
            price.click()
            price.fill(PRICE)
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_ZAKUPKA} step1: Narx maydoni topilmadi {_NEXT_STEP} | {type(e).__name__}: {e}")

    with allure.step("10 - [Закупки] 'Далее' — tasdiqlash qadamiga"):
        try:
            page.get_by_role("button", name="Далее").click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_ZAKUPKA} step1→step2 'Далее' topilmadi {_NEXT_STEP} | {type(e).__name__}: {e}")

    with allure.step("11 - [Закупки] 'Провести' bosish"):
        try:
            page.get_by_role("button", name="Провести").click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_ZAKUPKA} 'Провести' topilmadi {_NEXT_STEP} | {type(e).__name__}: {e}")

    with allure.step("12 - [Закупки] Tasdiqlash 'да'"):
        try:
            page.get_by_role("button", name="да").click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_ZAKUPKA} 'да' dialogi topilmadi {_NEXT_STEP} | {type(e).__name__}: {e}")

    with allure.step("13 - [Закупки] Ro'yxatga qaytilganini tekshirish"):
        try:
            expect(page.locator("#anor288-button-add")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False, f"❌ {_ZAKUPKA} Ro'yxatga qaytilmadi | {type(e).__name__}")

    # ══════════════════════════════════════════════════════════════════════
    # ПОСТУПЛЕНИЯ ТМЦ QADAMI
    # ══════════════════════════════════════════════════════════════════════

    with allure.step("14 - [Поступления ТМЦ] Склад → Поступления ТМЦ на склад"):
        try:
            page.get_by_role("link", name="Склад", exact=True).click()
            page.locator("#kt_header_menu").get_by_role(
                "link", name="Поступления ТМЦ на склад"
            ).click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_POSTUPL} navigatsiya muvaffaqiyatsiz | {type(e).__name__}: {e}")
        try:
            expect(page.locator("#anor113-button-add")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False, f"❌ {_POSTUPL} 'Создать' tugmasi ko'rinmaydi | {type(e).__name__}")

    with allure.step("15 - [Поступления ТМЦ] 'Создать' bosish"):
        try:
            page.locator("#anor113-button-add").click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_POSTUPL} 'Создать' bosilmadi | {type(e).__name__}: {e}")

    with allure.step(f"16 - [Поступления ТМЦ] Ombor '{WAREHOUSE_NAME}' tanlash"):
        try:
            page.get_by_role("textbox", name="Поиск").click()
            page.get_by_text(WAREHOUSE_NAME).click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_POSTUPL} step0: '{WAREHOUSE_NAME}' topilmadi | {type(e).__name__}: {e}")

    with allure.step("17 - [Поступления ТМЦ] 'Далее' — закупка ulash qadamiga"):
        try:
            page.get_by_role("button", name="Далее").click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_POSTUPL} step0→step1 'Далее' topilmadi | {type(e).__name__}: {e}")

    with allure.step("18 - [Поступления ТМЦ] Закупka qidirib birinchi aktiv natijani tanlash"):
        try:
            page.get_by_role("textbox", name="Поиск закупки").click()
            page.locator("div:nth-child(2) > .hint-item.ng-scope.active").click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_POSTUPL} step1: Закупka qidiruv yoki aktiv natija topilmadi | {type(e).__name__}: {e}")

    with allure.step("19 - [Поступления ТМЦ] Tanlangan закупka tovarlarini qo'shish"):
        try:
            page.get_by_role("button").nth(4).click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_POSTUPL} step1: Tovar qo'shish tugmasi (nth=4) topilmadi | {type(e).__name__}: {e}")

    with allure.step("20 - [Поступления ТМЦ] 'Далее' — yakunlash qadamiga"):
        try:
            page.get_by_role("button", name="Далее").click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_POSTUPL} step1→step2 'Далее' topilmadi | {type(e).__name__}: {e}")

    with allure.step("21 - [Поступления ТМЦ] Status 'Завершено' ni tanlash"):
        try:
            page.get_by_label("Select box activate").click()
            page.get_by_text("Завершено").click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_POSTUPL} step2: 'Завершено' status topilmadi | {type(e).__name__}: {e}")

    with allure.step("22 - [Поступления ТМЦ] 'Завершить' bosish"):
        try:
            page.get_by_role("button", name="Завершить").click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_POSTUPL} 'Завершить' topilmadi | {type(e).__name__}: {e}")

    with allure.step("23 - [Поступления ТМЦ] Tasdiqlash 'да'"):
        try:
            page.get_by_role("button", name="да").click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_POSTUPL} 'да' dialogi topilmadi | {type(e).__name__}: {e}")

    with allure.step("24 - [Поступления ТМЦ] Ro'yxatga qaytilganini tekshirish"):
        try:
            expect(page.locator("#anor113-button-add")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False, f"❌ {_POSTUPL} Ro'yxatga qaytilmadi | {type(e).__name__}")

    # ══════════════════════════════════════════════════════════════════════
    # ОСТАТКИ ТМЦ TEKSHIRUVI — hammasi soft
    # ══════════════════════════════════════════════════════════════════════

    with allure.step("25 - [Остатки ТМЦ] Склад → Остатки ТМЦ ga o'tish"):
        try:
            page.get_by_role("link", name="Склад").click()
            page.get_by_role("link", name="Остатки ТМЦ").click()
        except Exception as e:
            soft.check(False,
                f"❌ {_OSTATKI} navigatsiya muvaffaqiyatsiz | {type(e).__name__}")

    with allure.step("26 - [Остатки ТМЦ] 'В наличии' ustuni ko'rinishini tekshirish"):
        try:
            expect(page.locator("b-page")).to_contain_text("В наличии")
        except Exception as e:
            soft.check(False,
                f"❌ {_OSTATKI} 'В наличии' ustuni topilmadi | {type(e).__name__}")

    with allure.step(f"27 - [Остатки ТМЦ] '{PRODUCT_NAME}' miqdori {QUANTITY} ko'rinishini tekshirish"):
        try:
            expect(page.locator("b-page")).to_contain_text(QUANTITY)
        except Exception as e:
            soft.check(False,
                f"❌ {_OSTATKI} '{PRODUCT_NAME}' miqdori ({QUANTITY}) topilmadi | {type(e).__name__}")

    # ══════════════════════════════════════════════════════════════════════
    # ЗАКАЗЫ QADAMI — yaratish va arxivgacha olib borish
    # ══════════════════════════════════════════════════════════════════════

    with allure.step("28 - [Заказы] Продажа → Заказы ga o'tish"):
        try:
            page.get_by_role("link", name="Продажа").click()
            page.get_by_role("link", name="Заказы", exact=True).click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_ORDER} navigatsiya muvaffaqiyatsiz {_NEXT_STEP} | {type(e).__name__}: {e}")

    order_time: str | None = None

    with allure.step("29 - [Заказы] 'Создать' bosish va Дата заказа vaqtini o'qish"):
        try:
            page.get_by_role("button", name="Создать", exact=True).click()
            raw = page.get_by_placeholder("Выбрать дату").first.input_value()
            m = re.search(r"\d{2}:\d{2}", raw)
            order_time = m.group() if m else None
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_ORDER} 'Создать' wizard ochilmadi {_NEXT_STEP} | {type(e).__name__}: {e}")

    with allure.step(f"30 - [Заказы] step0: Штат '{STAFF_NAME}' tanlash"):
        try:
            page.get_by_text(
                "Штат* Штат Торговый представитель NovaTrade - Kassir Nazarova Dilnoza Baxtiyor"
            ).click()
            page.get_by_text(STAFF_NAME).click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_ORDER} step0: '{STAFF_NAME}' topilmadi {_NEXT_STEP} | {type(e).__name__}: {e}")

    with allure.step(f"31 - [Заказы] step0: Клиент '{CLIENT_NAME}' tanlash"):
        try:
            page.get_by_text("Клиент* ИНН Клиент Abdullayev").click()
            page.get_by_text(CLIENT_NAME).click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_ORDER} step0: '{CLIENT_NAME}' topilmadi {_NEXT_STEP} | {type(e).__name__}: {e}")

    with allure.step("32 - [Заказы] 'Далее' — tovar qo'shish qadamiga"):
        try:
            page.get_by_role("button", name=" Далее").click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_ORDER} step0→step1 'Далее' topilmadi {_NEXT_STEP} | {type(e).__name__}: {e}")

    with allure.step(f"33 - [Заказы] step1: '{PRODUCT_NAME}' qidirish va tanlash"):
        try:
            page.locator("#anor279_input-b_input-product_name_goods0").get_by_role(
                "textbox", name="Поиск"
            ).click()
            page.get_by_text(f"{PRODUCT_NAME} {WAREHOUSE_NAME}").click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_ORDER} step1: '{PRODUCT_NAME}' topilmadi {_NEXT_STEP} | {type(e).__name__}: {e}")

    with allure.step(f"34 - [Заказы] step1: Miqdor = {QUANTITY}"):
        try:
            qty = page.locator("#anor279_input-b_pg_col-quantity_0")
            qty.click()
            qty.fill(QUANTITY)
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_ORDER} step1: Miqdor maydoni topilmadi {_NEXT_STEP} | {type(e).__name__}: {e}")

    with allure.step("35 - [Заказы] 'Далее' — to'lov qadamiga"):
        try:
            page.get_by_role("button", name=" Далее").click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_ORDER} step1→step2 'Далее' topilmadi {_NEXT_STEP} | {type(e).__name__}: {e}")

    with allure.step(f"36 - [Заказы] step2: To'lov turi '{PAYMENT_TYPE}' tanlash"):
        try:
            page.locator("#anor279-inpu-b_input-payment_type").get_by_role(
                "textbox", name="Поиск"
            ).click()
            page.get_by_text(PAYMENT_TYPE).click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_ORDER} step2: '{PAYMENT_TYPE}' topilmadi {_NEXT_STEP} | {type(e).__name__}: {e}")

    with allure.step("37 - [Заказы] 'Сохранить' va 'да' bilan tasdiqlash"):
        try:
            page.get_by_role("button", name=" Сохранить").click()
            page.get_by_role("button", name="да").click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_ORDER} 'Сохранить' yoki 'да' topilmadi {_NEXT_STEP} | {type(e).__name__}: {e}")

    with allure.step("38 - [Заказы] Yaratilgan buyurtmani vaqt bo'yicha topib ochish"):
        try:
            page.get_by_text(order_time).first.click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_ORDER} order_time='{order_time}' bo'yicha buyurtma topilmadi {_NEXT_STEP} | {type(e).__name__}: {e}")

    with allure.step("39 - [Заказы] Status: 'В обработке' ga o'tkazish"):
        try:
            page.get_by_role("button", name=" В обработке").click()
            page.get_by_role("button", name="да", exact=True).click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_ORDER} 'В обработке' statusi topilmadi {_NEXT_STEP} | {type(e).__name__}: {e}")

    with allure.step("40 - [Заказы] Vaqt yozuviga bosib 'Изменить статус' ni chiqarish (В ожидании)"):
        try:
            page.get_by_text(order_time).first.click()
            page.get_by_role("button", name="Изменить статус").click()
            page.get_by_role("link", name=" В ожидании").click()
            page.get_by_role("button", name="да", exact=True).click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_ORDER} 'В ожидании' statusi topilmadi {_NEXT_STEP} | {type(e).__name__}: {e}")

    with allure.step("41 - [Заказы] Status: 'Отгружен' ga o'tkazish"):
        try:
            page.get_by_role("button", name=" Отгружен").click()
            page.get_by_role("button", name="да", exact=True).click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_ORDER} 'Отгружен' statusi topilmadi {_NEXT_STEP} | {type(e).__name__}: {e}")

    with allure.step("42 - [Заказы] Vaqt yozuviga bosib 'Изменить статус' ni chiqarish (Доставлен)"):
        try:
            page.get_by_text(order_time).first.click()
            page.get_by_role("button", name="Изменить статус").click()
            page.get_by_role("link", name=" Доставлен").click()
            page.get_by_role("button", name="да", exact=True).click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_ORDER} 'Доставлен' statusi topilmadi {_NEXT_STEP} | {type(e).__name__}: {e}")

    with allure.step("43 - [Заказы] 'Архив' ga o'tkazish"):
        try:
            page.get_by_role("link", name="Доставлен").click()
            page.get_by_role("button", name=" Архив").click()
            page.get_by_role("button", name="да", exact=True).click()
        except Exception as e:
            soft.hard_check(False,
                f"❌ {_ORDER} 'Архив' statusi topilmadi {_NEXT_STEP} | {type(e).__name__}: {e}")
