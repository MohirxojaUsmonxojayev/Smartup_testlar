import allure
from playwright.sync_api import expect

# ----------------------------------------------------------------------------------------------------------------------

def flow_order_view(page, get_value=None):
    page.wait_for_url("**/order_view**")
    expect(page.locator("#kt_content")).to_contain_text("Заказ / Просмотр")

    result = {}
    if get_value is not None:
        keys = get_value if isinstance(get_value, list) else [get_value]
        for key in keys:
            with allure.step(f"Order View: value -> '{key}' olindi"):
                # Exact label mosligi: contains() endi "Статус" ni "Статус заказов, которые более 90 (дней)"
                # kabi yangi matnlarga ham moslab strict mode violation berardi.
                result[key] = page.locator(f'//t[normalize-space()="{key}"]/../../span').inner_text().strip()

    page.get_by_role("button", name="Закрыть").click()

    if get_value is None:
        return None

    return result if isinstance(get_value, list) else result[get_value]

# ----------------------------------------------------------------------------------------------------------------------
