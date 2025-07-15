# 📄 Resume Analyzer

A smart web application that analyzes resumes and predicts the most suitable job role using NLP and Machine Learning. Built with Flask, this tool helps automate the resume screening process for recruiters and HR professionals.

---

## 🚀 Features

- 📂 Upload resumes in PDF or DOCX format  
- 🧠 Extracts skills,name,education, and experience  
- 🔍 Predicts relevant job category using an ML model  
- 💾 Stores uploaded data in MongoDB  
- 🌐 Simple and clean web interface

---

## 🧠 Tech Stack

- **Frontend**: HTML, CSS, Bootstrap  
- **Backend**: Flask (Python)  
- **NLP & ML**: scikit-learn, spaCy, TfidfVectorizer  
- **Database**: MongoDB  
- **Others**: PyPDF2, python-docx, pandas

---

## 📁 Project Structure

resume_analyzer/
├── app.py # Main Flask app
├── job_predictor.py # ML prediction logic
├── models/ # Trained model & vectorizer
├── templates/ # HTML templates
│ ├── index.html
│ └── result.html
├── static/
│ └── uploads/ # Uploaded resumes
├── utils/ # Resume parsing functions
├── requirements.txt # Project dependencies
└── README.md # Project documentation