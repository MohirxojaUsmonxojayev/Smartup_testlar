import allure
from playwright.sync_api import Page

from tests.smoke.test_groups.test_B_grup.test_order import (
    test_b_group_create_order_with_consignment_limit as run_create_order_with_consignment_limit,
    test_b_group_edit_order_with_consignment_limit as run_edit_order_with_consignment_limit,
)

pytestmark = [allure.epic("B Group"), allure.feature("B Group Runner"), allure.story("Order Consignment")]


@allure.title("B-01 - Konsignatsiya limiti bilan zakaz yaratish")
def test_b_01_create_order_with_consignment_limit(session_page: Page, code: str, save_data) -> None:
    run_create_order_with_consignment_limit(session_page, code, save_data)


@allure.title("B-02 - Konsignatsiyali zakazni edit qilish va split qilish")
def test_b_02_edit_order_with_consignment_limit(
    session_page: Page,
    code: str,
    load_data,
    save_data,
) -> None:
    run_edit_order_with_consignment_limit(session_page, code, load_data, save_data)
