# resume_parser.py
import re
from docx import Document
import PyPDF2


def parse_resume(file_path):
    skills = []

    if file_path.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file_path)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                skills.extend(extract_skills_from_text(text))

    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        for para in doc.paragraphs:
            skills.extend(extract_skills_from_text(para.text))

    # Remove duplicates and return the extracted skills
    return list(set(skills))


def extract_skills_from_text(text):
    # Define skill keywords (you can add more here as needed)
    keywords = ['python', 'java', 'c++', 'javascript', 'html', 'css', 'sql', 'management', 'leadership', 'aws']

    # Convert text to lowercase to make matching case-insensitive
    text = text.lower()

    # Use regular expression to extract keywords, handling word boundaries and punctuations
    skills = []
    for keyword in keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', text):
            skills.append(keyword)

    return skills
