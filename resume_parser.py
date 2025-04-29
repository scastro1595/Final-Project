# resume_parser.py
import docx
import PyPDF2
import re


def extract_text_from_pdf(file_path):
    """
    Extract text from PDF files

    Args:
        file_path (str): Path to the PDF file

    Returns:
        str: Extracted text from the PDF
    """
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""


def extract_text_from_docx(file_path):
    """
    Extract text from DOCX files

    Args:
        file_path (str): Path to the DOCX file

    Returns:
        str: Extracted text from the DOCX
    """
    try:
        doc = docx.Document(file_path)
        return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return ""


def extract_text_from_txt(file_path):
    """
    Extract text from TXT files

    Args:
        file_path (str): Path to the TXT file

    Returns:
        str: Extracted text from the TXT
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading TXT file: {e}")
        return ""


def parse_resume(file_path):
    """
    Parse resume and extract skills from various file types

    Args:
        file_path (str): Path to the resume file

    Returns:
        list: Extracted skills
    """
    # Determine file type
    file_extension = file_path.lower().split('.')[-1]

    # Extract text based on file type
    if file_extension == 'pdf':
        text = extract_text_from_pdf(file_path)
    elif file_extension in ['docx', 'doc']:
        text = extract_text_from_docx(file_path)
    elif file_extension == 'txt':
        text = extract_text_from_txt(file_path)
    else:
        print(f"Unsupported file type: {file_extension}")
        return []

    # Convert to lowercase and remove special characters
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())

    # Split into words
    words = text.split()

    # Filter and clean skills
    skills = list(set(
        word for word in words
        if len(word) > 2 and  # Longer than 2 characters
        not word.isdigit()  # Not a number
    ))

    return skills
