import allure
from playwright.sync_api import expect

from tests.smoke.flows.flow_authorization import authorization
from tests.smoke.flows.flow_navigate import navigate_to, expect_page, switch_filial
from utils.base_page import BasePage

pytestmark = [allure.epic("Smoke"), allure.feature("Setup"), allure.story("Robot")]

# ----------------------------------------------------------------------------------------------------------------------

def run_robot(page, code):
    """Testcase: yangi xodim (robot) yaratish.

    1. Справочники -> Штат ro'yxatini ochish.
    2. "Создать" -> kod (code_robot-pw{code}) va nom (robot-pw{code}) ni kiritish.
    3. ATS rolini "Админ" qilib belgilab, Рабочая зона sifatida room-pw{code} ni
       biriktirish va "Активный" statusini tekshirish.
    4. Saqlab, ro'yxatda xodim nomi va kodi ko'rinishini tekshirish.
    """
    robot_name = f"robot-pw{code}"
    robot_code = f"code_robot-pw{code}"
    room_name = f"room-pw{code}"

    with allure.step("1 - Xodimlar ro'yxatiga o'tish"):
        navigate_to(page, tab="Справочники", name="Штат")
        expect_page(page, heading="Штат")

    with allure.step("2 - Yangi xodim formasini to'ldirish"):
        page.get_by_role("button", name="Создать").click()
        expect_page(page, heading="Штат (создание)")
        BasePage(page).input(label="Код", value=robot_code)
        BasePage(page).input(label="Название", value=robot_name)

    with allure.step("3 - ATS roli (Админ) va ish zonasini biriktirish"):
        BasePage(page).multiselect("Роли", "Админ")
        BasePage(page).multiselect("Рабочие зоны", room_name)
        BasePage(page).checkbox(label="Статус", expect_checked=True)

    with allure.step("4 - Saqlash va ro'yxatda tekshirish"):
        page.get_by_role("button", name="Сохранить", exact=True).first.click()
        expect_page(page, heading="Штат")
        BasePage(page).grid_row(robot_name, robot_code)

# ----------------------------------------------------------------------------------------------------------------------

@allure.title("Xodim (robot) yaratish")
def test_robot(page, code):
    authorization(page, who='admin')
    switch_filial(page, name=f"filial-pw{code}")
    run_robot(page, code)
