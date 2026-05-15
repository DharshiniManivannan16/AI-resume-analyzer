from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# ---------------- OPENROUTER API KEY ----------------
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
print("API KEY LOADED:", OPENROUTER_API_KEY)

# ---------------- FREE AI MODEL ----------------
AI_MODEL = "openai/gpt-3.5-turbo"

# ---------------- HOME ----------------
@app.route("/")
def home():
    return "🔥 AI Resume Analyzer Backend Running"

# ---------------- CHATBOT ----------------
@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()

        user_message = data.get("message", "")

        response = requests.post(

            url="https://openrouter.ai/api/v1/chat/completions",

            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:5173",
                "X-Title": "AI Resume Analyzer"
            },

            json={

                "model": AI_MODEL,

                "messages": [

                    {
                        "role": "system",
                        "content": """
You are a professional AI Resume Analyzer Assistant.

Help users with:
- ATS score improvement
- Resume optimization
- Skills improvement
- Career guidance
- Interview preparation
- Resume formatting

Keep responses:
- Professional
- Short
- Helpful
- Modern
"""
                    },

                    {
                        "role": "user",
                        "content": user_message
                    }

                ],

                "temperature": 0.7

            }

        )

        result = response.json()

        print(result)

        if "choices" not in result:

            return jsonify({
                "reply": "❌ AI Server Error"
            }), 500

        reply = result["choices"][0]["message"]["content"]

        return jsonify({
            "reply": reply
        })

    except Exception as e:

        print(e)

        return jsonify({
            "reply": f"AI Server Error: {str(e)}"
        }), 500

# ---------------- RESUME UPLOAD ----------------
@app.route("/upload-resume", methods=["POST"])
def upload_resume():

    try:

        file = request.files.get("resume")

        if not file:
            return jsonify({
                "error": "No file uploaded"
            }), 400

        text = ""

        # PDF TEXT EXTRACTION
        if file.filename.endswith(".pdf"):

            with pdfplumber.open(file) as pdf:

                for page in pdf.pages:

                    page_text = page.extract_text()

                    if page_text:
                        text += page_text

        text_lower = text.lower()

        # ---------------- SKILLS ----------------

        check_skills = [

            "python",
            "react",
            "javascript",
            "sql",
            "machine learning",
            "html",
            "css",
            "flask",
            "firebase",
            "node",
            "mongodb",
            "tailwind",
            "java",
            "c++"

        ]

        skills = []
        missing = []

        for skill in check_skills:

            if skill in text_lower:
                skills.append(skill)

            else:
                missing.append(skill)

        # ---------------- ATS SCORE ----------------

        score = int((len(skills) / len(check_skills)) * 100)

        # ---------------- JOBS ----------------

        jobs = []

        if "python" in skills:

            jobs.append({

                "role": "Python Developer",
                "match": 92,
                "skills": ["Python", "Flask"]

            })

        if "react" in skills:

            jobs.append({

                "role": "Frontend Developer",
                "match": 88,
                "skills": ["React", "JavaScript"]

            })

        if "machine learning" in skills:

            jobs.append({

                "role": "AI Engineer",
                "match": 96,
                "skills": ["Machine Learning", "Python"]

            })

        if "firebase" in skills:

            jobs.append({

                "role": "Firebase Developer",
                "match": 85,
                "skills": ["Firebase", "React"]

            })

        if len(jobs) == 0:

            jobs.append({

                "role": "Software Developer",
                "match": 70,
                "skills": ["Programming"]

            })

        # ---------------- SUGGESTIONS ----------------

        suggestions = []

        if score < 50:

            suggestions.append("Add more technical skills")
            suggestions.append("Add more real-world projects")
            suggestions.append("Improve ATS keywords")
            suggestions.append("Add certifications")

        if "github" not in text_lower:
            suggestions.append("Add GitHub profile")

        if "linkedin" not in text_lower:
            suggestions.append("Add LinkedIn profile")

        if "project" not in text_lower:
            suggestions.append("Add project section")

        if len(suggestions) == 0:

            suggestions.append("Excellent ATS Resume")
            suggestions.append("Resume looks professional")

        # ---------------- FINAL RESPONSE ----------------

        return jsonify({

            "resume_text": text[:2000],

            "ats_score": score,

            "skills": skills,

            "missing_skills": missing,

            "recommended_jobs": jobs,

            "suggestions": suggestions

        })

    except Exception as e:

        print(e)

        return jsonify({
            "error": str(e)
        }), 500

# ---------------- AI RESUME REWRITE ----------------
@app.route("/rewrite", methods=["POST"])
def rewrite_resume():

    try:

        data = request.get_json()

        content = data.get("content", "")
        rewrite_type = data.get("type", "")

        prompt = f"""
You are a professional ATS resume expert.

Rewrite this {rewrite_type} professionally.

Content:
{content}

Requirements:
- ATS optimized
- Professional
- Strong action words
- Modern resume style
- Better readability
"""

        response = requests.post(

            url="https://openrouter.ai/api/v1/chat/completions",

            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:5173",
                "X-Title": "AI Resume Analyzer"
            },

            json={

                "model": AI_MODEL,

                "messages": [

                    {
                        "role": "system",
                        "content": """
You are a professional resume rewriting assistant.
Rewrite resumes professionally with ATS optimization.
"""
                    },

                    {
                        "role": "user",
                        "content": prompt
                    }

                ],

                "temperature": 0.7

            }

        )

        result = response.json()

        print(result)

        if "choices" not in result:

            return jsonify({
                "error": "AI Rewrite Failed"
            }), 500

        answer = result["choices"][0]["message"]["content"]

        return jsonify({
            "result": answer
        })

    except Exception as e:

        print(e)

        return jsonify({
            "error": str(e)
        }), 500

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(debug=True)