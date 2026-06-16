from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def extract_text(pdf_path):
    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():

    file = request.files["resume"]

    path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(path)

    resume_text = extract_text(path)

    prompt = f"""
    Analyze this resume.

    Return:

    ATS Score /100

    Skills Found

    Missing Skills

    Resume Strengths

    Resume Weaknesses

    Improvement Suggestions

    Resume:

    {resume_text}
    """

    response = model.generate_content(prompt)

    result = response.text

    return render_template(
        "result.html",
        result=result
    )

if __name__ == "__main__":
    app.run(debug=True)