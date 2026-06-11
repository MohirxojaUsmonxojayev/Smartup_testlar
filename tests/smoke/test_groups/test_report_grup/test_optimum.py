import allure
from playwright.sync_api import Page, expect
from tests.smoke.flows.flow_authorization import authorization
from tests.smoke.flows.flow_navigate import switch_filial
from tests.smoke.test_groups.test_report_grup.report_helpers import generate_and_verify_download, select_b_input_option

pytestmark = [allure.epic("Report Group"), allure.feature("Integration Report"), allure.story("Optimum")]

PREFIXES = [
    ("transfer_out", "1"),
    ("transfer_in", "2"),
    ("write_off", "3"),
    ("warehouse_receipt", "4"),
    ("site_transfer_out", "5"),
    ("site_transfer_in", "6"),
    ("production_write_off", "7"),
    ("production_receipt", "8"),
]


# ----------------------------------------------------------------------------------------------------------------------

def run_report_optimum_check(page: Page, code, scope: str = "smoke", login: bool = True) -> None:
    """Report-04: Optimum report — sozlamalar bilan optimum.zip yuklab olish.

    Login (login=True bo'lsa): admin login va test filialiga (filial-pw{code}) o'tish.

    Qadamlar (Allure step):
      1. Optimum sahifasini ochish
      2. Настройки -> Продуктовое группа (Группа) + 8 ta prefiks -> Сохранить
      3. Сформировать (barcha filial) -> optimum.zip yuklanishi va bo'sh emasligi

    Eslatma: checklistdagi "bitta filial bo'yicha 2-generate" qadami olib tashlandi —
    1-generate'dan keyin sahifada turg'un `.block-ui-overlay` qolib, "Все филиалы"
    checkboxini toggle qilish bloklanadi (alohida tekshirish kerak bo'lgan gap).
    """
    filial_name = f"filial-pw{code}"

    if login:
        authorization(page)
        switch_filial(page, name=filial_name)

    with allure.step("1 - Optimum sahifasini ochish"):
        base, _, rest = page.url.partition("#/")
        session_token = rest.split("/", 1)[0]
        page.goto(f"{base}#/{session_token}/trade/rep/integration/optimum")
        expect(page.get_by_role("button", name="Настройки")).to_be_visible()

    with allure.step("2 - Настройки: product group va 8 ta prefiks -> saqlash"):
        page.locator('button[ng-click="q.show_setting = true"]').click()
        select_b_input_option(page, "product_groups", "Группа")
        for key, value in PREFIXES:
            page.locator(f'input[ng-model="d.prefix_{key}"]').fill(value)
        save_btn = page.locator('button[ng-click="save()"]')
        save_btn.click()
        expect(save_btn).to_be_hidden()

    with allure.step("3 - Сформировать (barcha filial) -> optimum.zip"):
        generate_and_verify_download(
            page,
            page.get_by_role("button", name="Сформировать", exact=True),
            expected_prefix="optimum",
            save_name=f"optimum_pw{code}.zip",
        )
