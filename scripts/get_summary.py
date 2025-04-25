import os
from services.llm import query_openai
from libs.context import ProcessingContextManager
from libs.storage import save_to_file
from prompts.summary import summary_prompt
from libs.logger import logger

input_path = os.getenv("DOCUMENT_PATH")
output_path = os.getenv("SUMMARY_OUTPUT_PATH")

if not input_path or not os.path.exists(input_path):
    logger.error("-x-> DOCUMENT_PATH is not set or file does not exist.")
    exit(1)

try:
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    with ProcessingContextManager() as context:
        result = query_openai(summary_prompt, text, context.token_counter)
        save_to_file(output_path, result)

except Exception as e:
    logger.exception("-x-> Error while generating summary")
