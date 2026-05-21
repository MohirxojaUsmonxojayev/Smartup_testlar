import allure
from playwright.sync_api import expect

from tests.smoke.flows import flow_modal

# ----------------------------------------------------------------------------------------------------------------------

def flow_order_list(page, add=False, find_row=None, view=False, edit=False, status=None):
    page.wait_for_url("**/order_list")
    expect(page.get_by_role("heading")).to_contain_text("Заказы")

    if add:
        with allure.step("Order List: 'Создать' button click"):
            page.get_by_role("button", name="Создать", exact=True).click()
            return

    if find_row:
        with allure.step(f"Order List: find_row -> '{find_row}'"):
            page.get_by_text(find_row).first.click()

    if view:
        with allure.step("Order List: 'Просмотреть' button click"):
            page.get_by_role("button", name="Просмотреть", exact=True).click()

    if edit:
        with allure.step("Order List: 'Изменить' button click"):
            page.get_by_role("button", name="Изменить", exact=True).click()

    if status:
        with allure.step("Order List: 'Изменить статус' button click"):
            page.get_by_role("button", name="Изменить статус", exact=True).click()

            flow_modal.dialog_status(page)

            page.get_by_role("link", name=status).click()
            expect(page.locator("#biruniConfirm")).to_contain_text(f"Изменить на {status}?")
            expect(page.locator("#biruniConfirm")).to_have_css("opacity", "1")
            page.get_by_role("button", name="да", exact=True).click()
            page.locator("#biruniConfirm").wait_for(state="hidden")

            expect(page.locator("#dropdown").first).to_contain_text(status)

# ----------------------------------------------------------------------------------------------------------------------

def flow_order_list_grid_setting(page, colum_name, search_name):
    page.wait_for_url("**/order_list")
    expect(page.get_by_role("heading")).to_contain_text("Заказы")
    page.locator(".btn.btn-default.dropdown-toggle.no-after").first.click()
    page.get_by_role("link", name="Настройка таблицы").click()

    expect(page.locator("#kt_content")).to_contain_text("Настройка таблицы: Заказы")
    page.locator("#deal_id").get_by_text(colum_name).click()
    page.locator("label").filter(has_text=search_name).click()
    expect(page.locator("#deal_id")).to_contain_text(colum_name)
    page.get_by_role("button", name="Сохранить").click()

    page.wait_for_url("**/order_list")
    expect(page.get_by_role("heading")).to_contain_text("Заказы")

# ----------------------------------------------------------------------------------------------------------------------