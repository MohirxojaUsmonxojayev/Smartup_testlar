import allure
import pytest

from tests.smoke.test_groups.test_B_grup.order_helpers import (
    run_b_group_create_order_with_consignment_limit,
)

pytestmark = [
    pytest.mark.smoke_group("B"),
    allure.epic("B Group"),
    allure.feature("Order Consignment"),
    allure.story("B-01 Create Order"),
]


@allure.title("B-01 - Konsignatsiya limiti bilan zakaz yaratish")
def test_b_01_create_order_with_consignment_limit(
    group_user_page,
    code,
    save_data,
):
    run_b_group_create_order_with_consignment_limit(
        group_user_page,
        code,
        save_data,
        login=False,
    )
