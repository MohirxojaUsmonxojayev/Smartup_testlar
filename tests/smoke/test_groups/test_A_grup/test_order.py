import re

import allure
from playwright.sync_api import Page, expect

from tests.smoke.flows.flow_authorization import authorization_user
from tests.smoke.flows.flow_order.flow_order_add import (
    flow_order_final_page,
    flow_order_prepare_with_contract,
)
from tests.smoke.flows.flow_order.flow_order_list import flow_open_order_list, flow_order_list
from utils.base_page import BasePage

pytestmark = [allure.epic("A Group"), allure.feature("Order"), allure.story("Order With Contract")]


@allure.title("A Group: Contract limit tekshiruvi va limit ichida zakaz yaratish")
def test_a_group_contract_limit_validation_and_valid_order(page: Page, code: str, load_data, save_data) -> None:
    """
    Testcase:
    1. User sifatida tizimga kirish.
    2. A-group contract testida yaratilgan contract name qiymatini data_store.json dan olish.
    3. Order listdagi oldin yaratilgan orderlarni Отменен statusga o'tkazib, product bookingni tozalash.
    4. Contract bilan 700000 summali zakaz yaratib, limit error xabarini tekshirish.
    5. Limitdan oshgan zakaz saqlanmay, order add formasida qolganini tekshirish.
    6. Order listga qaytib, shu contract bilan 1 ta mahsulotli zakaz yaratish.
    7. 7000 summali zakaz muvaffaqiyatli saqlanishini tekshirish.
    8. Zakaz listda ko'rinishini va view oynasida contract, client, summa, product ko'ringanini tekshirish.
    9. Order id qiymatini keyingi A-group testlari uchun data_store.json ga saqlash.
    """

    with allure.step("1 - User tizimga muvaffaqiyatli kiradi"):
        authorization_user(page, code)
        expect(page.get_by_role("heading", name="Trade")).to_be_visible()

    with allure.step("2 - A-group contract name data_store.json dan olinadi"):
        contract_name = load_data("contract_name")
        if not contract_name:
            raise AssertionError("A-group contract_name topilmadi. Avval test_contract.py ni run qiling.")

    with allure.step("3 - Eski orderlar Отменен statusga o'tkazilib, product booking tozalanadi"):
        flow_open_order_list(page)
        expect(page.locator("b-grid")).to_contain_text("Статус")
        for _ in range(10):
            if page.locator("b-grid .tbl-row").filter(has_text=f"natural_client-pw{code}").count() == 0:
                break
            flow_order_list(page, find_row=f"natural_client-pw{code}", status="Отменен")
            flow_open_order_list(page)
            expect(page.locator("b-grid")).to_contain_text("Статус")

    with allure.step("4 - Contract bilan 700000 summali zakaz tayyorlanadi"):
        flow_order_prepare_with_contract(
            page,
            code,
            contract_name,
            quantity="100",
            payment_type="Наличные деньги",
            status="Черновик",
            contract_balance_text="500 000",
        )
        expect(page.locator("#kt_content")).to_contain_text("ИТОГО")
        expect(page.locator("#kt_content")).to_contain_text("700 000")
        expect(page.locator("#kt_content")).to_contain_text(contract_name)
        expect(page.locator("#kt_content")).to_contain_text("Наличные деньги")
        expect(page.locator("#kt_content")).to_contain_text("Черновик")

    with allure.step("5 - Contract limitidan oshgani uchun save xabari chiqadi"):
        page.get_by_role("button", name="Сохранить").click()
        expect(page.locator("#biruniConfirm")).to_contain_text("Сохранить?")
        expect(page.locator("#biruniConfirm")).to_have_css("opacity", "1")
        page.locator("#biruniConfirm").get_by_role("button", name="да").click()
        page.locator("#biruniConfirm").wait_for(state="hidden")
        expect(page.locator("body")).to_contain_text("Сумма заказа превышает сумму остатка по договору")
        expect(page.locator("body")).to_contain_text(re.compile(r"Сумма остатка по договору: \d+"))
        expect(page.locator("body")).to_contain_text("сумма заказа = 700000")
        expect(page).to_have_url(re.compile(r".*/order\+add"))
        expect(page.locator("#kt_content")).to_contain_text("Заказ (создание)")
        BasePage(page).close_extended_alert()

    with allure.step("6 - Order listga qaytib, contract bilan 1 ta mahsulotli zakaz tayyorlanadi"):
        flow_open_order_list(page)
        flow_order_prepare_with_contract(
            page,
            code,
            contract_name,
            quantity="1",
            payment_type="Наличные деньги",
            status="Черновик",
            contract_balance_text="500 000",
        )
        expect(page.locator("#kt_content")).to_contain_text("ИТОГО")
        expect(page.locator("#kt_content")).to_contain_text("7 000")
        expect(page.locator("#kt_content")).to_contain_text(contract_name)

    with allure.step("7 - 7000 summali zakaz muvaffaqiyatli saqlanadi"):
        page.get_by_role("button", name="Сохранить").click()
        expect(page.locator("#biruniConfirm")).to_contain_text("Сохранить?")
        expect(page.locator("#biruniConfirm")).to_have_css("opacity", "1")
        page.locator("#biruniConfirm").get_by_role("button", name="да").click()
        page.locator("#biruniConfirm").wait_for(state="hidden")
        expect(page).to_have_url(re.compile(r".*/order_list"))
        expect(page.get_by_role("heading")).to_contain_text("Заказы")

    with allure.step("8 - Zakaz list va view oynasida contract bilan tekshiriladi"):
        expect(page.locator("b-grid")).to_contain_text("7 000")
        page.locator("b-grid").get_by_text("7 000").first.click()
        expect(page.get_by_role("button", name="Просмотреть", exact=True)).to_be_visible()
        page.get_by_role("button", name="Просмотреть", exact=True).click()
        expect(page).to_have_url(re.compile(r".*/order_view"))
        BasePage(page).wait_for_loader()
        expect(page.locator("#kt_content")).to_contain_text(f"natural_client-pw{code}")
        expect(page.locator("#kt_content")).to_contain_text(contract_name)
        expect(page.locator("#kt_content")).to_contain_text("Наличные деньги")
        expect(page.locator("#kt_content")).to_contain_text("Черновик")
        expect(page.locator("#kt_content")).to_contain_text(f"product-pw{code}")
        expect(page.locator("#kt_content")).to_contain_text("7 000")

    with allure.step("9 - Order id keyingi A-group testlari uchun saqlanadi"):
        save_data("a_group_order_id", page.locator('//t[contains(text(),"ИД заказа")]/../../span').inner_text().strip())
        page.get_by_role("button", name="Закрыть").click()
        expect(page).to_have_url(re.compile(r".*/order_list"))


@allure.title("A Group: Contract tip oplati auto-fill va limit tekshiruvi")
def test_a_group_order_uses_contract_payment_type(page: Page, code: str, load_data, save_data) -> None:
    """
    Testcase:
    1. User sifatida tizimga kirish.
    2. Типы оплат = Перечисление bilan yaratilgan contract ma'lumotlarini data_store.json dan olish.
    3. Order listdagi oldin yaratilgan orderlarni Отменен statusga o'tkazib, product bookingni tozalash.
    4. Shu contract bilan 700000 summali zakaz yaratib, contract limit error xabarini tekshirish.
    5. Shu contract bilan 1 ta mahsulotli zakaz yaratib, Тип оплаты avtomatik Перечисление bo'lib kelganini tekshirish.
    6. User Тип оплаты qiymatini Наличные деньги ga o'zgartira olishini va order saqlanishini tekshirish.
    7. Zakaz view oynasida contract, o'zgartirilgan payment type, client, product va summa ko'ringanini tekshirish.
    8. Order id qiymatini keyingi A-group testlari uchun data_store.json ga saqlash.
    """

    with allure.step("1 - User tizimga muvaffaqiyatli kiradi"):
        authorization_user(page, code)
        expect(page.get_by_role("heading", name="Trade")).to_be_visible()

    with allure.step("2 - Tip oplati contract ma'lumotlari data_store.json dan olinadi"):
        contract_name = load_data("contract_payment_type_name")
        contract_payment_type = load_data("contract_payment_type")
        if not contract_name or not contract_payment_type:
            raise AssertionError(
                "Tip oplati contract ma'lumotlari topilmadi. Avval "
                "test_a_group_create_order_contract_with_payment_type ni run qiling."
            )

    with allure.step("3 - Eski orderlar Отменен statusga o'tkazilib, product booking tozalanadi"):
        flow_open_order_list(page)
        expect(page.locator("b-grid")).to_contain_text("Статус")
        for _ in range(10):
            if page.locator("b-grid .tbl-row").filter(has_text=f"natural_client-pw{code}").count() == 0:
                break
            flow_order_list(page, find_row=f"natural_client-pw{code}", status="Отменен")
            flow_open_order_list(page)
            expect(page.locator("b-grid")).to_contain_text("Статус")

    with allure.step("4 - Tip oplati contract bilan 700000 summali zakaz error beradi"):
        flow_order_prepare_with_contract(
            page,
            code,
            contract_name,
            quantity="100",
            contract_balance_text="500 000",
        )
        expect(page.locator("#kt_content")).to_contain_text("ИТОГО")
        expect(page.locator("#kt_content")).to_contain_text("700 000")
        expect(page.locator("#kt_content")).to_contain_text(contract_name)
        BasePage(page).expect_b_input_value_by_label("Тип оплаты", contract_payment_type)

        page.get_by_role("button", name="Сохранить").click()
        expect(page.locator("#biruniConfirm")).to_contain_text("Сохранить?")
        expect(page.locator("#biruniConfirm")).to_have_css("opacity", "1")
        page.locator("#biruniConfirm").get_by_role("button", name="да").click()
        page.locator("#biruniConfirm").wait_for(state="hidden")
        expect(page.locator("body")).to_contain_text("Сумма заказа превышает сумму остатка по договору")
        expect(page.locator("body")).to_contain_text(re.compile(r"Сумма остатка по договору: \d+"))
        expect(page.locator("body")).to_contain_text("сумма заказа = 700000")
        expect(page).to_have_url(re.compile(r".*/order\+add"))
        BasePage(page).close_extended_alert()

    with allure.step("5 - Tip oplati contract bilan 1 ta mahsulotli zakaz tayyorlanadi"):
        flow_open_order_list(page)
        flow_order_prepare_with_contract(
            page,
            code,
            contract_name,
            quantity="1",
            contract_balance_text="500 000",
        )
        expect(page.locator("#kt_content")).to_contain_text("ИТОГО")
        expect(page.locator("#kt_content")).to_contain_text("7 000")
        expect(page.locator("#kt_content")).to_contain_text(contract_name)

    with allure.step("6 - Contractdagi Типы оплат auto-fill bo'ladi va user uni o'zgartira oladi"):
        BasePage(page).expect_b_input_value_by_label("Тип оплаты", contract_payment_type)
        BasePage(page).select_b_input_by_label("Тип оплаты", "Наличные деньги", clear=True)
        BasePage(page).expect_b_input_value_by_label("Тип оплаты", "Наличные деньги")

    with allure.step("7 - O'zgartirilgan tip oplati bilan zakaz muvaffaqiyatli saqlanadi"):
        flow_order_final_page(
            page,
            status="Черновик",
            save=True,
        )
        expect(page).to_have_url(re.compile(r".*/order_list"))
        expect(page.get_by_role("heading")).to_contain_text("Заказы")

    with allure.step("8 - Zakaz view oynasida contract va o'zgartirilgan tip oplati tekshiriladi"):
        expect(page.locator("b-grid")).to_contain_text("7 000")
        page.locator("b-grid").get_by_text("7 000").first.click()
        expect(page.get_by_role("button", name="Просмотреть", exact=True)).to_be_visible()
        page.get_by_role("button", name="Просмотреть", exact=True).click()
        expect(page).to_have_url(re.compile(r".*/order_view"))
        BasePage(page).wait_for_loader()
        expect(page.locator("#kt_content")).to_contain_text(f"natural_client-pw{code}")
        expect(page.locator("#kt_content")).to_contain_text(contract_name)
        expect(page.locator("#kt_content")).to_contain_text("Наличные деньги")
        expect(page.locator("#kt_content")).to_contain_text("Черновик")
        expect(page.locator("#kt_content")).to_contain_text(f"product-pw{code}")
        expect(page.locator("#kt_content")).to_contain_text("7 000")

    with allure.step("9 - Tip oplati order id keyingi A-group testlari uchun saqlanadi"):
        save_data("a_group_payment_type_order_id", page.locator('//t[contains(text(),"ИД заказа")]/../../span').inner_text().strip())
        page.get_by_role("button", name="Закрыть").click()
        expect(page).to_have_url(re.compile(r".*/order_list"))
