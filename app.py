from flask import Flask, request, render_template
from pymongo import MongoClient
import os
from job_predictor import predict_resume
import hashlib

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# MongoDB Setup
client = MongoClient('mongodb://localhost:27017/')
db = client['resume_analyzer']
collection = db['resumes']

def get_resume_has(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'resume' not in request.files:
        return render_template('results.html', prediction='No file uploaded.')

    file = request.files['resume']
    if file.filename == '':
        return render_template('results.html', prediction='No selected file.')

    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        result = predict_resume(file_path)
        resume_has = get_resume_has(result['text'])
        
        existing = collection.find_one({'resume_has':resume_has})
        if existing:
            print("duplicate resume. Not inserting.")
        else:
            collection.insert_one({
                'filename': file.filename,
                'filepath': file_path,
                'name': result['name'],
                'email': result['email'],
                'predicted_job': result['job'],
                'resume_score': result['score'],
                'resume_has':resume_has
            })

        return render_template(
            'results.html',
            prediction=result['job'],
            name=result['name'],
            email=result['email'],
            score=result['score']
        )

    return render_template('results.html', prediction='Invalid file format. Only PDFs are allowed.')

if __name__ == '__main__':
    app.run(debug=True)
