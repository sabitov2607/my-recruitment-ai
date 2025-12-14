import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from ai_module import process_candidate

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "backend/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

@app.post("/analyze")
async def analyze_candidate(
    file: UploadFile = File(...),
    vacancy: str = Form(...)
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    result = process_candidate(file_path, vacancy)

    return {
        "filename": file.filename,
        "skills": result["skills"],
        "match_score": result["match_score"],
        "preview": result["cv_text"]
    }
