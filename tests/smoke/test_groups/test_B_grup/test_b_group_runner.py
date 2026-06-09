import allure
import pytest
from playwright.sync_api import Page, expect

from tests.smoke.flows.flow_authorization import authorization_user
from tests.smoke.progress import progress_step
from tests.smoke.test_groups.test_B_grup.test_b_04_invoice_report_template import (
    run_b_group_create_custom_invoice_report_template,
)
from tests.smoke.test_groups.test_B_grup.order_helpers import (
    run_b_group_create_order_with_consignment_limit,
    run_b_group_edit_order_with_consignment_limit,
    run_b_group_order_invoice_reports,
)

pytestmark = [
    pytest.mark.smoke_group("B"),
    allure.epic("B Group"),
    allure.feature("B Group Runner"),
    allure.story("Order Consignment"),
]

B_GROUP_TEST_SCENARIO = """
B Group test ssenariysi:
1. User group boshida bir marta login qiladi va B-group tugaguncha shu oynada ishlaydi.
2. Order settingsda konsignatsiya yoqiladi va limit 30 kun qilib saqlanadi.
3. Mavjud active orderlar bo'lsa Отменен statusga o'tkazilib, product booking tozalanadi.
4. Konsignatsiya limiti bilan 5 dona productdan order yaratiladi.
5. Final sahifada konsignatsiya date/amount, payment type va status to'ldirilib order saqlanadi.
6. Order viewda asosiy qiymatlar va Консигнация tabidagi date/summa tekshiriladi.
7. Shu order edit qilinib quantity 5 dan 4 ga kamaytiriladi.
8. Eski konsignatsiya summasi totaldan katta bo'lganda error va clear bo'lishi tekshiriladi.
9. 30 kundan katta konsignatsiya sanasi save confirm ochmasligi tekshiriladi.
10. Konsignatsiya ikkita sanaga 14 000 + 14 000 qilib bo'linadi va viewda tekshiriladi.
11. Editdan keyin draft order listda qolgan holatda Накладные dropdown optionlari tekshiriladi.
12. Накладные reportlari B-group order datasi bilan ochilishi tekshiriladi.
13. Admin bilan custom invoice report template yaratiladi, Админ rolega attach qilinadi va order listda tekshiriladi.
"""

B_GROUP_RUNNER_TEST = "test_03_b_group_runner"


def run_b_group_chain(group_page: Page, code: str, save_data, load_data, scope: str = "smoke") -> None:
    """B group chainni pytest test funksiyalarini chaqirmasdan bajaradi."""
    allure.dynamic.description(B_GROUP_TEST_SCENARIO)
    with progress_step(
        group="B group",
        runner=B_GROUP_RUNNER_TEST,
        test_id="b_group_login",
        title="B Group: user bir marta login qiladi",
        display="B Group login",
    ):
        authorization_user(group_page, code)
        expect(group_page.get_by_role("heading", name="Trade")).to_be_visible()
    with progress_step(
        group="B group",
        runner=B_GROUP_RUNNER_TEST,
        test_id="test_b_01_create_order_with_consignment_limit",
        title="B-01 - Konsignatsiya limiti bilan zakaz yaratish",
    ):
        run_b_group_create_order_with_consignment_limit(group_page, code, save_data, scope=scope, login=False)
    with progress_step(
        group="B group",
        runner=B_GROUP_RUNNER_TEST,
        test_id="test_b_02_edit_order_with_consignment_limit",
        title="B-02 - Konsignatsiyali zakazni edit qilish va split qilish",
    ):
        run_b_group_edit_order_with_consignment_limit(group_page, code, load_data, save_data, scope=scope, login=False)
    with progress_step(
        group="B group",
        runner=B_GROUP_RUNNER_TEST,
        test_id="test_b_03_order_invoice_reports",
        title="B-03 - Draft zakaz Накладные reportlarini tekshirish",
    ):
        run_b_group_order_invoice_reports(group_page, code, load_data, scope=scope)
    with progress_step(
        group="B group",
        runner=B_GROUP_RUNNER_TEST,
        test_id="test_b_04_invoice_report_template",
        title="B-04 - Custom invoice report template yaratish va orderda tekshirish",
    ):
        run_b_group_create_custom_invoice_report_template(group_page, code, load_data, scope=scope)


@allure.title("B Group runner")
def test_b_group_runner(group_session_page: Page, code: str, save_data, load_data, test_scope) -> None:
    run_b_group_chain(group_session_page, code, save_data, load_data, scope=test_scope)
