import logging
from datetime import datetime, timedelta
from pathlib import Path

LOGS_ROOT = Path("logs")


class RunLogger:
    """
    Kunlik konsolidatsiya log fayli.
    Bir kunda bir nechta run bo'lsa, bir xil faylga append qilinadi.
    Python logging.FileHandler thread-safe — parallel testlarda xavfsiz.
    """

    def __init__(self):
        self._log_path = self._daily_path()
        self._logger = self._build_logger()
        self._run_start: datetime | None = None
        self._passed = 0
        self._failed = 0
        self._skipped = 0
        self._test_starts: dict[str, datetime] = {}

    @staticmethod
    def _daily_path() -> Path:
        now = datetime.now()
        month_dir = LOGS_ROOT / now.strftime("%Y-%m")
        month_dir.mkdir(parents=True, exist_ok=True)
        return month_dir / now.strftime("%Y-%m-%d.log")

    def _build_logger(self) -> logging.Logger:
        logger = logging.getLogger(f"run_logger.{id(self)}")
        logger.setLevel(logging.DEBUG)
        logger.propagate = False
        fmt = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        fh = logging.FileHandler(self._log_path, mode="a", encoding="utf-8")
        fh.setFormatter(fmt)
        logger.addHandler(fh)
        return logger

    @property
    def log_path(self) -> Path:
        return self._log_path

    # ------------------------------------------------------------------
    # Sessiya
    # ------------------------------------------------------------------

    def session_start(self, base_url: str = "", browser: str = "Chromium", headless: bool = False):
        self._run_start = datetime.now()
        sep = "=" * 70
        self._logger.info(sep)
        self._logger.info(f"[RUN START]  {self._run_start.strftime('%Y-%m-%d %H:%M:%S')}")
        self._logger.info(f"Browser: {browser}  |  Headless: {headless}")
        if base_url:
            self._logger.info(f"Base URL: {base_url}")
        self._logger.info(sep)

    def session_finish(self):
        end = datetime.now()
        total_s = (end - self._run_start).total_seconds() if self._run_start else 0.0
        m, s = divmod(int(total_s), 60)
        total = self._passed + self._failed + self._skipped
        sep = "=" * 70
        self._logger.info(sep)
        self._logger.info(f"[RUN END]    {end.strftime('%Y-%m-%d %H:%M:%S')}")
        self._logger.info(
            f"Passed: {self._passed}  Failed: {self._failed}  "
            f"Skipped: {self._skipped}  Total: {total}  Duration: {m}m {s}s"
        )
        self._logger.info(sep + "\n")
        self._close()

    # ------------------------------------------------------------------
    # Test hayot sikli
    # ------------------------------------------------------------------

    def test_start(self, node_id: str):
        self._test_starts[node_id] = datetime.now()
        self._logger.info(f"[TEST START] {node_id}")

    def step(self, node_id: str, message: str):
        short = node_id.split("::")[-1]
        self._logger.info(f"[STEP]       {short} — {message}")

    def test_pass(self, node_id: str, trace: str = ""):
        self._passed += 1
        dur = self._pop_duration(node_id)
        self._logger.info(f"[PASS]       {node_id}  ({dur:.1f}s)")
        if trace:
            self._logger.debug(f"             Trace: {trace}")

    def test_fail(self, node_id: str, error: str = "", trace: str = ""):
        self._failed += 1
        dur = self._pop_duration(node_id)
        self._logger.error(f"[FAIL]       {node_id}  ({dur:.1f}s)")
        if error:
            self._logger.error(f"             {error[:800]}")
        if trace:
            self._logger.error(f"             Trace: {trace}")

    def test_skip(self, node_id: str, reason: str = ""):
        self._skipped += 1
        self._test_starts.pop(node_id, None)
        self._logger.warning(f"[SKIP]       {node_id}  — {reason}")

    # ------------------------------------------------------------------
    # Eski loglarni tozalash
    # ------------------------------------------------------------------

    @staticmethod
    def cleanup_old_logs(days: int = 30) -> int:
        """Belgilangan kundan eski .log fayllarni o'chiradi, bo'sh papkalarni ham."""
        if not LOGS_ROOT.exists():
            return 0
        cutoff = datetime.now() - timedelta(days=days)
        deleted = 0
        for log_file in LOGS_ROOT.rglob("*.log"):
            if datetime.fromtimestamp(log_file.stat().st_mtime) < cutoff:
                log_file.unlink()
                deleted += 1
        for month_dir in list(LOGS_ROOT.iterdir()):
            if month_dir.is_dir() and not any(month_dir.iterdir()):
                month_dir.rmdir()
        return deleted

    # ------------------------------------------------------------------
    # Ichki yordamchilar
    # ------------------------------------------------------------------

    def _pop_duration(self, node_id: str) -> float:
        start = self._test_starts.pop(node_id, None)
        return (datetime.now() - start).total_seconds() if start else 0.0

    def _close(self):
        for h in self._logger.handlers[:]:
            h.close()
            self._logger.removeHandler(h)
