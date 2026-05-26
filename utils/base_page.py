import re
from datetime import datetime, timedelta

from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    # ------------------------------------------------------------------------------------------------------------------

    def click_js(self):
        self.page.wait_for_load_state("networkidle")
        checkbox = self.page.locator(".checkbox").first
        checkbox.evaluate("el => el.click()")

    # ------------------------------------------------------------------------------------------------------------------

    def wait_for_loader(self, timeout=120_000):
        """
        Loader (overlay) paydo bo'lishini va keyin yo'qolishini kutadi.
        """
        overlay = self.page.locator(".block-ui-overlay")
        try:
            overlay.wait_for(state="visible", timeout=2_000)
        except Exception:
            # Agar loader 2 soniyada chiqmasa, demak jarayon tugagan yoki juda tez o'tgan
            return

        try:
            overlay.wait_for(state="hidden", timeout=timeout)
        except Exception as e:
            print(f"Xato: Loader {timeout} ms ichida yo'qolmadi: {e}")
            raise

    # ------------------------------------------------------------------------------------------------------------------

    def select_option(self, ng_model, option_text, clear=False):
        b_input = self.page.locator(f'b-input:has(input[ng-model="{ng_model}"])')
        b_input.locator("input").click()
        if clear:
            b_input.locator(".edit").click()
        b_input.locator("div.hint").get_by_text(option_text).click()

    # ------------------------------------------------------------------------------------------------------------------

    def select_b_input(self, ng_model, option_text, clear=False):
        b_input = self.page.locator(f'b-input:has(input[ng-model="{ng_model}"])')
        search = b_input.get_by_placeholder("Поиск")
        search.click()
        if clear:
            b_input.locator(".edit").click()
            search.click()
        search.fill(option_text)
        option = b_input.locator("div.hint").get_by_text(option_text, exact=True)
        expect(option).to_be_visible()
        option.click()
        expect(search).to_have_value(option_text)

    # ------------------------------------------------------------------------------------------------------------------

    def _field_container_by_label(self, label, needs_search=False):
        label_locator = self.page.get_by_text(re.compile(rf"^{re.escape(label)}\*?$"))

        for index in range(label_locator.count()):
            label_item = label_locator.nth(index)
            for ancestor in (
                "ancestor::*[contains(@class,'col-')][1]",
                "ancestor::div[contains(@class,'form-group')][1]",
            ):
                container = label_item.locator(f"xpath={ancestor}")
                if container.count() == 0:
                    continue

                if needs_search and container.get_by_placeholder("Поиск").count() > 0:
                    return container

                if not needs_search and container.get_by_role("textbox").count() > 0:
                    return container

        raise AssertionError(f"Field container not found by label: {label}")

    # ------------------------------------------------------------------------------------------------------------------

    def fill_textbox_by_label(self, label, value, expected_value=None):
        textbox = self._field_container_by_label(label).get_by_role("textbox").first
        textbox.fill(value)
        expect(textbox).to_have_value(expected_value or value)

    # ------------------------------------------------------------------------------------------------------------------

    def select_b_input_by_label(self, label, option_text, clear=False, exact=True):
        container = self._field_container_by_label(label, needs_search=True)
        search = container.get_by_placeholder("Поиск").first
        search.click()
        if clear:
            edit = container.locator(".edit")
            if edit.count() > 0 and edit.first.is_visible():
                edit.first.click()
            search.click()
        search.fill(option_text)
        option = container.locator("div.hint").get_by_text(option_text, exact=exact)
        expect(option).to_be_visible()
        option.click()
        expect(search).to_have_value(re.compile(re.escape(option_text)))

    # ------------------------------------------------------------------------------------------------------------------

    def expect_b_input_value_by_label(self, label, expected_value):
        container = self._field_container_by_label(label, needs_search=True)
        search = container.get_by_placeholder("Поиск").first
        expect(search).to_have_value(re.compile(re.escape(expected_value)))

    # ------------------------------------------------------------------------------------------------------------------

    def close_extended_alert(self):
        alert = self.page.locator("#biruniAlertExtended")
        expect(alert).to_be_visible()
        alert.locator("button.close").click()
        alert.wait_for(state="hidden")

    # ------------------------------------------------------------------------------------------------------------------

    def select_date(self, ng_model, option="custom", day=None, add_days=0):
        today = datetime.today()

        if option == "first":
            target = today.replace(day=1)
        elif option == "last":
            next_month = today.replace(day=28) + timedelta(days=4)
            target = next_month - timedelta(days=next_month.day)
        elif option == "today":
            target = today + timedelta(days=add_days)
        else:  # custom
            target = today.replace(day=day)

        self.page.locator(f'input[ng-model="{ng_model}"]').click()
        # self.page.get_by_role("cell", name=str(target.day)).first.click()
        self.page.get_by_role("cell", name=str(target.day), exact=True).first.click()

    # ------------------------------------------------------------------------------------------------------------------
