import random
import re

import allure
from faker import Faker
from playwright.sync_api import Page, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from tests.smoke.flows.flow_navigate import navigate_to
from tests.smoke.test_setup.test_natural_person import create_natural_person_record, natural_person_values
from utils.base_page import BasePage

pytestmark = [allure.epic("Smoke"), allure.feature("Setup"), allure.story("Legal Person")]

# ----------------------------------------------------------------------------------------------------------------------

fake_ru = Faker("ru_RU")

_REGRESSION_DATA_KEYS = (
    "legal_person_owner_code",
    "legal_person_owner_name",
    "legal_person_director_code",
    "legal_person_director_name",
    "legal_person_accountant_name",
    "legal_person_tin",
    "legal_person_phone",
    "legal_person_email",
    "legal_person_region",
    "legal_person_gps",
    "legal_person_bank_mfo",
    "legal_person_bank_name",
    "legal_person_bank_account_code",
    "legal_person_bank_account_name",
    "legal_person_contact_name",
    "legal_person_contact_phone",
    "legal_person_contact_position_code",
    "legal_person_contact_position_name",
)


def _digits(count: int) -> str:
    return "".join(str(random.randint(0, 9)) for _ in range(count))


def _uz_phone() -> str:
    return f"9989{random.randint(0, 9)}{_digits(7)}"


def _clean_address(value: str) -> str:
    return value.replace("\n", ", ")


def _legal_person_values(code: str, code_prefix: str, name_suffix: str) -> dict[str, str]:
    return {
        "code": f"{code_prefix}{code}",
        "name": f"{fake_ru.company()} {name_suffix}-pw{code}",
        "short_name": f"{fake_ru.company()} {name_suffix[:18]}-pw{code}",
        "web": f"https://{name_suffix.replace('_', '-')}-pw{code}.example.test",
        "barcode": _digits(13),
        "zip_code": _digits(6),
        "phone": _uz_phone(),
        "telegram": f"@{name_suffix.replace('_', '')}_pw{code}",
        "email": f"{name_suffix}-pw{code}@example.test",
        "region": "город Ташкент",
        "address": _clean_address(fake_ru.address()),
        "post_address": _clean_address(fake_ru.address()),
        "tin": _digits(9),
        "cea": "62010",
        "vat_code": _digits(12),
        "gps_search": "41.2994958,69.2400734",
        "gps": "41.2994958,69.2400734,12",
        "address_guide": fake_ru.street_name(),
        "note": fake_ru.paragraph(nb_sentences=2),
    }


def _contact_position_values(code: str) -> dict[str, str]:
    return {
        "code": f"contact_position_pw{code}",
        "name": f"Директор по развитию-pw{code}",
    }


def _bank_account_values(code: str) -> dict[str, str]:
    return {
        "name": f"Основной расчетный счет-pw{code}",
        "mfo": "00001",
        "bank_name": "Центр расчетов Центрального банка по г. Ташкенту",
        "account_code": f"20208000{_digits(12)}",
        "currency": "Узбекский сум",
        "note": f"Bank account for legal_person-pw{code}",
    }


def _contact_person_values(code: str) -> dict[str, str]:
    first_name = fake_ru.first_name_male()
    last_name = fake_ru.last_name_male()
    middle_name = fake_ru.middle_name_male()
    return {
        "full_name": f"{last_name} {first_name} {middle_name}",
        "phone": _uz_phone(),
        "birthday": fake_ru.date_of_birth(minimum_age=25, maximum_age=50).strftime("%d.%m.%Y"),
        "note": f"Contact person for legal_person-pw{code}",
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


def _select_b_input_by_search(page: Page, ng_model: str, search_text: str, expected_value: str) -> None:
    b_input = page.locator(f'b-input:has(input[ng-model="{ng_model}"])').first
    search = b_input.get_by_placeholder("Поиск").first
    search.click()
    search.fill(search_text)
    option = b_input.locator("div.hint").filter(has_text=search_text).first
    expect(option).to_be_visible()
    option.click()
    expect(search).to_have_value(re.compile(re.escape(expected_value)))


def _select_gps_coordinates(page: Page, search_value: str, expected_value: str) -> None:
    latlng = page.locator('input[ng-model="d.latlng"]').first
    expect(latlng).to_be_visible()
    latlng.locator("xpath=ancestor::*[contains(@class,'input-group')][1]//button[1]").click()

    modal = page.locator(".modal.show").last
    expect(modal).to_be_visible()
    search = modal.locator('input[ng-model="q.search_lat_lng"]')
    expect(search).to_be_visible()
    search.fill(search_value)
    modal.get_by_role("button", name="Создать и закрыть", exact=True).click()
    expect(latlng).to_have_value(expected_value)

    try:
        expect(modal).to_be_visible(timeout=2_000)
        modal.get_by_role("button", name="Закрыть", exact=True).click()
        modal.wait_for(state="hidden")
    except (AssertionError, PlaywrightTimeoutError):
        pass


def _modal_fill_input(modal, ng_model: str, value: str) -> None:
    field = modal.locator(f'input[ng-model="{ng_model}"]:visible').first
    expect(field).to_be_visible()
    field.fill(value)
    expect(field).to_have_value(value)


def _modal_fill_textarea(modal, ng_model: str, value: str) -> None:
    field = modal.locator(f'textarea[ng-model="{ng_model}"]:visible').first
    expect(field).to_be_visible()
    field.fill(value)
    expect(field).to_have_value(value)


def _modal_select_b_input_by_search(modal, ng_model: str, search_text: str, expected_value: str) -> None:
    b_input = modal.locator(f'b-input:has(input[ng-model="{ng_model}"])').first
    search = b_input.get_by_placeholder("Поиск").first
    search.click()
    search.fill(search_text)
    option = b_input.locator("div.hint").filter(has_text=search_text).first
    expect(option).to_be_visible()
    option.click()
    expect(search).to_have_value(re.compile(re.escape(expected_value)))


def _modal_set_checkbox(modal, ng_model: str, checked: bool) -> None:
    checkbox = modal.locator(f'input[ng-model="{ng_model}"]').first
    if checkbox.is_checked() != checked:
        control = checkbox.locator(
            "xpath=ancestor::*[contains(@class,'checkbox') or contains(@class,'switch')][1]"
        )
        if control.count() > 0 and control.first.is_visible():
            control.first.click()
        else:
            expect(checkbox).to_be_visible()
            checkbox.click()
    expect(checkbox).to_be_checked() if checked else expect(checkbox).not_to_be_checked()


def _open_legal_person_add(page: Page) -> None:
    navigate_to(page, tab="Справочники", name="Юридические лица")
    expect(page.get_by_role("heading")).to_contain_text("Юридические лица")
    page.get_by_role("button", name="Создать").click()
    expect(page.get_by_role("heading")).to_contain_text("Юридическое лицо (создание)")


def _fill_legal_person_main_fields(page: Page, values: dict[str, str]) -> None:
    _fill_input(page, "d.code", values["code"])
    _fill_input(page, "d.details.web", values["web"])
    _fill_input(page, "d.details.barcode", values["barcode"])
    _fill_input(page, "d.details.zip_code", values["zip_code"])
    _fill_input(page, "d.name", values["name"])
    _fill_input(page, "d.short_name", values["short_name"])
    expect(page.get_by_text("Активный")).to_be_visible()
    _fill_input(page, "d.details.main_phone", values["phone"])
    _fill_input(page, "d.details.telegram", values["telegram"])
    _fill_input(page, "d.email", values["email"])
    _select_tashkent_region(page)
    _fill_textarea(page, "d.details.address", values["address"])
    _fill_textarea(page, "d.details.post_address", values["post_address"])
    _fill_input(page, "d.details.tin", values["tin"])
    _fill_input(page, "d.details.cea", values["cea"])
    _fill_input(page, "d.details.vat_code", values["vat_code"])
    _select_gps_coordinates(page, values["gps_search"], values["gps"])
    _fill_textarea(page, "d.details.address_guide", values["address_guide"])


def _fill_legal_person_smoke_fields(page: Page, values: dict[str, str]) -> None:
    _fill_input(page, "d.code", values["code"])
    _fill_input(page, "d.name", values["name"])
    expect(page.get_by_text("Активный")).to_be_visible()


def _fill_legal_person_extra_tabs(page: Page, values: dict[str, str], director: dict[str, str]) -> None:
    page.locator("a:visible").filter(has_text="Примечание").first.click()
    _fill_textarea(page, "d.details.note", values["note"])

    accountant_first_name = fake_ru.first_name_female()
    accountant_last_name = fake_ru.last_name_female()
    accountant_middle_name = fake_ru.middle_name_female()

    page.locator("a:visible").filter(has_text="Руководящие должности").first.click()
    _fill_input(page, "d.details.director_first_name", director["first_name"])
    _fill_input(page, "d.details.director_last_name", director["last_name"])
    _fill_input(page, "d.details.director_middle_name", director["middle_name"])
    _fill_input(page, "d.details.director_tin", director["tin"])
    _fill_input(page, "d.details.accountant_first_name", accountant_first_name)
    _fill_input(page, "d.details.accountant_last_name", accountant_last_name)
    _fill_input(page, "d.details.accountant_middle_name", accountant_middle_name)

    values["accountant_full_name"] = f"{accountant_last_name} {accountant_first_name} {accountant_middle_name}"


def _fill_bank_account_tab(page: Page, values: dict[str, str]) -> None:
    page.locator("a:visible").filter(has_text="Расчетный счет").first.click()
    page.get_by_role("button", name="Создать", exact=True).click()

    modal = page.locator(".modal.show").last
    expect(modal).to_be_visible()
    _modal_fill_input(modal, "p.data.bank_account_name", values["name"])
    _modal_fill_input(modal, "p.data.bank_code", values["mfo"])
    modal.locator('input[ng-model="p.data.bank_code"]').press("Tab")
    expect(modal.locator('input[ng-model="p.data.bank_name"]')).to_have_value(values["bank_name"])
    _modal_fill_input(modal, "p.data.bank_account_code", values["account_code"])
    _modal_set_checkbox(modal, "p.data.is_main", True)
    _modal_select_b_input_by_search(modal, "p.data.currency_name", values["currency"], values["currency"])
    _modal_fill_textarea(modal, "p.data.note", values["note"])
    modal.get_by_role("button", name="Создать и закрыть", exact=True).click()
    modal.wait_for(state="hidden")
    expect(page.get_by_text(values["account_code"]).first).to_be_visible()


def _fill_contact_person_tab(
    page: Page,
    contact_values: dict[str, str],
    position_values: dict[str, str],
) -> None:
    page.locator("a:visible").filter(has_text="Контактные лица").first.click()
    page.get_by_role("button", name="Создать", exact=True).click()

    modal = page.locator(".modal.show").last
    expect(modal).to_be_visible()
    _modal_fill_input(modal, "p.data.contact_name", contact_values["full_name"])
    _modal_select_b_input_by_search(
        modal,
        "p.data.position_name",
        position_values["name"],
        position_values["name"],
    )
    _modal_fill_input(modal, "p.data.phone_number", contact_values["phone"])
    _modal_fill_input(modal, "p.data.birthday", contact_values["birthday"])
    _modal_fill_textarea(modal, "p.data.note", contact_values["note"])
    modal.get_by_role("button", name="Создать и закрыть", exact=True).click()
    modal.wait_for(state="hidden")
    expect(page.get_by_text(contact_values["full_name"]).first).to_be_visible()


def _save_add_form(page: Page, list_heading: str, confirm_text: str | None = "Сохранить") -> None:
    page.get_by_role("button", name="Сохранить").click()
    BasePage(page).confirm_biruni(confirm_text)
    BasePage(page).wait_for_loader()
    expect(page.get_by_role("heading")).to_contain_text(list_heading)


def _assert_legal_person_list_row(page: Page, values: dict[str, str], scope: str = "smoke") -> None:
    page.get_by_role("searchbox", name="Поиск").fill(values["code"])
    page.get_by_role("searchbox", name="Поиск").press("Enter")
    BasePage(page).wait_for_loader()
    row = page.locator("b-grid .tbl-row").filter(has_text=values["code"]).first
    expect(row).to_be_visible()
    expect(row).to_contain_text(values["name"])
    if scope == "regression":
        expect(row).to_contain_text(values["short_name"])
    expect(row).to_contain_text("Активный")


def _open_selected_legal_person_view(page: Page, values: dict[str, str]) -> None:
    row = page.locator("b-grid .tbl-row").filter(has_text=values["code"]).first
    expect(row).to_be_visible()
    row.click()
    page.get_by_role("button", name="Просмотреть", exact=True).click()
    BasePage(page).wait_for_loader()
    expect(page).to_have_url(re.compile(r".*/anor/mr/person/legal_person_view"))
    expect(page.get_by_role("heading").filter(has_text="Юридическое лицо (просмотр)").first).to_be_visible()


def _assert_visible_page_text(page: Page, *values: str) -> None:
    content = page.locator("b-page")
    for value in values:
        expect(content).to_contain_text(value)


def _open_view_tab(page: Page, tab_name: str) -> None:
    page.locator("a:visible").filter(has_text=tab_name).first.click()
    BasePage(page).wait_for_loader()


def _assert_legal_person_view(
    page: Page,
    main_values: dict[str, str],
    owner_values: dict[str, str] | None,
    director_values: dict[str, str] | None,
    bank_values: dict[str, str] | None,
    contact_values: dict[str, str] | None,
    position_values: dict[str, str] | None,
) -> None:
    _open_view_tab(page, "Основная информация")
    _assert_visible_page_text(
        page,
        main_values["name"],
        main_values["short_name"],
        owner_values["name"],
        main_values["code"],
        main_values["barcode"],
        main_values["email"],
    )

    _open_view_tab(page, "Дополнительная информация")
    _assert_visible_page_text(
        page,
        director_values["full_name"],
        main_values["phone"],
        main_values["region"],
        main_values["zip_code"],
        main_values["address"],
        main_values["post_address"],
        main_values["address_guide"],
        main_values["gps"],
        main_values["tin"],
        main_values["cea"],
        main_values["note"],
        main_values["accountant_full_name"],
    )

    _open_view_tab(page, "Расчетный счет")
    _assert_visible_page_text(
        page,
        bank_values["bank_name"],
        bank_values["name"],
        bank_values["account_code"],
        "Да",
        "Активный",
    )

    _open_view_tab(page, "Контактные лица")
    _assert_visible_page_text(
        page,
        contact_values["full_name"],
        position_values["name"],
        contact_values["phone"],
        contact_values["birthday"],
        contact_values["note"],
    )


def _close_legal_person_view(page: Page) -> None:
    page.get_by_role("button", name=re.compile("Закрыть", re.IGNORECASE)).click()
    BasePage(page).wait_for_loader()
    expect(page.get_by_role("heading").filter(has_text="Юридические лица").first).to_be_visible()


def _create_support_legal_person(page: Page, values: dict[str, str]) -> None:
    _open_legal_person_add(page)
    _fill_legal_person_main_fields(page, values)
    page.locator("a:visible").filter(has_text="Примечание").first.click()
    _fill_textarea(page, "d.details.note", values["note"])
    _save_add_form(page, list_heading="Юридические лица")


def _create_contact_position(page: Page, values: dict[str, str]) -> None:
    _open_legal_person_add(page)
    page.locator("a:visible").filter(has_text="Контактные лица").first.click()
    page.get_by_role("button", name="Создать", exact=True).click()
    position = page.locator('b-input:has(input[ng-model="p.data.position_name"])').first
    position.get_by_placeholder("Поиск").click()
    add_button = position.get_by_role("link", name="Добавить", exact=True)
    try:
        expect(add_button).to_be_visible(timeout=5_000)
    except PlaywrightTimeoutError:
        pass
    add_button.click(force=True)

    expect(page.get_by_role("heading")).to_contain_text("Должности (создание)")
    _fill_input(page, "d.name", values["name"])
    _fill_input(page, "d.code", values["code"])
    page.get_by_role("button", name="Сохранить").click()
    BasePage(page).wait_for_loader()
    expect(page.get_by_role("heading").filter(has_text="Юридическое лицо (создание)").first).to_be_visible()
    modal = page.locator(".modal.show").last
    try:
        expect(modal).to_be_visible(timeout=2_000)
        modal.get_by_role("button", name="Закрыть", exact=True).click()
        modal.wait_for(state="hidden")
    except (AssertionError, PlaywrightTimeoutError):
        pass


def _save_legal_person_data(
    save_data,
    main_values: dict[str, str],
    owner_values: dict[str, str],
    director_values: dict[str, str],
    bank_values: dict[str, str],
    contact_values: dict[str, str],
    position_values: dict[str, str],
) -> None:
    if save_data is None:
        return

    save_data("legal_person_code", main_values["code"])
    save_data("legal_person_name", main_values["name"])
    if not all((owner_values, director_values, bank_values, contact_values, position_values)):
        for key in _REGRESSION_DATA_KEYS:
            save_data(key, None)
        return

    save_data("legal_person_owner_code", owner_values["code"])
    save_data("legal_person_owner_name", owner_values["name"])
    save_data("legal_person_director_code", director_values["code"])
    save_data("legal_person_director_name", director_values["full_name"])
    save_data("legal_person_accountant_name", main_values["accountant_full_name"])
    save_data("legal_person_tin", main_values["tin"])
    save_data("legal_person_phone", main_values["phone"])
    save_data("legal_person_email", main_values["email"])
    save_data("legal_person_region", main_values["region"])
    save_data("legal_person_gps", main_values["gps"])
    save_data("legal_person_bank_mfo", bank_values["mfo"])
    save_data("legal_person_bank_name", bank_values["bank_name"])
    save_data("legal_person_bank_account_code", bank_values["account_code"])
    save_data("legal_person_bank_account_name", bank_values["name"])
    save_data("legal_person_contact_name", contact_values["full_name"])
    save_data("legal_person_contact_phone", contact_values["phone"])
    save_data("legal_person_contact_position_code", position_values["code"])
    save_data("legal_person_contact_position_name", position_values["name"])


def run_legal_person(page: Page, code, save_data=None, scope: str = "smoke") -> None:
    owner_values = _legal_person_values(code, code_prefix="cod_owner_lg_pw", name_suffix="legal_owner")
    director_values = natural_person_values(code, code_prefix="director_np_pw", name_suffix="director")
    main_values = _legal_person_values(code, code_prefix="cod_lg_pw", name_suffix="legal_person")
    position_values = _contact_position_values(code)
    bank_values = _bank_account_values(code)
    contact_values = _contact_person_values(code)

    with allure.step("1 - Yuridik shaxslar ro'yxatiga o'tish"):
        navigate_to(page, tab="Справочники", name="Юридические лица")
        expect(page.get_by_role("heading")).to_contain_text("Юридические лица")

    if scope == "regression":
        with allure.step("2 - Regression: Собственник uchun alohida yuridik shaxs yaratish"):
            _create_support_legal_person(page, owner_values)

        with allure.step("3 - Regression: Руководитель uchun alohida jismoniy shaxs yaratish"):
            create_natural_person_record(page, director_values, scope="regression")

        with allure.step("4 - Regression: Kontakt shaxs lavozimini yaratish"):
            _create_contact_position(page, position_values)

    with allure.step("5 - Yangi yuridik shaxs formasini scope bo'yicha to'ldirish"):
        _open_legal_person_add(page)
        if scope == "regression":
            _fill_legal_person_main_fields(page, main_values)
            _select_b_input_by_search(page, "d.parent_person_name", owner_values["code"], owner_values["name"])
            _select_b_input_by_search(page, "d.primary_person_name", director_values["code"], director_values["full_name"])
            _fill_bank_account_tab(page, bank_values)
            _fill_contact_person_tab(page, contact_values, position_values)
            _fill_legal_person_extra_tabs(page, main_values, director_values)
        else:
            _fill_legal_person_smoke_fields(page, main_values)

    with allure.step("6 - Saqlash va tasdiqlash"):
        _save_add_form(page, list_heading="Юридические лица")

    with allure.step("7 - Ro'yxatda yaratilgan legal person qiymatlarini tekshirish"):
        _assert_legal_person_list_row(page, main_values, scope=scope)

    if scope == "regression":
        with allure.step("8 - Regression: Legal person view oynasida qo'shilgan qiymatlarni tekshirish"):
            _open_selected_legal_person_view(page, main_values)
            _assert_legal_person_view(
                page,
                main_values,
                owner_values,
                director_values,
                bank_values,
                contact_values,
                position_values,
            )
            _close_legal_person_view(page)

    with allure.step("9 - Muhim legal person ma'lumotlarini data storega saqlash"):
        _save_legal_person_data(
            save_data,
            main_values,
            owner_values if scope == "regression" else None,
            director_values if scope == "regression" else None,
            bank_values if scope == "regression" else None,
            contact_values if scope == "regression" else None,
            position_values if scope == "regression" else None,
        )


@allure.title("Yuridik shaxs yaratish")
def test_legal_person(page: Page, code, save_data, test_scope) -> None:
    run_legal_person(page, code, save_data, scope=test_scope)
