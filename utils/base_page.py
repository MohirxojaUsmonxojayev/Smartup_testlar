import re
from datetime import datetime, timedelta

from playwright.sync_api import Page, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    # ------------------------------------------------------------------------------------------------------------------

    def current_heading_text(self) -> str:
        try:
            headings = [item.strip() for item in self.page.get_by_role("heading").all_inner_texts()]
        except Exception:
            return ""
        return " | ".join(item for item in headings if item)

    # ------------------------------------------------------------------------------------------------------------------

    def visible_error_text(self, timeout=1_000) -> str:
        selectors = (
            "#biruniAlertExtended",
            "#biruniAlert",
            "[role='alert']:visible",
            ".alert-danger:visible",
            ".toast-message:visible",
            ".toast:visible",
        )
        for index, selector in enumerate(selectors):
            locator = self.page.locator(selector).first
            try:
                if index == 0 and timeout:
                    expect(locator).to_be_visible(timeout=timeout)
                elif not locator.is_visible():
                    continue
                text = re.sub(r"\s+", " ", locator.inner_text(timeout=timeout)).strip()
            except Exception:
                continue
            if text:
                return text
        return ""

    # ------------------------------------------------------------------------------------------------------------------

    def _transition_failure_message(
        self,
        *,
        action: str,
        expected: str,
        before_state: str,
        actual_state: str,
        ui_error: str = "",
        location_hint: str = "",
    ) -> str:
        lines = [
            "Smartup transition failed",
            f"Before page: {before_state or 'unknown'}",
            f"Action: {action}",
            f"Expected: {expected}",
            f"Actual: {actual_state or 'unknown'}",
        ]
        if ui_error:
            lines.append(f"UI error: {ui_error}")
        if location_hint:
            lines.append(f"Location hint: {location_hint}")
        return "\n".join(lines)

    # ------------------------------------------------------------------------------------------------------------------

    def save_and_expect_heading(
        self,
        expected_heading: str,
        *,
        action: str = "Сохранить",
        before_state: str | None = None,
        expected_state: str | None = None,
        confirm_text: str | None = None,
        button_name: str = "Сохранить",
        exact_button: bool = True,
        timeout=120_000,
        location_hint: str = "",
    ) -> None:
        before = before_state or self.current_heading_text()
        button = self.page.get_by_role("button", name=button_name, exact=exact_button).first
        expect(button).to_be_visible()
        button.click()

        if confirm_text is not None:
            self.confirm_biruni(confirm_text or None)
        self.wait_for_loader(timeout=timeout)

        expected = expected_state or f"{expected_heading} heading ochilishi"
        ui_error = self.visible_error_text(timeout=1_000)
        if ui_error:
            actual = f"still on {self.current_heading_text() or before or 'unknown'}"
            raise AssertionError(
                self._transition_failure_message(
                    action=action,
                    expected=expected,
                    before_state=before,
                    actual_state=actual,
                    ui_error=ui_error,
                    location_hint=location_hint,
                )
            )

        heading = self.page.get_by_role("heading").filter(has_text=expected_heading).first
        try:
            expect(heading).to_be_visible(timeout=timeout)
        except (AssertionError, PlaywrightTimeoutError) as exc:
            actual = f"still on {self.current_heading_text() or before or 'unknown'}; url={self.page.url}"
            raise AssertionError(
                self._transition_failure_message(
                    action=action,
                    expected=expected,
                    before_state=before,
                    actual_state=actual,
                    ui_error=self.visible_error_text(timeout=500),
                    location_hint=location_hint,
                )
            ) from exc

    # ------------------------------------------------------------------------------------------------------------------

    def _expect_checkbox_state(self, checkbox, checked=True, timeout=10_000):
        if checked:
            expect(checkbox).to_be_checked(timeout=timeout)
        else:
            expect(checkbox).not_to_be_checked(timeout=timeout)

    # ------------------------------------------------------------------------------------------------------------------

    def _checkbox_state_matches(self, checkbox, checked=True, timeout=1_000):
        try:
            self._expect_checkbox_state(checkbox, checked=checked, timeout=timeout)
            return True
        except (AssertionError, PlaywrightTimeoutError):
            return False

    # ------------------------------------------------------------------------------------------------------------------

    def _click_grid_checkbox_cell(self, grid_cell, checkbox, checked=True):
        cell = grid_cell.first
        cell.scroll_into_view_if_needed()
        box = cell.bounding_box()
        if box is None or box["width"] <= 0 or box["height"] <= 0:
            return False

        y = box["height"] / 2
        click_x_positions = (
            min(24, box["width"] / 2),
            min(12, box["width"] / 2),
            box["width"] / 2,
        )
        for x in click_x_positions:
            cell.click(position={"x": x, "y": y})
            if self._checkbox_state_matches(checkbox, checked=checked):
                return True
        return False

    def click_first_visible_checkbox(self):
        self.page.wait_for_load_state("networkidle")
        checkbox = self.page.locator("b-grid:visible input[type='checkbox']").first
        if checkbox.count() == 0:
            checkbox = self.page.locator("input[type='checkbox']").first
        expect(checkbox).to_be_attached()
        self.set_checkbox(checkbox, checked=True)

    # ------------------------------------------------------------------------------------------------------------------

    def set_checkbox(self, checkbox, checked=True):
        """Checkboxni ko'rinadigan control orqali real click bilan kerakli holatga keltiradi."""
        if checkbox.is_checked() == checked:
            return

        label = checkbox.locator("xpath=ancestor::label[1]")
        if label.count() > 0 and label.first.is_visible():
            label.first.click()
            self._expect_checkbox_state(checkbox, checked=checked)
            return
        if label.count() > 0:
            label_box = label.first.bounding_box()
            checkbox_box = checkbox.bounding_box()
            if label_box is not None and checkbox_box is not None and label_box["width"] > 0:
                self.page.mouse.click(
                    label_box["x"] + min(10, label_box["width"] / 2),
                    checkbox_box["y"] + checkbox_box["height"] / 2,
                )
                if self._checkbox_state_matches(checkbox, checked=checked):
                    return

        grid_cell = checkbox.locator(
            "xpath=ancestor::*[contains(@class,'tbl-checkbox-cell') or contains(@class,'tbl-header-cell')][1]"
        )
        if grid_cell.count() > 0 and grid_cell.first.is_visible():
            if self._click_grid_checkbox_cell(grid_cell, checkbox, checked=checked):
                return
            self._expect_checkbox_state(checkbox, checked=checked)
            return

        wrapper = checkbox.locator(
            "xpath=ancestor::*[contains(@class,'checkbox') or contains(@class,'smt-checkbox') or contains(@class,'custom-control')][1]"
        )
        if wrapper.count() > 0 and wrapper.first.is_visible():
            wrapper.first.click()
        else:
            expect(checkbox).to_be_visible()
            checkbox.click()

        self._expect_checkbox_state(checkbox, checked=checked)

    # ------------------------------------------------------------------------------------------------------------------

    def set_checkall(self, checked=True):
        self.set_checkbox(self.page.locator("input[bcheckall]").first, checked=checked)

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

    def confirm_biruni(self, expected_text=None, button_name="да"):
        """Biruni confirm modalini barqaror tasdiqlaydi."""
        confirm = self.page.locator("#biruniConfirm")
        expect(confirm).to_be_visible()
        if expected_text:
            expect(confirm).to_contain_text(expected_text)
        expect(confirm).to_have_css("opacity", "1")
        confirm.get_by_role("button", name=button_name, exact=True).click()
        confirm.wait_for(state="hidden")

    # ------------------------------------------------------------------------------------------------------------------

    def grid_row(self, text, grid_selector="b-grid"):
        grid = self.page.locator(grid_selector)
        row = grid.locator(".tbl-row").filter(has_text=text).first
        expect(row).to_be_visible()
        return row

    # ------------------------------------------------------------------------------------------------------------------

    def click_grid_row(self, text, grid_selector="b-grid"):
        row = self.grid_row(text, grid_selector=grid_selector)
        row.click()
        return row

    # ------------------------------------------------------------------------------------------------------------------

    def select_option(self, ng_model, option_text, clear=False):
        b_input = self.page.locator(f'b-input:has(input[ng-model="{ng_model}"])')
        b_input.locator("input").click()
        if clear:
            edit = b_input.locator(".edit")
            if edit.count() > 0 and edit.first.is_visible():
                edit.first.click()
                b_input.locator("input").click()
        option = b_input.locator("div.hint").get_by_text(option_text, exact=True).first
        expect(option).to_be_visible()
        option.click()

    # ------------------------------------------------------------------------------------------------------------------

    def select_b_input(self, ng_model, option_text, clear=False):
        b_input = self.page.locator(f'b-input:has(input[ng-model="{ng_model}"])')
        search = b_input.get_by_placeholder("Поиск")
        search.click()
        if clear:
            edit = b_input.locator(".edit")
            if edit.count() > 0 and edit.first.is_visible():
                edit.first.click()
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

    def _label_field_container(self, label, index=0):
        """Label matni orqali form-group/col/form-row konteynerini topadi."""
        label_locator = self.page.get_by_text(label, exact=True).nth(index)
        expect(label_locator).to_be_visible()
        field = label_locator.locator(
            "xpath=ancestor::*[contains(@class,'form-group') or contains(@class,'col') or contains(@class,'form-row')][1]"
        )
        if field.count() == 0:
            field = label_locator.locator("xpath=..")
        return field

    # ------------------------------------------------------------------------------------------------------------------

    def input_by_label_text(self, label, index=0):
        field = self._label_field_container(label, index)
        input_el = field.locator("input:not([type='checkbox']):not([type='radio'])").first
        expect(input_el).to_be_visible()
        return input_el

    # ------------------------------------------------------------------------------------------------------------------

    def fill_input_by_label_text(self, label, value, index=0):
        input_el = self.input_by_label_text(label, index)
        input_el.click()
        input_el.press("ControlOrMeta+A")
        input_el.press("Backspace")
        input_el.fill(value)
        input_el.press("Tab")

    # ------------------------------------------------------------------------------------------------------------------

    def input_value_by_label_text(self, label, index=0) -> str:
        return self.input_by_label_text(label, index).input_value()

    # ------------------------------------------------------------------------------------------------------------------

    def switch_checkbox_by_label_text(self, label, index=0):
        return self._label_field_container(label, index).locator("input[type='checkbox']").first

    # ------------------------------------------------------------------------------------------------------------------

    def set_switch_by_label_text(self, label, enabled=True):
        field = self._label_field_container(label)
        checkbox = field.locator("input[type='checkbox']").first
        if checkbox.is_checked() != enabled:
            switch = field.locator("[role='switch'], .switch span").first
            if switch.count() > 0:
                expect(switch).to_be_visible()
                switch.click()
            else:
                expect(checkbox).to_be_visible()
                checkbox.click()
        self._expect_checkbox_state(checkbox, checked=enabled)

    # ------------------------------------------------------------------------------------------------------------------

    def switch_checked_by_label_text(self, label) -> bool:
        return self.switch_checkbox_by_label_text(label).is_checked()

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
