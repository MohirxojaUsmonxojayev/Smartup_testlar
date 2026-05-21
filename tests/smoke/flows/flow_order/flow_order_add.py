import re
import allure
from playwright.sync_api import expect

# ----------------------------------------------------------------------------------------------------------------------

def flow_order_main_page(page, check_form=False, deal_time=None, delivery_date=None, room=None, robot=None, natural_client=None, next_page=True):
    page.wait_for_url(re.compile(r".*/order\+(add|edit)"))
    expect(page.locator("#kt_content")).to_have_text(re.compile(r"Заказ \((создание|изменение)\)"))

    if check_form:
        with allure.step("Main Page: Auto fill bo'lganini tekshirish"):
            # expected_deal_time = deal_time or datetime.now().strftime("%d.%m.%Y %H:%M")
            # delivery_date = datetime.now().strftime("%d.%m.%Y")

            expect(page.locator("#anor279-input-deal_time")).to_have_value(deal_time)
            expect(page.locator("#anor279-input-delivery_date")).to_have_value(delivery_date)
            expect(page.locator("#anor279-input-b_input-room_name").get_by_role("textbox", name="Поиск")).to_have_value(room)
            expect(page.locator("#anor279-input-b_input-robot_name").get_by_role("textbox", name="Поиск")).to_have_value(robot)
            expect(page.locator("#anor279-input-b_input-person_name").get_by_role("textbox", name="Поиск")).to_have_value(natural_client)

    if next_page:
        with allure.step("Main Page: Keyingi page ga o'tish"):
            page.get_by_role("button", name="Далее").click()

# ----------------------------------------------------------------------------------------------------------------------

def flow_order_product_page(page, check_form=False, product=None, quantity=None, warehouse=None, price_type=None, next_page=True):
    expect(page.locator("#kt_content")).to_have_text(re.compile(r"Заказ \((создание|изменение)\)"))

    if product and not check_form:
        with allure.step(f"Product Page: product -> '{product}' tanlash"):
            page.locator("#anor279_input-b_input-product_name_goods0").get_by_role("textbox", name="Поиск").click()
            page.get_by_text(product).click()
            expect(page.locator("#anor279_input-b_input-product_name_goods0").locator("input")).to_have_value(product)

    if quantity and not check_form:
        with allure.step(f"Product Page: quantity -> '{quantity}' kiritish"):
            page.locator("#anor279_input-b_pg_col-quantity_0").fill(quantity)

    if check_form:
        with allure.step(f"Product Page: "
                         f"Check product -> '{product}', "
                         f"Check warehouse -> '{warehouse}', "
                         f"Check price_type -> '{price_type}', "
                         f"Check quantity -> '{quantity}'"
                         ):
            expect(page.locator("#anor279_input-b_input-product_name_goods0").get_by_role("textbox", name="Поиск")).to_have_value(product)
            expect(page.locator("#anor279_input-b_pg_grid-goods_items")).to_contain_text(warehouse)
            expect(page.locator("#anor279_input-b_pg_grid-goods_items")).to_contain_text(price_type)
            expect(page.locator("#anor279_input-b_pg_col-quantity_0")).to_have_value(quantity)

    if next_page:
        with allure.step("Product Page: Keyingi page ga o'tish"):
            page.get_by_role("button", name="Далее").click()

# ----------------------------------------------------------------------------------------------------------------------

def flow_order_final_page(page, check_form=False, payment_type=None, natural_client=None, room=None, robot=None, status=None, save=True):
    expect(page.locator("#kt_content")).to_have_text(re.compile(r"Заказ \((создание|изменение)\)"))

    if payment_type and not check_form:
        with allure.step(f"Final Page: Payment Type -> '{payment_type}' tanlash"):
            page.locator("#anor279-inpu-b_input-payment_type").get_by_role("textbox", name="Поиск").click()
            page.get_by_text(payment_type).click()

    if status and not check_form:
        with allure.step(f"Final Page: Order status -> '{status}' tanlash"):
            page.locator("#anor279-ui_select-status").get_by_label("Select box activate").click()
            page.get_by_text(status).click()

    if check_form:
        with allure.step(f"Final Page: "
                         f"Check payment_type -> '{payment_type}',  "
                         f"Check status -> '{status}'"
                         f"Check natural_client -> '{natural_client}'"
                         f"Check room -> '{room}'"
                         f"Check robot -> '{robot}'"
                         ):
            expect(page.locator("#anor279-inpu-b_input-payment_type").get_by_role("textbox", name="Поиск")).to_have_value(payment_type)
            expect(page.locator("#anor279-ui_select-status")).to_contain_text(status)
            expect(page.locator("form[name=\"step2\"]")).to_contain_text(natural_client)
            expect(page.locator("form[name=\"step2\"]")).to_contain_text(room)
            expect(page.locator("form[name=\"step2\"]")).to_contain_text(robot)

    if save:
        with allure.step("Final Page: Order save qilish"):
            page.get_by_role("button", name="Сохранить").click()
            expect(page.locator("#biruniConfirm")).to_contain_text("Сохранить?")
            expect(page.locator("#biruniConfirm")).to_have_css("opacity", "1")
            page.locator("#biruniConfirm").get_by_role("button", name="да").click()
            page.locator("#biruniConfirm").wait_for(state="hidden")

# ----------------------------------------------------------------------------------------------------------------------
