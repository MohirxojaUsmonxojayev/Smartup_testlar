import re

import allure
from playwright.sync_api import Page, expect
from tests.smoke.flows.flow_form import fill_input, select_b_input_by_search, set_checkbox
from tests.smoke.flows.flow_navigate import navigate_to
from utils.base_page import BasePage

pytestmark = [allure.epic("Smoke"), allure.feature("Setup"), allure.story("Filial")]

# ----------------------------------------------------------------------------------------------------------------------

def _assert_filial_list_row(
    page: Page,
    filial_name: str,
    legal_person_code: str,
    legal_person_name: str | None = None,
) -> None:
    row = page.locator("b-grid .tbl-row").filter(has_text=filial_name).first
    expect(row).to_be_visible()
    expect(row).to_contain_text(filial_name)
    expect(row).to_contain_text(legal_person_code)
    expect(row).to_contain_text("Активный")


def _open_filial_view(page: Page, filial_name: str) -> None:
    row = page.locator("b-grid .tbl-row").filter(has_text=filial_name).first
    expect(row).to_be_visible()
    row.click()
    page.get_by_role("button", name="Просмотреть", exact=True).click()
    BasePage(page).wait_for_loader()
    expect(page.get_by_role("heading").filter(has_text="Организация")).to_be_visible()


def _assert_filial_view_page_fields(
    page: Page,
    filial_name: str,
    legal_person_code: str,
    legal_person_name: str | None = None,
    vat_percent: str | None = None,
    timezone: str | None = None,
) -> None:
    expect(page.locator("b-page")).to_contain_text(filial_name)
    expect(page.locator("b-page")).to_contain_text("Узбекский сум")
    expect(page.locator("b-page")).to_contain_text(legal_person_code)
    expect(page.locator("b-page")).to_contain_text("Активный")
    if legal_person_name:
        expect(page.locator("b-page")).to_contain_text(legal_person_name)
    if vat_percent:
        expect(page.locator("b-page")).to_contain_text("Ставка НДС (%)")
        expect(page.locator("b-page")).to_contain_text(vat_percent)
    expect(page.locator("b-page")).to_contain_text("Акциз")
    expect(page.locator("b-page")).to_contain_text("Да")
    if timezone:
        expect(page.locator("b-page")).to_contain_text(timezone)


def _assert_checked_product_switches(page: Page, expected_texts: tuple[str, ...]) -> None:
    for text in expected_texts:
        label = page.get_by_text(text, exact=True).first
        expect(label).to_be_visible()
        row = label.locator("xpath=ancestor::*[.//input[@type='checkbox']][1]")
        checkbox = row.locator("input[type='checkbox']").first
        expect(checkbox).to_be_checked()


def _assert_filial_product_modules(page: Page) -> None:
    page.locator("a:visible").filter(has_text="Продукты").first.click()
    BasePage(page).wait_for_loader()
    expect(page.get_by_role("button", name="Сохранить")).to_be_visible()
    expect(page.locator("b-page")).to_contain_text("trade")

    _assert_checked_product_switches(
        page,
        (
            "trade",
            "Equipment",
            "Finance - Main",
            "Finance - Advanced",
            "HR and Payroll",
            "Image Recognition",
            "Main",
            "Manufacturing",
            "Marking",
            "Sales - Main",
            "Sales - Advanced",
            "Store",
            "Telegram",
            "Trade Marketing",
            "Uzbekistan Module",
            "Warehouse - Main",
            "Warehouse - Advanced",
        ),
    )


def _save_filial_data(
    save_data,
    filial_name: str,
    legal_person_code: str,
    legal_person_name: str | None = None,
    timezone: str | None = None,
    order_no: str | None = None,
    vat_enabled: bool | None = None,
    vat_percent: str | None = None,
    excise_enabled: bool | None = None,
) -> None:
    if save_data is None:
        return
    save_data("filial_name", filial_name)
    save_data("filial_currency", "Узбекский сум")
    save_data("filial_legal_person_code", legal_person_code)
    if legal_person_name:
        save_data("filial_legal_person_name", legal_person_name)
    if timezone:
        save_data("filial_timezone", timezone)
    if order_no:
        save_data("filial_order_no", order_no)
    if vat_enabled is not None:
        save_data("filial_vat_enabled", vat_enabled)
    if vat_percent:
        save_data("filial_vat_percent", vat_percent)
    if excise_enabled is not None:
        save_data("filial_excise_enabled", excise_enabled)


def _close_filial_view(page: Page) -> None:
    page.get_by_role("button", name=re.compile("Закрыть", re.IGNORECASE)).click()
    BasePage(page).wait_for_loader()
    expect(page.get_by_role("heading")).to_contain_text("Организации")


def _fill_filial_regression_fields(page: Page, code: str) -> dict[str, str]:
    order_no = str(int(code))
    timezone_name = "(+05:00) Ташкент"
    timezone_code = "Asia/Tashkent"
    vat_percent = "12"

    with allure.step("2.1 - Regression: mavjud filial add maydonlarini to'ldirish"):
        select_b_input_by_search(
            page,
            ng_model="d.timezone_name",
            search_text="Ташкент",
            option_text=timezone_code,
            expected_value="Ташкент",
        )
        fill_input(page, "d.order_no", order_no)
        set_checkbox(page, "d.vat_enabled", True)
        fill_input(page, "d.vat_percent", vat_percent)
        set_checkbox(page, "d.excise_enabled", True)

    return {
        "timezone": timezone_name,
        "timezone_code": timezone_code,
        "order_no": order_no,
        "vat_enabled": True,
        "vat_percent": vat_percent,
        "excise_enabled": True,
    }


def run_filial(
    page: Page,
    code,
    scope: str = "smoke",
    legal_person_code: str | None = None,
    legal_person_name: str | None = None,
    save_data=None,
) -> None:
    filial_name = f"filial-pw{code}"
    legal_person_code = legal_person_code or f"cod_lg_pw{code}"
    regression_values: dict[str, str] = {}

    with allure.step("1 - Tashkilotlar ro'yxatiga o'tish"):
        navigate_to(page, tab="Главное", name="Организации")
        expect(page.get_by_role("heading")).to_contain_text("Организации")

    with allure.step("2 - Yangi tashkilot formasini to'ldirish"):
        page.get_by_role("button", name="Создать").click()
        expect(page.get_by_role("heading")).to_contain_text("Организация (создание)")
        fill_input(page, "d.name", filial_name)

        select_b_input_by_search(
            page,
            ng_model="d.base_currency_name",
            search_text="Узбекский сум",
            option_text="Узбекский сум",
            expected_value="Узбекский сум",
        )
        BasePage(page).confirm_biruni("Продолжить?")

        select_b_input_by_search(
            page,
            ng_model="d.person_name",
            search_text=legal_person_code,
            option_text=legal_person_code,
            expected_value=legal_person_name,
        )

        if scope == "regression":
            regression_values = _fill_filial_regression_fields(page, code)

    with allure.step("3 - Saqlash va tasdiqlash"):
        BasePage(page).save_and_expect_heading(
            "Организации",
            action="Организация (создание) -> Сохранить",
            before_state="Организация (создание)",
            expected_state="Организации list ochilishi",
            confirm_text="Сохранить",
            location_hint="tests/smoke/test_setup/test_filial.py::run_filial",
        )

    with allure.step("4 - Ro'yxatda yaratilganini tekshirish"):
        page.get_by_role("searchbox", name="Поиск").fill(filial_name)
        page.get_by_role("searchbox", name="Поиск").press("Enter")
        BasePage(page).wait_for_loader()
        _assert_filial_list_row(page, filial_name, legal_person_code, legal_person_name)

        page.reload()
        BasePage(page).wait_for_loader(timeout=600_000)

    if scope == "regression":
        with allure.step("5 - Regression: Filial view oynasida qiymatlarni tekshirish"):
            _open_filial_view(page, filial_name)
            _assert_filial_view_page_fields(
                page,
                filial_name,
                legal_person_code,
                legal_person_name,
                vat_percent=regression_values.get("vat_percent"),
                timezone=regression_values.get("timezone"),
            )
            _assert_filial_product_modules(page)
            _close_filial_view(page)

    _save_filial_data(
        save_data=save_data,
        filial_name=filial_name,
        legal_person_code=legal_person_code,
        legal_person_name=legal_person_name,
        timezone=regression_values.get("timezone_code"),
        order_no=regression_values.get("order_no"),
        vat_enabled=regression_values.get("vat_enabled"),
        vat_percent=regression_values.get("vat_percent"),
        excise_enabled=regression_values.get("excise_enabled"),
    )

# ----------------------------------------------------------------------------------------------------------------------

@allure.title("Filial (tashkilot) yaratish")
def test_filial(page: Page, code, load_data, save_data, test_scope) -> None:
    run_filial(
        page,
        code,
        scope=test_scope,
        legal_person_code=load_data("legal_person_code"),
        legal_person_name=load_data("legal_person_name"),
        save_data=save_data,
    )
