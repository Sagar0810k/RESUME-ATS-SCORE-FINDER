import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_suggestions(resume_text):
    prompt = f"""
    Analyze this resume and suggest improvements for ATS compatibility.
    
    Resume:
    {resume_text}

    Your response should include:
    - Missing keywords relevant to ATS
    - Formatting improvements
    - Readability enhancements
    - Any errors or inconsistencies

    Provide clear and concise bullet-pointed suggestions.
    """
    
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text.split("\n")
