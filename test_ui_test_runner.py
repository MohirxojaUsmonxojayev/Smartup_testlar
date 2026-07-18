import inspect
import allure

from tests.ui.test_cashin.test_cashin import test_cashin_add_A
from tests.ui.test_finance.test_currency import test_currency_add_USA
from tests.ui.test_order.order_invoice_report.test_order_invoice_report import \
    test_add_template_for_order_invoice_report
from tests.ui.test_order.order_report.test_order_report import test_check_report_for_order_list, \
    test_check_report_for_order_history_list
from tests.ui.test_order.test_order_return import test_order_return
from tests.ui.test_warehouse.test_supplier import test_add_supplier
from tests.ui.test_warehouse.test_warehouse import test_add_warehouse
from tests.ui.test_purchase.test_extra_cost import test_add_extra_cost
from tests.ui.test_movement.test_movement import test_add_internal_movement
from tests.ui.test_stocktaking.test_stocktaking import test_add_stocktaking
from tests.ui.test_offset.test_offset import test_offset_add_A, test_offset_add_B
from tests.ui.test_rep.integration.spot.test_spot import test_check_report_spot_2d
from tests.ui.test_rep.integration.optimum.test_optimum import test_check_report_optimum
from tests.ui.test_input.test_input import test_add_input, test_add_input_with_extra_cost
from tests.ui.test_rep.integration.cislink.test_cislink import test_check_report_cis_link
from tests.ui.test_license.test_license import test_add_user_license, test_add_purchase_license
from tests.ui.test_rep.integration.saleswork.test_saleswork import test_check_report_sales_work
from tests.ui.test_payment_to_suppliers.test_payment_to_suppliers import test_payment_to_suppliers
from tests.ui.test_reference.test_action import test_add_action_cash_money, test_add_action_terminal
from tests.ui.test_reference.test_client import test_client_add_A, test_client_add_B, test_client_add_C
from tests.ui.test_writeoff.test_writeoff import test_add_write_off, test_check_constructor_report_write_off
from tests.ui.test_reference.test_product import test_product_add_as_product_1, test_product_add_as_product_2
from tests.ui.test_reference.test_legal_person import test_add_legal_person, test_add_legal_person_by_supplier
from tests.ui.test_rep.integration.integration_two.test_integration_two import test_check_report_integration_two
from tests.ui.test_return_supplier.test_return_supplier import test_add_purchase_to_supplier, test_return_to_supplier
from tests.ui.test_rep.integration.integration_three.test_integration_three import test_check_report_integration_three
from tests.ui.test_reference.test_price_type import (
    test_price_type_add_UZB, test_price_type_add_USA, test_price_type_min_amount_on, test_price_type_min_amount_off
)
from tests.ui.test_finance.test_contract import (
    test_add_contract_for_client_A_UZB, test_add_contract_for_client_B_UZB, test_add_contract_for_client_C_USA,
)
from tests.ui.test_order.test_life_cycle import (
    test_adding_permissions_to_user,
    test_check_price_tag,
    test_filial_create,
    test_init_balance,
    test_margin_add,
    test_payment_type_add,
    test_robot_add,
    test_room_add,
    test_room_attachment,
    test_sector_add,
    test_setting_consignment,
    test_setting_prepayment_off,
    test_setting_prepayment_on,
    test_sub_filial_add,
    test_user_change_password,
    test_user_create,
)
from tests.ui.test_order.test_order import (
    test_add_order_for_action,
    test_add_order_for_price_type_USA,
    test_add_order_for_sub_filial,
    test_add_order_with_contract,
    test_min_order_amount,
    test_add_order_with_consignment,
)
from tests.ui.test_order.test_order_change_status import (
    test_change_status_draft_and_archive,
    test_change_status_draft_and_delivered,
    test_change_status_new_and_cancelled,
    test_order_change_status_from_draft_to_cancelled,
)
from tests.ui.test_order.test_order_edit import (
    test_edit_order_for_action,
    test_edit_order_for_price_type_USA,
    test_edit_order_with_consignment,
)
from tests.ui.test_order.test_order_list import test_copy_search_filter_in_order_list
from tests.ui.test_order.test_order_report import (
    test_check_invoice_report_for_order_list,
    test_sales_report_constructor,
)
from tests.ui.test_purchase.test_purchase import (
    test_add_purchase,
    test_add_purchase_with_extra_cost_quantity,
    test_add_purchase_with_extra_cost_sum,
    test_add_purchase_with_extra_cost_weight_brutto,
)
from tests.ui.test_reference.test_natural_person import (
    test_natural_person_add,
    test_natural_person_client_add_A,
    test_natural_person_client_add_B,
    test_natural_person_client_add_C,
)
from utils.test_retry import retry_on_failure
from utils.api_fallback import APIFallbackManager

# ======================================================================================================================

test_cases = [
    # User Setup:
    {"name": "Add Legal Person",     "func": test_add_legal_person,            "retry_count":3, "retry_delay":2, "deps": []},
    {"name": "Add Filial",           "func": test_filial_create,               "deps": ["test_add_legal_person"]},
    # {"name": "Add Room",             "func": test_room_add,                    "deps": ["test_filial_create"]},
    # {"name": "Add Robot",            "func": test_robot_add,                   "deps": ["test_room_add"]},
    # {"name": "Add Sub filial",       "func": test_sub_filial_add,              "deps": ["test_robot_add"]},
    # {"name": "Add Natural Person",   "func": test_natural_person_add,          "deps": []},
    # {"name": "Add User",             "func": test_user_create,                 "deps": ["test_robot_add", "test_natural_person_add"]},
    # {"name": "Add Permissions",      "func": test_adding_permissions_to_user,  "deps": ["test_user_create"]},
    # {"name": "Add User License",     "func": test_add_user_license,            "deps": ["test_user_create"]},
    # {"name": "Add Purchase License", "func": test_add_purchase_license,        "deps": ["test_user_create"]},
    # {"name": "Edit User Password",   "func": test_user_change_password,        "deps": ["test_user_create"]},
    # {"name": "Add Price Type (UZB)", "func": test_price_type_add_UZB,          "deps": ["test_room_add"]},
    # {"name": "Add Price Type (USA)", "func": test_price_type_add_USA,          "deps": ["test_room_add"]},
    # {"name": "Add Payment Type",     "func": test_payment_type_add,            "deps": []},
    # {"name": "Add Sector",           "func": test_sector_add,                  "deps": ["test_room_add"]},
    # {"name": "Add Product-1",        "func": test_product_add_as_product_1,    "deps": ["test_sector_add", "test_price_type_add_UZB", "test_price_type_add_USA"]},
    # {"name": "Check Price Tag",      "func": test_check_price_tag,             "deps": ["test_price_type_add_UZB"]},
    # {"name": "Add Currency",         "func": test_currency_add_USA,            "deps": []},
    # {"name": "Add Margin",           "func": test_margin_add,                  "deps": []},
    # {"name": "Add Natural Person-A", "func": test_natural_person_client_add_A, "deps": []},
    # {"name": "Add Natural Person-B", "func": test_natural_person_client_add_B, "deps": []},
    # {"name": "Add Natural Person-C", "func": test_natural_person_client_add_C, "deps": []},
    # {"name": "Add Client-A",         "func": test_client_add_A,                "deps": ["test_natural_person_client_add_A"]},
    # {"name": "Add Client-B",         "func": test_client_add_B,                "deps": ["test_natural_person_client_add_B"]},
    # {"name": "Add Client-C",         "func": test_client_add_C,                "deps": ["test_natural_person_client_add_C"]},
    # {"name": "Attachment Room",      "func": test_room_attachment,             "deps": ["test_robot_add",
    #                                                                                     "test_price_type_add_UZB", "test_price_type_add_USA",
    #                                                                                     "test_payment_type_add", "test_sector_add", "test_margin_add",
    #                                                                                     "test_client_add_A", "test_client_add_B", "test_client_add_C"]},
    # {"name": "Add Init Balance",     "func": test_init_balance,                "deps": ["test_room_attachment", "test_product_add_as_product_1"]},
    #
    # # (Group-A) Order with Consignment:
    # {"name": "(Group-A) Add Contract For Client UZB",           "func": test_add_contract_for_client_A_UZB,               "deps": ["test_client_add_A", "test_price_type_add_UZB"]},
    # {"name": "(Group-A) On Setting Consignment",                "func": test_setting_consignment,                         "deps": []},
    # {"name": "(Group-A) Add Order With Consignment",            "func": test_add_order_with_consignment,                  "deps": ["test_setting_consignment", "test_add_contract_for_client_A_UZB"]},
    # {"name": "(Group-A) Check Report For Order List",           "func": test_check_report_for_order_list,                 "deps": ["test_add_order_with_consignment"]},
    # {"name": "(Group-A) Edit Order With Consignment",           "func": test_edit_order_with_consignment,                 "deps": ["test_add_order_with_consignment"]},
    # {"name": "(Group-A) Copy Search Filter In Order List",      "func": test_copy_search_filter_in_order_list,            "deps": ["test_edit_order_with_consignment"]},
    # {"name": "(Group-A) Sales Report Constructor Demo",         "func": test_sales_report_constructor,                    "deps": ["test_add_order_with_consignment"]},
    # {"name": "(Group-A) Change Status From Draft To Cancelled", "func": test_order_change_status_from_draft_to_cancelled, "deps": ["test_copy_search_filter_in_order_list"]},
    # {"name": "(Group-A) Check Report For Order History List",   "func": test_check_report_for_order_history_list,         "deps": ["test_order_change_status_from_draft_to_cancelled"]},
    # {"name": "(Group-A) Add Cashin-A",                          "func": test_cashin_add_A,                                "deps": ["test_payment_type_add", "test_client_add_A"]},
    # {"name": "(Group-A) Add Offset-A",                          "func": test_offset_add_A,                                "deps": ["test_cashin_add_A"]},
    #
    # # (Group-B) Order with Contract:
    # {"name": "(Group-B) Add Contract For Client UZB-B",     "func": test_add_contract_for_client_B_UZB,   "deps": ["test_client_add_B", "test_price_type_add_UZB"]},
    # {"name": "(Group-B) Add Order With Contract-B",         "func": test_add_order_with_contract,         "deps": ["test_add_contract_for_client_B_UZB"]},
    # {"name": "(Group-B) Change Status Draft And Archive-B", "func": test_change_status_draft_and_archive, "deps": ["test_add_order_with_contract"]},
    # {"name": "(Group-B) Add Offset-B",                      "func": test_offset_add_B,                    "deps": ["test_change_status_draft_and_archive"]},
    #
    # # (Group-C) Order with Price Type USA:
    # {"name": "(Group-C) Add Contract For Client USA-C",   "func": test_add_contract_for_client_C_USA,      "deps": ["test_client_add_C", "test_price_type_add_USA"]},
    # {"name": "(Group-C) Add Order With Price Type-C",     "func": test_add_order_for_price_type_USA,       "deps": ["test_add_contract_for_client_C_USA"]},
    # {"name": "(Group-C) On Test Setting Prepayment",      "func": test_setting_prepayment_on,              "deps": []},
    # {"name": "(Group-C) Edit Order For Price Type USA-C", "func": test_edit_order_for_price_type_USA,      "deps": ["test_setting_prepayment_on", "test_add_order_for_price_type_USA"]},
    # {"name": "(Group-C) Off Test Setting Prepayment",     "func": test_setting_prepayment_off,             "deps": []},
    #
    # {"name": "(Group-C) Price Type Min Amount On",        "func": test_price_type_min_amount_on,           "deps": ["test_price_type_add_UZB"]},
    # {"name": "(Group-C) Min Order Amount",                "func": test_min_order_amount,                   "deps": ["test_price_type_min_amount_on"]},
    # {"name": "(Group-C) Price Type Min Amount Off",       "func": test_price_type_min_amount_off,          "deps": ["test_min_order_amount"]},
    #
    # # (Group-D) Order with Sub Filial:
    # {"name": "(Group-D) Add Template For Order Invoice Report", "func": test_add_template_for_order_invoice_report, "deps": ["test_sub_filial_add"]},
    # {"name": "(Group-D) Add Order For Sub Filial Select-C",     "func": test_add_order_for_sub_filial,              "deps": ["test_sub_filial_add", "test_add_contract_for_client_C_USA"]},
    # {"name": "(Group-D) Check Invoice Report For Order List-C", "func": test_check_invoice_report_for_order_list,   "deps": ["test_add_template_for_order_invoice_report", "test_add_order_for_sub_filial"]},
    # {"name": "(Group-D) Change Status Draft And Cancelled-C",   "func": test_change_status_new_and_cancelled,       "deps": ["test_add_order_for_sub_filial"]},
    #
    # # (Group-I) Order with Action:
    # {"name": "(Group-I) Add Action Cash Money",               "func": test_add_action_cash_money,             "deps": ["test_room_attachment"]},
    # {"name": "(Group-I) Add Action Terminal",                 "func": test_add_action_terminal,               "deps": ["test_room_attachment"]},
    # {"name": "(Group-I) Add Order For Action-C",              "func": test_add_order_for_action,              "deps": ["test_add_action_cash_money", "test_add_action_terminal"]},
    # {"name": "(Group-I) Edit Order For Action-C",             "func": test_edit_order_for_action,             "deps": ["test_add_order_for_action"]},
    # {"name": "(Group-I) Change Status Draft And Delivered-C", "func": test_change_status_draft_and_delivered, "deps": ["test_edit_order_for_action"]},
    # {"name": "(Group-I) Order Return",                        "func": test_order_return,                      "deps": ["test_change_status_draft_and_delivered"]},
    #
    # # Purchase and Extra Cost:
    # {"name": "Add Legal Person By Supplier",               "func": test_add_legal_person_by_supplier,               "deps": []},
    # {"name": "Add Supplier",                               "func": test_add_supplier,                               "deps": ["test_add_legal_person_by_supplier"]},
    # {"name": "Add Product-2",                              "func": test_product_add_as_product_2,                   "deps": ["test_sector_add", "test_price_type_add_UZB", "test_price_type_add_USA"]},
    # {"name": "Add Purchase",                               "func": test_add_purchase,                               "deps": ["test_add_supplier", "test_product_add_as_product_2"]},
    # {"name": "Add Extra Cost",                             "func": test_add_extra_cost,                             "deps": ["test_add_purchase"]},
    # {"name": "Add Purchase With Extra Cost Sum",           "func": test_add_purchase_with_extra_cost_sum,           "deps": ["test_add_purchase", "test_add_extra_cost"]},
    # {"name": "Add Purchase With Extra Cost Quantity",      "func": test_add_purchase_with_extra_cost_quantity,      "deps": ["test_add_purchase", "test_add_extra_cost"]},
    # {"name": "Add Purchase With Extra Cost Weight Brutto", "func": test_add_purchase_with_extra_cost_weight_brutto, "deps": ["test_add_purchase", "test_add_extra_cost"]},
    #
    # # Input with Purchase
    # {"name": "Add Input",                          "func": test_add_input,                          "deps": ["test_add_purchase"]},
    # {"name": "Add Input With Extra Cost",          "func": test_add_input_with_extra_cost,          "deps": ["test_add_purchase_with_extra_cost_sum"]},
    #
    # # Return Supplier with Purchase
    # {"name": "Add Purchase To Supplier",           "func": test_add_purchase_to_supplier,           "deps": ["test_add_purchase"]},
    # {"name": "Add Return To Supplier",             "func": test_return_to_supplier,                 "deps": ["test_add_purchase_to_supplier"]},
    #
    # # Internal Movement
    # {"name": "Add Warehouse",                      "func": test_add_warehouse,                      "deps": ["test_room_add"]},
    # {"name": "Add Internal Movement",              "func": test_add_internal_movement,              "deps": ["test_add_warehouse"]},
    #
    # # Write Off
    # {"name": "Add Write Off",                      "func": test_add_write_off,                      "deps": ["test_product_add_as_product_1"]},
    # {"name": "Check Constructor Report Write Off", "func": test_check_constructor_report_write_off, "deps": ["test_add_write_off"]},
    #
    # # Stocktaking
    # {"name": "Add Stocktaking",                    "func": test_add_stocktaking,                    "deps": ["test_product_add_as_product_1", "test_product_add_as_product_2"]},
    #
    # # Payment To Suppliers
    # {"name": "Add Payment To Suppliers",           "func": test_payment_to_suppliers,               "deps": ["test_add_supplier", "test_payment_type_add"]},
    #
    # # Integration Report:
    # {"name": "Check Report CisLink",               "func": test_check_report_cis_link,              "deps": ["test_price_type_add_UZB"]},
    # {"name": "Check Report Integration Three",     "func": test_check_report_integration_three,     "deps": []},
    # {"name": "Check Report Integration Two",       "func": test_check_report_integration_two,       "deps": ["test_price_type_add_UZB"]},
    # {"name": "Check Report Optimum",               "func": test_check_report_optimum,               "deps": ["test_filial_create"]},
    # {"name": "Check Report Sales Work",            "func": test_check_report_sales_work,            "deps": []},
    # {"name": "Check Report Spot 2d",               "func": test_check_report_spot_2d,               "deps": []},
]

# ======================================================================================================================

def pytest_generate_tests(metafunc):
    """Pytest parametrize uchun test case'larni generate qilish"""
    if "runner_case" in metafunc.fixturenames:
        metafunc.parametrize("runner_case", test_cases, ids=[c["name"] for c in test_cases])

# ======================================================================================================================

def test_run_with_state(runner_case, driver, test_data, save_data, load_data, assertions, soft_assertions):
    func = runner_case["func"]
    retry_count = runner_case.get("retry_count", 3)
    retry_delay = runner_case.get("retry_delay", 2)
    dependencies = runner_case.get("deps", [])
    alternative_test = runner_case.get("alternative_test", None)

    allure.dynamic.title(runner_case["name"])

    # Retry decorator bilan testni o'rash
    wrapped_func = retry_on_failure(
        retry_count=retry_count,
        retry_delay=retry_delay,
        dependencies=dependencies
    )(func)

    # Kerakli fixture'larni to'plash
    kwargs = _get_required_fixtures(func, {
        'driver': driver,
        'test_data': test_data,
        'save_data': save_data,
        'load_data': load_data,
        'assertions': assertions,
        'soft_assertions': soft_assertions,
    })

    try:
        wrapped_func(**kwargs)

    except Exception as ui_error:
        if alternative_test:
            print(f"\n{'=' * 80}")
            print(f"⚠️  UI TEST FAILED: {func.__name__}")
            print(f"{'=' * 80}")
            print(f"🔍 Alternative API test mavjud: {alternative_test.__name__}")
            print(f"🔄 API fallback mexanizmi ishga tushmoqda...\n")

            # API Fallback Manager yaratish
            fallback_manager = APIFallbackManager()

            # API testni ishga tushirish
            api_result = fallback_manager.execute_api_fallback(
                ui_test_name=func.__name__,
                api_test_func=alternative_test,
                save_data=save_data,
                load_data=load_data,
                ui_attempts=retry_count
            )

            # API test natijasini tekshirish
            if api_result and api_result["status"] == "PASSED":
                print(f"✅ Test davom ettirildi API ma'lumotlari bilan!")

                try:
                    allure.attach(
                        f"UI test failed but API fallback ({alternative_test.__name__}) passed. "
                        f"Continuing tests with API data.",
                        name="API Fallback Success",
                        attachment_type=allure.attachment_type.TEXT
                    )
                except:
                    pass

                return
            else:
                print(f"❌ API test ham fail bo'ldi!")
                print(f"🛑 Backend muammosi - test to'xtatiladi\n")

                # Allure reportga ma'lumot qo'shish
                try:
                    allure.attach(
                        f"Both UI and API ({alternative_test.__name__}) tests failed. "
                        f"Backend issue detected.",
                        name="API Fallback Failed",
                        attachment_type=allure.attachment_type.TEXT
                    )
                except:
                    pass

                # Original UI xatolikni raise qilamiz
                raise ui_error
        else:
            # Alternative test yo'q - xatolikni raise qilamiz
            raise ui_error

# ======================================================================================================================

def _get_required_fixtures(func, available_fixtures):
    """Test funksiyasi uchun kerakli fixture'larni ajratib olish"""
    sig = inspect.signature(func)

    required = {}
    for param_name in sig.parameters.keys():
        if param_name in available_fixtures:
            required[param_name] = available_fixtures[param_name]

    return required

# ======================================================================================================================
