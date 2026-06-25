"""Smartup ng-model asosidagi forma helper'lari.

`root` sifatida Page yoki Locator (masalan `.modal.show`) berish mumkin —
helper'lar shu root ichidagi maydonlar bilan ishlaydi.
"""

import re

from playwright.sync_api import Page, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

# ----------------------------------------------------------------------------------------------------------------------


def fill_input(root, ng_model: str, value: str) -> None:
    field = root.locator(f'input[ng-model="{ng_model}"]:visible').first
    expect(field).to_be_visible()
    field.fill(value)
    expect(field).to_have_value(value)

# ----------------------------------------------------------------------------------------------------------------------


def fill_textarea(root, ng_model: str, value: str) -> None:
    field = root.locator(f'textarea[ng-model="{ng_model}"]:visible').first
    expect(field).to_be_visible()
    field.fill(value)
    expect(field).to_have_value(value)

# ----------------------------------------------------------------------------------------------------------------------


def set_checkbox(root, ng_model: str, checked: bool) -> None:
    checkbox = root.locator(f'input[ng-model="{ng_model}"]').first
    if checkbox.is_checked() != checked:
        control = checkbox.locator(
            "xpath=ancestor::*[contains(@class,'checkbox') or contains(@class,'switch')][1]"
        )
        if control.count() > 0 and control.first.is_visible():
            control.first.click()
        else:
            expect(checkbox).to_be_visible()
            checkbox.click()
    expect(checkbox).to_be_checked() if checked else expect(checkbox).not_to_be_checked()

# ----------------------------------------------------------------------------------------------------------------------


def select_b_input_by_search(
    root,
    ng_model: str,
    search_text: str,
    option_text: str | None = None,
    expected_value: str | None = None,
) -> None:
    b_input = root.locator(f'b-input:has(input[ng-model="{ng_model}"])').first
    search = b_input.get_by_placeholder("Поиск").first
    expect(search).to_be_visible()
    search.click()
    search.fill(search_text)
    if option_text:
        option = b_input.locator("div.hint").get_by_text(option_text, exact=True).first
    else:
        option = b_input.locator("div.hint").filter(has_text=search_text).first
    expect(option).to_be_visible()
    option.click()
    if expected_value:
        expect(search).to_have_value(re.compile(re.escape(expected_value)))
    else:
        expect(search).to_have_value(re.compile(r".+"))

# ----------------------------------------------------------------------------------------------------------------------


def select_tashkent_region(page: Page) -> None:
    search = page.locator('b-tree-select:visible input[ng-model="_$bTree.searchValue"]').first
    expect(search).to_be_visible()
    search.click()
    search.fill("Ташкент")
    hint = page.locator("b-tree-select:visible .hint").first
    expect(hint).to_be_visible(timeout=5_000)

    for option_text in ("город Ташкент", "Ташкент"):
        options = (
            hint.get_by_text(option_text, exact=True).first,
            hint.locator("label").filter(has_text=option_text).first,
            hint.locator(".jstree-anchor").filter(has_text=option_text).first,
        )
        for option in options:
            try:
                expect(option).to_be_visible(timeout=5_000)
                option.click()
                expect(search).to_have_value(re.compile("Ташкент"))
                return
            except (AssertionError, PlaywrightTimeoutError):
                continue

    raise AssertionError("Region option 'город Ташкент' not found")

# ----------------------------------------------------------------------------------------------------------------------


def assert_visible_page_text(page: Page, *values: str) -> None:
    content = page.locator("b-page")
    for value in values:
        if value:
            expect(content).to_contain_text(value)
