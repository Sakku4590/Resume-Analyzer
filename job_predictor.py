import fitz  # PyMuPDF
import pandas as pd
import joblib
import re

# Load model and encoder
model = joblib.load("models/resume_analyze.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

def extract_email(text):
    match = re.search(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', text)
    return match.group(0) if match else "Not found"

def extract_name(text):
    # Assume name is the first capitalized line (can be improved with NLP)
    lines = text.strip().split('\n')
    for line in lines:
        if line.strip() and line.strip()[0].isupper() and len(line.split()) <= 4:
            return line.strip()
    return "Not found"

def calculate_resume_score(text):
    # Simple scoring: based on word count
    word_count = len(text.split())
    if word_count > 800:
        return "Excellent"
    elif word_count > 500:
        return "Good"
    elif word_count > 300:
        return "Average"
    else:
        return "Needs Improvement"

def predict_resume(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    email = extract_email(text)
    name = extract_name(text)
    score = calculate_resume_score(text)

    input_df = pd.DataFrame({'Resume_str': [text]})
    pred_encoded = model.predict(input_df)
    pred_label = label_encoder.inverse_transform(pred_encoded)[0]

    return {
        'job': pred_label,
        'email': email,
        'name': name,
        'score': score,
        'text':text
    }
