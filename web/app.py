from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from api.endpoints import app as api_app
from pathlib import Path
import shutil
import os
import httpx
from libs.logger import logger

app = FastAPI()

# Mount internal API and static files
app.mount("/api", api_app)
app.mount("/static", StaticFiles(directory="web/static"), name="static")

templates = Jinja2Templates(directory="web/templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def upload(request: Request, document: UploadFile = File(...), mode: str = Form(...)):
    safe_name = Path(document.filename).name
    temp_path = f"temp_{safe_name}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(document.file, buffer)

    logger.info(f"Received file '{safe_name}' with mode '{mode}'")

    try:
        if mode == "summary":
            result = await get_summary_from_api(temp_path)
        elif mode == "contents":
            result = await get_contents_from_api(temp_path)
        else:
            result = "Invalid mode selected."
    finally:
        os.remove(temp_path)

    return templates.TemplateResponse("index.html", {"request": request, "result": result})


async def get_summary_from_api(file_path: str) -> str:
    async with httpx.AsyncClient() as client:
        with open(file_path, "rb") as file:
            response = await client.post("http://localhost:8000/api/v1/get_summary", files={"file": file})

    if response.status_code == 200:
        data = response.json()
        return data.get("summary", "No summary found.")
    else:
        logger.error(f"API error: {response.status_code} - {response.text}")
        return f"API error: {response.status_code}"


async def get_contents_from_api(file_path: str) -> str:
    async with httpx.AsyncClient() as client:
        with open(file_path, "rb") as file:
            response = await client.post("http://localhost:8000/api/v1/get_contents_and_theses", files={"file": file})

    if response.status_code == 200:
        data = response.json()
        return data.get("contents", "No contents found.")
    else:
        logger.error(f"API error: {response.status_code} - {response.text}")
        return f"API error: {response.status_code}"
