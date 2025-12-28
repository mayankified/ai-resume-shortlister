from utils.gemini_utils import generate_response
import json
import re


def extract_json(text: str) -> dict:
    """
    Safely extract first JSON object from text
    """
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON found")
    return json.loads(match.group())


def score_resume(job_text: str, resume_text: str) -> dict:
    prompt = f"""
You are a professional ATS (Applicant Tracking System).

SCORING RULES:
- Skills match: 60%
- Experience relevance: 25%
- Nice-to-have skills: 15%
- Penalize missing core skills heavily

OUTPUT RULES:
- Return ONLY valid JSON
- No markdown
- No explanation text

JSON FORMAT:
{{
  "score": 0,
  "matched_skills": [],
  "missing_skills": [],
  "confidence": "low | medium | high",
  "summary": "",
  "reason": ""
}}

JOB REQUIREMENTS:
{job_text}

RESUME:
{resume_text}
"""

    response = generate_response(prompt)

    try:
        cleaned = re.sub(r"```json|```", "", response).strip()
        return extract_json(cleaned)

    except Exception:
        return {
            "score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "confidence": "low",
            "summary": "Unable to reliably evaluate resume",
            "reason": "AI response parsing failed",
        }
