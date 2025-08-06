from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from app import detect_eye_state
from fastapi.responses import RedirectResponse

app = FastAPI(title="Eye State Detection API")

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

@app.post("/detect_eyes/")
async def detect_eyes(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = detect_eye_state(image_bytes)
    return JSONResponse(content=result)