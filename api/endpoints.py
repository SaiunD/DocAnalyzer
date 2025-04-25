import time
from fastapi import UploadFile, File, APIRouter
from services.llm import query_openai
from prompts.summary import summary_prompt
from prompts.contents import contents_prompt
from libs.context import ProcessingContextManager

app = APIRouter(prefix="/v1")


@app.post("/get_summary")
async def get_summary(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")

    start_time = time.time()
    with ProcessingContextManager() as ctx:
        result = query_openai(summary_prompt, text, ctx.token_counter)
    duration = time.time() - start_time

    return {
        "summary": result,
        "tokens": ctx.token_counter.get_total_tokens(),
        "duration": duration
    }


@app.post("/get_contents_and_theses")
async def get_contents_and_theses(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")

    start_time = time.time()
    with ProcessingContextManager() as ctx:
        result = query_openai(contents_prompt, text, ctx.token_counter)
    duration = time.time() - start_time

    return {
        "contents": result,
        "tokens": ctx.token_counter.get_total_tokens(),
        "duration": duration
    }
