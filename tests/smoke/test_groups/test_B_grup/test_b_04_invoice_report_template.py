import json
import re
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, expect

from tests.smoke.flows.flow_authorization import authorization, authorization_user, logout
from tests.smoke.flows.flow_navigate import navigate_to
from tests.smoke.flows.flow_order.flow_order_list import flow_open_order_list, flow_order_list
from utils.base_page import BasePage

pytestmark = [
    pytest.mark.smoke_group("B"),
    allure.epic("B Group"),
    allure.feature("Invoice Report Template"),
    allure.story("B-04 Custom Invoice Report"),
]


def _search_grid(page: Page, text: str) -> None:
    search = page.locator('input[ng-model="o.searchValue"]').first
    expect(search).to_be_visible()
    search.click()
    search.press("ControlOrMeta+A")
    search.press("Backspace")
    search.fill(text)
    search.press("Enter")
    BasePage(page).wait_for_loader(timeout=120_000)


def _grid_row_is_visible(page: Page, text: str, timeout: int = 2_000) -> bool:
    try:
        expect(page.locator("b-grid .tbl-row").filter(has_text=text).first).to_be_visible(timeout=timeout)
        return True
    except (AssertionError, PlaywrightTimeoutError):
        return False


def _save_downloaded_report(download) -> str:
    failure = download.failure()
    if failure:
        raise AssertionError(f"Custom invoice report download xato bilan tugadi: {failure}")

    suggested_filename = download.suggested_filename
    if not suggested_filename:
        raise AssertionError("Custom invoice report download filename qaytarmadi")

    download_dir = Path("test-results/downloads")
    download_dir.mkdir(parents=True, exist_ok=True)
    target_path = download_dir / suggested_filename
    download.save_as(target_path)
    if not target_path.exists() or target_path.stat().st_size == 0:
        raise AssertionError(f"Custom invoice report fayli bo'sh yoki saqlanmadi: {target_path}")

    allure.attach(
        json.dumps({"filename": suggested_filename, "path": str(target_path)}, ensure_ascii=False, indent=2),
        name="custom-invoice-report-download",
        attachment_type=allure.attachment_type.JSON,
    )
    return suggested_filename


def run_b_group_create_custom_invoice_report_template(
    page: Page,
    code: str,
    load_data,
    scope: str = "smoke",
    login: bool = True,
) -> None:
    """
    Testcase:
    1. Mavjud admin bilan tizimga kirish.
    2. Главное -> Шаблоны накладных sahifasini ochish.
    3. Накладная (заказ) uchun Test_invoice_report-{code} template yaratish yoki mavjudini topish.
    4. data/test_invoice_report.xlsx faylini templatega upload qilish.
    5. Template'ni Админ rolega detach/attach qilib qayta ulash.
    6. Admin profildan chiqib user bilan kirish.
    7. Order list rowidagi Счет-фактуры buttonidan custom template download bo'lishini tekshirish.
    """
    template_name = f"Test_invoice_report-{code}"
    form_name = "Накладная (заказ)"
    role_name = "Админ"
    template_file = Path("data/test_invoice_report.xlsx")

    if not template_file.exists():
        raise AssertionError(f"Invoice report template fayli topilmadi: {template_file}")

    if login:
        with allure.step("1 - Admin user tizimga kiradi"):
            authorization(page)
            expect(page.locator("body")).to_contain_text("Trade", timeout=120_000)

    with allure.step("2 - Шаблоны накладных sahifasida custom template tayyorlanadi"):
        navigate_to(page, tab="Главное", name="Шаблоны накладных")
        expect(page).to_have_url(re.compile(r".*/template_list"))
        expect(page.locator("body")).to_contain_text("Шаблоны накладных")

        _search_grid(page, template_name)
        if _grid_row_is_visible(page, template_name):
            template_row = page.locator("b-grid .tbl-row").filter(has_text=template_name).first
            expect(template_row).to_contain_text(form_name)
        else:
            page.locator('button[ng-click="add()"]:visible').click()
            expect(page).to_have_url(re.compile(r".*/setting\+add"))
            expect(page.locator("body")).to_contain_text("Настройки шаблонов")
            expect(page.locator("body")).to_contain_text("Файл шаблона")

            origin = page.locator('b-input[name="origin"] input').first
            expect(origin).to_be_visible()
            origin.click()
            origin.fill(form_name)
            option = page.locator('b-input[name="origin"] .hint-item').filter(has_text=form_name).first
            expect(option).to_be_visible(timeout=30_000)
            option.click()
            expect(origin).to_have_value(re.compile(re.escape(form_name)))

            name_input = page.locator('input[ng-model="d.name"]').first
            expect(name_input).to_be_visible()
            name_input.fill(template_name)
            expect(name_input).to_have_value(template_name)

            page.locator('input[type="file"][accept=".xlsx"]').set_input_files(template_file)
            expect(page.locator("body")).to_contain_text(template_file.name, timeout=60_000)

            page.locator('button[ng-click="save()"]').click()
            BasePage(page).wait_for_loader(timeout=120_000)
            expect(page).to_have_url(re.compile(r".*/template_list"), timeout=60_000)

            _search_grid(page, template_name)
            template_row = page.locator("b-grid .tbl-row").filter(has_text=template_name).first
            expect(template_row).to_be_visible()
            expect(template_row).to_contain_text(form_name)
            expect(template_row).to_contain_text(template_file.name)
            expect(template_row).to_contain_text("Активный")

    with allure.step("3 - Template Админ rolega qayta attach qilinadi"):
        navigate_to(page, tab="Главное", name="Шаблоны накладных")
        expect(page).to_have_url(re.compile(r".*/template_list"))
        _search_grid(page, template_name)

        template_row = page.locator("b-grid .tbl-row").filter(has_text=template_name).first
        expect(template_row).to_be_visible()
        template_row.click()

        attach_roles_button = page.locator("button:visible").filter(has_text="Прикрепить роли").first
        expect(attach_roles_button).to_be_visible()
        attach_roles_button.click()
        expect(page).to_have_url(re.compile(r".*/template_role_list"))
        expect(page.locator("body")).to_contain_text(re.compile("прикрепленные", re.IGNORECASE))
        expect(page.locator("body")).to_contain_text(re.compile("доступные", re.IGNORECASE))

        page.locator("button").filter(has_text=re.compile(r"^\s*Прикрепленные\s*$", re.IGNORECASE)).first.click()
        BasePage(page).wait_for_loader(timeout=120_000)
        _search_grid(page, role_name)
        if _grid_row_is_visible(page, role_name):
            role_row = page.locator("b-grid .tbl-row").filter(has_text=role_name).first
            role_row.click()
            detach_button = page.locator("button:visible").filter(has_text="Открепить").first
            expect(detach_button).to_be_visible()
            detach_button.click()
            try:
                BasePage(page).confirm_biruni()
            except (AssertionError, PlaywrightTimeoutError):
                pass
            BasePage(page).wait_for_loader(timeout=120_000)
            _search_grid(page, role_name)
            if _grid_row_is_visible(page, role_name, timeout=1_000):
                raise AssertionError(f"{role_name} role template'dan detach bo'lmadi")

        page.locator("button").filter(has_text=re.compile(r"^\s*Доступные\s*$", re.IGNORECASE)).first.click()
        BasePage(page).wait_for_loader(timeout=120_000)
        _search_grid(page, role_name)
        role_row = page.locator("b-grid .tbl-row").filter(has_text=role_name).first
        expect(role_row).to_be_visible()
        role_row.click()

        attach_button = page.locator("button:visible").filter(has_text="Прикрепить").first
        expect(attach_button).to_be_visible()
        attach_button.click()
        try:
            BasePage(page).confirm_biruni()
        except (AssertionError, PlaywrightTimeoutError):
            pass
        BasePage(page).wait_for_loader(timeout=120_000)

        page.locator("button").filter(has_text=re.compile(r"^\s*Прикрепленные\s*$", re.IGNORECASE)).first.click()
        BasePage(page).wait_for_loader(timeout=120_000)
        _search_grid(page, role_name)
        role_row = page.locator("b-grid .tbl-row").filter(has_text=role_name).first
        expect(role_row).to_be_visible()
        expect(role_row).to_contain_text("Активный")

        page.locator("button").filter(has_text=re.compile(r"^\s*Закрыть\s*$", re.IGNORECASE)).first.click()
        expect(page).to_have_url(re.compile(r".*/template_list"))
        expect(page.locator("body")).to_contain_text("Шаблоны накладных")

    with allure.step("4 - User order listda Счет-фактуры custom template downloadini tekshiradi"):
        created_order_client = load_data("b_group_consignment_order_client") or f"natural_client-pw{code}"

        logout(page)
        authorization_user(page, code)

        flow_open_order_list(page)
        expect(page.locator("#kt_content")).to_contain_text(created_order_client, timeout=120_000)
        flow_order_list(page, find_row=created_order_client)

        invoice_button = page.locator("button:visible, a:visible").filter(
            has_text=re.compile(r"Счет-?фактуры", re.IGNORECASE)
        ).first
        expect(invoice_button).to_be_visible()
        invoice_button.click()

        dropdown = page.locator(".dropdown-menu:visible, .dropdown:visible").filter(has_text=template_name).first
        expect(dropdown).to_be_visible()
        expect(dropdown).to_contain_text(template_name)

        report_option = page.locator(".dropdown-menu:visible a, .dropdown-menu:visible span").filter(
            has_text=re.compile(rf"^\s*{re.escape(template_name)}\s*$")
        ).first
        expect(report_option).to_be_visible()
        with page.expect_download(timeout=60_000) as download_info:
            report_option.click()
        _save_downloaded_report(download_info.value)


@allure.title("B-04 - Custom invoice report template yaratish va orderda tekshirish")
def test_b_04_invoice_report_template(
    group_session_page: Page,
    code: str,
    load_data,
    test_scope,
) -> None:
    run_b_group_create_custom_invoice_report_template(
        group_session_page,
        code,
        load_data,
        scope=test_scope,
    )
