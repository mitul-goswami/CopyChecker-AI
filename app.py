import os
import uuid
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from utils.evaluator import evaluate_pdfs

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit
app.secret_key = os.urandom(24)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session_id = str(uuid.uuid4())
        os.makedirs(f"uploads/{session_id}", exist_ok=True)
        
        model_file = request.files['model_answer']
        student_file = request.files['student_answer']
        
        if model_file and allowed_file(model_file.filename):
            model_path = os.path.join(app.config['UPLOAD_FOLDER'], session_id, 
                           secure_filename("model_answer.pdf"))
            model_file.save(model_path)
            
        if student_file and allowed_file(student_file.filename):
            student_path = os.path.join(app.config['UPLOAD_FOLDER'], session_id,
                             secure_filename("student_answer.pdf"))
            student_file.save(student_path)
            
        return redirect(url_for('results', session_id=session_id))
    
    return render_template('index.html')

@app.route('/results/<session_id>')
def results(session_id):
    try:
        results = evaluate_pdfs(f"uploads/{session_id}/model_answer.pdf",
                               f"uploads/{session_id}/student_answer.pdf")
        return render_template('results.html', results=results)
    except Exception as e:
        return render_template('error.html', error=str(e))

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)