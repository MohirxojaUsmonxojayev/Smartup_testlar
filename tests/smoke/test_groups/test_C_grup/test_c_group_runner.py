import allure
import pytest
from playwright.sync_api import Page, expect

from tests.smoke.flows.flow_authorization import authorization_user
from tests.smoke.progress import progress_step
from tests.smoke.test_groups.test_C_grup.test_action import (
    run_c_group_create_action,
    run_c_group_order_action_discount,
)

pytestmark = [
    pytest.mark.smoke_group("C"),
    allure.epic("C Group"),
    allure.feature("C Group Runner"),
    allure.story("Marketing Action"),
]

C_GROUP_TEST_SCENARIO = """
C Group test ssenariysi:
1. User group boshida bir marta login qiladi va C-group tugaguncha shu oynada ishlaydi.
2. Справочники -> Маркетинг -> Акции da "10 dona olinganda 10% chegirma" aksiyasi yaratiladi
   (shart producti product-pw{code}, bonus 10% skidka).
3. Aksiya ro'yxatda nomi va "Активный" statusi bilan ko'rinishi tekshiriladi.
4. Order yaratilib, product-pw{code} 10 dona tanlanadi va "Акции" tabida aksiya bonusi yoqiladi.
5. Товар va final sahifada chegirma (-7 000) va ИТОГО 63 000 (70 000 dan 10%) tekshiriladi.
6. Order saqlanib, view oynasida ham chegirma va 63 000 ko'rinishi tekshiriladi.
"""

C_GROUP_RUNNER_TEST = "test_04_c_group_runner"


def run_c_group_chain(group_page: Page, code: str, save_data, load_data, scope: str = "smoke") -> None:
    """C group chainni pytest test funksiyalarini chaqirmasdan bajaradi."""
    allure.dynamic.description(C_GROUP_TEST_SCENARIO)
    with progress_step(
        group="C group",
        runner=C_GROUP_RUNNER_TEST,
        test_id="c_group_login",
        title="C Group: user bir marta login qiladi",
        display="C Group login",
    ):
        authorization_user(group_page, code)
        expect(group_page.get_by_role("heading", name="Trade")).to_be_visible()
    with progress_step(
        group="C group",
        runner=C_GROUP_RUNNER_TEST,
        test_id="test_c_01_create_action",
        title="C-01 - Aksiya (Скидка 10%) yaratish",
    ):
        run_c_group_create_action(group_page, code, scope=scope, login=False)
    with progress_step(
        group="C group",
        runner=C_GROUP_RUNNER_TEST,
        test_id="test_c_02_order_action_discount",
        title="C-02 - Orderda aksiya chegirmasini tekshirish",
    ):
        run_c_group_order_action_discount(group_page, code, scope=scope, login=False)


@allure.title("C-01 - Aksiya (Скидка 10%) yaratish")
def test_c_01_create_action(group_user_page: Page, code: str, test_scope) -> None:
    run_c_group_create_action(group_user_page, code, scope=test_scope, login=False)


@allure.title("C-02 - Orderda aksiya chegirmasini tekshirish")
def test_c_02_order_action_discount(group_user_page: Page, code: str, test_scope) -> None:
    run_c_group_order_action_discount(group_user_page, code, scope=test_scope, login=False)
