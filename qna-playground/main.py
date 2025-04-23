from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
import asyncio
from pathlib import Path
import pdfplumber 

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok = True)

def extract_text_from_pdf(pdf_path: str) ->str:
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
        return text

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)


    extracted_text = extract_text_from_pdf(file_location)
    asyncio.create_task(delete_file_after_delay(file_location, 300))
    return {"filename": file.filename, "status": "uploaded", "extracted_text": extracted_text[500]}

@app.post("/ask/")
async def ask_question(question: str = Form(...)):
    return JSONResponse(content = {
        "question": question, 
        "answer": "this is a dummy answer, the rela answer will come once we process the file!"
    })


async def delete_file_after_delay(file_location: str, delay: int):
    await asyncio.sleep(delay)

    file_path = Path(file_location)

    if(file_path.exists()):
        file_path.unlink()
        print(f"{file_location} deleted after {delay} seconds")
    else:
        print(f"{file_location} not found.")