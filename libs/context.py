import time
import traceback
from libs.logger import logger
from libs.tokens import TokenCounter


class ProcessingContextManager:
    def __enter__(self):
        self.start_time = time.time()
        self.token_counter = TokenCounter()
        logger.info("Started processing.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        tokens_used = self.token_counter.get_total_tokens()

        if exc_type:
            logger.error("Exception occurred:")
            logger.error(''.join(traceback.format_exception(exc_type, exc_val, exc_tb)))
        else:
            logger.info("Processing completed successfully.")

        logger.info(f"Duration: {duration:.2f} seconds")
        logger.info(f"Total tokens used: {tokens_used}")
