import os
from services.llm import query_openai
from prompts.summary import summary_prompt
from prompts.contents import contents_prompt
from libs.context import ProcessingContextManager
from libs.logger import logger

OUTPUT_DIR = "output"


def run_script_mode():
    doc_path = os.getenv("DOCUMENT_PATH")
    if not doc_path or not os.path.exists(doc_path):
        logger.error("-x-> DOCUMENT_PATH is not set or file does not exist.")
        return

    summary_path = os.path.join(OUTPUT_DIR, "script_summary.txt")
    contents_path = os.path.join(OUTPUT_DIR, "script_contents.txt")

    try:
        with open(doc_path, "r", encoding="utf-8") as f:
            content = f.read()

        with ProcessingContextManager() as ctx:
            summary = query_openai(summary_prompt, content, ctx.token_counter)
            with open(summary_path, "w", encoding="utf-8") as f:
                f.write(summary)
            logger.info(f"Summary saved to: {summary_path}")
            logger.info(f"Tokens used: {ctx.token_counter.total_tokens}")

        with ProcessingContextManager() as ctx:
            contents = query_openai(contents_prompt, content, ctx.token_counter)
            with open(contents_path, "w", encoding="utf-8") as f:
                f.write(contents)
            logger.info(f"Contents saved to: {contents_path}")
            logger.info(f"Tokens used: {ctx.token_counter.total_tokens}")

    except Exception as e:
        logger.exception("Error in script mode")
