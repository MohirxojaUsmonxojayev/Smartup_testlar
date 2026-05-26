import allure
from playwright.sync_api import Page

from tests.smoke.test_groups.test_A_grup.test_contract import (
    test_a_group_create_order_contract as run_create_order_contract,
    test_a_group_create_order_contract_with_payment_type as run_create_order_contract_with_payment_type,
)
from tests.smoke.test_groups.test_A_grup.test_order import (
    test_a_group_contract_limit_validation_and_valid_order as run_contract_limit_validation_and_valid_order,
    test_a_group_order_uses_contract_payment_type as run_order_uses_contract_payment_type,
)

pytestmark = [allure.epic("A Group"), allure.feature("A Group Runner"), allure.story("Contract And Order")]


@allure.title("A-01 - Zakaz uchun UZS contract yaratish")
def test_a_01_create_order_contract(session_page: Page, code: str, save_data) -> None:
    run_create_order_contract(session_page, code, save_data)


@allure.title("A-02 - Tip oplati sharti bilan zakaz contract yaratish")
def test_a_02_create_order_contract_with_payment_type(session_page: Page, code: str, save_data) -> None:
    run_create_order_contract_with_payment_type(session_page, code, save_data)


@allure.title("A-03 - Contract limit tekshiruvi va limit ichida zakaz yaratish")
def test_a_03_contract_limit_validation_and_valid_order(
    session_page: Page,
    code: str,
    load_data,
    save_data,
) -> None:
    run_contract_limit_validation_and_valid_order(session_page, code, load_data, save_data)


@allure.title("A-04 - Contract tip oplati auto-fill va limit tekshiruvi")
def test_a_04_order_uses_contract_payment_type(
    session_page: Page,
    code: str,
    load_data,
    save_data,
) -> None:
    run_order_uses_contract_payment_type(session_page, code, load_data, save_data)
