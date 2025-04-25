import os
from libs.logger import logger


def save_to_file(path: str, content: str):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info(f"Saved content to {path}")
    except Exception as e:
        logger.exception(f"-x-> Failed to save content to {path}")
        raise
