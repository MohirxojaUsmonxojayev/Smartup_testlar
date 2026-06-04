import re

import allure
from playwright.sync_api import Page, expect
from tests.smoke.flows.flow_navigate import navigate_to, switch_filial
from utils.base_page import BasePage

pytestmark = [allure.epic("Smoke"), allure.feature("Setup"), allure.story("Natural Person")]

# ----------------------------------------------------------------------------------------------------------------------


def _assert_natural_person_list_row(page: Page, person_name: str) -> None:
    row = page.locator("b-grid .tbl-row").filter(has_text=person_name).first
    expect(row).to_be_visible()
    expect(row).to_contain_text(person_name)
    expect(row).to_contain_text("Активный")


def _open_natural_person_view(page: Page, person_name: str) -> None:
    row = page.locator("b-grid .tbl-row").filter(has_text=person_name).first
    expect(row).to_be_visible()
    row.click()
    page.get_by_role("button", name="Просмотр", exact=True).click()
    BasePage(page).wait_for_loader()
    expect(page).to_have_url(re.compile(r".*/anor/mr/person/natural_person_view"))
    expect(page.get_by_role("heading").filter(has_text="Физическое лицо (просмотр)").first).to_be_visible()


def _assert_natural_person_view(page: Page, person_name: str) -> None:
    expect(page.locator("b-page")).to_contain_text(person_name)
    expect(page.locator("b-page")).to_contain_text("Активный")


def _close_natural_person_view(page: Page) -> None:
    page.get_by_role("button", name=re.compile("Закрыть", re.IGNORECASE)).click()
    BasePage(page).wait_for_loader()
    expect(page.get_by_role("heading").filter(has_text="Физические лица").first).to_be_visible()


def run_natural_person(page: Page, code, scope: str = "smoke") -> None:
    person_name = f"natural_person-pw{code}"

    with allure.step("1 - Filialga o'tish va jismoniy shaxslar ro'yxatini ochish"):
        switch_filial(page, name=f"filial-pw{code}")
        navigate_to(page, tab="Справочники", name="Физические лица")
        expect(page.get_by_role("heading")).to_contain_text("Физические лица")

    with allure.step("2 - Yangi jismoniy shaxs formasini to'ldirish"):
        page.get_by_role("button", name="Создать").click()
        expect(page.get_by_role("heading")).to_contain_text("Физическое лицо (создание)")
        page.get_by_role("textbox", name="Поиск").first.click()
        page.locator("b-input").filter(has_text="Поиск").get_by_placeholder("Поиск").fill(person_name)
        expect(page.get_by_text("Активный")).to_be_visible()

    with allure.step("3 - Saqlash va tasdiqlash"):
        page.get_by_role("button", name="Сохранить").click()
        BasePage(page).confirm_biruni()
        BasePage(page).wait_for_loader()
        expect(page.get_by_role("heading")).to_contain_text("Физические лица")

    with allure.step("4 - Ro'yxatda yaratilgan natural person qiymatlarini tekshirish"):
        _assert_natural_person_list_row(page, person_name)

    with allure.step("5 - Natural person view oynasida yaratilgan qiymatlarni tekshirish"):
        _open_natural_person_view(page, person_name)
        _assert_natural_person_view(page, person_name)
        _close_natural_person_view(page)

# ----------------------------------------------------------------------------------------------------------------------

def run_natural_person_for_client_1(page: Page, code, scope: str = "smoke") -> None:
    person_name = f"natural_client-pw{code}"

    with allure.step("1 - Jismoniy shaxslar ro'yxatini ochish"):
        navigate_to(page, tab="Справочники", name="Физические лица")
        expect(page.get_by_role("heading")).to_contain_text("Физические лица")

    with allure.step("2 - Yangi mijoz jismoniy shaxs formasini to'ldirish"):
        page.get_by_role("button", name="Создать").click()
        expect(page.get_by_role("heading")).to_contain_text("Физическое лицо (создание)")
        page.get_by_role("textbox", name="Поиск").first.click()
        page.locator("b-input").filter(has_text="Поиск").get_by_placeholder("Поиск").fill(person_name)
        expect(page.get_by_text("Активный")).to_be_visible()
        page.get_by_text("Клиент", exact=True).click()

    with allure.step("3 - Saqlash va tasdiqlash"):
        page.get_by_role("button", name="Сохранить").click()
        BasePage(page).confirm_biruni()
        BasePage(page).wait_for_loader()
        expect(page.get_by_role("heading")).to_contain_text("Физические лица")

    with allure.step("4 - Jismoniy shaxslar ro'yxati va view oynasida qiymatlarni tekshirish"):
        _assert_natural_person_list_row(page, person_name)
        _open_natural_person_view(page, person_name)
        _assert_natural_person_view(page, person_name)
        _close_natural_person_view(page)

    with allure.step("5 - Mijozlar ro'yxatida ko'rinishini tekshirish"):
        navigate_to(page, tab="Справочники", name="Клиенты")
        expect(page.get_by_role("heading")).to_contain_text("Клиенты")
        expect(page.locator("b-grid")).to_contain_text(person_name)

# ----------------------------------------------------------------------------------------------------------------------

@allure.title("Xodim uchun jismoniy shaxs yaratish")
def test_natural_person(page: Page, code, test_scope) -> None:
    run_natural_person(page, code, scope=test_scope)


@allure.title("Mijoz uchun jismoniy shaxs yaratish")
def test_natural_person_for_client_1(page: Page, code, test_scope) -> None:
    run_natural_person_for_client_1(page, code, scope=test_scope)
