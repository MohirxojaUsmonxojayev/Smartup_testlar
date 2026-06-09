import allure
import pytest
from playwright.sync_api import Page

from tests.smoke.test_groups.test_B_grup.order_helpers import (
    run_b_group_order_invoice_reports,
)

pytestmark = [
    pytest.mark.smoke_group("B"),
    allure.epic("B Group"),
    allure.feature("Order Consignment"),
    allure.story("B-03 Invoice Reports"),
]


@allure.title("B-03 - Draft zakaz Накладные reportlarini tekshirish")
def test_b_03_order_invoice_reports(
    group_user_page: Page,
    code: str,
    load_data,
    test_scope,
) -> None:
    run_b_group_order_invoice_reports(group_user_page, code, load_data, scope=test_scope)
