from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging

from resume_parser import extract_text_from_pdf, extract_text_from_docx
from skill_extractor import extract_skills
from matcher import calculate_match, find_missing_skills

# Initialize app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "AI Resume Analyzer Backend is Running"

@app.route("/upload", methods=["POST"])
def upload_resume():
    try:

        # Check resume file
        if "resume" not in request.files:
            return jsonify({"status": "error", "message": "No resume uploaded"}), 400

        # Check job description
        if "job_description" not in request.form:
            return jsonify({"status": "error", "message": "Job description is required"}), 400

        job_description = request.form["job_description"]

        file = request.files["resume"]
        filename = file.filename

        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Extract text
        if filename.endswith(".pdf"):
            with open(filepath, "rb") as f:
                resume_text = extract_text_from_pdf(f)

        elif filename.endswith(".docx"):
            resume_text = extract_text_from_docx(filepath)

        else:
            return jsonify({
                "status": "error",
                "message": "Only PDF and DOCX files are allowed"
            }), 400

        # Extract skills
        skills_found = extract_skills(resume_text)

        # Calculate match score
        match_score = calculate_match(resume_text, job_description)

        # Find missing skills
        missing_skills = find_missing_skills(skills_found, job_description)

        logging.info("Resume analyzed successfully")

        return jsonify({
            "status": "success",
            "data": {
                "match_score": match_score,
                "skills_found": skills_found,
                "missing_skills": missing_skills
            }
        })

    except Exception as e:
        logging.error(str(e))
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)