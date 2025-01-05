# PDF Question Generator App

This is a simple web application that allows users to upload a PDF, extract text from it, generate questions based on the extracted content, and then evaluate answers using semantic similarity. The app is built using Flask, pdfplumber, Hugging Face transformers, and SentenceTransformers.

## Features

- Upload a PDF file.
- Extract text from the PDF.
- Generate questions from the extracted text.
- Submit answers and receive feedback based on semantic similarity.

## Requirements

Before running the app, make sure you have the following installed:

- **Python 3.7+**
- **pip** (Python's package manager)

## Installation Steps

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/rodneykabiru/PDF_QA.git
cd PDF_QA
```
### 2. Set Up a Virtual Environment (Optional but Recommended)
It's a good practice to create a virtual environment to keep dependencies isolated:

```bash
python -m venv venv
```
On Windows, activate the virtual environment using:

```bash
venv\Scripts\activate
```
On macOS/Linux, use:

```bash
source venv/bin/activate
```
### 3. Install Dependencies
Install the required dependencies listed in requirements.txt:

```bash
pip install -r requirements.txt
Or manually install these dependencies:
```
```bash
pip install flask pdfplumber transformers sentence-transformers
```
### 4. Run the Application
To start the Flask application, run:

```bash
python app.py
The app will be available locally at http://127.0.0.1:5000/.
```
### 5. Open the App in Your Browser
Open your browser and go to http://127.0.0.1:5000/.
Upload a PDF file, and the app will generate questions based on the content of the PDF.
Submit your answers to get feedback on their similarity to the correct answers.
Folder Structure
```bash

PDF-QA-Project/
│
├── app.py                    # Your Flask application file
├── uploads/                  # Folder to store uploaded PDF files
│   └── (uploaded-pdfs)       # PDFs uploaded by users
├── templates/
│   ├── index.html            # Upload form and generated questions
│   └── result.html           # Display results (user answers and score)
├── venv/                     # Virtual environment (created by `python -m venv venv`)
├── requirements.txt          # List of dependencies (optional, but recommended)
└── README.md                 # Project documentation
```







