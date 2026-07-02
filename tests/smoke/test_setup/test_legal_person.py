import allure
from faker import Faker

from tests.smoke.flows.flow_authorization import authorization
from tests.smoke.flows.flow_navigate import navigate_to, expect_page
from utils.base_page import BasePage

pytestmark = [allure.epic("Smoke"), allure.feature("Setup"), allure.story("Legal Person")]

# ----------------------------------------------------------------------------------------------------------------------

fake_ru = Faker("ru_RU")


def run_legal_person(page, code, save_data=None):
    """Testcase: yangi yuridik shaxs (legal person) yaratish.

    1. Справочники -> Юридические лица ro'yxatini ochish.
    2. "Создать" -> Код (cod_lg_pw{code}) va Полное название (faker nomi) ni kiritish,
       Статус = Активный bo'lishini tekshirish.
    3. Saqlab, Юридические лица ro'yxatiga qaytishni tasdiqlash.
    4. Ro'yxatda yaratilgan yuridik shaxs kodi, nomi va "Активный" statusini tekshirish.
    5. legal_person_code va legal_person_name ni data_store ga saqlash.
    """
    legal_code = f"cod_lg_pw{code}"
    legal_name = f"{fake_ru.company()} legal_person-pw{code}"

    with allure.step("1 - Yuridik shaxslar ro'yxatiga o'tish"):
        navigate_to(page, tab="Справочники", name="Юридические лица")
        expect_page(page, heading="Юридические лица")

    with allure.step("2 - Yangi yuridik shaxs formasini to'ldirish"):
        page.get_by_role("button", name="Создать").click()
        expect_page(page, heading="Юридическое лицо (создание)")
        BasePage(page).input(label="Код", value=legal_code)
        BasePage(page).input(label="Полное название", value=legal_name)
        BasePage(page).checkbox(label="Статус", expect_checked=True)

    with allure.step("3 - Saqlash va ro'yxatga qaytishni tasdiqlash"):
        page.get_by_role("button", name="Сохранить", exact=True).first.click()
        BasePage(page).confirm_biruni("Сохранить")
        expect_page(page, heading="Юридические лица")

    with allure.step("4 - Ro'yxatda yaratilgan yuridik shaxsni tekshirish"):
        BasePage(page).grid_controller(search=legal_code)
        BasePage(page).grid_row(legal_code, legal_name, "Активный")

    with allure.step("5 - Muhim ma'lumotlarni data storega saqlash"):
        save_data("legal_person_code", legal_code)
        save_data("legal_person_name", legal_name)


@allure.title("Yuridik shaxs yaratish")
def test_legal_person(page, code, save_data):
    authorization(page, who='admin')
    run_legal_person(page, code, save_data)
