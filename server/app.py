from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Backend Running"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

app = Flask(__name__)
CORS(app)

# ---------------- JOB SKILLS ----------------
job_roles = {
    "Data Analyst": ["python", "sql", "excel", "power bi", "data analysis"],
    "Data Scientist": ["python", "machine learning", "pandas", "numpy", "sql"],
    "Web Developer": ["html", "css", "javascript", "react", "node js"],
    "Data Engineer": ["python", "sql", "spark", "etl", "mongodb"]
}

# ---------------- ATS ----------------
def calculate_ats(text, role):

    text = text.lower()
    role_skills = job_roles.get(role, [])

    found = []
    missing = []

    score = 0

    for s in role_skills:
        if s in text:
            found.append(s)
            score += 20
        else:
            missing.append(s)

    if "project" in text:
        score += 5
    if "experience" in text:
        score += 5
    if len(text) > 800:
        score += 10

    if score > 100:
        score = 100

    return score, found, missing


# ---------------- JOB RECOMMENDATION ----------------
def recommend_jobs(text):

    text = text.lower()

    jobs = {
        "Data Analyst": ["python", "sql", "excel", "power bi"],
        "Data Scientist": ["python", "machine learning", "pandas"],
        "Web Developer": ["html", "css", "javascript", "react"],
        "Data Engineer": ["spark", "etl", "sql"]
    }

    result = []

    for job, skills in jobs.items():

        match = 0

        for s in skills:
            if s in text:
                match += 1

        score = int((match / len(skills)) * 100)

        if score >= 30:
            result.append({
                "role": job,
                "match": score,
                "skills": skills
            })

    return result


# ---------------- AI SUGGESTIONS ----------------
def ai_suggestions(missing):

    return [
        f"Learn {skill} and build a small project"
        for skill in missing
    ]


# ---------------- ROUTE ----------------
@app.route("/upload-resume", methods=["POST"])
def upload_resume():

    try:

        file = request.files.get("resume")
        role = request.form.get("role", "Data Scientist")

        if not file:
            return jsonify({"error": "No file"}), 400

        text = ""

        if file.filename.endswith(".pdf"):
            with pdfplumber.open(file) as pdf:
                for p in pdf.pages:
                    t = p.extract_text()
                    if t:
                        text += t

        if text.strip() == "":
            text = "No text extracted"

        ats, found, missing = calculate_ats(text, role)

        jobs = recommend_jobs(text)

        suggestions = ai_suggestions(missing)

        return jsonify({
            "resume_text": text,
            "ats_score": ats,
            "skills": found,
            "missing_skills": missing,
            "recommended_jobs": jobs,
            "suggestions": suggestions
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)