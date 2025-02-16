import os
import base64
from io import BytesIO
import fitz  # PyMuPDF

def extract_text_and_images(stream):
    if not isinstance(stream, BytesIO):
        raise ValueError("Expected a BytesIO object")
    
    pdf = {
        "text" : [],
        "image" : []
    }

    # Open the PDF from the BytesIO stream
    doc = fitz.open(stream=stream, filetype="pdf")
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        #pdf["text"].append(page.get_text())
        text = {
            "page_no" : page_num + 1,
            "content" : page.get_text(),
            "type" : "text"
        }

        pdf["text"].append(text)
        
        count = 0
        # Extract images from the page
        for img_index in page.get_images(full=True):
            xref = img_index[0]  # Get the xref of the image
            base_image = doc.extract_image(xref)  # Extract the image
            image_data = base_image["image"]  # Get the image data
            
            # Convert image data to base64
            encoded_image = base64.b64encode(image_data).decode('utf-8')
            count += 1
            image = {
                "page_no" : page_num + 1,
                "id" : f"{page_num + 1}.{count}",
                "content" : encoded_image,
                "type" : "img"
            }
            pdf["image"].append(image)

    return pdf