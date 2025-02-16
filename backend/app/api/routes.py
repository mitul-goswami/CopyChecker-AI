from fastapi import UploadFile, File, APIRouter
from fastapi.responses import JSONResponse
from io import BytesIO
import fitz
from services.pdfer import extract_text_and_images
from services.dbops import dbOps

router = APIRouter()
ops = dbOps()

@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    pdf_stream = BytesIO(await file.read())
    cont = extract_text_and_images(pdf_stream)
    ops.insert_text(cont["text"])
    ops.insert_img(cont["text"])
    return JSONResponse(content=cont)
