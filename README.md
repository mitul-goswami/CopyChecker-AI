#  CopyChecker-AI  
### AI-Powered Intelligent Answer Evaluation System  

> A full-stack AI system that performs automated evaluation of student answer sheets based upon model answer key provided.

---

## 🌐 Overview

CopyChecker-AI is an intelligent academic evaluation system that:

- 📄 Accepts Model Answer Key and Student Answer PDFs  
- 🧠 Extracts text and images using advanced OCR pipelines  
- 🖼 Performs layout-aware segmentation using YOLOv8  
- 🔍 Detects structural and semantic similarities  
- 🤖 Uses LLM reasoning (Groq API) for evaluation scoring  
- ⚡ Generates structured evaluation results  

The system goes beyond simple text matching by combining:

- Computer Vision  
- OCR  
- Document Layout Analysis  
- Large Language Model evaluation  
- Parallel processing pipelines  

This makes it significantly more advanced than traditional plagiarism detection tools.

---

# 🎯 Problem Statement

Traditional answer checkers:

- ❌ Rely only on text matching
- ❌ Fail on scanned handwritten PDFs
- ❌ Ignore layout structure
- ❌ Cannot evaluate answer quality

CopyChecker-AI solves this by:

- Converting PDFs into high-resolution images
- Performing layout-aware segmentation
- Extracting text via OCR
- Using LLM-based semantic comparison
- Producing contextual evaluation output

---

# 🧠 Core Technologies Used

## 🔹 Backend & Frontend

- Python
- Flask (Backend interface)
- HTML & CSS (Frontend interface)

## 🔹 Computer Vision

- OpenCV
- YOLOv8 (Ultralytics)
- Image preprocessing with CLAHE
- Layout-aware segmentation

## 🔹 OCR & Document Processing

- Tesseract OCR
- pdf2image
- Poppler
- PyMuPDF (fitz)

## 🔹 AI & NLP

- Groq API (LLM reasoning)
- LangChain

## 🔹 Database

- Vector Indexing
- Full-text Search Index

---

# ⚙️ Key Engineering Components

---

## 1️⃣ PDF Processing Engine

### Features:

- Converts PDFs to 300 DPI images
- Multi-threaded page conversion
- Handles scanned and handwritten PDFs
- Extracts both text and embedded images

---

## 2️⃣ Layout-Aware Segmentation (YOLOv8)

Instead of naive OCR:

- Detects text blocks using YOLO segmentation model
- Extracts structured regions
- Preserves logical content flow

This improves:

- OCR accuracy
- Content alignment
- Context grouping

---

## 3️⃣ Intelligent OCR Pipeline

### Preprocessing:

- LAB color space conversion
- CLAHE contrast enhancement
- RGB normalization

### Extraction:

- Tesseract OCR
- Page-wise concurrent processing

Improves:

- Low contrast scan handling
- Handwritten text clarity
- Reduced OCR noise

---

## 4️⃣ Parallel Page Processing

Uses:
- `concurrent.futures`
- Multi-threading for performance

Benefit:
- Faster evaluation for multi-page PDFs
- Scalable evaluation architecture

---

## 5️⃣ LLM-Based Semantic Evaluation

Instead of simple similarity scores:

- Sends extracted content to Groq LLM endpoint
- Uses contextual comparison prompts
- Produces structured evaluation output


This enables:

- Context-aware grading
- Semantic similarity detection
- Answer quality assessment
