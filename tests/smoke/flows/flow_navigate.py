import re

from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError
from utils.base_page import BasePage

# ----------------------------------------------------------------------------------------------------------------------

def navigate_to(page, tab="Главное", name="Организации", timeout=120_000):
    base = BasePage(page)
    page.locator("a.menu-link.menu-toggle", has_text=tab).click()
    page.locator("a.menu-link.menu-link-title").get_by_text(name, exact=True).click()

    try:
        base.wait_for_loader(timeout=timeout)
    except Exception as exc:
        raise AssertionError(
            f"navigate_to: '{tab} -> {name}' sahifa {timeout // 1000}s ichida yuklanmadi "
            f"(loader yo'qolmadi), url={page.url}"
        ) from exc

# ----------------------------------------------------------------------------------------------------------------------

def expect_page(page, heading=None, url=None, timeout=120_000):
    if heading is None and url is None:
        raise ValueError("expect_page: kamida 'heading' yoki 'url' berilishi kerak")

    base = BasePage(page)

    if url is not None:
        pattern = url if isinstance(url, re.Pattern) else re.compile(re.escape(url))
        try:
            expect(page).to_have_url(pattern, timeout=timeout)
        except (AssertionError, PlaywrightTimeoutError) as exc:
            raise AssertionError(
                f"expect_page: kutilgan URL '{getattr(url, 'pattern', url)}' ochilmadi; "
                f"hozirgi url={page.url}"
            ) from exc

    if heading is not None:
        target = page.get_by_role("heading").filter(has_text=heading).first
        try:
            expect(target).to_be_visible(timeout=timeout)
        except (AssertionError, PlaywrightTimeoutError) as exc:
            shown = getattr(heading, "pattern", heading)
            raise AssertionError(
                f"expect_page: kutilgan heading '{shown}' ko'rinmadi; "
                f"hozirgi heading(lar)=\"{base.current_heading_text() or 'yo`q'}\", url={page.url}"
            ) from exc

# ----------------------------------------------------------------------------------------------------------------------

def switch_filial(page, name, timeout=120_000):
    base = BasePage(page)
    page.locator(".pt-3.px-2").click()
    option = page.get_by_role("link", name=name, exact=True)
    expect(option).to_be_visible()
    option.click()

    try:
        base.wait_for_loader(timeout=timeout)
    except Exception as exc:
        raise AssertionError(
            f"switch_filial: '{name}' filialiga o'tishda loader {timeout // 1000}s ichida "
            f"yo'qolmadi, url={page.url}"
        ) from exc

    expect(page.get_by_role("paragraph").filter(has_text=name)).to_be_visible()

    # page.get_by_role("textbox", name="Поиск организации").fill(name)

# ----------------------------------------------------------------------------------------------------------------------
