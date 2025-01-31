import base64
from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form, logger
from pydantic import BaseModel
import requests
from io import BytesIO
from fastapi.responses import Response

server = FastAPI()
BRIA_API_TOKEN = "0784c37334e44f509b4343f27d90de40"
REMOVE_BG_URL = "https://engine.prod.bria-api.com/v1/background/remove"
GENERATE_BG_URL = "https://engine.prod.bria-api.com/v1/background/replace"

@server.get("/test")
async def test_server():
    return {"message": "Server is running successfully!"}

@server.post("/background/remove")
async def remove_background(file: UploadFile = File(...)):
        file_bytes = await file.read()  # Read file as bytes
         print(f"Received file: {file.filename}, Size: {len(file_bytes)} bytes")
        result = call_bria_api(REMOVE_BG_URL, files={"file": (file.filename, file_bytes, file.content_type)})
        return result

@server.post("/background/generate")
async def generate_image(request: Request):
    req_body = await request.body()
    # result = call_bria_api(REPLACE_BG_URL, data={"bg_prompt": request_data.prompt,"file": image_file})
    # return result

def call_bria_api(url: str, files=None, data=None, json=None):
    headers = {"api_token": BRIA_API_TOKEN}
    response = requests.post(url, headers=headers, data=data, files=files, json=json)
    if response.status_code == 200:
        return response.json()
    else:
        return 'Failed to process image'
