import allure
import pytest

from tests.smoke.test_groups.test_B_grup.order_helpers import (
    run_b_group_edit_order_with_consignment_limit,
)

pytestmark = [
    pytest.mark.smoke_group("B"),
    allure.epic("B Group"),
    allure.feature("Order Consignment"),
    allure.story("B-02 Edit Order"),
]


@allure.title("B-02 - Konsignatsiyali zakazni edit qilish va split qilish")
def test_b_02_edit_order_with_consignment_limit(
    group_user_page,
    code,
    load_data,
    save_data,
):
    run_b_group_edit_order_with_consignment_limit(
        group_user_page,
        code,
        load_data,
        save_data,
        login=False,
    )
