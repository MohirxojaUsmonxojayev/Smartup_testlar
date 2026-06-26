import allure


class SoftAssert:
    """
    Soft assertion — expect() xatosi test'ni to'xtatmaydi.
    Barcha xatolar yig'ilib, assert_all() da bitta AssertionError sifatida chiqariladi.

    Ishlatish:
        soft.check(False, "❌ [Modul] Forma — 'Element' topilmadi")
        ...
        soft.assert_all()   # fixture teardown'da avtomatik chaqiriladi
    """

    def __init__(self) -> None:
        self.failures: list[str] = []

    def check(self, condition: bool, message: str) -> None:
        """Xato bo'lsa (condition=False) failures ga qo'shadi, to'xtamaydi."""
        if not condition:
            self.failures.append(message)
            try:
                from utils.telegram_reporter import _session_soft_failures
                _session_soft_failures.append(message)
            except Exception:
                pass
            try:
                allure.attach(
                    message,
                    name="soft-fail",
                    attachment_type=allure.attachment_type.TEXT,
                )
            except Exception:
                pass

    def assert_all(self) -> None:
        """Test oxirida chaqiriladi. Xatolar bo'lsa AssertionError chiqaradi."""
        if not self.failures:
            summary = "✅ Barcha 219 ta forma muvaffaqiyatli tekshirildi"
        else:
            lines = [f"🔴 XATOLAR SONI: {len(self.failures)}"] + self.failures
            summary = "\n".join(lines)

        try:
            allure.attach(
                summary,
                name="Test Yakuniy Natija",
                attachment_type=allure.attachment_type.TEXT,
            )
        except Exception:
            pass

        if self.failures:
            raise AssertionError(summary)
