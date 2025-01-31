import fitz  
from docx import Document
import pytesseract  
from PIL import Image  

def extract_text(file_path):
    """
    Extracts text from a PDF or DOCX file.
    If the PDF is scanned (image-based), OCR will be attempted.
    """
    text = ""

    if file_path.endswith(".pdf"):
        doc = fitz.open(file_path)

        for page in doc:
            page_text = page.get_text("text")  # Preserve formatting
            if not page_text.strip():  
                img = page.get_pixmap()  
                img = Image.frombytes("RGB", [img.width, img.height], img.samples)
                page_text = pytesseract.image_to_string(img)  # Extract text using OCR

            text += page_text + "\n"

    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"

    text = text.strip()
    
    if not text:  
        raise ValueError("Error: Could not extract text from the file.")

    return text
