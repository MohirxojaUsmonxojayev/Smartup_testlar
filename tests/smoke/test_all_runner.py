import allure
import pytest

from tests.smoke.test_groups.test_A_grup.test_a_group_runner import run_a_group_chain
from tests.smoke.test_groups.test_B_grup.test_b_group_runner import run_b_group_chain
from tests.smoke.test_groups.test_C_grup.test_c_group_runner import run_c_group_chain
from tests.smoke.test_groups.test_report_grup.test_report_group_runner import run_report_group_chain
from tests.smoke.test_setup.test_setup_runner import run_setup_chain


@pytest.mark.user_setup
@allure.epic("Smoke")
@allure.feature("Setup Runner")
@allure.story("Setup Chain")
@allure.title("01 - User setup runner")
def test_01_user_setup_runner(session_page, code, save_data, load_data, logger, company_setup_enabled):
    run_setup_chain(session_page, code, save_data, logger,
                    load_data=load_data,
                    company_setup_enabled=company_setup_enabled)


@pytest.mark.smoke_group("A")
@allure.epic("A Group")
@allure.feature("A Group Runner")
@allure.story("Contract And Order")
@allure.title("02 - A group runner")
def test_02_a_group_runner(group_page, code, save_data, load_data, logger):
    run_a_group_chain(group_page, code, save_data, load_data)


@pytest.mark.smoke_group("B")
@allure.epic("B Group")
@allure.feature("B Group Runner")
@allure.story("Order Consignment")
@allure.title("03 - B group runner")
def test_03_b_group_runner(group_page, code, save_data, load_data, logger):
    run_b_group_chain(group_page, code, save_data, load_data)


@pytest.mark.smoke_group("C")
@allure.epic("C Group")
@allure.feature("C Group Runner")
@allure.story("Marketing Action")
@allure.title("04 - C group runner")
def test_04_c_group_runner(group_page, code, save_data, load_data, logger):
    run_c_group_chain(group_page, code, save_data, load_data)


@pytest.mark.smoke_group("Report", independent=True)
@allure.epic("Report Group")
@allure.feature("Report Group Runner")
@allure.story("Integration Reports")
@allure.title("05 - Report group runner")
def test_05_report_group_runner(group_page, code, save_data, load_data, logger):
    run_report_group_chain(group_page, code, save_data, load_data)
