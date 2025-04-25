import subprocess
import threading
import sys
from libs.logger import logger


def run_telegram_mode():
    def start_bot():
        try:
            logger.info("Starting Telegram bot...")
            subprocess.run([sys.executable, "telegram_bot/bot.py"])
        except Exception as e:
            logger.exception("-x-> Telegram bot crashed")

    bot_thread = threading.Thread(target=start_bot)
    bot_thread.start()

    logger.info("Starting web server for Telegram bot...")
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", "web.app:app", "--host", "127.0.0.1", "--port", "8000", "--reload"
        ])
    except Exception as e:
        logger.exception("-x-> Web server for Telegram crashed")
