import argparse
import sys

from dotenv import load_dotenv

from scripts.script_mode import run_script_mode
from scripts.api_test_mode import run_rest_api_and_test
from scripts.telegram_mode import run_telegram_mode

load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="🧠 Document Analysis System")
    parser.add_argument(
        "--mode",
        choices=["script", "api", "web", "telegram"],
        help="Select mode of operation",
        required=True,
    )
    args = parser.parse_args()

    if args.mode == "script":
        run_script_mode()
    elif args.mode == "api":
        run_rest_api_and_test()
    elif args.mode == "web":
        from subprocess import run
        run([sys.executable, "-m", "uvicorn", "web.app:app", "--host", "127.0.0.1", "--port", "8000", "--reload"])
    elif args.mode == "telegram":
        run_telegram_mode()


if __name__ == "__main__":
    main()
