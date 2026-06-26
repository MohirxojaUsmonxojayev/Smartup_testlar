import allure
from playwright.sync_api import Page, expect

from tests.regression.test_auth import run_user_login
from utils.soft_assert import SoftAssert

pytestmark = [
    allure.epic("Regression"),
    allure.feature("Formalar ochilishi"),
    allure.story("Barcha bo'limlar"),
]

# ----------------------------------------------------------------------------------------------------------------------


def run_check_forms_opening(page: Page, soft: SoftAssert) -> None:
    """
    Barcha bo'limlardagi formalar xatosiz ochilishini tekshiradi.
    Soft assert — xato bo'lsa to'xtamaydi, hammasini tekshirib chiqadi.

    Boshqa testlarda chaqirish:
        from tests.regression.test_check_forms_opening import run_check_forms_opening
        run_check_forms_opening(page, soft)
    """

    # ── Login ──────────────────────────────────────────────────────────────

    with allure.step("1 - Tizimga kirish va filial tanlash"):
        run_user_login(page)

    # Login dan keyingi haqiqiy URL (kompaniya tokeni bilan) — navigation reset uchun
    _home_url = page.url

    # ── Главное bo'limi ────────────────────────────────────────────────────

    with allure.step("2 - [Главное] Организации — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Главное").click()
        page.get_by_role("link", name="Организации").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Главное] Организации — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("3 - [Главное] Пользователи — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Главное").click()
        page.get_by_role("link", name="Пользователи").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Главное] Пользователи — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("4 - [Главное] Проекты — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Главное").click()
        page.get_by_role("link", name="Проекты").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Главное] Проекты — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("5 - [Главное] Шаблоны накладных — 'Добавить' ko'rinadi"):
        page.get_by_role("link", name="Главное").click()
        page.get_by_role("link", name="Шаблоны накладных").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Добавить")
        except Exception as e:
            soft.check(False,
                f"❌ [Главное] Шаблоны накладных — 'Добавить' topilmadi | {type(e).__name__}")

    with allure.step("6 - [Главное] Настройки системы — 'Сохранить' ko'rinadi"):
        page.get_by_role("link", name="Главное").click()
        page.get_by_role("link", name="Настройки системы").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Сохранить")
        except Exception as e:
            soft.check(False,
                f"❌ [Главное] Настройки системы — 'Сохранить' topilmadi | {type(e).__name__}")

    with allure.step("7 - [Главное] История изменений — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Главное").click()
        page.get_by_role("link", name="История изменений").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Главное] История изменений — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("8 - [Главное] Шаги визита — jadvalda 'Роль' ustuni ko'rinadi"):
        page.get_by_role("link", name="Главное").click()
        page.get_by_role("link", name="Шаги визита").click()
        try:
            expect(page.locator("b-grid")).to_contain_text("Роль")
        except Exception as e:
            soft.check(False,
                f"❌ [Главное] Шаги визита — jadvalda 'Роль' ustuni topilmadi | {type(e).__name__}")

    with allure.step("9 - [Главное] Настройки интеграции со сторонним ПО — 'Сохранить' ko'rinadi"):
        page.get_by_role("link", name="Главное").click()
        page.get_by_role("link", name="Настройки интеграции со сторонним ПО").click()
        try:
            expect(page.locator("form")).to_contain_text("Сохранить")
        except Exception as e:
            soft.check(False,
                f"❌ [Главное] Настройки интеграции со сторонним ПО — 'Сохранить' topilmadi | {type(e).__name__}")

    with allure.step("10 - [Главное] Объекты — jadvalda 'Объект' ustuni ko'rinadi"):
        page.get_by_role("button", name="Главное").click()
        page.get_by_role("menuitem", name="Объекты").click()
        try:
            expect(page.locator("b-grid")).to_contain_text("Объект")
        except Exception as e:
            soft.check(False,
                f"❌ [Главное] Объекты — jadvalda 'Объект' ustuni topilmadi | {type(e).__name__}")

    with allure.step("11 - [Главное] Динамичные поля — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Главное").click()
        page.get_by_role("link", name="Динамичные поля").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Главное] Динамичные поля — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("12 - [Главное] Отчeты — 'Дополнительно' ko'rinadi"):
        page.get_by_role("link", name="Главное").click()
        page.get_by_role("link", name="Отчeты").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Дополнительно")
        except Exception as e:
            soft.check(False,
                f"❌ [Главное] Отчeты — 'Дополнительно' topilmadi | {type(e).__name__}")

    # ── Продажа bo'limi ────────────────────────────────────────────────────

    with allure.step("13 - [Продажа] Визиты — sarlavhada 'Визиты' ko'rinadi"):
        page.get_by_role("link", name="Продажа", exact=True).click()
        page.get_by_role("link", name="Визиты").click()
        try:
            expect(page.get_by_role("heading")).to_contain_text("Визиты")
        except Exception as e:
            soft.check(False,
                f"❌ [Продажа] Визиты — sarlavhada 'Визиты' topilmadi | {type(e).__name__}")

    with allure.step("14 - [Продажа] Архив визитов — sarlavhada 'Архив визитов' ko'rinadi"):
        page.get_by_role("link", name="Продажа").click()
        page.get_by_role("link", name="Архив визитов").click()
        try:
            expect(page.get_by_role("heading")).to_contain_text("Архив визитов")
        except Exception as e:
            soft.check(False,
                f"❌ [Продажа] Архив визитов — sarlavhada 'Архив визитов' topilmadi | {type(e).__name__}")

    with allure.step("15 - [Продажа] Отслеживание пользователей — 'Обновить' ko'rinadi"):
        page.get_by_role("link", name="Продажа").click()
        page.get_by_role("link", name="Отслеживание пользователей").click()
        try:
            expect(page.get_by_role("complementary")).to_contain_text("Обновить")
        except Exception as e:
            soft.check(False,
                f"❌ [Продажа] Отслеживание пользователей — 'Обновить' topilmadi | {type(e).__name__}")

    with allure.step("16 - [Продажа] Отслеживание мобильных представителей — 'Обновить' ko'rinadi"):
        page.get_by_role("button", name="Продажа").click()
        page.get_by_role("menuitem", name="Отслеживание мобильных представителей").click()
        try:
            expect(page.locator("trade-lib-tph-user-tracking")).to_contain_text("Обновить")
        except Exception as e:
            soft.check(False,
                f"❌ [Продажа] Отслеживание мобильных представителей — 'Обновить' topilmadi | {type(e).__name__}")

    with allure.step("17 - [Продажа] Планирование визитов — 'Импорт' ko'rinadi"):
        page.get_by_role("button", name="Продажа").click()
        page.get_by_role("menuitem", name="Планирование визитов").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Импорт")
        except Exception as e:
            soft.check(False,
                f"❌ [Продажа] Планирование визитов — 'Импорт' topilmadi | {type(e).__name__}")

    with allure.step("18 - [Продажа] Планы — sahifada 'Планы' ko'rinadi"):
        page.get_by_role("link", name="Продажа").click()
        page.get_by_role("link", name="Планы").click()
        try:
            expect(page.locator("#kt_content")).to_contain_text("Планы")
        except Exception as e:
            soft.check(False,
                f"❌ [Продажа] Планы — sahifada 'Планы' topilmadi | {type(e).__name__}")

    with allure.step("19 - [Продажа] Отслеживание оборудования — 'Архивировать успешные' ko'rinadi"):
        page.get_by_role("link", name="Продажа").click()
        page.get_by_role("link", name="Отслеживание оборудования").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Архивировать успешные")
        except Exception as e:
            soft.check(False,
                f"❌ [Продажа] Отслеживание оборудования — 'Архивировать успешные' topilmadi | {type(e).__name__}")

    with allure.step("20 - [Продажа] Фото- и видеоотчеты — 'Применить' ko'rinadi"):
        page.get_by_role("link", name="Продажа").click()
        page.get_by_role("link", name="Фото- и видеоотчеты").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Применить")
        except Exception as e:
            soft.check(False,
                f"❌ [Продажа] Фото- и видеоотчеты — 'Применить' topilmadi | {type(e).__name__}")

    with allure.step("21 - [Продажа] Заказы — 'Создать' tugmasi ko'rinadi"):
        page.get_by_role("link", name="Продажа").click()
        page.get_by_role("link", name="Заказы", exact=True).click()
        try:
            expect(page.locator("#trade81-button-add")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Продажа] Заказы — 'Создать' tugmasi topilmadi | {type(e).__name__}")

    with allure.step("22 - [Продажа] Архив заказов — sahifada 'Архив заказов' ko'rinadi"):
        page.get_by_role("link", name="Продажа").click()
        page.get_by_role("link", name="Архив заказов").click()
        try:
            expect(page.locator("#kt_content")).to_contain_text("Архив заказов")
        except Exception as e:
            soft.check(False,
                f"❌ [Продажа] Архив заказов — sahifada 'Архив заказов' topilmadi | {type(e).__name__}")

    with allure.step("23 - [Продажа] Отмененные заказы — sarlavhada ko'rinadi"):
        page.get_by_role("link", name="Продажа").click()
        page.get_by_role("link", name="Отмененные заказы").click()
        try:
            expect(page.get_by_role("heading")).to_contain_text("Отмененные заказы")
        except Exception as e:
            soft.check(False,
                f"❌ [Продажа] Отмененные заказы — sarlavhada topilmadi | {type(e).__name__}")

    with allure.step("24 - [Продажа] Возвраты — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Продажа").click()
        page.get_by_role("link", name="Возвраты").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Продажа] Возвраты — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("25 - [Продажа] Взаиморасчеты с клиентами — 'Взаиморасчет' ko'rinadi"):
        page.get_by_role("link", name="Продажа").click()
        page.get_by_role("link", name="Взаиморасчеты с клиентами").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Взаиморасчет")
        except Exception as e:
            soft.check(False,
                f"❌ [Продажа] Взаиморасчеты с клиентами — 'Взаиморасчет' topilmadi | {type(e).__name__}")

    with allure.step("26 - [Продажа] Лиды — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Продажа").click()
        page.get_by_role("link", name="Лиды").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Продажа] Лиды — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("27 - [Продажа] Дашборд — 'Сформировать' ko'rinadi"):
        page.get_by_role("link", name="Продажа").click()
        page.get_by_role("link", name="Дашборд", exact=True).click()
        try:
            expect(page.locator("b-page")).to_contain_text("Сформировать")
        except Exception as e:
            soft.check(False,
                f"❌ [Продажа] Дашборд — 'Сформировать' topilmadi | {type(e).__name__}")

    with allure.step("28 - [Продажа] Дашборд по продажам — 'Сформировать' ko'rinadi"):
        page.get_by_role("link", name="Продажа").click()
        page.get_by_role("link", name="Дашборд по продажам", exact=True).click()
        try:
            expect(page.locator("b-page")).to_contain_text("Сформировать")
        except Exception as e:
            soft.check(False,
                f"❌ [Продажа] Дашборд по продажам — 'Сформировать' topilmadi | {type(e).__name__}")

    with allure.step("29 - [Продажа] Конструктор отчетов по продажам — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Продажа").click()
        page.get_by_role("link", name="Конструктор отчетов по продажам").click()
        try:
            page.wait_for_selector(
                "app-mbi-report-constructor, b-page", timeout=15000
            )
        except Exception:
            pass
        try:
            angular = page.locator("app-mbi-report-constructor")
            if angular.count() > 0:
                expect(angular).to_contain_text("Параметры", timeout=10000)
            else:
                expect(page.locator("b-page")).to_contain_text("Параметры", timeout=10000)
        except Exception as e:
            soft.check(False,
                f"❌ [Продажа] Конструктор отчетов по продажам — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("30 - [Продажа] Общий отчет по продажам (организации) — 'Параметры' ko'rinadi"):
        try:
            page.goto(_home_url, wait_until="domcontentloaded", timeout=8000)
        except Exception:
            pass
        page.get_by_role("link", name="Продажа").click()
        page.get_by_role("link", name="Общий отчет по продажам (организации)").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Продажа] Общий отчет по продажам (организации) — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("31 - [Продажа] Задолженность покупателей по срокам задолженности — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Продажа").click()
        page.get_by_role("link", name="Задолженность покупателей по срокам задолженности").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Продажа] Задолженность покупателей по срокам задолженности — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("32 - [Продажа] Расчет бонуса за оплату долга — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Продажа").click()
        page.get_by_role("link", name="Расчет бонуса за оплату долга").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Продажа] Расчет бонуса за оплату долга — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("33 - [Продажа] Коммерческий дашборд — 'Экспорт' ko'rinadi"):
        page.get_by_role("link", name="Продажа").click()
        page.get_by_role("link", name="Коммерческий дашборд").click()
        try:
            expect(page.locator("smt-dropdown-button")).to_contain_text("Экспорт")
        except Exception as e:
            soft.check(False,
                f"❌ [Продажа] Коммерческий дашборд — 'Экспорт' topilmadi | {type(e).__name__}")

    with allure.step("34 - [Продажа] Конструктор отчётов по визитам — 'Просмотр' ko'rinadi"):
        page.get_by_role("button", name="Продажа").click()
        page.get_by_role("menuitem", name="Конструктор отчётов по визитам").click()
        try:
            page.wait_for_selector(
                "app-mbi-report-constructor, b-page", timeout=15000
            )
        except Exception:
            pass
        try:
            angular = page.locator("app-mbi-report-constructor")
            if angular.count() > 0:
                expect(angular).to_contain_text("Просмотр", timeout=10000)
            else:
                expect(page.locator("b-page")).to_contain_text("Просмотр", timeout=10000)
        except Exception as e:
            soft.check(False,
                f"❌ [Продажа] Конструктор отчётов по визитам — 'Просмотр' topilmadi | {type(e).__name__}")

    with allure.step("35 - [Продажа] Отчет по визитам — 'Параметры' ko'rinadi"):
        try:
            page.goto(_home_url, wait_until="domcontentloaded", timeout=8000)
        except Exception:
            pass
        page.get_by_role("link", name="Продажа").click()
        page.get_by_role("link", name="Отчет по визитам").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Продажа] Отчет по визитам — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("36 - [Продажа] Анализ маршрута — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Продажа").click()
        page.get_by_role("link", name="Анализ маршрута").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Продажа] Анализ маршрута — 'Параметры' topilmadi | {type(e).__name__}")

    # ── Склад bo'limi ──────────────────────────────────────────────────────

    with allure.step("37 - [Склад] Ввод начальных остатков ТМЦ — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Ввод начальных остатков ТМЦ").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Ввод начальных остатков ТМЦ — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("38 - [Склад] Запросы на закупку — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Запросы на закупку").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Запросы на закупку — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("39 - [Склад] Заказы на закупку — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Склад").click()
        page.locator("#kt_header_menu").get_by_role("link", name="Заказы на закупку").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Заказы на закупку — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("40 - [Склад] Закупки — 'Создать' tugmasi ko'rinadi"):
        page.get_by_role("link", name="Склад").click()
        page.locator("#kt_header_menu").get_by_role("link", name="Закупки", exact=True).click()
        try:
            expect(page.locator("#anor288-button-add")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Закупки — 'Создать' tugmasi topilmadi | {type(e).__name__}")

    with allure.step("41 - [Склад] Дополнительные расходы — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Склад", exact=True).click()
        page.get_by_role("link", name="Дополнительные расходы").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Дополнительные расходы — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("42 - [Склад] Поступления ТМЦ на склад — 'Создать' tugmasi ko'rinadi"):
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Поступления ТМЦ на склад").click()
        try:
            expect(page.locator("#anor113-button-add")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Поступления ТМЦ на склад — 'Создать' tugmasi topilmadi | {type(e).__name__}")

    with allure.step("43 - [Склад] Возвраты поставщику — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Возвраты поставщику").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Возвраты поставщику — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("44 - [Склад] Списания — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Списания").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Списания — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("45 - [Склад] Инвентаризации — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Склад").click()
        page.locator("#kt_header_menu").get_by_role("link", name="Инвентаризации").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Инвентаризации — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("46 - [Склад] Переоценки себестоимости ТМЦ — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Склад", exact=True).click()
        page.get_by_role("link", name="Переоценки себестоимости ТМЦ").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Переоценки себестоимости ТМЦ — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("47 - [Склад] Взаиморасчеты с поставщиками — 'Взаиморасчет' ko'rinadi"):
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Взаиморасчеты с поставщиками").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Взаиморасчет")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Взаиморасчеты с поставщиками — 'Взаиморасчет' topilmadi | {type(e).__name__}")

    with allure.step("48 - [Склад] Пересчет приходных цен — 'Скорректировать' ko'rinadi"):
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Пересчет приходных цен").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Скорректировать")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Пересчет приходных цен — 'Скорректировать' topilmadi | {type(e).__name__}")

    with allure.step("49 - [Склад] Прогноз для закупки — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Прогноз для закупки").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Прогноз для закупки — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("50 - [Склад] Запросы на внутр. перемещения — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Запросы на внутр. перемещения").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Запросы на внутр. перемещения — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("51 - [Склад] Внутренние перемещения — 'Создать' tugmasi ko'rinadi"):
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Внутренние перемещения").click()
        try:
            expect(page.locator("#anor132-button-add")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Внутренние перемещения — 'Создать' tugmasi topilmadi | {type(e).__name__}")

    with allure.step("52 - [Склад] Запросы на межорг. перемещ.: отправка — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Запросы на межорг. перемещ.: отправка").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Запросы на межорг. перемещ.: отправка — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("53 - [Склад] Запросы на межорг. перемещ.: прием — sarlavha ko'rinadi"):
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Запросы на межорг. перемещ.: прием").click()
        try:
            expect(page.get_by_role("heading")).to_contain_text("Запросы на межорг. перемещ.: прием")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Запросы на межорг. перемещ.: прием — sarlavha topilmadi | {type(e).__name__}")

    with allure.step("54 - [Склад] Межорг. перемещения: отправка — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Межорг. перемещения: отправка").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Межорг. перемещения: отправка — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("55 - [Склад] Межорг. перемещения: прием — sahifada ko'rinadi"):
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Межорг. перемещения: прием").click()
        try:
            expect(page.locator("#kt_content")).to_contain_text("Межорг. перемещения: прием")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Межорг. перемещения: прием — sahifada topilmadi | {type(e).__name__}")

    with allure.step("56 - [Склад] Архив межорг. перемещений — sarlavha ko'rinadi"):
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Архив межорг. перемещений").click()
        try:
            expect(page.get_by_role("heading")).to_contain_text("Архив межорг. перемещений")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Архив межорг. перемещений — sarlavha topilmadi | {type(e).__name__}")

    with allure.step("57 - [Склад] Отмененные межорг. перемещения — sarlavha ko'rinadi"):
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Отмененные межорг. перемещения").click()
        try:
            expect(page.get_by_role("heading")).to_contain_text("Отмененные межорг. перемещения")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Отмененные межорг. перемещения — sarlavha topilmadi | {type(e).__name__}")

    with allure.step("58 - [Склад] Поставщики — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Поставщики").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Поставщики — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("59 - [Склад] Автотранспорт — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Автотранспорт").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Автотранспорт — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("60 - [Склад] Склады — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Склады").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Склады — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("61 - [Склад] Остатки ТМЦ — 'Детали' ko'rinadi"):
        page.get_by_role("link", name="Склад", exact=True).click()
        page.get_by_role("link", name="Остатки ТМЦ").click()
        try:
            expect(page.locator("t")).to_contain_text("Детали")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Остатки ТМЦ — 'Детали' topilmadi | {type(e).__name__}")

    with allure.step("62 - [Склад] Логистика — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Логистика").click()
        try:
            expect(page.locator("smt-data-table")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Логистика — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("63 - [Склад] Рекламное оборудование — sarlavha ko'rinadi"):
        page.get_by_role("button", name="Склад").click()
        page.get_by_role("menuitem", name="Рекламное оборудование").click()
        try:
            expect(page.get_by_role("heading")).to_contain_text("Рекламное оборудование")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Рекламное оборудование — sarlavha topilmadi | {type(e).__name__}")

    with allure.step("64 - [Склад] Материальный отчет — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Материальный отчет").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Материальный отчет — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("65 - [Склад] Общий отчет по складам — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Общий отчет по складам").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Общий отчет по складам — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("66 - [Склад] Конструктор отчетов по внутр. перемещениям — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Конструктор отчетов по внутр. перемещениям").click()
        try:
            page.wait_for_selector(
                "app-mbi-report-constructor, b-page", timeout=15000
            )
        except Exception:
            pass
        try:
            angular = page.locator("app-mbi-report-constructor")
            if angular.count() > 0:
                expect(angular).to_contain_text("Параметры", timeout=10000)
            else:
                expect(page.locator("b-page")).to_contain_text("Параметры", timeout=10000)
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Конструктор отчетов по внутр. перемещениям — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("67 - [Склад] Конструктор отчетов по запросам на закуп — 'Просмотр' ko'rinadi"):
        try:
            page.goto(_home_url, wait_until="domcontentloaded", timeout=8000)
        except Exception:
            pass
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Конструктор отчетов по запросам на закуп").click()
        try:
            page.wait_for_selector(
                "app-mbi-report-constructor, b-page", timeout=15000
            )
        except Exception:
            pass
        try:
            angular = page.locator("app-mbi-report-constructor")
            if angular.count() > 0:
                expect(angular).to_contain_text("Просмотр", timeout=10000)
            else:
                expect(page.locator("b-page")).to_contain_text("Просмотр", timeout=10000)
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Конструктор отчетов по запросам на закуп — 'Просмотр' topilmadi | {type(e).__name__}")

    with allure.step("68 - [Склад] Конструктор отчетов по закупкам — 'Просмотреть' ko'rinadi"):
        try:
            page.goto(_home_url, wait_until="domcontentloaded", timeout=8000)
        except Exception:
            pass
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Конструктор отчетов по закупкам").click()
        try:
            page.wait_for_selector(
                "app-mbi-report-constructor, b-page", timeout=15000
            )
        except Exception:
            pass
        try:
            angular = page.locator("app-mbi-report-constructor")
            if angular.count() > 0:
                expect(angular).to_contain_text("Просмотреть", timeout=10000)
            else:
                expect(page.locator("b-page")).to_contain_text("Просмотреть", timeout=10000)
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Конструктор отчетов по закупкам — 'Просмотреть' topilmadi | {type(e).__name__}")

    with allure.step("69 - [Склад] Конструктор отчетов по поступлениям — 'Просмотреть' ko'rinadi"):
        try:
            page.goto(_home_url, wait_until="domcontentloaded", timeout=8000)
        except Exception:
            pass
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Конструктор отчетов по поступлениям").click()
        try:
            page.wait_for_selector(
                "app-mbi-report-constructor, b-page", timeout=15000
            )
        except Exception:
            pass
        try:
            angular = page.locator("app-mbi-report-constructor")
            if angular.count() > 0:
                expect(angular).to_contain_text("Просмотреть", timeout=10000)
            else:
                expect(page.locator("b-page")).to_contain_text("Просмотреть", timeout=10000)
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Конструктор отчетов по поступлениям — 'Просмотреть' topilmadi | {type(e).__name__}")

    with allure.step("70 - [Склад] Конструктор отчетов по списанию — 'Просмотреть' ko'rinadi"):
        try:
            page.goto(_home_url, wait_until="domcontentloaded", timeout=8000)
        except Exception:
            pass
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Конструктор отчетов по списанию").click()
        try:
            page.wait_for_selector(
                "app-mbi-report-constructor, b-page", timeout=15000
            )
        except Exception:
            pass
        try:
            angular = page.locator("app-mbi-report-constructor")
            if angular.count() > 0:
                expect(angular).to_contain_text("Просмотреть", timeout=10000)
            else:
                expect(page.locator("b-page")).to_contain_text("Просмотреть", timeout=10000)
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Конструктор отчетов по списанию — 'Просмотреть' topilmadi | {type(e).__name__}")

    with allure.step("71 - [Склад] Конструктор отчетов по запросам на межорг. перемещения — 'Просмотреть' ko'rinadi"):
        try:
            page.goto(_home_url, wait_until="domcontentloaded", timeout=8000)
        except Exception:
            pass
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Конструктор отчетов по запросам на межорг. перемещения").click()
        try:
            page.wait_for_selector(
                "app-mbi-report-constructor, b-page", timeout=15000
            )
        except Exception:
            pass
        try:
            angular = page.locator("app-mbi-report-constructor")
            if angular.count() > 0:
                expect(angular).to_contain_text("Просмотреть", timeout=10000)
            else:
                expect(page.locator("b-page")).to_contain_text("Просмотреть", timeout=10000)
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Конструктор отчетов по запросам на межорг. перемещения — 'Просмотреть' topilmadi | {type(e).__name__}")

    with allure.step("72 - [Склад] Конструктор отчетов по межорг. перемещениям — 'Просмотреть' ko'rinadi"):
        try:
            page.goto(_home_url, wait_until="domcontentloaded", timeout=8000)
        except Exception:
            pass
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Конструктор отчетов по межорг. перемещениям").click()
        try:
            page.wait_for_selector(
                "app-mbi-report-constructor, b-page", timeout=15000
            )
        except Exception:
            pass
        try:
            angular = page.locator("app-mbi-report-constructor")
            if angular.count() > 0:
                expect(angular).to_contain_text("Просмотреть", timeout=10000)
            else:
                expect(page.locator("b-page")).to_contain_text("Просмотреть", timeout=10000)
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Конструктор отчетов по межорг. перемещениям — 'Просмотреть' topilmadi | {type(e).__name__}")

    with allure.step("73 - [Склад] Отчёт по отгрузкам и оплатам — 'Параметры' ko'rinadi"):
        try:
            page.goto(_home_url, wait_until="domcontentloaded", timeout=8000)
        except Exception:
            pass
        page.get_by_role("link", name="Склад").click()
        page.get_by_role("link", name="Отчёт по отгрузкам и оплатам").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Склад] Отчёт по отгрузкам и оплатам — 'Параметры' topilmadi | {type(e).__name__}")

    # ── Финансы bo'limi ────────────────────────────────────────────────────

    with allure.step("74 - [Финансы] Кассовые документы — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Кассовые документы").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Кассовые документы — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("75 - [Финансы] Банковские выписки — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Банковские выписки").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Банковские выписки — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("76 - [Финансы] Документы чековой книжки — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Документы чековой книжки").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Документы чековой книжки — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("77 - [Финансы] Платежные поручения — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Платежные поручения").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Платежные поручения — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("78 - [Финансы] Платежные требования — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Платежные требования").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Платежные требования — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("79 - [Финансы] Ручные операции — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Ручные операции").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Ручные операции — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("80 - [Финансы] Переоценки валют — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Переоценки валют").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Переоценки валют — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("81 - [Финансы] Уставный капитал — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Уставный капитал").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Уставный капитал — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("82 - [Финансы] Взаиморасчеты — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Взаиморасчеты").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Взаиморасчеты — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("83 - [Финансы] Перекидка аванса клиентов / поставщиков — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Перекидка аванса клиентов / поставщиков").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Перекидка аванса клиентов / поставщиков — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("84 - [Финансы] Оплаты от клиентов — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Оплаты от клиентов").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Оплаты от клиентов — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("85 - [Финансы] Оплаты поставщикам — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Оплаты поставщикам").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Оплаты поставщикам — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("86 - [Финансы] Запросы об оплате — sarlavha ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Запросы об оплате").click()
        try:
            expect(page.get_by_role("heading")).to_contain_text("Запросы об оплате")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Запросы об оплате — sarlavha topilmadi | {type(e).__name__}")

    with allure.step("87 - [Финансы] Мои заявки — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Мои заявки").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Мои заявки — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("88 - [Финансы] Согласование — sarlavha ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Согласование").click()
        try:
            expect(page.get_by_role("heading")).to_contain_text("Согласование")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Согласование — sarlavha topilmadi | {type(e).__name__}")

    with allure.step("89 - [Финансы] Оплаты (реестр) — sarlavha ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Оплаты").nth(2).click()
        try:
            expect(page.get_by_role("heading")).to_contain_text("Оплаты")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Оплаты (реестр) — sarlavha topilmadi | {type(e).__name__}")

    with allure.step("90 - [Финансы] Документооборот — sarlavha ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Документооборот").click()
        try:
            expect(page.get_by_role("heading")).to_contain_text("Документооборот")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Документооборот — sarlavha topilmadi | {type(e).__name__}")

    with allure.step("91 - [Финансы] Валюты — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Валюты").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Валюты — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("92 - [Финансы] План счетов — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="План счетов").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] План счетов — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("93 - [Финансы] Виды операций — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Виды операций").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Виды операций — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("94 - [Финансы] Договоры — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Договоры").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Договоры — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("95 - [Финансы] Статьи доходов — 'Прикрепление' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Статьи доходов").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Прикрепление")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Статьи доходов — 'Прикрепление' topilmadi | {type(e).__name__}")

    with allure.step("96 - [Финансы] Статьи расходов — 'Прикрепление' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Статьи расходов").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Прикрепление")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Статьи расходов — 'Прикрепление' topilmadi | {type(e).__name__}")

    with allure.step("97 - [Финансы] Дашборд по финансам — 'Аналитика по счету' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Дашборд по финансам").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Аналитика по счету")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Дашборд по финансам — 'Аналитика по счету' topilmadi | {type(e).__name__}")

    with allure.step("98 - [Финансы] Конструктор отчетов по финансам — 'Просмотреть' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Конструктор отчетов по финансам").click()
        try:
            page.wait_for_selector(
                "app-mbi-report-constructor, b-page", timeout=15000
            )
        except Exception:
            pass
        try:
            angular = page.locator("app-mbi-report-constructor")
            if angular.count() > 0:
                expect(angular).to_contain_text("Просмотреть", timeout=10000)
            else:
                expect(page.locator("b-page")).to_contain_text("Просмотреть", timeout=10000)
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Конструктор отчетов по финансам — 'Просмотреть' topilmadi | {type(e).__name__}")

    with allure.step("99 - [Финансы] Акт-сверки — 'Параметры' ko'rinadi"):
        try:
            page.goto(_home_url, wait_until="domcontentloaded", timeout=8000)
        except Exception:
            pass
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Акт-сверки").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Акт-сверки — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("100 - [Финансы] Оборотно-сальдовая ведомость — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Оборотно-сальдовая ведомость", exact=True).click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Оборотно-сальдовая ведомость — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("101 - [Финансы] Оборотно-сальдовая ведомость(BETA) — 'Закрыть' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Оборотно-сальдовая ведомость(BETA)").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Закрыть")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Оборотно-сальдовая ведомость(BETA) — 'Закрыть' topilmadi | {type(e).__name__}")

    with allure.step("102 - [Финансы] Оборотно-сальдовая ведомость по счету — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Оборотно-сальдовая ведомость по счету").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Оборотно-сальдовая ведомость по счету — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("103 - [Финансы] Проводки счетов — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Проводки счетов").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Проводки счетов — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("104 - [Финансы] Карточка счета — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Карточка счета").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Карточка счета — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("105 - [Финансы] Анализ счета — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Анализ счета").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Анализ счета — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("106 - [Финансы] Прибыль и убыток (P&L) — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Прибыль и убыток (P&L)").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Прибыль и убыток (P&L) — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("107 - [Финансы] Отчет о прибылях и убытках (БЕТА) — 'Закрыть' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Отчет о прибылях и убытках (БЕТА)").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Закрыть")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Отчет о прибылях и убытках (БЕТА) — 'Закрыть' topilmadi | {type(e).__name__}")

    with allure.step("108 - [Финансы] Отчет о движении денежных средств (БЕТА) — 'Закрыть' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Отчет о движении денежных средств (БЕТА)").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Закрыть")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Отчет о движении денежных средств (БЕТА) — 'Закрыть' topilmadi | {type(e).__name__}")

    with allure.step("109 - [Финансы] Денежный поток — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Денежный поток").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Денежный поток — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("110 - [Финансы] Оплаты (отчет) — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Оплаты").nth(3).click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Оплаты (отчет) — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("111 - [Финансы] Отчет по должникам — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Отчет по должникам").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Отчет по должникам — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("112 - [Финансы] Обороты по контрагентам — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Обороты по контрагентам").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Обороты по контрагентам — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("113 - [Финансы] Бухгалтерский баланс — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Бухгалтерский баланс").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Бухгалтерский баланс — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("114 - [Финансы] Журнал документов — sarlavha ko'rinadi"):
        page.get_by_role("link", name="Финансы").click()
        page.get_by_role("link", name="Журнал документов").click()
        try:
            expect(page.get_by_role("heading")).to_contain_text("Журнал документов")
        except Exception as e:
            soft.check(False,
                f"❌ [Финансы] Журнал документов — sarlavha topilmadi | {type(e).__name__}")

    # ── Кадры и зарплата bo'limi ───────────────────────────────────────────

    with allure.step("115 - [Кадры и зарплата] Расчеты зарплаты — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Кадры и зарплата").click()
        page.get_by_role("link", name="Расчеты зарплаты").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Кадры и зарплата] Расчеты зарплаты — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("116 - [Кадры и зарплата] Выплаты — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Кадры и зарплата").click()
        page.get_by_role("link", name="Выплаты").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Кадры и зарплата] Выплаты — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("117 - [Кадры и зарплата] Бонусная система — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Кадры и зарплата").click()
        page.get_by_role("link", name="Бонусная система").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Кадры и зарплата] Бонусная система — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("118 - [Кадры и зарплата] Сотрудники — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Кадры и зарплата").click()
        page.get_by_role("link", name="Сотрудники").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Кадры и зарплата] Сотрудники — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("119 - [Кадры и зарплата] Отделы — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Кадры и зарплата").click()
        page.get_by_role("link", name="Отделы").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Кадры и зарплата] Отделы — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("120 - [Кадры и зарплата] Должности — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Кадры и зарплата").click()
        page.get_by_role("link", name="Должности").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Кадры и зарплата] Должности — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("121 - [Кадры и зарплата] Виды начислений — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Кадры и зарплата").click()
        page.get_by_role("link", name="Виды начислений").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Кадры и зарплата] Виды начислений — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("122 - [Кадры и зарплата] Виды удержаний — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Кадры и зарплата").click()
        page.get_by_role("link", name="Виды удержаний").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Кадры и зарплата] Виды удержаний — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("123 - [Кадры и зарплата] Виды выплат — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Кадры и зарплата").click()
        page.get_by_role("link", name="Виды выплат").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Кадры и зарплата] Виды выплат — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("124 - [Кадры и зарплата] Отчёт по начислениям и выплатам персоналу — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Кадры и зарплата").click()
        page.get_by_role("link", name="Отчёт по начислениям и выплатам персоналу").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Кадры и зарплата] Отчёт по начислениям и выплатам персоналу — 'Параметры' topilmadi | {type(e).__name__}")

    # ── Производство bo'limi ───────────────────────────────────────────────

    with allure.step("125 - [Производство] Журнал план производства — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Производство").click()
        page.get_by_role("link", name="Журнал план производства").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Производство] Журнал план производства — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("126 - [Производство] План производства — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Производство").click()
        page.locator("#kt_header_menu").get_by_role("link", name="План производства", exact=True).click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Производство] План производства — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("127 - [Производство] Технологические операции — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Производство").click()
        page.get_by_role("link", name="Технологические операции").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Производство] Технологические операции — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("128 - [Производство] Заказы кодов маркировки — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Производство").click()
        page.get_by_role("link", name="Заказы кодов маркировки").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Производство] Заказы кодов маркировки — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("129 - [Производство] Отчет о нанесении — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Производство").click()
        page.get_by_role("link", name="Отчет о нанесении").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Производство] Отчет о нанесении — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("130 - [Производство] Заказ на производство — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Производство").click()
        page.get_by_role("link", name="Заказ на производство").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Производство] Заказ на производство — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("131 - [Производство] Производственные задания — sarlavha ko'rinadi"):
        page.get_by_role("link", name="Производство").click()
        page.get_by_role("link", name="Производственные задания").click()
        try:
            expect(page.get_by_role("heading")).to_contain_text("Производственные задания")
        except Exception as e:
            soft.check(False,
                f"❌ [Производство] Производственные задания — sarlavha topilmadi | {type(e).__name__}")

    with allure.step("132 - [Производство] Ввод производственных остатков ТМЦ — sarlavha ko'rinadi"):
        page.get_by_role("link", name="Производство").click()
        page.get_by_role("link", name="Ввод производственных остатков ТМЦ").click()
        try:
            expect(page.get_by_role("heading")).to_contain_text("Ввод производственных остатков ТМЦ")
        except Exception as e:
            soft.check(False,
                f"❌ [Производство] Ввод производственных остатков ТМЦ — sarlavha topilmadi | {type(e).__name__}")

    with allure.step("133 - [Производство] Спецификация — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Производство").click()
        page.get_by_role("link", name="Спецификация").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Производство] Спецификация — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("134 - [Производство] Ресурсы/доп.затраты — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Производство").click()
        page.get_by_role("link", name="Ресурсы/доп.затраты").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Производство] Ресурсы/доп.затраты — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("135 - [Производство] Технологическая карта — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Производство").click()
        page.get_by_role("link", name="Технологическая карта").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Производство] Технологическая карта — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("136 - [Производство] Оборудование — 'Добавить' ko'rinadi"):
        page.get_by_role("link", name="Производство").click()
        page.get_by_role("link", name="Оборудование").first.click()
        try:
            expect(page.locator("b-page")).to_contain_text("Добавить")
        except Exception as e:
            soft.check(False,
                f"❌ [Производство] Оборудование — 'Добавить' topilmadi | {type(e).__name__}")

    with allure.step("137 - [Производство] Обеспечение производства — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Производство").click()
        page.get_by_role("link", name="Обеспечение производства").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Производство] Обеспечение производства — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("138 - [Производство] Движение ТМЦ в производстве — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Производство").click()
        page.get_by_role("link", name="Движение ТМЦ в производстве").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Производство] Движение ТМЦ в производстве — 'Параметры' topilmadi | {type(e).__name__}")

    # ── Справочники bo'limi ────────────────────────────────────────────────

    with allure.step("139 - [Справочники] ТМЦ — 'Создать' tugmasi ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="ТМЦ", exact=True).click()
        try:
            expect(page.locator("#anor50-button-text-add")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] ТМЦ — 'Создать' tugmasi topilmadi | {type(e).__name__}")

    with allure.step("140 - [Справочники] Цены — 'Создать' tugmasi ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Цены").click()
        try:
            expect(page.locator("#anor182-button-add")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Цены — 'Создать' tugmasi topilmadi | {type(e).__name__}")

    with allure.step("141 - [Справочники] Услуги — 'Создать' tugmasi ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Услуги").click()
        try:
            expect(page.locator("#anor50-button-add")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Услуги — 'Создать' tugmasi topilmadi | {type(e).__name__}")

    with allure.step("142 - [Справочники] Скидки/наценки — jadvalda 'Название' ustuni ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Скидки/наценки").click()
        try:
            expect(page.locator("b-grid")).to_contain_text("Название")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Скидки/наценки — jadvalda 'Название' ustuni topilmadi | {type(e).__name__}")

    with allure.step("143 - [Справочники] Производители — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Производители").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Производители — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("144 - [Справочники] Типы фото-отчетов — 'Прикрепление' ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Типы фото-отчетов").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Прикрепление")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Типы фото-отчетов — 'Прикрепление' topilmadi | {type(e).__name__}")

    with allure.step("145 - [Справочники] Типы видео-отчетов — 'Прикрепление' ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Типы видео-отчетов").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Прикрепление")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Типы видео-отчетов — 'Прикрепление' topilmadi | {type(e).__name__}")

    with allure.step("146 - [Справочники] Комментарии — 'Прикрепление' ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Комментарии").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Прикрепление")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Комментарии — 'Прикрепление' topilmadi | {type(e).__name__}")

    with allure.step("148 - [Справочники] Опросники — 'Прикрепление' ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Опросники", exact=True).click()
        try:
            expect(page.locator("b-page")).to_contain_text("Прикрепление")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Опросники — 'Прикрепление' topilmadi | {type(e).__name__}")

    with allure.step("149 - [Справочники] Регионы — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Регионы").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Регионы — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("150 - [Справочники] Вопросы двойного визита — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Вопросы двойного визита").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Вопросы двойного визита — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("151 - [Справочники] Опросники двойных визитов — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Опросники двойных визитов").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Опросники двойных визитов — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("152 - [Справочники] Презентации — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Презентации").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Презентации — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("153 - [Справочники] Продавцы — jadvalda 'Название' ustuni ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Продавцы").click()
        try:
            expect(page.locator("b-grid")).to_contain_text("Название")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Продавцы — jadvalda 'Название' ustuni topilmadi | {type(e).__name__}")

    with allure.step("154 - [Справочники] Физические лица — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Физические лица").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Физические лица — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("155 - [Справочники] Юридические лица — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Юридические лица").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Юридические лица — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("156 - [Справочники] Отделы — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Отделы").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Отделы — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("157 - [Справочники] Должности — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Должности").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Должности — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("158 - [Справочники] Рабочие зоны — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Рабочие зоны").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Рабочие зоны — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("159 - [Справочники] Штат — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Штат").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Штат — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("160 - [Справочники] Клиенты — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Клиенты").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Клиенты — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("161 - [Справочники] Уведомления — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Уведомления").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Уведомления — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("162 - [Справочники] Акции — 'Создать' tugmasi ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Акции").click()
        try:
            expect(page.locator("#anor717-button-add")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Акции — 'Создать' tugmasi topilmadi | {type(e).__name__}")

    with allure.step("163 - [Справочники] Нагрузки — 'Создать' tugmasi ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Нагрузки").click()
        try:
            expect(page.locator("#anor723-button-add")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Нагрузки — 'Создать' tugmasi topilmadi | {type(e).__name__}")

    with allure.step("164 - [Справочники] Рекомендации — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Рекомендации").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Рекомендации — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("165 - [Справочники] Правила ограничений — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Правила ограничений").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Правила ограничений — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("166 - [Справочники] Продуктовая корзина — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Продуктовая корзина").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Продуктовая корзина — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("167 - [Справочники] Сеты ТМЦ — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Сеты ТМЦ").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Сеты ТМЦ — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("168 - [Справочники] Лимитирование ТМЦ — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Лимитирование ТМЦ").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Лимитирование ТМЦ — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("169 - [Справочники] Вопросы категоризации — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Вопросы категоризации").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Вопросы категоризации — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("170 - [Справочники] Категоризация физических лиц — jadvalda 'Название' ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Категоризация физических лиц").click()
        try:
            expect(page.locator("b-grid")).to_contain_text("Название")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Категоризация физических лиц — jadvalda 'Название' topilmadi | {type(e).__name__}")

    with allure.step("171 - [Справочники] Категоризация юридических лиц — jadvalda 'Название' ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Категоризация юридических лиц").click()
        try:
            expect(page.locator("b-grid")).to_contain_text("Название")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Категоризация юридических лиц — jadvalda 'Название' topilmadi | {type(e).__name__}")

    with allure.step("172 - [Справочники] Результат категоризации — jadvalda 'Пользователь' ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Результат категоризации").click()
        try:
            expect(page.locator("b-grid")).to_contain_text("Пользователь")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Результат категоризации — jadvalda 'Пользователь' topilmadi | {type(e).__name__}")

    with allure.step("173 - [Справочники] Отчет по результату категоризации — 'Просмотреть' ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Отчет по результату категоризации").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Отчет по результату категоризации — 'Просмотреть' topilmadi | {type(e).__name__}")

    with allure.step("174 - [Справочники] Публикация в бот — 'Добавить' ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Публикация в бот").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Добавить")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Публикация в бот — 'Добавить' topilmadi | {type(e).__name__}")

    with allure.step("175 - [Справочники] Минимальные обязательные ассортименты — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Справочники").click()
        page.get_by_role("link", name="Минимальные обязательные ассортименты").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Справочники] Минимальные обязательные ассортименты — 'Создать' topilmadi | {type(e).__name__}")

    # ── Торговый маркетинг bo'limi ─────────────────────────────────────────

    with allure.step("176 - [Торговый маркетинг] Настройки мерчандайзинга — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="Настройки мерчандайзинга").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] Настройки мерчандайзинга — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("177 - [Торговый маркетинг] Мерчандайзинг — jadvalda 'Пользователь' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="Мерчандайзинг", exact=True).click()
        try:
            expect(page.locator("b-grid")).to_contain_text("Пользователь")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] Мерчандайзинг — jadvalda 'Пользователь' topilmadi | {type(e).__name__}")

    with allure.step("178 - [Торговый маркетинг] КПЭ по штатам — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="КПЭ по штатам").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] КПЭ по штатам — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("179 - [Торговый маркетинг] КПЭ по рабочим зонам — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="КПЭ по рабочим зонам").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] КПЭ по рабочим зонам — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("180 - [Торговый маркетинг] КПЭ по характеристикам ТМЦ — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.locator("#kt_header_menu").get_by_role("link", name="КПЭ по характеристикам ТМЦ").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] КПЭ по характеристикам ТМЦ — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("181 - [Торговый маркетинг] КПЭ по ТМЦ — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.locator("#kt_header_menu").get_by_role("link", name="КПЭ по ТМЦ").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] КПЭ по ТМЦ — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("182 - [Торговый маркетинг] КПЭ по клиентам — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.locator("#kt_header_menu").get_by_role("link", name="КПЭ по клиентам").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] КПЭ по клиентам — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("183 - [Торговый маркетинг] КПЭ клиентов по ТМЦ — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.locator("#kt_header_menu").get_by_role("link", name="КПЭ клиентов по ТМЦ").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] КПЭ клиентов по ТМЦ — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("184 - [Торговый маркетинг] КПЭ клиентов по характеристикам ТМЦ — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.locator("#kt_header_menu").get_by_role("link", name="КПЭ клиентов по характеристикам ТМЦ").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] КПЭ клиентов по характеристикам ТМЦ — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("185 - [Торговый маркетинг] КПЭ на категорию клиентов по характеристикам ТМЦ — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.locator("#kt_header_menu").get_by_role("link", name="КПЭ на категорию клиентов по характеристикам ТМЦ").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] КПЭ на категорию клиентов по характеристикам ТМЦ — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("186 - [Торговый маркетинг] Шаблон КПЭ — 'Сохранить' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="Шаблон КПЭ").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Сохранить")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] Шаблон КПЭ — 'Сохранить' topilmadi | {type(e).__name__}")

    with allure.step("187 - [Торговый маркетинг] Настройки бонуса — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="Настройки бонуса").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] Настройки бонуса — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("188 - [Торговый маркетинг] Дашборд по КПЭ — 'Сформировать' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="Дашборд по КПЭ").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Сформировать")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] Дашборд по КПЭ — 'Сформировать' topilmadi | {type(e).__name__}")

    with allure.step("189 - [Торговый маркетинг] Настройка характеристики — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="Настройка характеристики").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] Настройка характеристики — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("190 - [Торговый маркетинг] Минимальные обязательные ассортименты — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="Минимальные обязательные ассортименты").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] Минимальные обязательные ассортименты — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("191 - [Торговый маркетинг] Ассортименты — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="Ассортименты", exact=True).click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] Ассортименты — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("192 - [Торговый маркетинг] Планограммы — 'Прикрепление' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="Планограммы").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Прикрепление")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] Планограммы — 'Прикрепление' topilmadi | {type(e).__name__}")

    with allure.step("193 - [Торговый маркетинг] POS-материалы — 'Прикрепление' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="POS-материалы").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Прикрепление")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] POS-материалы — 'Прикрепление' topilmadi | {type(e).__name__}")

    with allure.step("194 - [Торговый маркетинг] Причины несоответствия — 'Прикрепление' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="Причины несоответствия").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Прикрепление")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] Причины несоответствия — 'Прикрепление' topilmadi | {type(e).__name__}")

    with allure.step("195 - [Торговый маркетинг] Конкуренты — 'Прикрепление' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="Конкуренты").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Прикрепление")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] Конкуренты — 'Прикрепление' topilmadi | {type(e).__name__}")

    with allure.step("196 - [Торговый маркетинг] Шаблон отчета по опросам — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="Шаблон отчета по опросам").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] Шаблон отчета по опросам — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("197 - [Торговый маркетинг] Продукты конкурентов — jadvalda 'Название' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="Продукты конкурентов").click()
        try:
            expect(page.locator("b-grid")).to_contain_text("Название")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] Продукты конкурентов — jadvalda 'Название' topilmadi | {type(e).__name__}")

    with allure.step("198 - [Торговый маркетинг] Статусы мерчандайзинга — 'Прикрепление' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="Статусы мерчандайзинга").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Прикрепление")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] Статусы мерчандайзинга — 'Прикрепление' topilmadi | {type(e).__name__}")

    with allure.step("199 - [Торговый маркетинг] Отчет по доле на полке — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="Отчет по доле на полке").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] Отчет по доле на полке — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("200 - [Торговый маркетинг] Отчет по ассортиментам — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="Отчет по ассортиментам").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] Отчет по ассортиментам — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("201 - [Торговый маркетинг] Отчет по планограмме — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="Отчет по планограмме").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] Отчет по планограмме — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("202 - [Торговый маркетинг] Отчет по ценам на полке — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="Отчет по ценам на полке").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] Отчет по ценам на полке — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("203 - [Торговый маркетинг] Отчет по POS-материалам — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="Отчет по POS-материалам").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] Отчет по POS-материалам — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("204 - [Торговый маркетинг] Сводный отчет по мерчандайзингу — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="Сводный отчет по мерчандайзингу").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] Сводный отчет по мерчандайзингу — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("205 - [Торговый маркетинг] Отчет об отсутствии или несоответствии — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="Отчет об отсутствии или несоответствии").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] Отчет об отсутствии или несоответствии — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("206 - [Торговый маркетинг] Отчет анализа цен — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="Отчет анализа цен").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] Отчет анализа цен — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("207 - [Торговый маркетинг] Отчет по мерчандайзингу — 'Начало периода' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="Отчет по мерчандайзингу", exact=True).click()
        try:
            expect(page.locator("b-page")).to_contain_text("Начало периода")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] Отчет по мерчандайзингу — 'Начало периода' topilmadi | {type(e).__name__}")

    with allure.step("208 - [Торговый маркетинг] Экспорт фото и видео отчетов по визитам — 'Параметры' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="Экспорт фото и видео отчетов по визитам").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Параметры")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] Экспорт фото и видео отчетов по визитам — 'Параметры' topilmadi | {type(e).__name__}")

    with allure.step("209 - [Торговый маркетинг] Отчет по ценникам конкурентов — 'Сформировать' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="Отчет по ценникам конкурентов").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Сформировать")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] Отчет по ценникам конкурентов — 'Сформировать' topilmadi | {type(e).__name__}")

    with allure.step("210 - [Торговый маркетинг] Отчет по статусам мерчандайзинга — 'Сформировать' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="Отчет по статусам мерчандайзинга").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Сформировать")
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] Отчет по статусам мерчандайзинга — 'Сформировать' topilmadi | {type(e).__name__}")

    with allure.step("211 - [Торговый маркетинг] Конструктор отчетов по долям на полках — 'Просмотр' ko'rinadi"):
        page.get_by_role("link", name="Торговый маркетинг").click()
        page.get_by_role("link", name="Конструктор отчетов по долям на полках").click()
        try:
            page.wait_for_selector(
                "app-mbi-report-constructor, b-page", timeout=15000
            )
        except Exception:
            pass
        try:
            angular = page.locator("app-mbi-report-constructor")
            if angular.count() > 0:
                expect(angular).to_contain_text("Просмотр", timeout=10000)
            else:
                expect(page.locator("b-page")).to_contain_text("Просмотр", timeout=10000)
        except Exception as e:
            soft.check(False,
                f"❌ [Торговый маркетинг] Конструктор отчетов по долям на полках — 'Просмотр' topilmadi | {type(e).__name__}")

    # ── Оборудование bo'limi ───────────────────────────────────────────────

    with allure.step("212 - [Оборудование] Заявки на оборудование — 'Установить' ko'rinadi"):
        try:
            page.goto(_home_url, wait_until="domcontentloaded", timeout=8000)
        except Exception:
            pass
        page.get_by_role("link", name="Оборудование").click()
        page.get_by_role("link", name="Заявки на оборудование").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Установить")
        except Exception as e:
            soft.check(False,
                f"❌ [Оборудование] Заявки на оборудование — 'Установить' topilmadi | {type(e).__name__}")

    with allure.step("213 - [Оборудование] Заявки на перемещения — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Оборудование").click()
        page.get_by_role("link", name="Заявки на перемещения").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Оборудование] Заявки на перемещения — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("214 - [Оборудование] Межорг. перемещение оборудования: отправка — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Оборудование").click()
        page.get_by_role("link", name="Межорг. перемещение оборудования: отправка").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Оборудование] Межорг. перемещение оборудования: отправка — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("215 - [Оборудование] Межорг. перемещение оборудования: прием — jadvalda 'Вид перемещения' ko'rinadi"):
        page.get_by_role("link", name="Оборудование").click()
        page.get_by_role("link", name="Межорг. перемещение оборудования: прием").click()
        try:
            expect(page.locator("b-grid")).to_contain_text("Вид перемещения")
        except Exception as e:
            soft.check(False,
                f"❌ [Оборудование] Межорг. перемещение оборудования: прием — jadvalda 'Вид перемещения' topilmadi | {type(e).__name__}")

    with allure.step("216 - [Оборудование] Заявки на ремонт — jadvalda 'Номер заявки' ko'rinadi"):
        page.get_by_role("link", name="Оборудование").click()
        page.get_by_role("link", name="Заявки на ремонт").click()
        try:
            expect(page.locator("b-grid")).to_contain_text("Номер заявки")
        except Exception as e:
            soft.check(False,
                f"❌ [Оборудование] Заявки на ремонт — jadvalda 'Номер заявки' topilmadi | {type(e).__name__}")

    with allure.step("217 - [Оборудование] Неисправности оборудования — 'Прикрепление' ko'rinadi"):
        page.get_by_role("link", name="Оборудование").click()
        page.get_by_role("link", name="Неисправности оборудовния").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Прикрепление")
        except Exception as e:
            soft.check(False,
                f"❌ [Оборудование] Неисправности оборудования — 'Прикрепление' topilmadi | {type(e).__name__}")

    with allure.step("218 - [Оборудование] Конструктор отчетов по заявкам на оборудование — 'Просмотреть' ko'rinadi"):
        page.get_by_role("link", name="Оборудование").click()
        page.get_by_role("link", name="Конструктор отчетов по заявкам на оборудование").click()
        try:
            page.wait_for_selector(
                "app-mbi-report-constructor, b-page", timeout=15000
            )
        except Exception:
            pass
        try:
            angular = page.locator("app-mbi-report-constructor")
            if angular.count() > 0:
                expect(angular).to_contain_text("Просмотреть", timeout=10000)
            else:
                expect(page.locator("b-page")).to_contain_text("Просмотреть", timeout=10000)
        except Exception as e:
            soft.check(False,
                f"❌ [Оборудование] Конструктор отчетов по заявкам на оборудование — 'Просмотреть' topilmadi | {type(e).__name__}")

    with allure.step("219 - [Оборудование] Цели для рекламного оборудования — 'Создать' ko'rinadi"):
        try:
            page.goto(_home_url, wait_until="domcontentloaded", timeout=8000)
        except Exception:
            pass
        page.get_by_role("link", name="Оборудование").click()
        page.get_by_role("link", name="Цели для рекламного оборудования").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Оборудование] Цели для рекламного оборудования — 'Создать' topilmadi | {type(e).__name__}")

    with allure.step("220 - [Оборудование] Остатки по рекламному оборудованию — jadvalda 'Оборудование' ko'rinadi"):
        page.get_by_role("link", name="Оборудование").click()
        page.get_by_role("link", name="Остатки по рекламному оборудованию").click()
        try:
            expect(page.locator("b-grid")).to_contain_text("Оборудование")
        except Exception as e:
            soft.check(False,
                f"❌ [Оборудование] Остатки по рекламному оборудованию — jadvalda 'Оборудование' topilmadi | {type(e).__name__}")

    with allure.step("221 - [Оборудование] Характеристики оборудования — 'Создать' ko'rinadi"):
        page.get_by_role("link", name="Оборудование", exact=True).click()
        page.get_by_role("link", name="Характеристики оборудования").click()
        try:
            expect(page.locator("b-page")).to_contain_text("Создать")
        except Exception as e:
            soft.check(False,
                f"❌ [Оборудование] Характеристики оборудования — 'Создать' topilmadi | {type(e).__name__}")


# ----------------------------------------------------------------------------------------------------------------------


@allure.title("Barcha bo'limlar — formalar xatosiz ochiladi")
def test_check_forms_opening(page: Page, soft: SoftAssert) -> None:
    """
    Tekshiradi:
      - Главное bo'limi:        11 ta forma/sahifa xatosiz ochiladi
      - Продажа bo'limi:        24 ta forma/sahifa xatosiz ochiladi
      - Склад bo'limi:          37 ta forma/sahifa xatosiz ochiladi
      - Финансы bo'limi:        41 ta forma/sahifa xatosiz ochiladi
      - Кадры и зарплата:       10 ta forma/sahifa xatosiz ochiladi
      - Производство:           14 ta forma/sahifa xatosiz ochiladi
      - Справочники:            36 ta forma/sahifa xatosiz ochiladi
      - Торговый маркетинг:     36 ta forma/sahifa xatosiz ochiladi
      - Оборудование:           10 ta forma/sahifa xatosiz ochiladi
      - Jami: 219 ta forma, 220 ta qadam (1 ta login)
    """
    run_check_forms_opening(page, soft)
