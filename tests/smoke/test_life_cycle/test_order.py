import allure
from datetime import datetime
from tests.smoke.flows.flow_navigate import navigate_to
from tests.smoke.flows.flow_authorization import authorization_user
from tests.smoke.flows.flow_order.flow_order_add import flow_order_main_page, flow_order_product_page, flow_order_final_page
from tests.smoke.flows.flow_order.flow_order_list import flow_order_list, flow_order_list_grid_setting
from tests.smoke.flows.flow_order.flow_order_view import flow_order_view

pytestmark = [allure.epic("Smoke"), allure.feature("Life Cycle"), allure.story("Order")]

# ----------------------------------------------------------------------------------------------------------------------

@allure.title("Order Basic")
def test_order_basic(page, code, save_data) -> None:
    authorization_user(page, code)

    with allure.step("Navigate To: Order Page"):
        navigate_to(page,
                    tab="Продажа",
                    name="Заказы")

    with allure.step("Order List: Add Button"):
        flow_order_list(page, add=True)

    with allure.step("Order Add: Main Page"):
        deal_time =  datetime.now().strftime("%d.%m.%Y %H:%M")
        delivery_date = datetime.now().strftime("%d.%m.%Y")
        flow_order_main_page(page,
                             check_form=True,
                             deal_time=deal_time,
                             delivery_date=delivery_date,
                             room=f"room-pw{code}",
                             robot=f"robot-pw{code}",
                             natural_client=f"natural_client-pw{code}",
                             next_page=True)

    with allure.step("Order Add: Product Page"):
        flow_order_product_page(page,
                                product=f"product-pw{code}",
                                quantity="1",
                                next_page=True)

    with allure.step("Order Add: Final Page"):
        flow_order_final_page(page,
                              payment_type="Наличные деньги",
                              status="Черновик",
                              save=True)

    with allure.step("Order List: View Button"):
        flow_order_list(page,
                        find_row=f"room-pw{code}",
                        view=True)

    with allure.step("Order View: Get Value"):
        order_data = flow_order_view(page,
                                     get_value=[
                                         "ИД заказа",
                                         "Дата заказа",
                                         "Дата отгрузки",
                                         "Статус",
                                         "Рабочая зона",
                                         "Штат",
                                         "Клиент",
                                         "Тип оплаты"
                                     ])
        save_data("order_id", order_data["ИД заказа"])

    with allure.step("Order View: Assert Values"):
        assert order_data["Дата заказа"]   == delivery_date, f'Expected: "{delivery_date}", Actual: {order_data["Дата заказа"]}'
        assert order_data["Дата отгрузки"] == delivery_date,                 f'Expected: "{delivery_date}", Actual: {order_data["Дата отгрузки"]}'
        assert order_data["Статус"]       == "Черновик",                 f'Expected: "Черновик", Actual: {order_data["Статус"]}'
        assert order_data["Рабочая зона"] == f"room-pw{code}",           f'Expected: f"room-pw{code}", Actual: {order_data["Рабочая зона"]}'
        assert order_data["Штат"]         == f"robot-pw{code}",          f'Expected: f"robot-pw{code}", Actual: {order_data["Штат"]}'
        assert order_data["Клиент"]       == f"natural_client-pw{code}", f'Expected: f"natural_client-pw{code}", Actual: {order_data["Клиент"]}'
        assert order_data["Тип оплаты"]   == "Наличные деньги",          f'Expected: "Наличные деньги", Actual: {order_data["Тип оплаты"]}'

    with allure.step("Order List: Edit Button"):
        flow_order_list(page, edit=True)

    with allure.step("Order Edit: Main Page"):
        flow_order_main_page(page,
                             check_form=True,
                             deal_time=deal_time,
                             delivery_date=delivery_date,
                             room=f"room-pw{code}",
                             robot=f"robot-pw{code}",
                             natural_client=f"natural_client-pw{code}",
                             next_page=True)

    with allure.step("Order Edit: Product Page"):
        flow_order_product_page(page,
                                check_form=True,
                                product=f"product-pw{code}",
                                quantity="1",
                                warehouse="Основной склад",
                                price_type=f"Price Type UZB-pw{code}",
                                next_page=True)

    with allure.step("Order Edit: Final Page"):
        flow_order_final_page(page,
                              check_form=True,
                              payment_type="Наличные деньги",
                              natural_client=f"natural_client-pw{code}",
                              room=f"room-pw{code}",
                              robot=f"robot-pw{code}",
                              status="Черновик",
                              save=True)

    with allure.step("Order List: Status Button"):
        flow_order_list(page, find_row=f"room-pw{code}", status="Новый")
        flow_order_list(page, find_row=f"room-pw{code}", status="В обработке")
        flow_order_list(page, find_row=f"room-pw{code}", status="В ожидании")
        flow_order_list(page, find_row=f"room-pw{code}", status="Отгружен")
        flow_order_list(page, find_row=f"room-pw{code}", status="Доставлен")
        # flow_order_list(page, find_row=f"room-pw{code}", status="Архив")
        # flow_order_list(page, find_row=f"room-pw{code}", status="Отменен")
        test_order_add_column_order_id(page, code)

# ----------------------------------------------------------------------------------------------------------------------

@allure.title("Order Add Column -> Order Id")
def test_order_add_column_order_id(page, code) -> None:

    with allure.step("Order List: Grid Setting"):
        flow_order_list_grid_setting(page, colum_name="ИД заказа", search_name="ИД заказа")

# ----------------------------------------------------------------------------------------------------------------------
