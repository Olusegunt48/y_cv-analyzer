import pdfplumber
import re

def extract_text_from_pdf(uploaded_file):
    """Extracts text from an uploaded PDF file."""
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_email(text):
    """Extracts email from the resume text."""
    match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    return match.group(0) if match else None

def extract_name(text):
    """Extracts name (basic approach, can be improved with NLP)."""
    lines = text.split("\n")
    return lines[0] if lines else "Unknown"

def extract_skills(text):
    """Extracts skills from resume text (basic keyword matching)."""
    predefined_skills = {"Python", "SQL", "Machine Learning", "Data Science", "Excel", "Tableau"}
    words = set(text.split())
    return list(predefined_skills.intersection(words))

def extract_education(text):
    """Extracts education details (basic pattern matching)."""
    education_keywords = ["Bachelor", "Master", "PhD", "University", "Degree", "National Diploma"]
    for line in text.split("\n"):
        if any(keyword in line for keyword in education_keywords):
            return line
    return "Not Found"

def parse_resume(uploaded_file):
    """Parses resume and extracts details."""
    text = extract_text_from_pdf(uploaded_file)
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
    }
