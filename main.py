
from fastapi import FastAPI, HTTPException, UploadFile, File
import requests
from fastapi.responses import JSONResponse
from schemas import ImageGenerationRequest
import asyncio

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
        files={"file": (file.filename, file_bytes, file.content_type)}
        headers = {"api_token": BRIA_API_TOKEN}
        response = requests.post(REMOVE_BG_URL, headers=headers, files=files)
        if response.status_code == 200:
            return response.json()
        else:
            return 'Failed to process image'

@server.post("/background/generate")
async def generate_image(request: ImageGenerationRequest):
    try:
        headers = {"Content-Type": "application/json", "api_token": BRIA_API_TOKEN}
        payload = request.dict()
        response = requests.post(GENERATE_BG_URL, json=payload, headers=headers)
        if response.status_code == 200:
            result_data = response.json().get('result', [])
            
            # Format the results
            formatted_results = []
            for result in result_data:
                if len(result) >= 3:
                    image_url, seed, session_id = result
                    # Wait for image to be available if sync=false
                    is_available = await wait_for_image(image_url)
                    
                    formatted_results.append({
                        "image_url": image_url,
                        "seed": seed,
                        "session_id": session_id,
                        "is_available": is_available
                    })
            
            return JSONResponse(content={
                "status": "success",
                "results": formatted_results
            })
        else:
            return JSONResponse(
                status_code=response.status_code,
                content={
                    "status": "error",
                    "error": f"API Error: {response.status_code}",
                    "details": response.text
                }
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def wait_for_image(url: str, max_retries: int = 10, delay: int = 1):
    headers = {"api_token": BRIA_API_TOKEN}
    for _ in range(max_retries):
        response = requests.get(url, headers=headers)
        if response.status_code == 200 and len(response.content) > 0:
            return True
        await asyncio.sleep(delay)
    return False