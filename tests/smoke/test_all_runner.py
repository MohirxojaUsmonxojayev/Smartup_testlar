import allure
import pytest
from playwright.sync_api import Page

from tests.smoke.test_groups.test_A_grup.test_a_group_runner import run_a_group_chain
from tests.smoke.test_groups.test_B_grup.test_b_group_runner import run_b_group_chain
from tests.smoke.test_setup.test_setup_runner import run_setup_chain


@pytest.mark.user_setup
@allure.epic("Smoke")
@allure.feature("Setup Runner")
@allure.story("Setup Chain")
@allure.title("01 - User setup runner")
def test_01_user_setup_runner(
    session_page: Page,
    code: str,
    save_data,
    load_data,
    logger,
    test_scope,
    company_setup_enabled,
) -> None:
    run_setup_chain(
        session_page,
        code,
        save_data,
        logger,
        load_data=load_data,
        scope=test_scope,
        company_setup_enabled=company_setup_enabled,
    )


@pytest.mark.smoke_group("A")
@allure.epic("A Group")
@allure.feature("A Group Runner")
@allure.story("Contract And Order")
@allure.title("02 - A group runner")
def test_02_a_group_runner(group_page: Page, code: str, save_data, load_data, logger, test_scope) -> None:
    run_a_group_chain(group_page, code, save_data, load_data, scope=test_scope)


@pytest.mark.smoke_group("B")
@allure.epic("B Group")
@allure.feature("B Group Runner")
@allure.story("Order Consignment")
@allure.title("03 - B group runner")
def test_03_b_group_runner(group_page: Page, code: str, save_data, load_data, logger, test_scope) -> None:
    run_b_group_chain(group_page, code, save_data, load_data, scope=test_scope)
