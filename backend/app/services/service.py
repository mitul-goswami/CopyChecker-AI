from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import requests
import os
import io
from dotenv import load_dotenv
from ironpdf import *

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Get the Google Cloud Vision API key from environment variables
API_KEY = os.getenv("CLOUD_VISION_API_KEY")

@app.post("/detect-text/")
async def detect_text(file: UploadFile = File(...)):
    # Read the PDF file
    pdf_content = await file.read()

    # Save the PDF content to a temporary file
    temp_pdf_path = "temp.pdf"
    with open(temp_pdf_path, "wb") as temp_pdf_file:
        temp_pdf_file.write(pdf_content)

    # Convert PDF to images using IronPDF
    pdf = PdfDocument(temp_pdf_path)
    text_results = []

    for i in range(pdf.PageCount):
        # Render the page to an image
        image = pdf.get_Pages(i).Render()
        
        # Save the image to a byte array
        img_byte_arr = io.BytesIO()
        image.SaveAsPng(img_byte_arr)
        img_byte_arr.seek(0)

        # Prepare the request for the Vision API
        url = f"https://vision.googleapis.com/v1/images:annotate?key={API_KEY}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "requests": [
                {
                    "image": {
                        "content": img_byte_arr.getvalue().decode('ISO-8859-1')  # Encode image bytes to base64
                    },
                    "features": [
                        {
                            "type": "DOCUMENT_TEXT_DETECTION"
                        }
                    ]
                }
            ]
        }

        # Perform text detection
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            texts = response.json().get('responses', [])
            if texts and 'fullTextAnnotation' in texts[0]:
                detected_text = texts[0]['fullTextAnnotation']['text']
                text_results.append(detected_text)
        else:
            return JSONResponse(status_code=response.status_code, content={"error": response.text})

    # Clean up the temporary PDF file
    os.remove(temp_pdf_path)

    return {"detected_text": text_results}

# To run the application, use the command:
# uvicorn your_script_name:app --reload