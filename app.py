import os
import pdfplumber
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from flask import Flask, render_template, request
import uuid  # To generate a unique filename for each upload

# Initialize Flask app
app = Flask(__name__)

# Set up upload folder and allowed file extensions
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Ensure that the uploads folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Allowed file extensions check
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Step 1: Extract Text from PDF
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
            # Optionally, limit text length here (e.g., 1000 characters per page)
            if len(text) > 2000:  # Limit the text to the first 2000 characters
                break
    return text


# Step 2: Generate Questions from Text
question_generator = pipeline("text2text-generation", model="t5-small")

def generate_questions(text, num_questions=5):
    # Use top-k sampling to generate diverse sequences
    questions = question_generator(text, max_length=512, num_return_sequences=num_questions, do_sample=True, top_k=50)
    return [q['generated_text'] for q in questions]


# Step 3: Evaluate Answers Using Semantic Similarity
model = SentenceTransformer('all-MiniLM-L6-v2')

def evaluate_answer(user_answer, correct_answer):
    user_embedding = model.encode(user_answer, convert_to_tensor=True)
    correct_embedding = model.encode(correct_answer, convert_to_tensor=True)
    similarity = util.cos_sim(user_embedding, correct_embedding).item()
    return similarity

# Flask Application Setup
questions_answers = []

@app.route('/', methods=['GET', 'POST'])
def home():
    global questions_answers
    if request.method == 'POST':
        # Handle file upload
        file = request.files['file']
        if file and allowed_file(file.filename):
            # Save the uploaded file with a unique filename
            filename = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4().hex}_{file.filename}")
            file.save(filename)
            
            # Extract text from the uploaded PDF
            pdf_text = extract_text_from_pdf(filename)
            
            # Generate questions (only done once per session)
            if not questions_answers:
                questions = generate_questions(pdf_text, num_questions=5)
                # Placeholder for correct answers (to be replaced with real answers)
                questions_answers = [{"question": q, "answer": "Example Answer"} for q in questions]
            
            return render_template('index.html', questions=questions_answers)
    
    return render_template('index.html', questions=[])

@app.route('/submit', methods=['POST'])
def submit():
    user_answers = request.form
    score = 0
    detailed_feedback = []

    for i, qa in enumerate(questions_answers):
        user_answer = user_answers.get(f"q{i}")
        correct_answer = qa["answer"]
        similarity = evaluate_answer(user_answer, correct_answer)

        if similarity > 0.8:  # Threshold for considering the answer correct
            score += 1
        detailed_feedback.append({
            "question": qa["question"],
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "similarity": similarity
        })

    return render_template('result.html', score=score, feedback=detailed_feedback, total=len(questions_answers))

if __name__ == '__main__':
    from multiprocessing import freeze_support
    freeze_support()
    # Place your app's running code here (e.g., Flask or FastAPI app)
    app.run(debug=True)  # Replace with whatever you're using to run your app