"""Smartup ng-model asosidagi forma helper'lari.

`root` sifatida Page yoki Locator (masalan `.modal.show`) berish mumkin —
helper'lar shu root ichidagi maydonlar bilan ishlaydi.
"""

import re

from playwright.sync_api import expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

# ----------------------------------------------------------------------------------------------------------------------


def fill_textarea(root, ng_model, value):
    field = root.locator(f'textarea[ng-model="{ng_model}"]:visible').first
    expect(field).to_be_visible()
    field.fill(value)
    expect(field).to_have_value(value)

# ----------------------------------------------------------------------------------------------------------------------


def select_b_input_by_search(
    root,
    ng_model,
    search_text,
    option_text=None,
    expected_value=None,
):
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


def select_tashkent_region(page):
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


def assert_visible_page_text(page, *values):
    content = page.locator("b-page")
    for value in values:
        if value:
            expect(content).to_contain_text(value)
