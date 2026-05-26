import random

import allure
from faker import Faker
from playwright.sync_api import Page, expect

from tests.smoke.flows.flow_authorization import authorization_user
from tests.smoke.flows.flow_contract.flow_contract_add import (
    flow_contract_add_page,
    flow_contract_assert_list_row,
    flow_contract_assert_view,
    flow_contract_close_view,
    flow_contract_save,
)
from tests.smoke.flows.flow_contract.flow_contract_list import flow_contract_list, flow_open_contract_list

pytestmark = [allure.epic("A Group"), allure.feature("Order Preconditions"), allure.story("Contract")]


@allure.title("A Group: Zakaz uchun UZS contract yaratish")
def test_a_group_create_order_contract(page: Page, code: str, save_data) -> None:
    """
    Testcase:
    1. User sifatida tizimga kirish.
    2. Finans > Dоговоры ro'yxatini ochish.
    3. Zakaz uchun yangi contract yaratish formasini ochish.
    4. Contract code, raqami, nomi, jismoniy shaxs mijoz, valyuta va summa maydonlarini to'ldirish.
    5. Contractni saqlash va ro'yxatda yaratilgan recordni contract code orqali topish.
    6. Contract view oynasini ochib zakaz uchun kerakli asosiy qiymatlarni tekshirish.
    7. Contract code va contract name qiymatlarini keyingi A-group/order testlari uchun data_store.json ga saqlash.
    """
    contract_code = f"contract_code_{random.randint(1000, 9999)}"

    with allure.step("1 - User tizimga muvaffaqiyatli kiradi"):
        authorization_user(page, code)
        expect(page.get_by_role("heading", name="Trade")).to_be_visible()

    with allure.step("2 - Finans > Dоговоры ro'yxati ochiladi"):
        flow_open_contract_list(page)

    with allure.step("3 - Zakaz uchun contract yaratish formasi ochiladi"):
        flow_contract_list(page, add=True)

    with allure.step("4 - Contract asosiy maydonlari to'ldiriladi"):
        contract_name = f"{Faker('ru_RU').company()} order contract-pw{code}"
        flow_contract_add_page(page, code, contract_code, contract_name)

    with allure.step("5 - Contract saqlanadi va ro'yxatga qaytadi"):
        flow_contract_save(page)

    with allure.step("6 - Yaratilgan contract ro'yxatda contract code orqali topiladi"):
        flow_contract_list(page, find_code=contract_code)
        flow_contract_assert_list_row(page, code, contract_code, contract_name)

    with allure.step("7 - Contract view oynasi ochiladi va asosiy qiymatlar tekshiriladi"):
        flow_contract_list(page, view=True)
        flow_contract_assert_view(page, code, contract_code, contract_name)

    with allure.step("8 - View oynasi yopiladi va contract ro'yxatiga qaytiladi"):
        flow_contract_close_view(page)

    with allure.step("9 - Contract code va name keyingi A-group/order testlari uchun saqlanadi"):
        save_data("contract_code", contract_code)
        save_data("contract_name", contract_name)


@allure.title("A Group: Tip oplati sharti bilan zakaz contract yaratish")
def test_a_group_create_order_contract_with_payment_type(page: Page, code: str, save_data) -> None:
    """
    Testcase:
    1. User sifatida tizimga kirish.
    2. Finans > Dоговоры ro'yxatini ochish.
    3. Yangi contract yaratish formasini ochish.
    4. Contract asosiy maydonlarini to'ldirib, Типы оплат = Перечисление qilib belgilash.
    5. Contractni saqlash va ro'yxatda contract code orqali topish.
    6. Contract view oynasida Типы оплат va asosiy qiymatlar ko'rinishini tekshirish.
    7. Contract code, name va payment type qiymatlarini keyingi order testi uchun data_store.json ga saqlash.
    """
    contract_code = f"contract_payment_type_{random.randint(1000, 9999)}"

    with allure.step("1 - User tizimga muvaffaqiyatli kiradi"):
        authorization_user(page, code)
        expect(page.get_by_role("heading", name="Trade")).to_be_visible()

    with allure.step("2 - Finans > Договоры ro'yxati ochiladi"):
        flow_open_contract_list(page)

    with allure.step("3 - Tip oplati sharti uchun contract yaratish formasi ochiladi"):
        flow_contract_list(page, add=True)

    with allure.step("4 - Contract Типы оплат = Перечисление bilan to'ldiriladi"):
        contract_name = f"{Faker('ru_RU').company()} payment type contract-pw{code}"
        flow_contract_add_page(
            page,
            code,
            contract_code,
            contract_name,
            payment_type="Перечисление",
        )

    with allure.step("5 - Contract saqlanadi va ro'yxatda topiladi"):
        flow_contract_save(page)
        flow_contract_list(page, find_code=contract_code)
        flow_contract_assert_list_row(
            page,
            code,
            contract_code,
            contract_name,
        )

    with allure.step("6 - Contract view oynasida Типы оплат tekshiriladi"):
        flow_contract_list(page, view=True)
        flow_contract_assert_view(
            page,
            code,
            contract_code,
            contract_name,
            payment_type="Перечисление",
        )
        flow_contract_close_view(page)

    with allure.step("7 - Tip oplati contract ma'lumotlari saqlanadi"):
        save_data("contract_payment_type_code", contract_code)
        save_data("contract_payment_type_name", contract_name)
        save_data("contract_payment_type", "Перечисление")
