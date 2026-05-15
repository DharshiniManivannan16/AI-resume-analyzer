import os
import google.generativeai as genai

# 🔑 API KEY (you will replace this later from .env)
genai.configure(api_key="YOUR_GEMINI_API_KEY")

model = genai.GenerativeModel("gemini-1.5-flash")


# ---------------- AI RESUME IMPROVER ----------------

def improve_resume(text):
    prompt = f"""
    You are an expert ATS resume optimizer.

    Improve this resume content into a professional ATS-friendly version:

    {text}
    """

    response = model.generate_content(prompt)
    return response.text


# ---------------- SKILL GAP ANALYSIS ----------------

def skill_gap_analysis(text, job_role):
    prompt = f"""
    Analyze this resume and compare with role: {job_role}

    Resume:
    {text}

    Return:
    - Missing skills
    - Improvement suggestions
    - Learning roadmap
    """

    response = model.generate_content(prompt)
    return response.text


# ---------------- CHATBOT ----------------

def career_chatbot(question):
    prompt = f"""
    You are a career assistant AI.

    User question: {question}
    """

    response = model.generate_content(prompt)
    return response.text