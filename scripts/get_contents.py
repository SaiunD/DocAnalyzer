import os
from services.llm import query_openai
from libs.context import ProcessingContextManager
from libs.storage import save_to_file
from prompts.contents import contents_prompt
from libs.logger import logger

input_path = os.getenv("DOCUMENT_PATH")
output_path = os.getenv("CONTENTS_OUTPUT_PATH")

if not input_path or not os.path.exists(input_path):
    logger.error("-x-> DOCUMENT_PATH is not set or file does not exist.")
    exit(1)

try:
    logger.info(f"Reading document from: {input_path}")
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    with ProcessingContextManager() as context:
        logger.info("Generating contents and theses...")
        result = query_openai(contents_prompt, text, context.token_counter)

        logger.info(f"Saving result to: {output_path}")
        save_to_file(output_path, result)

except Exception as e:
    logger.exception("-x-> Error while generating contents and theses")
