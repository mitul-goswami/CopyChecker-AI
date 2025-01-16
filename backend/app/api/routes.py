from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from http import HTTPStatus
import PyPDF2 as pdf
import io

app = FastAPI()

@app.post('/ocr')
async def ocr(file: UploadFile = File(...)):
    filename = file.filename
    
    if ".pdf" not in filename:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="file type is not pdf",
        )
    
    pdf_file = await file.read()
    pdf_stream = io.BytesIO(pdf_file)
    reader = pdf.PdfReader(pdf_stream)
    no = len(reader.pages)

    if no > 4:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="no of pages must be less than or equal to 4",
        )

    return {
        "filename": filename,
        "page_count": no
    }