import allure
import pytest
from playwright.sync_api import Page
from tests.smoke.flows.flow_authorization import authorization
from tests.smoke.progress import progress_step
from tests.smoke.test_life_cycle.balance import run_balance
from tests.smoke.test_life_cycle.init_balance import run_init_balance
from tests.smoke.test_setup.test_payment_type import run_payment_type
from tests.smoke.test_setup.test_product import run_product
from tests.smoke.test_setup.test_robot import run_robot
from tests.smoke.test_setup.test_company import run_company
from tests.smoke.test_setup.test_filial import run_filial
from tests.smoke.test_setup.test_legal_person import run_legal_person
from tests.smoke.test_setup.test_license import run_attach_license, run_buy_license
from tests.smoke.test_setup.test_natural_person import run_natural_person, run_natural_person_for_client_1
from tests.smoke.test_setup.test_price_type import run_price_type_uzb
from tests.smoke.test_setup.test_room import run_room, run_room_attachment
from tests.smoke.test_setup.test_sector import run_sector
from tests.smoke.test_setup.test_user import (
    run_user,
    run_user_attach_form,
    run_role,
    run_role_attach_form,
    run_change_password,
)

pytestmark = [
    pytest.mark.user_setup,
    allure.epic("Smoke"),
    allure.feature("Setup"),
    allure.story("Setup Chain"),
]

# ----------------------------------------------------------------------------------------------------------------------

SETUP_RUNNER_TEST = "test_01_user_setup_runner"

def run_setup_authorization(session_page: Page, code, save_data, use_created_company: bool = False):
    save_data("code", code)
    if not use_created_company:
        save_data("company_code", None)
    authorization(session_page)


def run_setup_chain(
    session_page: Page,
    code,
    save_data,
    logger,
    load_data=None,
    scope: str = "smoke",
    company_setup_enabled: bool = False,
) -> None:
    """User setup chainni pytest test funksiyalarini chaqirmasdan bajaradi."""
    if company_setup_enabled:
        with progress_step(
            group="Setup",
            runner=SETUP_RUNNER_TEST,
            test_id="test_company",
            title="00 - Company",
            display="test_company",
        ):
            run_company(session_page, code, save_data)
    with progress_step(
        group="Setup",
        runner=SETUP_RUNNER_TEST,
        test_id="test_01_authorization",
        title="01 - Authorization",
        display="test_01_authorization",
    ):
        run_setup_authorization(session_page, code, save_data, use_created_company=company_setup_enabled)
    with progress_step(
        group="Setup",
        runner=SETUP_RUNNER_TEST,
        test_id="test_02_legal_person",
        title="02 - Legal Person",
        display="test_02_legal_person",
    ):
        run_legal_person(session_page, code, save_data, scope=scope)
    with progress_step(
        group="Setup",
        runner=SETUP_RUNNER_TEST,
        test_id="test_03_filial",
        title="03 - Filial",
        display="test_03_filial",
    ):
        legal_person_code = load_data("legal_person_code") if load_data else f"cod_lg_pw{code}"
        legal_person_name = load_data("legal_person_name") if load_data else None
        run_filial(
            session_page,
            code,
            scope=scope,
            legal_person_code=legal_person_code,
            legal_person_name=legal_person_name,
            save_data=save_data,
        )
    with progress_step(
        group="Setup",
        runner=SETUP_RUNNER_TEST,
        test_id="test_04_room",
        title="04 - Room",
        display="test_04_room",
    ):
        run_room(session_page, code, scope=scope)
    with progress_step(
        group="Setup",
        runner=SETUP_RUNNER_TEST,
        test_id="test_05_robot",
        title="05 - Robot",
        display="test_05_robot",
    ):
        run_robot(session_page, code, scope=scope)
    with progress_step(
        group="Setup",
        runner=SETUP_RUNNER_TEST,
        test_id="test_06_natural_person",
        title="06 - Natural Person",
        display="test_06_natural_person",
    ):
        run_natural_person(session_page, code, scope=scope)
    with progress_step(
        group="Setup",
        runner=SETUP_RUNNER_TEST,
        test_id="test_07_user",
        title="07 - User",
        display="test_07_user",
    ):
        run_user(session_page, code, scope=scope)
    with progress_step(
        group="Setup",
        runner=SETUP_RUNNER_TEST,
        test_id="test_08_user_attach_form",
        title="08 - User Attach Form",
        display="test_08_user_attach_form",
    ):
        run_user_attach_form(session_page, code, scope=scope)
    with progress_step(
        group="Setup",
        runner=SETUP_RUNNER_TEST,
        test_id="test_09_role",
        title="09 - Role",
        display="test_09_role",
    ):
        run_role(session_page, scope=scope)
    with progress_step(
        group="Setup",
        runner=SETUP_RUNNER_TEST,
        test_id="test_10_role_attach_form",
        title="10 - Role Attach Form",
        display="test_10_role_attach_form",
    ):
        run_role_attach_form(session_page, scope=scope)
    with progress_step(
        group="Setup",
        runner=SETUP_RUNNER_TEST,
        test_id="test_11_buy_license",
        title="11 - Buy License",
        display="test_11_buy_license",
    ):
        run_buy_license(session_page, logger, scope=scope)
    with progress_step(
        group="Setup",
        runner=SETUP_RUNNER_TEST,
        test_id="test_12_attach_license",
        title="12 - Attach License",
        display="test_12_attach_license",
    ):
        run_attach_license(session_page, code, logger, scope=scope)
    with progress_step(
        group="Setup",
        runner=SETUP_RUNNER_TEST,
        test_id="test_13_change_password",
        title="13 - Change Password",
        display="test_13_change_password",
    ):
        run_change_password(session_page, code, scope=scope)
    with progress_step(
        group="Setup",
        runner=SETUP_RUNNER_TEST,
        test_id="test_14_price_type",
        title="14 - Price Type",
        display="test_14_price_type",
    ):
        run_price_type_uzb(session_page, code, logger, save_data=save_data, scope=scope)
    with progress_step(
        group="Setup",
        runner=SETUP_RUNNER_TEST,
        test_id="test_15_payment_type",
        title="15 - Payment Type",
        display="test_15_payment_type",
    ):
        run_payment_type(session_page, scope=scope)
    with progress_step(
        group="Setup",
        runner=SETUP_RUNNER_TEST,
        test_id="test_16_sector",
        title="16 - Sector",
        display="test_16_sector",
    ):
        run_sector(session_page, code, scope=scope)
    with progress_step(
        group="Setup",
        runner=SETUP_RUNNER_TEST,
        test_id="test_17_product",
        title="17 - Product",
        display="test_17_product",
    ):
        run_product(session_page, code, scope=scope)
    with progress_step(
        group="Setup",
        runner=SETUP_RUNNER_TEST,
        test_id="test_18_natural_person_for_client_1",
        title="18 - Natural Person For Client_1",
        display="test_18_natural_person_for_client_1",
    ):
        run_natural_person_for_client_1(session_page, code, scope=scope)
    with progress_step(
        group="Setup",
        runner=SETUP_RUNNER_TEST,
        test_id="test_19_room_attachment",
        title="19 - Room Attachment",
        display="test_19_room_attachment",
    ):
        run_room_attachment(session_page, code, scope=scope)
    with progress_step(
        group="Setup",
        runner=SETUP_RUNNER_TEST,
        test_id="test_20_init_balance",
        title="20 - Init Balance",
        display="test_20_init_balance",
    ):
        run_init_balance(session_page, code, scope=scope)
    with progress_step(
        group="Setup",
        runner=SETUP_RUNNER_TEST,
        test_id="test_21_balance",
        title="21 - Balance",
        display="test_21_balance",
    ):
        run_balance(session_page, code, scope=scope)


@allure.title("00 - Company")
def test_00_company(session_page: Page, code, save_data, company_setup_enabled):
    if not company_setup_enabled:
        pytest.skip("Company setup faqat --create-company flagi bilan ishlaydi")
    run_company(session_page, code, save_data)

@allure.title("01 - Authorization")
def test_01_authorization(session_page: Page, code, save_data, company_setup_enabled):
    run_setup_authorization(session_page, code, save_data, use_created_company=company_setup_enabled)

@allure.title("02 - Legal Person")
def test_02_legal_person(session_page: Page, code, save_data, test_scope):
    run_legal_person(session_page, code, save_data, scope=test_scope)

@allure.title("03 - Filial")
def test_03_filial(session_page: Page, code, load_data, save_data, test_scope):
    run_filial(
        session_page,
        code,
        scope=test_scope,
        legal_person_code=load_data("legal_person_code"),
        legal_person_name=load_data("legal_person_name"),
        save_data=save_data,
    )

@allure.title("04 - Room")
def test_04_room(session_page: Page, code, test_scope):
    run_room(session_page, code, scope=test_scope)

@allure.title("05 - Robot")
def test_05_robot(session_page: Page, code, test_scope):
    run_robot(session_page, code, scope=test_scope)

@allure.title("06 - Natural Person")
def test_06_natural_person(session_page: Page, code, test_scope):
    run_natural_person(session_page, code, scope=test_scope)

@allure.title("07 - User")
def test_07_user(session_page: Page, code, test_scope):
    run_user(session_page, code, scope=test_scope)

@allure.title("08 - User Attach Form")
def test_08_user_attach_form(session_page: Page, code, test_scope):
    run_user_attach_form(session_page, code, scope=test_scope)

@allure.title("09 - Role")
def test_09_role(session_page: Page, test_scope):
    run_role(session_page, scope=test_scope)

@allure.title("10 - Role Attach Form")
def test_10_role_attach_form(session_page: Page, test_scope):
    run_role_attach_form(session_page, scope=test_scope)

@allure.title("11 - Buy License")
def test_11_buy_license(session_page: Page, logger, test_scope):
    run_buy_license(session_page, logger, scope=test_scope)

@allure.title("12 - Attach License")
def test_12_attach_license(session_page: Page, code, logger, test_scope):
    run_attach_license(session_page, code, logger, scope=test_scope)

@allure.title("13 - Change Password")
def test_13_change_password(session_page: Page, code, test_scope):
    run_change_password(session_page, code, scope=test_scope)

@allure.title("14 - Price Type")
def test_14_price_type(session_page: Page, code, logger, save_data, test_scope):
    run_price_type_uzb(session_page, code, logger, save_data=save_data, scope=test_scope)

@allure.title("15 - Payment Type")
def test_15_payment_type(session_page: Page, test_scope):
    run_payment_type(session_page, scope=test_scope)

@allure.title("16 - Sector")
def test_16_sector(session_page: Page, code, test_scope):
    run_sector(session_page, code, scope=test_scope)

@allure.title("17 - Product")
def test_17_product(session_page: Page, code, test_scope):
    run_product(session_page, code, scope=test_scope)

@allure.title("18 - Natural Person For Client_1")
def test_18_natural_person_for_client_1(session_page: Page, code, test_scope):
    run_natural_person_for_client_1(session_page, code, scope=test_scope)

@allure.title("19 - Room Attachment")
def test_19_room_attachment(session_page: Page, code, test_scope):
    run_room_attachment(session_page, code, scope=test_scope)

@allure.title("20 - Init Balance")
def test_20_init_balance(session_page: Page, code, test_scope):
    run_init_balance(session_page, code, scope=test_scope)

@allure.title("21 - Balance")
def test_21_balance(session_page: Page, code, test_scope):
    run_balance(session_page, code, scope=test_scope)

# ----------------------------------------------------------------------------------------------------------------------
