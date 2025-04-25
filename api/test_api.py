import requests
from libs.logger import logger

BASE_URL = "http://127.0.0.1:8000/api/v1"


def send_file_to_endpoint(endpoint: str, file_path: str):
    url = f"{BASE_URL}/{endpoint}"
    with open(file_path, "rb") as f:
        files = {"file": f}
        try:
            response = requests.post(url, files=files)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.exception(f"-x-> Failed request to {endpoint}")
            return {"error": str(e)}


def main():
    file_path = "./input/example.txt"

    logger.info("Testing /get_summary")
    result = send_file_to_endpoint("get_summary", file_path)
    print("Summary result:", result)

    logger.info("Testing /get_contents_and_theses")
    result = send_file_to_endpoint("get_contents_and_theses", file_path)
    print("Contents result:", result)


if __name__ == "__main__":
    main()
