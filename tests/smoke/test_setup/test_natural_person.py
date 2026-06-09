import random
import re

import allure
from faker import Faker
from playwright.sync_api import Page, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from tests.smoke.flows.flow_navigate import navigate_to, switch_filial
from utils.base_page import BasePage

pytestmark = [allure.epic("Smoke"), allure.feature("Setup"), allure.story("Natural Person")]

# ----------------------------------------------------------------------------------------------------------------------

fake_ru = Faker("ru_RU")


def _digits(count: int) -> str:
    return "".join(str(random.randint(0, 9)) for _ in range(count))


def _uz_phone() -> str:
    return f"9989{random.randint(0, 9)}{_digits(7)}"


def _clean_address(value: str) -> str:
    return value.replace("\n", ", ")


def natural_person_values(
    code: str,
    code_prefix: str = "natural_person_pw",
    full_name: str | None = None,
    name_suffix: str = "natural_person",
) -> dict[str, str]:
    if full_name:
        first_name = full_name
        last_name = ""
        middle_name = ""
    else:
        first_name = fake_ru.first_name_male()
        last_name = fake_ru.last_name_male()
        middle_name = fake_ru.middle_name_male()
        full_name = f"{last_name} {first_name} {middle_name}"

    slug = name_suffix.replace("_", "-")
    return {
        "code": f"{code_prefix}{code}",
        "first_name": first_name,
        "last_name": last_name,
        "middle_name": middle_name,
        "full_name": full_name,
        "birthday": fake_ru.date_of_birth(minimum_age=25, maximum_age=55).strftime("%d.%m.%Y"),
        "passport_series": "AA",
        "passport_digits": _digits(7),
        "region": "город Ташкент",
        "address": _clean_address(fake_ru.address()),
        "post_address": _clean_address(fake_ru.address()),
        "phone": _uz_phone(),
        "tin": _digits(14),
        "telegram": f"@{name_suffix.replace('_', '')}_pw{code}",
        "email": f"{slug}-pw{code}@example.test",
        "web": f"https://{slug}-pw{code}.example.test",
    }


def _fill_input(page: Page, ng_model: str, value: str) -> None:
    field = page.locator(f'input[ng-model="{ng_model}"]:visible').first
    expect(field).to_be_visible()
    field.fill(value)
    expect(field).to_have_value(value)


def _fill_textarea(page: Page, ng_model: str, value: str) -> None:
    field = page.locator(f'textarea[ng-model="{ng_model}"]:visible').first
    expect(field).to_be_visible()
    field.fill(value)
    expect(field).to_have_value(value)


def _fill_optional_input(page: Page, ng_model: str, value: str) -> None:
    if value:
        _fill_input(page, ng_model, value)


def _select_tashkent_region(page: Page) -> None:
    search = page.locator('b-tree-select:visible input[ng-model="_$bTree.searchValue"]').first
    expect(search).to_be_visible()
    search.click()
    search.fill("Ташкент")
    hint = page.locator("b-tree-select:visible .hint").first
    expect(hint).to_be_visible(timeout=5_000)

    for option_text in ("город Ташкент", "Ташкент"):
        options = (
            hint.get_by_text(option_text, exact=True).first,
            hint.locator("label").filter(has_text=option_text).first,
            hint.locator(".jstree-anchor").filter(has_text=option_text).first,
        )
        for option in options:
            try:
                expect(option).to_be_visible(timeout=5_000)
                option.click()
                expect(search).to_have_value(re.compile("Ташкент"))
                return
            except (AssertionError, PlaywrightTimeoutError):
                continue

    raise AssertionError("Region option 'город Ташкент' not found")


def open_natural_person_list(page: Page) -> None:
    navigate_to(page, tab="Справочники", name="Физические лица")
    expect(page.get_by_role("heading")).to_contain_text("Физические лица")


def _open_natural_person_add(page: Page) -> None:
    page.get_by_role("button", name="Создать").click()
    expect(page.get_by_role("heading")).to_contain_text("Физическое лицо (создание)")


def _fill_natural_person_name_fields(page: Page, values: dict[str, str]) -> None:
    _fill_optional_input(page, "d.last_name", values["last_name"])
    _fill_input(page, "d.first_name", values["first_name"])
    _fill_optional_input(page, "d.middle_name", values["middle_name"])


def _fill_natural_person_smoke_fields(page: Page, values: dict[str, str]) -> None:
    _fill_natural_person_name_fields(page, values)
    _fill_input(page, "d.code", values["code"])
    expect(page.get_by_text("Активный")).to_be_visible()


def _fill_natural_person_regression_fields(page: Page, values: dict[str, str]) -> None:
    _fill_natural_person_smoke_fields(page, values)
    _fill_input(page, "d.birthday", values["birthday"])
    _fill_input(page, "d.passport_series", values["passport_series"])
    _fill_input(page, "d.passport_digits", values["passport_digits"])
    _select_tashkent_region(page)
    _fill_textarea(page, "d.address", values["address"])
    _fill_textarea(page, "d.post_address", values["post_address"])
    _fill_input(page, "d.main_phone", values["phone"])
    _fill_input(page, "d.tin", values["tin"])
    _fill_input(page, "d.telegram", values["telegram"])
    _fill_input(page, "d.email", values["email"])
    _fill_input(page, "d.web", values["web"])


def fill_natural_person_add_form(
    page: Page,
    values: dict[str, str],
    scope: str = "smoke",
    client: bool = False,
) -> None:
    if scope == "regression":
        _fill_natural_person_regression_fields(page, values)
    else:
        _fill_natural_person_smoke_fields(page, values)

    if client:
        page.get_by_text("Клиент", exact=True).click()


def _save_natural_person_add(page: Page) -> None:
    page.get_by_role("button", name="Сохранить").click()
    BasePage(page).confirm_biruni()
    BasePage(page).wait_for_loader()
    expect(page.get_by_role("heading")).to_contain_text("Физические лица")


def assert_natural_person_list_row(
    page: Page,
    values: dict[str, str],
    search_by_code: bool = False,
) -> None:
    search_text = values["code"] if search_by_code else values["full_name"]
    page.get_by_role("searchbox", name="Поиск").fill(search_text)
    page.get_by_role("searchbox", name="Поиск").press("Enter")
    BasePage(page).wait_for_loader()

    row = page.locator("b-grid .tbl-row").filter(has_text=values["full_name"]).first
    try:
        expect(row).to_be_visible(timeout=5_000)
    except (AssertionError, PlaywrightTimeoutError):
        row = page.locator("b-grid .tbl-row").first

    expect(row).to_be_visible()
    expect(row).to_contain_text(values["full_name"])
    expect(row).to_contain_text("Активный")


def _assert_list_row_by_search(page: Page, text: str) -> None:
    page.get_by_role("searchbox", name="Поиск").fill(text)
    page.get_by_role("searchbox", name="Поиск").press("Enter")
    BasePage(page).wait_for_loader()
    row = page.locator("b-grid .tbl-row").filter(has_text=text).first
    expect(row).to_be_visible()
    expect(row).to_contain_text(text)


def _open_natural_person_view(page: Page, values: dict[str, str]) -> None:
    row = page.locator("b-grid .tbl-row").filter(has_text=values["full_name"]).first
    expect(row).to_be_visible()
    row.click()
    page.get_by_role("button", name="Просмотр", exact=True).click()
    BasePage(page).wait_for_loader()
    expect(page).to_have_url(re.compile(r".*/anor/mr/person/natural_person_view"))
    expect(page.get_by_role("heading").filter(has_text="Физическое лицо (просмотр)").first).to_be_visible()


def _assert_visible_page_text(page: Page, *values: str) -> None:
    content = page.locator("b-page")
    for value in values:
        if value:
            expect(content).to_contain_text(value)


def _assert_natural_person_view(page: Page, values: dict[str, str], scope: str = "smoke") -> None:
    _assert_visible_page_text(page, values["full_name"], "Активный")

    if scope == "regression":
        _assert_visible_page_text(
            page,
            values["code"],
            values["birthday"],
            values["email"],
            values["address"],
            values["post_address"],
        )


def _close_natural_person_view(page: Page) -> None:
    page.get_by_role("button", name=re.compile("Закрыть", re.IGNORECASE)).click()
    BasePage(page).wait_for_loader()
    expect(page.get_by_role("heading").filter(has_text="Физические лица").first).to_be_visible()


def create_natural_person_record(
    page: Page,
    values: dict[str, str],
    scope: str = "smoke",
    client: bool = False,
) -> None:
    open_natural_person_list(page)
    _open_natural_person_add(page)
    fill_natural_person_add_form(page, values, scope=scope, client=client)
    _save_natural_person_add(page)
    assert_natural_person_list_row(page, values, search_by_code=True)


def _assert_natural_person_created(page: Page, values: dict[str, str], scope: str) -> None:
    assert_natural_person_list_row(page, values, search_by_code=True)
    _open_natural_person_view(page, values)
    _assert_natural_person_view(page, values, scope=scope)
    _close_natural_person_view(page)


def run_natural_person(page: Page, code, scope: str = "smoke") -> None:
    values = natural_person_values(
        code,
        code_prefix="natural_person_pw",
        full_name=f"natural_person-pw{code}",
        name_suffix="natural_person",
    )

    with allure.step("1 - Filialga o'tish va jismoniy shaxslar ro'yxatini ochish"):
        switch_filial(page, name=f"filial-pw{code}")
        open_natural_person_list(page)

    with allure.step("2 - Yangi jismoniy shaxs formasini scope bo'yicha to'ldirish"):
        _open_natural_person_add(page)
        fill_natural_person_add_form(page, values, scope=scope)

    with allure.step("3 - Saqlash va tasdiqlash"):
        _save_natural_person_add(page)

    with allure.step("4 - Ro'yxatda yaratilgan natural person qiymatlarini tekshirish"):
        assert_natural_person_list_row(page, values, search_by_code=True)

    with allure.step("5 - Natural person view oynasida yaratilgan qiymatlarni tekshirish"):
        _open_natural_person_view(page, values)
        _assert_natural_person_view(page, values, scope=scope)
        _close_natural_person_view(page)

# ----------------------------------------------------------------------------------------------------------------------


def run_natural_person_for_client_1(page: Page, code, scope: str = "smoke") -> None:
    values = natural_person_values(
        code,
        code_prefix="natural_client_pw",
        full_name=f"natural_client-pw{code}",
        name_suffix="natural_client",
    )

    with allure.step("1 - Jismoniy shaxslar ro'yxatini ochish"):
        open_natural_person_list(page)

    with allure.step("2 - Yangi mijoz jismoniy shaxs formasini scope bo'yicha to'ldirish"):
        _open_natural_person_add(page)
        fill_natural_person_add_form(page, values, scope=scope, client=True)

    with allure.step("3 - Saqlash va tasdiqlash"):
        _save_natural_person_add(page)

    with allure.step("4 - Jismoniy shaxslar ro'yxati va view oynasida qiymatlarni tekshirish"):
        _assert_natural_person_created(page, values, scope=scope)

    with allure.step("5 - Mijozlar ro'yxatida ko'rinishini tekshirish"):
        navigate_to(page, tab="Справочники", name="Клиенты")
        expect(page.get_by_role("heading")).to_contain_text("Клиенты")
        _assert_list_row_by_search(page, values["full_name"])

# ----------------------------------------------------------------------------------------------------------------------


@allure.title("Xodim uchun jismoniy shaxs yaratish")
def test_natural_person(page: Page, code, test_scope) -> None:
    """Xodim natural personini yaratadi, listda topadi va viewda tekshiradi."""
    run_natural_person(page, code, scope=test_scope)


@allure.title("Mijoz uchun jismoniy shaxs yaratish")
def test_natural_person_for_client_1(page: Page, code, test_scope) -> None:
    """Mijoz natural personini yaratadi, viewda va Clients listida tekshiradi."""
    run_natural_person_for_client_1(page, code, scope=test_scope)
