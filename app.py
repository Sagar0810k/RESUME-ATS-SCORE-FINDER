import os
import google.generativeai as genai
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from utils.ats_scoring import analyze_resume
from dotenv import load_dotenv

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure uploads directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Home Route - Upload Page
@app.route('/')
def index():
    return render_template('index.html')

# Resume Upload and Processing
@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['resume']
    if file.filename == '':
        return redirect(url_for('index'))

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Analyze Resume using Gemini API
    ats_score, feedback_points = analyze_resume(filepath)

    return render_template('result.html', ats_score=ats_score, feedback_points=feedback_points)

if __name__ == '__main__':
    app.run(debug=True)
