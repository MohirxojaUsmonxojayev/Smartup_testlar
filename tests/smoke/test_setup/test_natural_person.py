import allure
from playwright.sync_api import expect

from tests.smoke.flows.flow_authorization import authorization
from tests.smoke.flows.flow_form import assert_visible_page_text
from tests.smoke.flows.flow_navigate import navigate_to, switch_filial, expect_page
from utils.base_page import BasePage

pytestmark = [allure.epic("Smoke"), allure.feature("Setup"), allure.story("Natural Person")]

# ----------------------------------------------------------------------------------------------------------------------

def create_natural_person(page, full_name, person_code, *, client=False):
    """Физические лица ro'yxatidan yangi jismoniy shaxs yaratib saqlaydi.

    Qayta ishlatiladi (masalan legal person regressioni director uchun chaqirishi mumkin).
    `page` to'g'ri filialda login qilingan deb keladi. `client=True` bo'lsa "Клиент" yoqiladi.
    """
    navigate_to(page, tab="Справочники", name="Физические лица")
    expect_page(page, heading="Физические лица")
    page.get_by_role("button", name="Создать").click()

    expect_page(page, heading="Физическое лицо (создание)")
    BasePage(page).input(ng_model="d.first_name", value=full_name)
    BasePage(page).input(label="Код", value=person_code)
    if client:
        BasePage(page).checkbox(label="Клиент", checked=True)
        BasePage(page).checkbox(label="Клиент", expect_checked=True)
    BasePage(page).checkbox(label="Статус", expect_checked=True)
    BasePage(page).save_and_expect_heading("Физические лица", confirm_text="")

# ----------------------------------------------------------------------------------------------------------------------

def assert_natural_person_view(page, full_name):
    """Ro'yxatdan shaxsni ochib (Просмотр), view oynasida nom/status tekshirib, yopadi."""
    BasePage(page).click_grid_row(full_name)
    page.get_by_role("button", name="Просмотр", exact=True).click()
    expect_page(page, heading="Физическое лицо (просмотр)")
    assert_visible_page_text(page, full_name, "Активный")
    page.get_by_role("button", name="Закрыть").first.click()
    expect_page(page, heading="Физические лица")

# ----------------------------------------------------------------------------------------------------------------------

def run_natural_person(page, code):
    """Testcase: xodim uchun jismoniy shaxs (natural person) yaratish.

    1. Физические лица ro'yxatidan yangi shaxs yaratish
       (Имя = natural_person-pw{code}, Код = natural_person_pw{code}) va saqlash.
    2. Ro'yxatda yaratilgan shaxs nomi va "Активный" statusini tekshirish.
    3. View oynasida nom va statusni tekshirib, oynani yopish.

    Setup zanjirida sahifa allaqachon filial-pw{code} da (run_room shu filialga
    o'tgan), shuning uchun bu yerda switch_filial qilinmaydi — standalone debug uchun
    filialga o'tish test_natural_person wrapper'ida bajariladi.
    """
    full_name = f"natural_person-pw{code}"
    person_code = f"natural_person_pw{code}"

    with allure.step("1 - Yangi jismoniy shaxs yaratish"):
        create_natural_person(page, full_name, person_code)

    with allure.step("2 - Ro'yxatda yaratilgan shaxsni tekshirish"):
        BasePage(page).grid_controller(search=person_code)
        BasePage(page).grid_row(full_name, "Активный")

    with allure.step("3 - View oynasida tekshirish"):
        assert_natural_person_view(page, full_name)

# ----------------------------------------------------------------------------------------------------------------------

def run_natural_person_for_client_1(page, code):
    """Testcase: mijoz uchun jismoniy shaxs (natural client) yaratish.

    1. Физические лица ro'yxatidan "Клиент" belgili yangi shaxs yaratish
       (Имя = natural_client-pw{code}, Код = natural_client_pw{code}) va saqlash.
    2. Ro'yxat va view oynasida nom/status tekshirish.
    3. Клиенты ro'yxatida ham ko'rinishini tekshirish.
    """
    full_name = f"natural_client-pw{code}"
    person_code = f"natural_client_pw{code}"

    with allure.step("1 - 'Клиент' belgili yangi jismoniy shaxs yaratish"):
        create_natural_person(page, full_name, person_code, client=True)

    with allure.step("2 - Ro'yxat va view oynasida tekshirish"):
        BasePage(page).grid_controller(search=person_code)
        BasePage(page).grid_row(full_name, "Активный")
        assert_natural_person_view(page, full_name)

    with allure.step("3 - Mijozlar ro'yxatida ko'rinishini tekshirish"):
        navigate_to(page, tab="Справочники", name="Клиенты")
        expect_page(page, heading="Клиенты")
        BasePage(page).grid_controller(search=full_name)
        BasePage(page).grid_row(full_name)

# ----------------------------------------------------------------------------------------------------------------------

@allure.title("Xodim uchun jismoniy shaxs yaratish")
def test_natural_person(page, code):
    authorization(page, who='admin')
    switch_filial(page, name=f"filial-pw{code}")
    run_natural_person(page, code)


@allure.title("Mijoz uchun jismoniy shaxs yaratish")
def test_natural_person_for_client_1(page, code):
    authorization(page, who='admin')
    switch_filial(page, name=f"filial-pw{code}")
    run_natural_person_for_client_1(page, code)
