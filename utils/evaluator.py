import json
import requests
import re
import concurrent.futures
import pytesseract
import cv2
import numpy as np
import time
from ultralytics import YOLO
from pdf2image import convert_from_path
from PIL import Image
from werkzeug.utils import secure_filename

# Configuration for OCR components
TESSERACT_PATH = r'C://Program Files//tesseract.exe'
POPPLER_PATH = r'C://poppler-24.02.0//Library//bin'
YOLO_MODEL = 'yolov8n-seg.pt'
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

# Groq API Configuration
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

# OCR Pipeline Functions
def pdf_to_images(pdf_path):
    """Convert PDF to optimized images for OCR"""
    return convert_from_path(
        pdf_path, 
        dpi=300,
        thread_count=4,
        fmt='jpeg',
        poppler_path=POPPLER_PATH
    )

def preprocess_for_yolo(img):
    """Enhanced preprocessing for YOLOv8 text detection"""
    img_np = np.array(img)
    if img_np.shape[-1] == 4:
        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGBA2RGB)
    lab = cv2.cvtColor(img_np, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    limg = cv2.merge((clahe.apply(l), a, b))
    return cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)

def layout_analysis(image):
    """YOLOv8 text block segmentation"""
    model = YOLO(YOLO_MODEL)
    try:
        results = model(
            image, 
            imgsz=1280, 
            conf=0.4, 
            classes=[91],
            verbose=False
        )
        return results[0].masks.xy if results and results[0].masks else []
    except Exception as e:
        print(f"YOLOv8 Error: {str(e)}")
        return []

def process_page(args):
    """Page processing pipeline"""
    page_num, image = args
    start_time = time.time()
    
    processed_img = preprocess_for_yolo(image)
    text_regions = layout_analysis(processed_img)
    
    if not text_regions:
        text = pytesseract.image_to_string(
            image, config='--psm 11 -c preserve_interword_spaces=1'
        )
    else:
        crops = [image.crop((x1,y1,x2,y2)) for region in text_regions for x1,y1,x2,y2 in region]
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            ocr_results = list(executor.map(
                lambda img: pytesseract.image_to_string(img, config='--psm 6'),
                crops
            ))
        sorted_results = sorted(zip(
            [crop.getbbox() for crop in crops],
            ocr_results
        ), key=lambda x: (x[0][1], x[0][0]))
        text = '\n'.join([res[1].strip() for res in sorted_results if res[1].strip()])
    
    return (page_num, text, time.time() - start_time)

def ocr_pipeline(pdf_path, output_file):
    """End-to-end OCR pipeline"""
    total_start = time.time()
    images = pdf_to_images(pdf_path)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_page, (i+1, img)) for i, img in enumerate(images)]
        results = []
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    
    results.sort(key=lambda x: x[0])
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join([res[1] for res in results]))

# Evaluation Functions
def extract_text_from_pdf(pdf_path, output_file):
    ocr_pipeline(pdf_path, output_file)
    with open(output_file, 'r', encoding='utf-8') as f:
        return f.read().strip()

def split_answers(text, is_model=False):
    qna_dict = {}
    pattern = (
        r"Question\s*(\d+)\.\s*(.*?)\s*\[(\d+)\]\s*\nAnswer\.\s*(.*?)(?=\nQuestion\s*\d+\.|\Z)"
        if is_model
        else r"Question\s*(\d+)\.\s*(.*?)\nAnswer\.\s*(.*?)(?=\nQuestion\s*\d+\.|\Z)"
    )
    matches = re.findall(pattern, text, re.DOTALL)
    for match in matches:
        q_num = match[0].strip()
        if is_model:
            question, marks, answer = match[1].strip(), int(match[2].strip()), match[3].strip()
            qna_dict[q_num] = {"question": question, "answer": answer, "marks": marks}
        else:
            question, answer = match[1].strip(), match[2].strip()
            qna_dict[q_num] = {"question": question, "answer": answer}
    return qna_dict

def extract_score(response_text, max_marks):
    match = re.search(rf"Score:\s*(\d+\.?\d*)\s*/\s*{max_marks}", response_text)
    return float(match.group(1)) if match else 0

def evaluate_answer(model_answer, student_answer, max_marks):
    prompt = f"""
    Evaluate the student's answer against the model answer. Provide a score out of {max_marks} with feedback.
    Model Answer:
    {model_answer}
    Student Answer:
    {student_answer}
    Start with 'Score: X/{max_marks}'.
    """
    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a technical evaluator."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(GROQ_API_URL, headers=HEADERS, json=data)
    return response.json()["choices"][0]["message"]["content"] if response.status_code == 200 else "Error"

# Main Evaluation Flow
def evaluate_pdfs(model_pdf_path, student_pdf_path):
    model_answers = extract_text_from_pdf(model_pdf_path, "model_output.txt")
    student_answers = extract_text_from_pdf(student_pdf_path, "student_output.txt")

    model_qna = split_answers(model_answers, is_model=True)
    student_qna = split_answers(student_answers)

    grades = {}
    total_score = 0
    full_marks = sum(q["marks"] for q in model_qna.values())

    for q_num, model_data in model_qna.items():
        if q_num not in student_qna:
            continue
        student_data = student_qna[q_num]
        max_marks = model_data["marks"]
        model_text = f"{model_data['question']}\n{model_data['answer']}"
        student_text = f"{student_data['question']}\n{student_data['answer']}"
        result = evaluate_answer(model_text, student_text, max_marks)
        score = extract_score(result, max_marks)
        grades[q_num] = {"score": score, "feedback": result, "max_marks": max_marks}
        total_score += score

    return {
        "grades": grades,
        "total_score": total_score,
        "full_marks": full_marks,
        "percentage": (total_score / full_marks) * 100
    }

if __name__ == "__main__":
    results = evaluate_pdfs("model_answer.pdf", "student_answer.pdf")
    print(f"Total Score: {results['total_score']}/{results['full_marks']} ({results['percentage']:.2f}%)")
