import os
import subprocess
import time
import socket
import sys
import requests
from libs.logger import logger

OUTPUT_DIR = "output"


def wait_for_server(host="127.0.0.1", port=8000, timeout=10):
    logger.info("Waiting for server to start...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                logger.info("Server is up!")
                return True
        except OSError:
            time.sleep(0.5)
    logger.error("-x-> Server did not start in time.")
    return False


def run_rest_api_and_test():
    logger.info("Starting REST API server...")
    server = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "web.app:app", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    if not wait_for_server():
        logger.error("-x-> Server failed to start.")
        stdout, _ = server.communicate(timeout=5)
        logger.error(stdout)
        server.terminate()
        server.wait()
        return

    doc_path = os.getenv("DOCUMENT_PATH")
    if not doc_path or not os.path.exists(doc_path):
        logger.error("-x-> DOCUMENT_PATH not set or file missing.")
        return

    try:
        with open(doc_path, "rb") as f:
            files = {"file": f}
            logger.info("Sending request to /api/v1/get_summary ...")
            resp1 = requests.post("http://127.0.0.1:8000/api/v1/get_summary", files=files)
            data1 = resp1.json()
            summary = data1.get("summary", "")
            tokens1 = data1.get("tokens", "N/A")
            duration1 = data1.get("duration", "N/A")
            summary_path = os.path.join(OUTPUT_DIR, "api_summary.txt")
            with open(summary_path, "w", encoding="utf-8") as f:
                f.write(summary)
            logger.info(f"Summary: {tokens1} tokens, Duration: {duration1:.2f}s")
            logger.info(f"Summary saved to: {summary_path}")

        with open(doc_path, "rb") as f:
            files = {"file": f}
            logger.info("Sending request to /api/v1/get_contents_and_theses ...")
            resp2 = requests.post("http://127.0.0.1:8000/api/v1/get_contents_and_theses", files=files)
            data2 = resp2.json()
            contents = data2.get("contents", "")
            tokens2 = data2.get("tokens", "N/A")
            duration2 = data2.get("duration", "N/A")
            contents_path = os.path.join(OUTPUT_DIR, "api_contents.txt")
            with open(contents_path, "w", encoding="utf-8") as f:
                f.write(contents)
            logger.info(f"Contents: {tokens2} tokens, Duration: {duration2:.2f}s")
            logger.info(f"Contents saved to: {contents_path}")

    except Exception as e:
        logger.exception("-x-> Error during API testing")

    finally:
        logger.info("Stopping REST API server...")
        server.terminate()
        server.wait()
