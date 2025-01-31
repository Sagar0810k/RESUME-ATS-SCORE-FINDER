import google.generativeai as genai
import os
import re
from dotenv import load_dotenv
from utils.resume_parser import extract_text  

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_resume(filepath):
    """
    Extract text from a resume and analyze it using Gemini API.
    """
    resume_text = extract_text(filepath)  # Extract plain text from PDF or DOCX

    if not resume_text.strip():
        return "Error: Could not extract text from the file.", []

    prompt = f"""
    You are an ATS (Applicant Tracking System) resume analyzer.
    Analyze the following resume and provide:

    **1. ATS Score (out of 100):**
    - Example: "ATS Score: 85"

    **2. 5 Key Improvement Points (Numbered List)**
    - Example:
      1. Missing industry keywords.
      2. Resume formatting needs improvement.
      3. Improve bullet point consistency.
      4. Use more quantifiable achievements.
      5. Reduce personal information..

    Resume Content:
    {resume_text}
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    # Process API response
    lines = response.text.split("\n")
    ats_score = None
    feedback_points = []

    score_pattern = re.compile(r'ATS Score.*?(\d{1,3})')  
    
    for line in lines:
        match = score_pattern.search(line)  # Check if the line contains an ATS score
        if match:
            ats_score = int(match.group(1))  # Extract and convert the score to integer
        else:
            feedback_points.append(line.strip())

    selected_points = [feedback_points[i] for i in [3, 5, 7, 9, 11] if i < len(feedback_points)]

    return ats_score, selected_points  
