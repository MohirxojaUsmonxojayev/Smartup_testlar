import allure
import re
from playwright.sync_api import expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from tests.smoke.flows.flow_authorization import login, USER_PASS, user_email_for
from tests.smoke.flows.flow_navigate import navigate_to, switch_filial, expect_page
from utils.base_page import BasePage

pytestmark = [allure.epic("Smoke"), allure.feature("Setup"), allure.story("User")]

# ----------------------------------------------------------------------------------------------------------------------

ROLE_SWITCH_CLICK_TIMEOUT = 2_000
BOTTOM_LEFT_WIDGET_MAX_X = 360
BOTTOM_LEFT_WIDGET_MIN_Y = 760

# ----------------------------------------------------------------------------------------------------------------------

def _remaining_role_switches(page):
    return page.locator(".switch span").filter(has_text="нет")


def _is_bottom_left_widget_zone(box):
    return box["x"] < BOTTOM_LEFT_WIDGET_MAX_X and box["y"] > BOTTOM_LEFT_WIDGET_MIN_Y


def _role_switch_count_is(page, expected_count):
    try:
        expect(_remaining_role_switches(page)).to_have_count(expected_count, timeout=ROLE_SWITCH_CLICK_TIMEOUT)
        return True
    except (AssertionError, PlaywrightTimeoutError):
        return False


def _click_role_switch_target(page, target, expected_remaining_count):
    try:
        target.click(timeout=ROLE_SWITCH_CLICK_TIMEOUT)
        if _role_switch_count_is(page, expected_remaining_count):
            return True
    except PlaywrightTimeoutError:
        pass

    box = target.bounding_box()
    if box is None or box["width"] <= 0 or box["height"] <= 0:
        return False

    y = box["height"] / 2
    x_positions = (
        max(1, box["width"] - 8),
        box["width"] / 2,
        min(16, box["width"] / 2),
    )
    for x in x_positions:
        try:
            target.click(position={"x": x, "y": y}, timeout=ROLE_SWITCH_CLICK_TIMEOUT)
            if _role_switch_count_is(page, expected_remaining_count):
                return True
        except PlaywrightTimeoutError:
            continue
    return False


def _click_role_switch(page, remaining, remaining_count):
    expected_remaining_count = remaining_count - 1

    for index in range(remaining_count):
        switch = remaining.nth(index)
        switch.scroll_into_view_if_needed()
        box = switch.bounding_box()
        if box is None or _is_bottom_left_widget_zone(box):
            continue
        if _click_role_switch_target(page, switch, expected_remaining_count):
            return

    switch = remaining.first
    switch.scroll_into_view_if_needed()
    page.mouse.wheel(0, 360)
    if _click_role_switch_target(page, switch, expected_remaining_count):
        return

    label = switch.locator("xpath=ancestor::label[1]")
    if label.count() > 0 and _click_role_switch_target(page, label.first, expected_remaining_count):
        return

    switch.click()
    expect(_remaining_role_switches(page)).to_have_count(expected_remaining_count)


def _set_permission_page_size_1000(page, base_page):
    page_size = page.locator("button").filter(has_text=re.compile(r"\b50\s*/")).first
    if page_size.count() == 0 or not page_size.is_visible():
        return
    page_size.click()
    option = page.get_by_role("link", name="1000").first
    expect(option).to_be_visible()
    option.click()
    base_page.wait_for_loader()


def _available_permissions_empty(page):
    try:
        expect(page.locator("b-page")).to_contain_text("нет данных", timeout=1_000)
        return True
    except (AssertionError, PlaywrightTimeoutError):
        return False


def _attach_available_permissions(page, base_page):
    _set_permission_page_size_1000(page, base_page)
    if _available_permissions_empty(page):
        return

    base_page.checkbox(first_visible=True, checked=True)
    base_page.wait_for_loader()
    page.get_by_role("button", name="Прикрепить").click()
    expect(page.get_by_role("heading", name="Прикрепить формы в количестве", exact=False)).to_be_visible()
    base_page.confirm_biruni()
    base_page.wait_for_loader()
    expect(page.locator("b-page")).to_contain_text("нет данных")


def run_user(page, code):
    with allure.step("1 - Foydalanuvchilar ro'yxatiga o'tish"):
        switch_filial(page, name=f"filial-pw{code}")
        navigate_to(page, tab="Главное", name="Пользователи")
        expect_page(page, heading="Пользователи")

    with allure.step("2 - Yangi foydalanuvchi formasini to'ldirish"):
        page.get_by_role("button", name="Создать").click()
        expect(page.get_by_role("heading")).to_contain_text("Пользователь (создание)")
        page.get_by_role("textbox").nth(2).fill(f"user-pw{code}")
        page.locator("#new_password").fill(USER_PASS)
        page.locator("#new_password").press("Tab")
        BasePage(page).wait_for_loader()
        base = BasePage(page)
        base.b_input_by_label("Физическое лицо", value=f"natural_person-pw{code}")
        base.wait_for_loader()
        base.b_input_by_label("Штат", value=f"robot-pw{code}")
        base.wait_for_loader()
        expect(page.get_by_text("Админ", exact=True)).to_be_visible()

    with allure.step("3 - Saqlash va ro'yxatda tekshirish"):
        page.get_by_role("button", name="Сохранить", exact=True).first.click()
        BasePage(page).wait_for_loader()
        expect_page(page, heading="Пользователи")
        expect(page.get_by_text(f"natural_person-pw{code}").first).to_be_visible()
        expect(page.get_by_text(user_email_for(code))).to_be_visible()

# ----------------------------------------------------------------------------------------------------------------------

def run_user_attach_form(page, code):
    base_page = BasePage(page)

    with allure.step("1 - Foydalanuvchi sahifasini ochish"):
        switch_filial(page, name=f"filial-pw{code}")
        navigate_to(page, tab="Главное", name="Пользователи")
        base_page.wait_for_loader()
        expect_page(page, heading="Пользователи")
        search = page.get_by_role("searchbox", name="Поиск")
        expect(search).to_be_visible()
        search.fill(f"natural_person-pw{code}")
        search.press("Enter")
        base_page.wait_for_loader()
        user_row = page.get_by_text(f"natural_person-pw{code}").first
        expect(user_row).to_be_visible()
        user_row.click()
        page.get_by_role("button", name="Просмотреть").click()
        expect(page.get_by_text(f"natural_person-pw{code}").first).to_be_visible()
        page.get_by_role("link", name=" Формы").click()

    with allure.step("2 - Формы ulash"):
        page.get_by_role("tab", name="Формы").click()
        page.get_by_role("button", name="Доступные").click()
        _attach_available_permissions(page, base_page)

    with allure.step("3 - Отчеты ulash"):
        page.get_by_role("tab", name="Отчеты").click()
        _attach_available_permissions(page, base_page)

    with allure.step("4 - Накладные ulash"):
        page.get_by_role("tab", name="Накладные").click()
        base_page.wait_for_loader()
        _attach_available_permissions(page, base_page)

    with allure.step("5 - Внешние системы ulash"):
        page.get_by_role("tab", name="Внешние системы").click()
        base_page.wait_for_loader()
        _attach_available_permissions(page, base_page)

    with allure.step("6 - Foydalanuvchilar ro'yxatiga qaytish"):
        page.get_by_role("button", name="Закрыть").click()
        expect_page(page, heading="Пользователи")

# ----------------------------------------------------------------------------------------------------------------------

def run_role(page):
    with allure.step("1 - Rollar ro'yxatiga o'tish"):
        expect_page(page, heading="Пользователи")
        page.get_by_role("link", name="Роли").click()
        expect(page.get_by_role("heading")).to_contain_text("Роли")

    with allure.step("2 - Admin rolini o'zgartirish — barcha switchlarni yoqish"):
        page.get_by_text("Админ", exact=True).click()
        page.get_by_role("button", name="Изменить").click()
        expect(page.get_by_role("heading")).to_contain_text("Роль (изменение)")

        clicked = 0
        while True:
            remaining = _remaining_role_switches(page)
            remaining_count = remaining.count()
            if remaining_count == 0:
                break
            _click_role_switch(page, remaining, remaining_count)
            expect(remaining).to_have_count(remaining_count - 1)
            clicked += 1

    with allure.step("3 - Saqlash va natijani tekshirish"):
        page.get_by_role("button", name="Сохранить", exact=True).first.click()
        BasePage(page).wait_for_loader(timeout=600_000)
        expect_page(page, heading="Роли", timeout=600_000)

# ----------------------------------------------------------------------------------------------------------------------

def run_role_attach_form(page):
    with allure.step("1 - Admin roli Formalar sahifasini ochish"):
        page.get_by_text("Админ", exact=True).click()
        page.get_by_role("button", name="Просмотреть").click()
        page.get_by_role("link", name=" Формы").click()

    with allure.step("2 - Barcha formalarga ruxsat berish"):
        page.get_by_role("button", name="Доступ ко всем формам").click()
        page.get_by_role("link", name="Разрешить").click()
        BasePage(page).confirm_biruni()
        BasePage(page).wait_for_loader(timeout=600_000)

    with allure.step("3 - Ruxsatlar berilganini tekshirish"):
        page.get_by_role("button", name="Доступные").click()
        expect(page.locator("b-page")).to_contain_text("нет данных")
        page.get_by_role("button", name="Закрыть").click()
        expect(page.get_by_role("heading")).to_contain_text("Роли")

# ----------------------------------------------------------------------------------------------------------------------

def run_change_password(page, code):
    with allure.step("1 - Foydalanuvchi sifatida kirish"):
        login(page, email=user_email_for(code), password=USER_PASS)
        expect(page.locator(".alert-icon")).to_be_visible()

    with allure.step("2 - Yangi parol kiritish va tasdiqlash"):
        page.locator("#current_password").fill(USER_PASS)
        page.locator("#new_password").fill(USER_PASS)
        page.locator("#rewritten_password").fill(USER_PASS)
        page.get_by_role("button", name="Подтвердить").click()
        BasePage(page).confirm_biruni()

# ----------------------------------------------------------------------------------------------------------------------

@allure.title("Foydalanuvchi yaratish")
def test_user(page, code):
    run_user(page, code)


@allure.title("Foydalanuvchiga formalar ulash")
def test_user_attach_form(page, code):
    run_user_attach_form(page, code)


@allure.title("Admin rolini sozlash (barcha ruxsatlar)")
def test_role(page):
    run_role(page)


@allure.title("Admin roliga barcha formalarga ruxsat berish")
def test_role_attach_form(page):
    run_role_attach_form(page)


@allure.title("Foydalanuvchi parolini o'zgartirish")
def test_change_password(page, code):
    run_change_password(page, code)
