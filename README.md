# CopyChecker-AI



AI Copychecking is an innovative solution designed to automate the grading process by comparing original answer keys with students' handwritten answer scripts. The project uses advanced NLP techniques, similarity metrics, and OCR technology to provide an accurate grading system. The application is deployed on Azure and features a user-friendly frontend.

---

## Workflow

### Step-by-Step Process

1. **Input**:
   - Users upload two files:
     - The **original answer key** in PDF format.
     - The **student's handwritten notes** (image or scanned PDF).

2. **Text Extraction**:
   - **From PDFs (Typed Text)**:
     - Text is extracted using the `PyPDF2` library.
     - This ensures clean and structured text data from the answer key.
   - **From Handwritten Notes**:
     - Handwritten text is extracted using the **Gemini OCR API**.
     - The OCR API processes the image or scanned notes and converts it into machine-readable text.

3. **Text Comparison**:
   - **Naive Similarity**:
     - Basic word overlap and matching techniques are applied.
   - **Context-Based Similarity**:
     - Tools like `Gensim` and `Word2Vec` are used to measure the semantic similarity between the extracted texts.
   - **Evaluation Metrics**:
     - **BLEU** (Bilingual Evaluation Understudy): Measures precision-based similarity.
     - **ROUGE-N**: Measures recall-based similarity.

4. **Grading System**:
   - A grading algorithm assigns scores based on threshold values of BLEU, ROUGE-N, and other metrics.
   - These thresholds can be adjusted for different grading criteria.

5. **Frontend**:
   - A user-friendly interface allows:
     - File uploads.
     - Viewing similarity scores and grades.
   - Built using **Gradio** or **Hugging Face Spaces**.

6. **Deployment**:
   - The entire application is hosted on **Azure** for scalability and reliability.

---

## Tech Stack

### Libraries and Tools

1. **NLP Operations**:
   - [NLTK](https://www.nltk.org/): For basic text processing and tokenization.
   - [spaCy](https://spacy.io/): For advanced NLP tasks like named entity recognition and dependency parsing.

2. **Word Similarity Mapping by Context**:
   - [Gensim](https://radimrehurek.com/gensim/): For topic modeling and semantic similarity.
   - [Word2Vec](https://code.google.com/archive/p/word2vec/): For word embeddings and context-based similarity.

3. **Text Extraction**:
   - **Typed Text from PDFs**: [PyPDF2](https://pypi.org/project/PyPDF2/): For extracting text from PDF files.
   - **Handwritten Notes**: [Gemini OCR API](https://gemini.com/ocr-api): For converting handwritten content into text. (Paid API; ensure you have access.)

4. **Frontend**:
   - [Gradio](https://gradio.app/): For building interactive user interfaces.
   - [Hugging Face Spaces](https://huggingface.co/spaces): Alternative for hosting simple apps.

5. **Backend**:
   - [Flask](https://flask.palletsprojects.com/): Lightweight web framework for handling backend operations.
   - [FastAPI](https://fastapi.tiangolo.com/): For building APIs quickly and efficiently.

6. **Deployment**:
   - [Azure](https://azure.microsoft.com/): For hosting and scaling the application.

---

## Installation and Setup

### Prerequisites

1. Install **Python 3.8+**.
2. Create an **Azure account**.
3. Obtain a subscription for the **Gemini OCR API** (if needed).

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/ai-copychecking.git
   cd ai-copychecking
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Keys**:
   - Create a `config.py` file.
   - Add your API keys:
     ```python
     GEMINI_OCR_API_KEY = "your_api_key_here"
     ```

5. **Run the Application**:
   ```bash
   python app.py
   ```

6. **Access the Application**:
   - Open your browser and navigate to `http://localhost:5000`.

---

## Features

- **Automated Text Extraction**:
  - Extracts text from PDFs and handwritten notes seamlessly.
- **Advanced Comparison**:
  - Uses both naive and context-based similarity techniques.
- **Customizable Grading System**:
  - Adjust thresholds for BLEU, ROUGE-N, and other metrics.
- **Interactive Frontend**:
  - Simple interface for uploading files and viewing results.
- **Cloud Deployment**:
  - Hosted on Azure for high availability and scalability.

---

## Resources

- **BLEU Metric**: [BLEU Explained](https://en.wikipedia.org/wiki/BLEU)
- **ROUGE Metric**: [ROUGE Explained](https://en.wikipedia.org/wiki/ROUGE_(metric))
- **Gradio**: [Documentation](https://gradio.app/docs/)
- **Azure Deployment**: [Getting Started](https://learn.microsoft.com/en-us/azure/)
- **Gemini OCR API**: [API Details](https://gemini.com/ocr-api)
- **FastAPI**: [Documentation](https://fastapi.tiangolo.com/)

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
