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
    parser.add_argument("--head-email")
    parser.add_argument("--head-password")


def configure_company_env(args: Namespace) -> None:
    company_url = args.url.strip().rstrip("/")
    if not company_url:
        raise SystemExit("--url bo'sh bo'lishi mumkin emas")
    os.environ["COMPANY_URL"] = company_url

    company_password = (args.company_password or "").strip()
    head_email = (args.head_email or "").strip()
    head_password = (args.head_password or "").strip()

    if args.create_company:
        if args.company_code:
            raise SystemExit("--create-company bilan --company-code berilmaydi")
        if company_password:
            raise SystemExit("--company-password --create-company bilan berilmaydi; yangi company admin paroli test ichidagi default qiymat")
        if not head_email:
            raise SystemExit("--head-email majburiy: --create-company uchun head profil emailini bering")
        if not head_password:
            raise SystemExit("--head-password majburiy: --create-company uchun head profil parolini bering")
        os.environ["CREATE_COMPANY"] = "1"
        os.environ["COMPANY_PASSWORD"] = CREATED_COMPANY_PASSWORD
        os.environ["HEAD_ADMIN_EMAIL"] = head_email
        os.environ["HEAD_ADMIN_PASSWORD"] = head_password
        os.environ.pop("COMPANY_CODE", None)
        return

    company_code = (args.company_code or "").strip().lstrip("@")

    if head_email or head_password:
        raise SystemExit("--head-email/--head-password faqat --create-company bilan ishlaydi")

    if not company_code:
        data_company_code = _load_data_store().get("company_code")
        if data_company_code:
            company_code = str(data_company_code).strip().lstrip("@")

    if not company_code or not company_password:
        raise SystemExit("--company-code/--company-password yoki --create-company credentiallari kerak")

    os.environ.pop("CREATE_COMPANY", None)
    os.environ["COMPANY_CODE"] = company_code
    os.environ["COMPANY_PASSWORD"] = company_password
    os.environ.pop("HEAD_ADMIN_EMAIL", None)
    os.environ.pop("HEAD_ADMIN_PASSWORD", None)
