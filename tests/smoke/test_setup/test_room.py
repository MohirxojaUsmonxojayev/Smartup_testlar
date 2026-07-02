import allure
from playwright.sync_api import expect
from tests.smoke.flows.flow_authorization import authorization, USER_PASS, user_email_for
from tests.smoke.flows.flow_navigate import navigate_to, switch_filial, expect_page
from utils.base_page import BasePage

pytestmark = [allure.epic("Smoke"), allure.feature("Setup"), allure.story("Room")]

# ----------------------------------------------------------------------------------------------------------------------

def _select_grid_checkall(page, grid_name):
    expect(page.locator(f'b-grid[name="{grid_name}"]')).to_be_visible()
    BasePage(page).checkbox(check_all=True, grid_name=grid_name, checked=True)

# ----------------------------------------------------------------------------------------------------------------------

def run_room(page, code):
    """Testcase: yangi ish zonasi (room) yaratish.

    1. filial-pw{code} ga o'tib, Справочники -> Рабочие зоны ro'yxatini ochish.
    2. "Создать" -> code (code_room_pw{code}) va nom (room-pw{code}) ni kiritish.
    3. Saqlab, ro'yxatda room nomi va kodi ko'rinishini tekshirish.
    """
    room_name = f"room-pw{code}"
    room_code = f"code_room_pw{code}"

    with allure.step("1 - Ish zonalari ro'yxatiga o'tish"):
        switch_filial(page, name=f"filial-pw{code}")
        navigate_to(page, tab="Справочники", name="Рабочие зоны")
        expect_page(page, heading="Рабочие зоны")

    with allure.step("2 - Yangi ish zonasi formasini to'ldirish"):
        page.get_by_role("button", name="Создать").click()
        expect_page(page, heading="Рабочая зона (создание)")
        BasePage(page).input(label="Код", value=room_code)
        BasePage(page).input(label="Название", value=room_name)
        BasePage(page).checkbox(label="Статус", expect_checked=True)

    with allure.step("3 - Saqlash va ro'yxatda tekshirish"):
        page.get_by_role("button", name="Сохранить", exact=True).first.click()
        expect_page(page, heading="Рабочие зоны")
        BasePage(page).grid_row(room_name, room_code)

# ----------------------------------------------------------------------------------------------------------------------

def run_room_attachment(page, code):
    """Testcase: oldingi setup testlari yaratgan narsalarni ish zonasiga (room) ulash.

    1. User sifatida kirib, room-pw{code} ning "Прикрепление" sahifasini ochish.
    2. To'lov turlarini (Типы оплат) ulash.
    3. Omborni (Склады) ulash.
    4. Kassani (Кассы) ulash.
    5. Mijozni (Физические лица: natural_client-pw{code}) ulash.
    6. "Акция" narx turini (Тип цены) ulash — bu C-group aksiya chegirmasi order'da
       ishlashi uchun zarur (room'ga ulanmasa, order'da aksiya chiqmaydi).
    7. Sahifani yopib, "Рабочие зоны" ro'yxatiga qaytishni tekshirish.
    """
    room_name = f"room-pw{code}"
    client_name = f"natural_client-pw{code}"

    with allure.step("1 - Foydalanuvchi sifatida kirish va ish zonasini ochish"):
        authorization(page, email=user_email_for(code), password=USER_PASS)
        navigate_to(page, tab="Справочники", name="Рабочие зоны")
        expect_page(page, heading="Рабочие зоны")
        BasePage(page).click_grid_row(room_name)
        page.get_by_role("button", name="Прикрепление").click()
        expect(page.locator("#kt_content")).to_contain_text(f"Рабочая зона (прикрепление): {room_name}")

    with allure.step("2 - To'lov turlarini ulash"):
        page.get_by_role("link", name="Типы оплат").click()
        expect(page.locator("b-page")).to_contain_text("Типы оплат")
        page.get_by_role("button", name="Доступные").click()
        BasePage(page).wait_for_loader()
        _select_grid_checkall(page, "table_payment_type")
        page.get_by_role("button", name="Прикрепить").click()
        BasePage(page).confirm_biruni("Прикрепить 4?")
        expect(page.locator("b-page")).to_contain_text("нет данных")

    with allure.step("3 - Skladni ulash"):
        page.get_by_role("link", name="Склады").click()
        expect(page.locator("b-page")).to_contain_text("Склады")
        page.get_by_role("button", name="Доступные").click()
        BasePage(page).wait_for_loader()
        _select_grid_checkall(page, "table_warehouse")
        page.get_by_role("button", name="Прикрепить").click()
        BasePage(page).confirm_biruni("Прикрепить 1?")
        expect(page.locator("b-page")).to_contain_text("нет данных")

    with allure.step("4 - Kassani ulash"):
        page.get_by_role("link", name="Кассы").click()
        expect(page.locator("b-page")).to_contain_text("Кассы")
        page.get_by_role("button", name="Доступные").click()
        BasePage(page).wait_for_loader()
        _select_grid_checkall(page, "table_cashbox")
        page.get_by_role("button", name="Прикрепить").click()
        BasePage(page).confirm_biruni("Прикрепить 1?")
        expect(page.locator("b-page")).to_contain_text("нет данных")

    with allure.step("5 - Mijozni ulash"):
        page.get_by_role("link", name="Физические лица").click()
        expect(page.locator("b-page")).to_contain_text("Физические лица")
        page.get_by_role("button", name="Доступные").click()
        BasePage(page).wait_for_loader()
        BasePage(page).click_grid_row(client_name)
        page.get_by_role("button", name="Прикрепить").click()
        BasePage(page).confirm_biruni(f"Прикрепить {client_name}?")
        page.get_by_role("button", name="Прикрепленные").click()
        expect(page.locator("b-page")).to_contain_text(client_name)

    with allure.step("6 - 'Акция' narx turini ulash (Тип цены tab)"):
        # "Акция" narx turi C-group aksiya chegirmasi orderda ishlashi uchun room'ga ulanadi.
        # Ulanish 2 bosqichli: avval "Создать тип цены" orqali "Доступные" ro'yxatiga qo'shiladi,
        # so'ng "Доступные"da belgilab "Прикрепить" qilinadi (MCP bilan 2026-06-16 tasdiqlangan).
        page.get_by_role("link", name="Тип цены").click()
        expect(page.locator("b-page")).to_contain_text("Тип цены")

        # 1) Katalogdan "Акция"ni room "Доступные" ro'yxatiga qo'shish
        page.get_by_role("button", name="Доступные").click()
        BasePage(page).wait_for_loader()
        page.get_by_role("button", name="Создать тип цены").click()
        expect_page(page, heading="Цены (прикрепление)")
        BasePage(page).wait_for_loader()
        page.get_by_text("Акция", exact=True).first.click()
        page.get_by_role("button", name="Прикрепить", exact=True).click()
        BasePage(page).confirm_biruni("Прикрепить Акция?")
        BasePage(page).wait_for_loader()

        # 2) "Доступные"da "Акция"ni belgilab "Прикрепить" -> "Прикрепленные"ga o'tadi
        page.get_by_role("link", name="Тип цены").click()
        page.get_by_role("button", name="Доступные").click()
        BasePage(page).wait_for_loader()
        page.get_by_text("Акция", exact=True).first.click()
        page.get_by_role("button", name="Прикрепить", exact=True).click()
        BasePage(page).confirm_biruni("Прикрепить Акция?")
        BasePage(page).wait_for_loader()

        page.get_by_role("button", name="Прикрепленные").click()
        BasePage(page).wait_for_loader()
        expect(page.locator("b-page")).to_contain_text("Акция")

    with allure.step("7 - Sahifani yopish"):
        page.get_by_role("button", name="Закрыть").click()
        expect_page(page, heading="Рабочие зоны")

# ----------------------------------------------------------------------------------------------------------------------

@allure.title("Ish zonasi yaratish")
def test_room(page, code):
    authorization(page, who='admin')
    run_room(page, code)


@allure.title("Ish zonasiga to'lov, sklad, kassa va mijoz ulash")
def test_room_attachment(page, code):
    run_room_attachment(page, code)
