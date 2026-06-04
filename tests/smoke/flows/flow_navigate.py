from playwright.sync_api import Page, expect
from utils.base_page import BasePage

# ----------------------------------------------------------------------------------------------------------------------

def navigate_to(page: Page, tab: str = "Главное", name: str = "Организации") -> None:
    page.locator("a.menu-link.menu-toggle", has_text=tab).click()
    page.locator("a.menu-link.menu-link-title").get_by_text(name, exact=True).click()

# ----------------------------------------------------------------------------------------------------------------------

def switch_filial(page: Page, name) -> None:
    page.locator(".pt-3.px-2").click()
    option = page.get_by_role("link", name=name, exact=True)
    expect(option).to_be_visible()
    option.click()
    BasePage(page).wait_for_loader()
    expect(page.get_by_role("paragraph").filter(has_text=name)).to_be_visible()

    # page.get_by_role("textbox", name="Поиск организации").fill(name)

# ----------------------------------------------------------------------------------------------------------------------
