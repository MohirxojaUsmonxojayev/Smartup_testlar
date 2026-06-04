import json
import os
from argparse import ArgumentParser, Namespace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_STORE_PATH = ROOT / "test-results/data/data_store.json"
CREATED_COMPANY_PASSWORD = "greenwhite"


def _load_data_store() -> dict:
    if not DATA_STORE_PATH.exists():
        return {}
    try:
        data = json.loads(DATA_STORE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def add_company_args(parser: ArgumentParser) -> None:
    parser.add_argument("--url", required=True)
    parser.add_argument("--company-code")
    parser.add_argument("--company-password")
    parser.add_argument("--create-company", action="store_true")


def configure_company_env(args: Namespace) -> None:
    company_url = args.url.strip().rstrip("/")
    if not company_url:
        raise SystemExit("--url bo'sh bo'lishi mumkin emas")
    os.environ["COMPANY_URL"] = company_url

    if args.create_company:
        os.environ["CREATE_COMPANY"] = "1"
        os.environ["COMPANY_PASSWORD"] = CREATED_COMPANY_PASSWORD
        os.environ.pop("COMPANY_CODE", None)
        return

    company_code = (args.company_code or "").strip().lstrip("@")
    company_password = (args.company_password or "").strip()

    if not company_code:
        data_company_code = _load_data_store().get("company_code")
        if data_company_code:
            os.environ["CREATE_COMPANY"] = "1"
            os.environ["COMPANY_PASSWORD"] = CREATED_COMPANY_PASSWORD
            os.environ.pop("COMPANY_CODE", None)
            return

    if not company_code or not company_password:
        raise SystemExit("--company-code/--company-password yoki --create-company kerak")

    os.environ.pop("CREATE_COMPANY", None)
    os.environ["COMPANY_CODE"] = company_code
    os.environ["COMPANY_PASSWORD"] = company_password
