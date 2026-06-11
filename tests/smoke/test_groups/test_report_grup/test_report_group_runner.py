import allure
import pytest
from playwright.sync_api import Page

from tests.smoke.flows.flow_authorization import authorization
from tests.smoke.flows.flow_navigate import switch_filial
from tests.smoke.progress import progress_step
from tests.smoke.test_groups.test_report_grup.test_cislink import run_report_cislink_check
from tests.smoke.test_groups.test_report_grup.test_integration_three import run_report_integration_three_check
from tests.smoke.test_groups.test_report_grup.test_saleswork import run_report_saleswork_check
from tests.smoke.test_groups.test_report_grup.test_optimum import run_report_optimum_check
from tests.smoke.test_groups.test_report_grup.test_spot import run_report_spot_check
from tests.smoke.test_groups.test_report_grup.test_integration_two import run_report_integration_two_check

pytestmark = [
    pytest.mark.smoke_group("Report", independent=True),
    allure.epic("Report Group"),
    allure.feature("Report Group Runner"),
    allure.story("Integration Reports"),
]

REPORT_GROUP_TEST_SCENARIO = """
Report Group test ssenariysi:
1. Admin login — Администрирование filialida (default).
2. CisLink: Настройки (identification code, Характеристики/Продуктовое направление=Группа, Тип цены=Price Type UZB-pw{code}),
   Сформировать -> cislink*.zip yuklanishi.
3. Integration №3 (NEON): Настройки saqlanib, begin_date kiritilib, Сформировать (HTML) ->
   iframe'da 3 ta sheet (sheet1/sheet2/sheet3) render bo'lishi.
4. SalesWork: yangi SalesWork-pw{code} shablon yaratib, Экспорт -> sales_work.zip yuklanishi.
5. Optimum: Настройки (Группа + 8 ta prefiks), Сформировать -> optimum.zip yuklanishi.
6. Spot 2d: yangi Spot2D-pw{code} shablon yaratib, Сформировать -> Spot2D.zip yuklanishi.
7. Integration Two (монолит): Настройки (Тип цены data_store'dan), 4 ta exchange rejimi
   (CRMOrder/CRMDespatch/CRMOrderStatus/CRMInput) -> har biri uchun .xml yuklanishi.
"""

REPORT_GROUP_RUNNER_TEST = "test_05_report_group_runner"


def run_report_group_chain(group_page: Page, code: str, save_data, load_data, scope: str = "smoke") -> None:
    """Report group chainni pytest test funksiyalarini chaqirmasdan bajaradi."""
    allure.dynamic.description(REPORT_GROUP_TEST_SCENARIO)
    with progress_step(
        group="Report group",
        runner=REPORT_GROUP_RUNNER_TEST,
        test_id="report_group_login",
        title="Report Group: admin login va filialga o'tish",
        display="Report Group login",
    ):
        authorization(group_page)  # ADMIN
        switch_filial(group_page, name=f"filial-pw{code}")
    with progress_step(
        group="Report group",
        runner=REPORT_GROUP_RUNNER_TEST,
        test_id="test_report_01_cislink",
        title="Report-01 - CisLink integration report yuklab olish",
    ):
        run_report_cislink_check(group_page, code, scope=scope, login=False)
    with progress_step(
        group="Report group",
        runner=REPORT_GROUP_RUNNER_TEST,
        test_id="test_report_02_integration_three",
        title="Report-02 - Integration №3 report (3 sheet)",
    ):
        run_report_integration_three_check(group_page, code, scope=scope, login=False)
    with progress_step(
        group="Report group",
        runner=REPORT_GROUP_RUNNER_TEST,
        test_id="test_report_03_saleswork",
        title="Report-03 - SalesWork report (sales_work.zip)",
    ):
        run_report_saleswork_check(group_page, code, scope=scope, login=False)
    with progress_step(
        group="Report group",
        runner=REPORT_GROUP_RUNNER_TEST,
        test_id="test_report_04_optimum",
        title="Report-04 - Optimum report (optimum.zip)",
    ):
        run_report_optimum_check(group_page, code, scope=scope, login=False)
    with progress_step(
        group="Report group",
        runner=REPORT_GROUP_RUNNER_TEST,
        test_id="test_report_05_spot",
        title="Report-05 - Spot 2d report (Spot2D.zip)",
    ):
        run_report_spot_check(group_page, code, scope=scope, login=False)
    with progress_step(
        group="Report group",
        runner=REPORT_GROUP_RUNNER_TEST,
        test_id="test_report_06_integration_two",
        title="Report-06 - Integration Two report (4 xml)",
    ):
        run_report_integration_two_check(group_page, code, load_data, scope=scope, login=False)


@allure.title("Report-01 - CisLink integration report")
def test_report_01_cislink(group_session_page: Page, code: str, test_scope) -> None:
    run_report_cislink_check(group_session_page, code, scope=test_scope, login=True)


@allure.title("Report-02 - Integration №3 report")
def test_report_02_integration_three(group_session_page: Page, code: str, test_scope) -> None:
    run_report_integration_three_check(group_session_page, code, scope=test_scope, login=True)


@allure.title("Report-03 - SalesWork report")
def test_report_03_saleswork(group_session_page: Page, code: str, test_scope) -> None:
    run_report_saleswork_check(group_session_page, code, scope=test_scope, login=True)


@allure.title("Report-04 - Optimum report")
def test_report_04_optimum(group_session_page: Page, code: str, test_scope) -> None:
    run_report_optimum_check(group_session_page, code, scope=test_scope, login=True)


@allure.title("Report-05 - Spot 2d report")
def test_report_05_spot(group_session_page: Page, code: str, test_scope) -> None:
    run_report_spot_check(group_session_page, code, scope=test_scope, login=True)


@allure.title("Report-06 - Integration Two report")
def test_report_06_integration_two(group_session_page: Page, code: str, load_data, test_scope) -> None:
    run_report_integration_two_check(group_session_page, code, load_data, scope=test_scope, login=True)
