import base64
from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form, logger
from pydantic import BaseModel
import requests
from io import BytesIO
from fastapi.responses import Response

server = FastAPI()

API_TOKEN = "0784c37334e44f509b4343f27d90de40"

REMOVE_BG_URL = "https://engine.prod.bria-api.com/v1/background/remove"
# REPLACE_BG_URL = "https://engine.prod.bria-api.com/v1/background/replace"


@server.get("/test")
async def test_server():
    return {"message": "Server is running successfully!"}

@server.post("/remove-background")
async def remove_background(request: Request):
        image_data = await request.body()

        result = call_bria_api(REMOVE_BG_URL, files={"file": image_data})

        return result


# class ImageRequest(BaseModel):
#     prompt: str
#     image: str 


# @server.post("/generate-background")
# async def generate_image(request_data: ImageRequest):

#     image_file =request_data.image
#     result = call_bria_api(REPLACE_BG_URL, data={"bg_prompt": request_data.prompt,"file": image_file})

#     return result



def call_bria_api(url: str, files=None, data=None, json=None):
    headers = {
        "api_token": API_TOKEN}
    
    try:
        response = requests.post(url, headers=headers, data=data,files=files,json=json)
        
        print(response)
        if response.status_code == 200:
            return response.json()
        else:
            return 'Failed to process image'
    
    except Exception as e:
        return str(e)
    
