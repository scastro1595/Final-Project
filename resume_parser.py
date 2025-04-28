# resume_parser.py
from docx import Document
import PyPDF2

def parse_resume(file_path):
    skills = []

    if file_path.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file_path)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                skills.extend(text.lower().split())

    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        for para in doc.paragraphs:
            skills.extend(para.text.lower().split())

    # Simulate extracting keywords (basic filtering)
    keywords = ['python', 'java', 'c++', 'javascript', 'html', 'css', 'sql', 'management', 'leadership', 'aws']
    extracted_skills = [word for word in skills if word in keywords]

    return list(set(extracted_skills))
