import allure
import pytest
from playwright.sync_api import Page, expect

from tests.smoke.flows.flow_authorization import authorization_user
from tests.smoke.test_groups.test_A_grup.test_contract import (
    run_a_group_create_order_contract,
    run_a_group_create_order_contract_with_payment_type,
)
from tests.smoke.test_groups.test_A_grup.test_order import (
    run_a_group_contract_limit_validation_and_valid_order,
    run_a_group_edit_order_and_save_as_new,
    run_a_group_order_uses_contract_payment_type,
)

pytestmark = [
    pytest.mark.smoke_group("A"),
    allure.epic("A Group"),
    allure.feature("A Group Runner"),
    allure.story("Contract And Order"),
]

A_GROUP_TEST_SCENARIO = """
A Group test ssenariysi:
1. User group boshida bir marta login qiladi va A-group tugaguncha shu oynada ishlaydi.
2. Zakaz uchun UZS contract yaratiladi va list/viewda tekshiriladi.
3. Типы оплат = Перечисление sharti bilan ikkinchi contract yaratiladi va viewda tekshiriladi.
4. Contract limitidan oshgan 700 000 summali order save bo'lmasligi tekshiriladi.
5. Limit ichida 7 000 summali order yaratiladi va viewda contract, client, product, payment type, status tekshiriladi.
6. Типы оплат contracti order final sahifasida payment typeni auto-fill qilishi tekshiriladi.
7. Payment type user tomonidan Наличные деньги ga o'zgartirilganda order saqlanishi tekshiriladi.
8. Yaratilgan order edit qilinadi, ko'rinib turgan qiymatlar tekshiriladi va status Новый qilib saqlanadi.
"""


def run_a_group_chain(group_page: Page, code: str, save_data, load_data, scope: str = "smoke") -> None:
    """A group chainni pytest test funksiyalarini chaqirmasdan bajaradi."""
    allure.dynamic.description(A_GROUP_TEST_SCENARIO)
    with allure.step("A Group: user bir marta login qiladi"):
        authorization_user(group_page, code)
        expect(group_page.get_by_role("heading", name="Trade")).to_be_visible()
    with allure.step("A-01 - Zakaz uchun UZS contract yaratish"):
        run_a_group_create_order_contract(group_page, code, save_data, scope=scope, login=False)
    with allure.step("A-02 - Tip oplati sharti bilan zakaz contract yaratish"):
        run_a_group_create_order_contract_with_payment_type(group_page, code, save_data, scope=scope, login=False)
    with allure.step("A-03 - Contract limit tekshiruvi va limit ichida zakaz yaratish"):
        run_a_group_contract_limit_validation_and_valid_order(group_page, code, load_data, save_data, scope=scope, login=False)
    with allure.step("A-04 - Contract tip oplati auto-fill va limit tekshiruvi"):
        run_a_group_order_uses_contract_payment_type(group_page, code, load_data, save_data, scope=scope, login=False)
    with allure.step("A-05 - Order editda statusni Новый qilib saqlash"):
        run_a_group_edit_order_and_save_as_new(group_page, code, load_data, scope=scope, login=False)


@allure.title("A-01 - Zakaz uchun UZS contract yaratish")
def test_a_01_create_order_contract(group_user_page: Page, code: str, save_data, test_scope) -> None:
    run_a_group_create_order_contract(group_user_page, code, save_data, scope=test_scope, login=False)


@allure.title("A-02 - Tip oplati sharti bilan zakaz contract yaratish")
def test_a_02_create_order_contract_with_payment_type(group_user_page: Page, code: str, save_data, test_scope) -> None:
    run_a_group_create_order_contract_with_payment_type(group_user_page, code, save_data, scope=test_scope, login=False)


@allure.title("A-03 - Contract limit tekshiruvi va limit ichida zakaz yaratish")
def test_a_03_contract_limit_validation_and_valid_order(
    group_user_page: Page,
    code: str,
    load_data,
    save_data,
    test_scope,
) -> None:
    run_a_group_contract_limit_validation_and_valid_order(group_user_page, code, load_data, save_data, scope=test_scope, login=False)


@allure.title("A-04 - Contract tip oplati auto-fill va limit tekshiruvi")
def test_a_04_order_uses_contract_payment_type(
    group_user_page: Page,
    code: str,
    load_data,
    save_data,
    test_scope,
) -> None:
    run_a_group_order_uses_contract_payment_type(group_user_page, code, load_data, save_data, scope=test_scope, login=False)


@allure.title("A-05 - Order editda statusni Новый qilib saqlash")
def test_a_05_edit_order_and_save_as_new(
    group_user_page: Page,
    code: str,
    load_data,
    test_scope,
) -> None:
    run_a_group_edit_order_and_save_as_new(group_user_page, code, load_data, scope=test_scope, login=False)
