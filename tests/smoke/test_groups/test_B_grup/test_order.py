import re
from datetime import datetime, timedelta

import allure
from playwright.sync_api import Page, expect

from tests.smoke.flows.flow_authorization import authorization_user
from tests.smoke.flows.flow_navigate import navigate_to
from tests.smoke.flows.flow_order.flow_order_add import (
    flow_order_final_page,
    flow_order_main_page,
    flow_order_product_page,
)
from tests.smoke.flows.flow_order.flow_order_list import flow_open_order_list, flow_order_list

pytestmark = [allure.epic("B Group"), allure.feature("Order"), allure.story("Consignment")]


def _save_visible_confirm_if_open(page: Page) -> None:
    confirm = page.get_by_role("dialog").filter(has=page.get_by_role("button", name="да"))
    try:
        expect(confirm).to_be_visible(timeout=3_000)
    except Exception:
        return

    confirm.get_by_role("button", name="да").click()
    confirm.wait_for(state="hidden")


def _input_by_label_text(page: Page, label: str, index: int = 0):
    return page.get_by_text(label, exact=True).nth(index).evaluate_handle(
        """label => {
            const field = label.closest(".form-group, .col, .col-sm, .col-sm-12, .form-row")
                || label.parentElement;
            const input = field.querySelector("input:not([type='checkbox']):not([type='radio'])");
            if (!input) {
                throw new Error(`Input not found for label: ${label.textContent.trim()}`);
            }
            return input;
        }"""
    ).as_element()


def _fill_input_by_label_text(page: Page, label: str, value: str, index: int = 0) -> None:
    input_el = _input_by_label_text(page, label, index)
    input_el.click()
    input_el.press("ControlOrMeta+A")
    input_el.press("Backspace")
    input_el.fill(value)
    input_el.press("Tab")


def _input_value_by_label_text(page: Page, label: str, index: int = 0) -> str:
    return _input_by_label_text(page, label, index).input_value()


def _set_switch_by_label_text(page: Page, label: str, enabled: bool) -> None:
    page.get_by_text(label, exact=True).first.evaluate(
        """(label, enabled) => {
            const field = label.closest(".form-group") || label.parentElement;
            const checkbox = field.querySelector("input[type='checkbox']");
            if (!checkbox) {
                throw new Error(`Checkbox not found for label: ${label.textContent.trim()}`);
            }
            if (checkbox.checked !== enabled) {
                checkbox.click();
            }
        }""",
        enabled,
    )


def _switch_checked_by_label_text(page: Page, label: str) -> bool:
    return page.get_by_text(label, exact=True).first.evaluate(
        """label => {
            const field = label.closest(".form-group") || label.parentElement;
            const checkbox = field.querySelector("input[type='checkbox']");
            if (!checkbox) {
                throw new Error(`Checkbox not found for label: ${label.textContent.trim()}`);
            }
            return checkbox.checked;
        }"""
    )


def _page_text_is_present(page: Page, text: str, timeout: int = 3_000) -> bool:
    try:
        page.wait_for_function(
            "text => document.body && document.body.innerText.includes(text)",
            arg=text,
            timeout=timeout,
        )
        return True
    except Exception:
        return False


def _page_text_occurrences(page: Page, text: str) -> int:
    return page.evaluate(
        """text => {
            const bodyText = document.body.innerText || "";
            return bodyText.split(text).length - 1;
        }""",
        text,
    )


def _order_id_from_current_url(page: Page) -> str:
    order_id = re.search(r"[?&]deal_id=(\d+)", page.url)
    if not order_id:
        raise AssertionError(f"Order id URL ichidan topilmadi: {page.url}")
    return order_id.group(1)


def _expect_text_visible(page: Page, text: str) -> None:
    page.wait_for_function(
        """text => Array.from(document.body.querySelectorAll("*")).some(element => {
            if (!element.innerText || !element.innerText.includes(text)) {
                return false;
            }
            const style = window.getComputedStyle(element);
            const rect = element.getBoundingClientRect();
            return style.display !== "none"
                && style.visibility !== "hidden"
                && rect.width > 0
                && rect.height > 0;
        })""",
        arg=text,
        timeout=10_000,
    )


def _click_visible_text(page: Page, text: str) -> None:
    _expect_text_visible(page, text)
    page.get_by_text(text, exact=True).evaluate_all(
        """elements => {
            const visible = elements.find(element => {
                const style = window.getComputedStyle(element);
                const rect = element.getBoundingClientRect();
                return style.display !== "none"
                    && style.visibility !== "hidden"
                    && rect.width > 0
                    && rect.height > 0;
            });
            if (!visible) {
                throw new Error(`Visible text not found: ${text}`);
            }
            const clickable = visible.closest("a, button") || visible;
            clickable.click();
        }"""
    )


def _close_error_dialog(page: Page, expected_text: str | None = None) -> None:
    dialog = page.get_by_role("dialog").filter(has_text="Ошибка")
    expect(dialog).to_be_visible()
    if expected_text:
        expect(dialog).to_contain_text(expected_text)
    dialog.get_by_role("button").first.click()
    dialog.wait_for(state="hidden")


def _save_order_from_final_page(page: Page) -> None:
    page.get_by_role("button", name="Сохранить").click()
    confirm = page.get_by_role("dialog").filter(has=page.get_by_role("button", name="да"))
    expect(confirm).to_be_visible()
    confirm.get_by_role("button", name="да").click()
    confirm.wait_for(state="hidden")


def _assert_save_blocked_without_confirm(page: Page) -> None:
    page.get_by_role("button", name="Сохранить").click()
    confirm = page.get_by_role("dialog").filter(has=page.get_by_role("button", name="да"))
    try:
        expect(confirm).to_be_visible(timeout=1_500)
    except Exception:
        try:
            _close_error_dialog(page)
        except Exception:
            pass
        return
    raise AssertionError("30 kundan katta konsignatsiya sanasi qabul qilindi")


def _click_consignment_add_button(page: Page) -> None:
    page.get_by_text("Дата оплаты по консигнации", exact=True).first.evaluate(
        """label => {
            const section = label.closest(".mb-4") || label.parentElement;
            const visible = element => {
                const style = window.getComputedStyle(element);
                const rect = element.getBoundingClientRect();
                return style.display !== "none"
                    && style.visibility !== "hidden"
                    && rect.width > 0
                    && rect.height > 0;
            };
            const addButton = Array.from(section.querySelectorAll("button"))
                .find(button => visible(button) && button.querySelector("i.fa-plus"));
            if (!addButton) {
                throw new Error("Consignment plus button not found");
            }
            addButton.click();
        }"""
    )


def _open_order_settings(page: Page) -> None:
    navigate_to(page, tab="Главное", name="Настройки системы")
    expect(page.get_by_role("heading", name="Настройки системы")).to_be_visible()
    page.get_by_role("link", name="Заказ").click()
    expect(page.get_by_text("Разрешить выдачу консигнации", exact=True)).to_be_visible()


def _enable_consignment_for_orders(page: Page) -> None:
    _open_order_settings(page)

    _set_switch_by_label_text(page, "Разрешить выдачу консигнации", True)
    _fill_input_by_label_text(page, "Лимит консигнации (в днях)", "30")
    if _input_value_by_label_text(page, "Лимит консигнации (в днях)") != "30":
        raise AssertionError("Лимит консигнации (в днях) qiymati 30 bo'lmadi")

    page.get_by_role("button", name="Сохранить").first.click()
    _save_visible_confirm_if_open(page)

    if not _switch_checked_by_label_text(page, "Разрешить выдачу консигнации"):
        raise AssertionError("Разрешить выдачу консигнации yoqilmadi")
    if _input_value_by_label_text(page, "Лимит консигнации (в днях)") != "30":
        raise AssertionError("Лимит консигнации (в днях) saqlangandan keyin 30 emas")


def _cancel_existing_client_orders_if_any(page: Page, code: str) -> None:
    flow_open_order_list(page)

    for _ in range(20):
        if not _page_text_is_present(page, f"natural_client-pw{code}", timeout=2_000):
            break

        flow_order_list(page, find_row=f"natural_client-pw{code}", status="Отменен")
        flow_open_order_list(page)

    if _page_text_is_present(page, f"natural_client-pw{code}", timeout=2_000):
        raise AssertionError(f"natural_client-pw{code} uchun active orderlar tozalanmadi")


def _consignment_limit_state(page: Page) -> dict[str, str]:
    return page.get_by_text("Дата оплаты по консигнации", exact=True).first.evaluate(
        """label => {
            const scope = angular.element(label.closest("b-page")).scope();
            return {
                limit: String(scope.q.consignment_day_limit),
                max_date: scope.d.max_consignment_date.format("DD.MM.YYYY"),
            };
        }"""
    )


@allure.title("B Group: Konsignatsiya limiti bilan zakaz yaratish")
def test_b_group_create_order_with_consignment_limit(page: Page, code: str, save_data) -> None:
    """
    Testcase:
    1. User sifatida tizimga kirish.
    2. Главное > Настройки системы > Заказ tabida Разрешить выдачу консигнации yoqiladi.
    3. Лимит консигнации (в днях) qiymati 30 qilib saqlanadi.
    4. Mavjud active orderlar bo'lsa Отменен statusga o'tkazilib, product booking tozalanadi.
    5. Yangi order yaratiladi va 3-formada konsignatsiya kartasi ko'rinishi tekshiriladi.
    6. Konsignatsiya limiti 30 kun ekanligi max date orqali tekshiriladi.
    7. Konsignatsiya date/amount, payment type va status to'ldirilib 5 dona order saqlanadi.
    8. Order viewda asosiy ma'lumotlar va Консигнация tabidagi date/amount tekshiriladi.
    """
    with allure.step("1 - User tizimga muvaffaqiyatli kiradi"):
        authorization_user(page, code)
        expect(page.get_by_role("heading", name="Trade")).to_be_visible()

    with allure.step("2 - Order settingsda konsignatsiya yoqiladi va limit 30 kun qilinadi"):
        _enable_consignment_for_orders(page)

    with allure.step("3 - Mavjud active orderlar bo'lsa Отменен statusga o'tkazilib, product booking tozalanadi"):
        _cancel_existing_client_orders_if_any(page, code)

    with allure.step("4 - Yangi zakaz asosiy va TMC qadamlaridan o'tkaziladi"):
        flow_order_list(page, add=True)
        delivery_date = _input_value_by_label_text(page, "Дата отгрузки")
        flow_order_main_page(
            page,
            check_form=True,
            deal_time=datetime.now().strftime("%d.%m.%Y %H:%M"),
            delivery_date=delivery_date,
            room=f"room-pw{code}",
            robot=f"robot-pw{code}",
            natural_client=f"natural_client-pw{code}",
            next_page=True,
        )
        flow_order_product_page(
            page,
            product=f"product-pw{code}",
            quantity="5",
            next_page=True,
        )

    with allure.step("5 - 3-formada konsignatsiya kartasi va 30 kunlik limit tekshiriladi"):
        _expect_text_visible(page, "Дата оплаты по консигнации")
        _expect_text_visible(page, "Сумма консигнации")
        _expect_text_visible(page, "ИТОГО")

        consignment_state = _consignment_limit_state(page)
        expected_limit_date = (
            datetime.strptime(delivery_date, "%d.%m.%Y") + timedelta(days=30)
        ).strftime("%d.%m.%Y")
        if consignment_state["limit"] != "30":
            raise AssertionError(f"Expected consignment limit 30, got {consignment_state['limit']}")
        if consignment_state["max_date"] != expected_limit_date:
            raise AssertionError(
                f"Expected max consignment date {expected_limit_date}, got {consignment_state['max_date']}"
            )

    with allure.step("6 - Konsignatsiya date/amount, tip oplati va status to'ldirilib saqlanadi"):
        _fill_input_by_label_text(page, "Дата оплаты по консигнации", expected_limit_date)
        if _input_value_by_label_text(page, "Дата оплаты по консигнации") != expected_limit_date:
            raise AssertionError("Дата оплаты по консигнации qiymati to'g'ri kiritilmadi")

        _fill_input_by_label_text(page, "Сумма консигнации", "35000")
        if _input_value_by_label_text(page, "Сумма консигнации") != "35 000":
            raise AssertionError("Сумма консигнации qiymati 35 000 formatiga kelmadi")

        flow_order_final_page(
            page,
            payment_type="Наличные деньги",
            status="Черновик",
            save=True,
        )
        expect(page).to_have_url(re.compile(r".*/order_list"))
        expect(page.get_by_role("heading")).to_contain_text("Заказы")

    with allure.step("7 - Zakaz view oynasida asosiy ma'lumotlar tekshiriladi"):
        flow_order_list(page, find_row=f"natural_client-pw{code}", view=True)
        expect(page).to_have_url(re.compile(r".*/order_view"))
        _expect_text_visible(page, f"natural_client-pw{code}")
        _expect_text_visible(page, f"room-pw{code}")
        _expect_text_visible(page, f"robot-pw{code}")
        _expect_text_visible(page, "Наличные деньги")
        _expect_text_visible(page, "Черновик")
        _expect_text_visible(page, f"product-pw{code}")
        _expect_text_visible(page, "35 000")
        _expect_text_visible(page, "Ответственный за консигнацию")
        _expect_text_visible(page, "Согласование консигнации")

    with allure.step("8 - Viewdagi Консигнация tabida date va summa tekshiriladi"):
        _click_visible_text(page, "Консигнация")
        _expect_text_visible(page, expected_limit_date)
        _expect_text_visible(page, "35 000")

    with allure.step("9 - B-group konsignatsiya order id saqlanadi"):
        save_data("b_group_consignment_order_client", f"natural_client-pw{code}")
        save_data(
            "b_group_consignment_order_id",
            _order_id_from_current_url(page),
        )
        page.get_by_role("button", name="Закрыть").click()
        expect(page).to_have_url(re.compile(r".*/order_list"))


@allure.title("B Group: Konsignatsiyali zakazni edit qilish va split qilish")
def test_b_group_edit_order_with_consignment_limit(page: Page, code: str, load_data, save_data) -> None:
    """
    Testcase:
    1. User sifatida tizimga kirish.
    2. test_b_group_create_order_with_consignment_limit yaratgan active order listda topiladi.
    3. Order edit qilinib quantity 5 dan 4 ga kamaytiriladi.
    4. Eski konsignatsiya summasi order totalidan katta bo'lgani uchun error chiqishi va konsignatsiya clear bo'lishi tekshiriladi.
    5. 30 kundan katta konsignatsiya sanasi kiritilib, save confirm chiqmasligi tekshiriladi.
    6. Konsignatsiya summasi + orqali 2 ta sanaga bo'linadi va order saqlanadi.
    7. Order viewda 28 000 total hamda ikki konsignatsiya sana/summa tekshiriladi.
    """
    with allure.step("1 - User tizimga muvaffaqiyatli kiradi"):
        authorization_user(page, code)
        expect(page.get_by_role("heading", name="Trade")).to_be_visible()

    with allure.step("2 - B-group create testi yaratgan active order listda topiladi"):
        created_order_client = load_data("b_group_consignment_order_client") or f"natural_client-pw{code}"
        flow_open_order_list(page)
        if not _page_text_is_present(page, created_order_client):
            raise AssertionError(
                "Konsignatsiyali active order topilmadi. "
                "Avval test_b_group_create_order_with_consignment_limit ni run qiling."
            )

    with allure.step("3 - Order edit qilinib quantity 5 dan 4 ga kamaytiriladi"):
        flow_order_list(page, find_row=created_order_client, edit=True)
        expect(page).to_have_url(re.compile(r".*/order\+edit"))
        delivery_date = _input_value_by_label_text(page, "Дата отгрузки")
        delivery_date_value = datetime.strptime(delivery_date, "%d.%m.%Y")
        first_split_date = (delivery_date_value + timedelta(days=15)).strftime("%d.%m.%Y")
        limit_date = (delivery_date_value + timedelta(days=30)).strftime("%d.%m.%Y")
        invalid_date = (delivery_date_value + timedelta(days=31)).strftime("%d.%m.%Y")

        page.get_by_role("button", name="Далее").click()
        flow_order_product_page(
            page,
            quantity="4",
            next_page=True,
        )

    with allure.step("4 - Eski konsignatsiya order totalidan katta bo'lgani uchun error chiqadi va clear bo'ladi"):
        _close_error_dialog(
            page,
            "Общая сумма консигнаций не должна быть больше суммы заказа",
        )
        if _input_value_by_label_text(page, "Дата оплаты по консигнации") != "":
            raise AssertionError("Дата оплаты по консигнации clear bo'lmadi")
        if _input_value_by_label_text(page, "Сумма консигнации") != "":
            raise AssertionError("Сумма консигнации clear bo'lmadi")
        _expect_text_visible(page, "ИТОГО")
        _expect_text_visible(page, "28 000")

    with allure.step("5 - 30 kundan katta konsignatsiya sanasi save qilinmaydi"):
        _fill_input_by_label_text(page, "Дата оплаты по консигнации", invalid_date)
        _fill_input_by_label_text(page, "Сумма консигнации", "28000")
        if _input_value_by_label_text(page, "Дата оплаты по консигнации") != invalid_date:
            raise AssertionError("Invalid konsignatsiya sanasi inputga kiritilmadi")
        if _input_value_by_label_text(page, "Сумма консигнации") != "28 000":
            raise AssertionError("Invalid date tekshiruv summasi 28 000 formatiga kelmadi")
        _assert_save_blocked_without_confirm(page)
        expect(page).to_have_url(re.compile(r".*/order\+edit"))

    with allure.step("6 - Konsignatsiya + orqali 2 ta sanaga bo'linadi"):
        _fill_input_by_label_text(page, "Дата оплаты по консигнации", first_split_date)
        _fill_input_by_label_text(page, "Сумма консигнации", "14000")
        if _input_value_by_label_text(page, "Сумма консигнации") != "14 000":
            raise AssertionError("Birinchi konsignatsiya summasi 14 000 formatiga kelmadi")

        _click_consignment_add_button(page)
        _fill_input_by_label_text(page, "Дата оплаты по консигнации", limit_date, index=1)
        _fill_input_by_label_text(page, "Сумма консигнации", "14000", index=1)
        if _input_value_by_label_text(page, "Дата оплаты по консигнации", index=1) != limit_date:
            raise AssertionError("Ikkinchi konsignatsiya sanasi to'g'ri kiritilmadi")
        if _input_value_by_label_text(page, "Сумма консигнации", index=1) != "14 000":
            raise AssertionError("Ikkinchi konsignatsiya summasi 14 000 formatiga kelmadi")

    with allure.step("7 - Order save qilinadi"):
        _save_order_from_final_page(page)
        expect(page).to_have_url(re.compile(r".*/order_list"))
        expect(page.get_by_role("heading")).to_contain_text("Заказы")

    with allure.step("8 - Order viewda split qilingan konsignatsiya tekshiriladi"):
        flow_order_list(page, find_row=created_order_client, view=True)
        expect(page).to_have_url(re.compile(r".*/order_view"))
        _expect_text_visible(page, created_order_client)
        _expect_text_visible(page, f"product-pw{code}")
        _expect_text_visible(page, "28 000")
        _click_visible_text(page, "Консигнация")
        _expect_text_visible(page, first_split_date)
        _expect_text_visible(page, limit_date)
        if _page_text_occurrences(page, "14 000") < 2:
            raise AssertionError("Viewda ikkita 14 000 konsignatsiya summasi ko'rinmadi")

    with allure.step("9 - Edit qilingan order ma'lumotlari saqlanadi"):
        save_data("b_group_consignment_order_split_first_date", first_split_date)
        save_data("b_group_consignment_order_split_second_date", limit_date)
        page.get_by_role("button", name="Закрыть").click()
        expect(page).to_have_url(re.compile(r".*/order_list"))
