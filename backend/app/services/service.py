from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import requests
import io
from pdf2image import convert_from_bytes
import os
from dotenv import load_dotenv

app = FastAPI()

API_KEY=os.getenv("CLOUD_VISION_API")

@app.post("/detect-text/")
async def detect_text(file: UploadFile = File(...)):
    # Read the PDF file
    pdf_content = await file.read()

    # Convert PDF to images
    images = convert_from_bytes(pdf_content)

    # Store the text results
    text_results = []

    for image in images:
        # Convert the image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # Prepare the request for the Vision API
        url = f"https://vision.googleapis.com/v1/images:annotate?key={API_KEY}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "requests": [
                {
                    "image": {
                        "content": img_byte_arr.decode('ISO-8859-1')  # Encode image bytes to base64
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

    return {"detected_text": text_results}

# To run the application, use the command:
# uvicorn your_script_name:app --reload