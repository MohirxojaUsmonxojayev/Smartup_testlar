import allure
from playwright.sync_api import Page, expect

from tests.regression.flows.flow_authorization import (
    authorization,
    login,
    dashboard,
)
from tests.regression.flows.flow_navigate import switch_filial

pytestmark = [
    allure.epic("Regression"),
    allure.feature("Auth"),
    allure.story("Login va filial tanlash"),
]

# ----------------------------------------------------------------------------------------------------------------------
# Konstantalar — faqat shu fayldagi test profili uchun

FILIAL_NAME   = "NovaTrade - Toshkent Filiali"

USER_LOGIN    = "moxir@novatrade"
USER_PASSWORD = "1"


# ----------------------------------------------------------------------------------------------------------------------
# Reusable flow funksiyalari — boshqa testlarda import qilib chaqiriladi

def run_admin_login(page: Page) -> None:
    """
    Admin sifatida tizimga kiradi va filial tanlaydi.

    Credentials conftest --company-code / --company-password dan olinadi:
      email    → admin@<company-code>   (admin@novatrade)
      password → <company-password>     (greenwhite)

    Boshqa test fayllarida:
        from tests.regression.test_auth import run_admin_login
        run_admin_login(page)
    """
    with allure.step("1 - Admin sifatida tizimga kirish"):
        authorization(page)
        expect(page.get_by_role("heading", name="Trade")).to_be_visible()

    with allure.step(f"2 - '{FILIAL_NAME}' filialini tanlash"):
        switch_filial(page, name=FILIAL_NAME)


def run_user_login(page: Page) -> None:
    """
    Foydalanuvchi (moxir@novatrade) sifatida tizimga kiradi va filial tanlaydi.

    Boshqa test fayllarida:
        from tests.regression.test_auth import run_user_login
        run_user_login(page)
    """
    with allure.step(f"1 - '{USER_LOGIN}' sifatida tizimga kirish"):
        login(page, email=USER_LOGIN, password=USER_PASSWORD)
        dashboard(page)
        expect(page.get_by_role("heading", name="Trade")).to_be_visible()

    with allure.step(f"2 - '{FILIAL_NAME}' filialini tanlash"):
        switch_filial(page, name=FILIAL_NAME)


# ----------------------------------------------------------------------------------------------------------------------
# Pytest test funksiyalari

@allure.title("Admin login va filial tanlash")
def test_admin_login(page: Page) -> None:
    """
    Tekshiradi:
      - admin@novatrade / greenwhite bilan kirish muvaffaqiyatli
      - Dashboard (Trade sarlavhasi) ko'rinadi
      - 'NovaTrade - Toshkent Filiali' tanlanadi va aktiv bo'ladi
    """
    run_admin_login(page)


@allure.title("Foydalanuvchi login va filial tanlash")
def test_user_login(page: Page) -> None:
    """
    Tekshiradi:
      - moxir@novatrade (USER_LOGIN) / 1 bilan kirish muvaffaqiyatli
      - Dashboard (Trade sarlavhasi) ko'rinadi
      - 'NovaTrade - Toshkent Filiali' tanlanadi va aktiv bo'ladi
    """
    run_user_login(page)
