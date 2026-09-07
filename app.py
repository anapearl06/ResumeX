import os
import json
import re
import tempfile
from flask import Flask, render_template, request, jsonify, session
from resume_parser import read_resume, parse_resume
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max

RESUME_KEYWORDS = [
    "experience", "education", "skills", "resume", "curriculum",
    "objective", "summary", "employment", "qualification", "certification",
    "project", "training", "references", "contact", "address", "phone",
    "email", "linkedin", "github", "portfolio", "objective", "career",
    "work history", "professional", "intern", "bachelor", "master",
    "degree", "university", "college", "gpa", "cgpa"
]


def is_likely_resume(text):
    text_lower = text.lower()
    matches = sum(1 for kw in RESUME_KEYWORDS if kw in text_lower)
    return matches >= 3

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "qwen/qwen3.8-27b"

# ── In-memory storage (replaces cookie-based session for large data) ──
_store = {}


def _sid():
    if "_id" not in session:
        import uuid
        session["_id"] = str(uuid.uuid4())[:8]
    return session["_id"]


def _get(key):
    s = _sid()
    return _store.get(s, {}).get(key)


def _set(key, val):
    s = _sid()
    if s not in _store:
        _store[s] = {}
    _store[s][key] = val


def _get_dict(key):
    val = _get(key)
    return val if val else {}


def _get_list(key):
    val = _get(key)
    return val if isinstance(val, list) else []


def llm_json(system_prompt, user_content, max_tokens=None):
    import re
    kwargs = {"model": MODEL, "temperature": 0,
              "messages": [
                  {"role": "system", "content": system_prompt},
                  {"role": "user", "content": user_content},
              ]}
    if max_tokens:
        kwargs["max_tokens"] = max_tokens
    completion = client.chat.completions.create(**kwargs)
    raw = completion.choices[0].message.content.strip()

    # Remove markdown code fences
    raw = re.sub(r'```(?:json)?', '', raw).strip()

    # Try to find the outermost JSON object/array if surrounded by extra text
    def extract_json(text):
        # try whole thing first
        candidates = []
        # find first '{' or '[' and match braces
        start = None
        for i, ch in enumerate(text):
            if ch in '{[':
                start = i
                break
        if start is None:
            return None
        depth = 0
        for j in range(start, len(text)):
            ch = text[j]
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    candidates.append(text[start:j+1])
                    break
            elif ch == '[':
                depth += 1
            elif ch == ']':
                depth -= 1
                if depth == 0:
                    candidates.append(text[start:j+1])
                    break
        for cand in candidates:
            cand = re.sub(r',\s*([}\]])', r'\1', cand)
            try:
                return json.loads(cand)
            except Exception:
                continue
        return None

    parsed = extract_json(raw)
    if parsed is not None:
        return parsed

    # Final fallback: clean extra newlines
    cleaned = raw.replace('\n', ' ')
    cleaned = re.sub(r',\s*([}\]])', r'\1', cleaned)
    return json.loads(cleaned)


@app.errorhandler(413)
def too_large(e):
    return jsonify({"error": "File is too large. Maximum upload size is 5MB."}), 413


# ── Landing ──────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


# ── Candidate Routes ─────────────────────────────────────────────────
@app.route("/candidate")
def candidate_dashboard():
    return render_template("candidate/dashboard.html")


@app.route("/candidate/upload")
def candidate_upload():
    return render_template("candidate/upload.html")


@app.route("/candidate/analysis")
def candidate_analysis():
    return render_template("candidate/analysis.html")


@app.route("/candidate/jobs")
def candidate_jobs():
    return render_template("candidate/jobs.html")


@app.route("/candidate/skills")
def candidate_skills():
    return render_template("candidate/skills.html")


@app.route("/candidate/interview")
def candidate_interview():
    return render_template("candidate/interview.html")


@app.route("/candidate/jd-matcher")
def candidate_jd_matcher():
    return render_template("candidate/jd_matcher.html")


# ── HR Routes ────────────────────────────────────────────────────────
@app.route("/hr")
def hr_dashboard():
    return render_template("hr/dashboard.html")


@app.route("/hr/jobs")
def hr_jobs():
    return render_template("hr/jobs.html")


@app.route("/hr/jobs/create")
def hr_job_create():
    return render_template("hr/job_create.html")


@app.route("/hr/candidates")
def hr_candidates():
    return render_template("hr/candidates.html")


@app.route("/hr/candidate/<int:cid>")
def hr_candidate_detail(cid):
    return render_template("hr/candidate_detail.html", cid=cid)


@app.route("/hr/compare")
def hr_compare():
    return render_template("hr/compare.html")


@app.route("/hr/shortlist")
def hr_shortlist():
    return render_template("hr/shortlist.html")


# ══════════════════════════════════════════════════════════════════════
# API ENDPOINTS
# ══════════════════════════════════════════════════════════════════════

# ── Upload & Parse Resume ────────────────────────────────────────────
@app.route("/api/upload", methods=["POST"])
def api_upload():
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["resume"]
    if not file.filename:
        return jsonify({"error": "No file selected"}), 400
    ext = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in ("pdf", "docx"):
        return jsonify({"error": "Only PDF and DOCX files are supported"}), 400
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name
        resume_text = read_resume(tmp_path)
        if not is_likely_resume(resume_text):
            return jsonify({"error": "This file doesn't appear to be a resume. Please upload a valid resume (PDF or DOCX)."}), 400
        parsed = parse_resume(resume_text)
        _set("resume", parsed.model_dump())
        _set("resume_text", resume_text)
        return jsonify(parsed.model_dump())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)


# ── Get Stored Resume ───────────────────────────────────────────────
@app.route("/api/resume", methods=["GET"])
def api_get_resume():
    resume = _get("resume")
    if not resume:
        return jsonify({"error": "No resume uploaded yet"}), 404
    return jsonify(resume)


# ── AI Job Matcher ───────────────────────────────────────────────────
@app.route("/api/job-match", methods=["POST"])
def api_job_match():
    resume = _get("resume")
    if not resume:
        return jsonify({"error": "No resume uploaded yet"}), 400
    system = """You are an expert career advisor. Based on the candidate's resume,
recommend the top 6 most suitable job roles.
For each role provide these exact fields:
- "title": job title (keep it short, no more than 4 words)
- "match": a number between 0 and 100
- "reason": a 1-2 sentence explanation
- "required_skills": array of skill strings
- "matching_skills": array of skill strings the candidate already has
- "missing_skills": array of skill strings the candidate needs to learn

CRITICAL RULES:
- Return ONLY valid JSON array
- Do NOT use trailing commas
- Keep titles short (e.g. "Frontend Developer", not "Frontend Developer specializing in React and Vue")
- Every string must be properly quoted
- Double check the JSON is valid before returning"""
    user = f"Resume data:\n{json.dumps(resume, indent=2)}"
    try:
        data = llm_json(system, user, max_tokens=900)
        _set("job_matches", data)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Skill Gap Analysis ──────────────────────────────────────────────
@app.route("/api/skill-gap", methods=["POST"])
def api_skill_gap():
    resume = _get("resume")
    if not resume:
        return jsonify({"error": "No resume uploaded yet"}), 400
    body = request.get_json() or {}
    job_title = body.get("job_title", "Software Engineer")
    system = f"""You are a career skill gap analyst. For the job role "{job_title}",
compare required skills with the candidate's resume.
Return ONLY valid JSON:
{{
  "job_title": "{job_title}",
  "overall_match": 85,
  "have": [{{"skill": "React", "level": "Advanced"}}],
  "missing": [{{"skill": "TypeScript", "importance": "High", "learn_time": "2-4 weeks"}}],
  "recommendations": ["Learn TypeScript", "Practice testing frameworks"]
}}"""
    user = f"Resume:\n{json.dumps(resume, indent=2)}"
    try:
        data = llm_json(system, user, max_tokens=600)
        _set("skill_gap", data)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Interview Prep ──────────────────────────────────────────────────
@app.route("/api/interview-prep", methods=["POST"])
def api_interview_prep():
    resume = _get("resume")
    if not resume:
        return jsonify({"error": "No resume uploaded yet"}), 400
    body = request.get_json() or {}
    job_title = body.get("job_title", "Software Engineer") or "Software Engineer"
    user_resume = json.dumps(resume, indent=2)

    def gen_batch(category):
        schema = {
            "technical": '{"technical":[{"question":"...","topic":"...","difficulty":"Easy/Medium/Hard","tips":"...","suggested_answer":"..."}]}',
            "resume_based": '{"resume_based":[{"question":"...","context":"...","tips":"...","suggested_answer":"..."}]}',
            "project_based": '{"project_based":[{"question":"...","project":"...","tips":"...","suggested_answer":"..."}]}',
            "hr_behavioral": '{"hr_behavioral":[{"question":"...","category":"...","tips":"...","suggested_answer":"..."}]}',
        }
        system = f"""You are an expert interview coach. Based on the candidate's resume
and target role "{job_title}", generate {5 if category == 'technical' else 4} interview questions
for the category "{category}".
Return ONLY valid JSON matching this exact shape:
{schema[category]}

STRICT RULES:
- All fields must be SHORT: 1-2 sentences max each.
- suggested_answer: write a ONE-LINE hint (10-15 words only). Example: "Mention DOM diffing, reconciliation, and how React batches state updates."
- No long explanations.
- No extra text, no trailing commas."""
        try:
            part = llm_json(system, user_resume, max_tokens=700)
            return part.get(category, [])
        except Exception:
            return []

    data = {
        "technical": gen_batch("technical"),
        "resume_based": gen_batch("resume_based"),
        "project_based": gen_batch("project_based"),
        "hr_behavioral": gen_batch("hr_behavioral"),
    }
    _set("interview_prep", data)
    return jsonify(data)


# ── JD Matcher ──────────────────────────────────────────────────────
@app.route("/api/jd-match", methods=["POST"])
def api_jd_match():
    resume = _get("resume")
    if not resume:
        return jsonify({"error": "No resume uploaded yet"}), 400
    body = request.get_json() or {}
    jd = body.get("job_description", "")
    if not jd:
        return jsonify({"error": "Job description is required"}), 400
    system = """You are an expert recruiter. Compare the candidate's resume
with the job description. Return ONLY valid JSON:
{
  "match_percentage": 78,
  "verdict": "green",
  "verdict_label": "Ready to Apply",
  "verdict_reason": "...",
  "matching_skills": ["React", "JavaScript"],
  "missing_skills": ["TypeScript", "AWS"],
  "missing_keywords": ["CI/CD", "microservices"],
  "experience_match": "Strong",
  "strengths": ["Strong frontend skills"],
  "weaknesses": ["No cloud experience"],
  "recommendations": ["Learn AWS basics"]
}"""
    user = f"Resume:\n{json.dumps(resume, indent=2)}\n\nJob Description:\n{jd}"
    try:
        data = llm_json(system, user, max_tokens=700)
        _set("jd_match", data)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── HR: Create Job ──────────────────────────────────────────────────
@app.route("/api/hr/job", methods=["POST"])
def api_hr_create_job():
    body = request.get_json()
    if not body:
        return jsonify({"error": "No data provided"}), 400
    jobs = _get_list("hr_jobs")
    job = {
        "id": len(jobs) + 1,
        "title": body.get("title", ""),
        "company": body.get("company", ""),
        "description": body.get("description", ""),
        "required_skills": body.get("required_skills", []),
        "preferred_skills": body.get("preferred_skills", []),
        "experience_required": body.get("experience_required", 0),
        "education": body.get("education", ""),
    }
    jobs.append(job)
    _set("hr_jobs", jobs)
    return jsonify(job)


@app.route("/api/hr/jobs", methods=["GET"])
def api_hr_list_jobs():
    return jsonify(_get_list("hr_jobs"))


# ── HR: Upload Candidate Resumes ────────────────────────────────────
@app.route("/api/hr/upload-candidate", methods=["POST"])
def api_hr_upload_candidate():
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["resume"]
    if not file.filename:
        return jsonify({"error": "No file selected"}), 400
    ext = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in ("pdf", "docx"):
        return jsonify({"error": "Only PDF and DOCX files are supported"}), 400
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name
        resume_text = read_resume(tmp_path)
        if not is_likely_resume(resume_text):
            return jsonify({"error": "This file doesn't appear to be a resume. Please upload a valid resume (PDF or DOCX)."}), 400
        parsed = parse_resume(resume_text)
        candidates = _get_list("hr_candidates")
        candidate = parsed.model_dump()
        candidate["id"] = len(candidates) + 1
        candidate["filename"] = file.filename
        candidates.append(candidate)
        _set("hr_candidates", candidates)
        return jsonify(candidate)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)


@app.route("/api/hr/candidates", methods=["GET"])
def api_hr_list_candidates():
    return jsonify(_get_list("hr_candidates"))


# ── HR: Match Candidates to Job ─────────────────────────────────────
@app.route("/api/hr/match", methods=["POST"])
def api_hr_match():
    body = request.get_json() or {}
    job_id = body.get("job_id")
    jobs = _get_list("hr_jobs")
    candidates = _get_list("hr_candidates")
    if not jobs:
        return jsonify({"error": "No jobs created yet"}), 400
    if not candidates:
        return jsonify({"error": "No candidates uploaded yet"}), 400
    job = None
    for j in jobs:
        if j["id"] == job_id:
            job = j
            break
    if not job:
        return jsonify({"error": "Job not found"}), 404
    system = """You are an expert AI recruiter. Rank candidates for a job role.
For each candidate provide:
- id: candidate id
- name: candidate name
- match: match percentage (0-100)
- category: "strong" or "potential" or "weak"
- reason: 1-2 sentence explanation
- matching_skills: skills that match
- missing_skills: skills that are missing
Return ONLY valid JSON as an array sorted by match score descending."""
    user = f"Job:\n{json.dumps(job, indent=2)}\n\nCandidates:\n{json.dumps(candidates, indent=2)}"
    try:
        data = llm_json(system, user, max_tokens=900)
        _set("hr_matches", data)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── HR: Candidate Detail ────────────────────────────────────────────
@app.route("/api/hr/candidate/<int:cid>", methods=["GET"])
def api_hr_candidate_detail(cid):
    candidates = _get_list("hr_candidates")
    for c in candidates:
        if c.get("id") == cid:
            return jsonify(c)
    return jsonify({"error": "Candidate not found"}), 404


# ── HR: Compare Candidates ──────────────────────────────────────────
@app.route("/api/hr/compare", methods=["POST"])
def api_hr_compare():
    body = request.get_json() or {}
    ids = body.get("candidate_ids", [])
    candidates = _get_list("hr_candidates")
    selected = [c for c in candidates if c.get("id") in ids]
    if len(selected) < 2:
        return jsonify({"error": "Select at least 2 candidates"}), 400
    system = """Compare these candidates side by side. Return ONLY valid JSON:
{
  "comparison": [
    {
      "candidate_id": 1,
      "name": "...",
      "strengths": ["..."],
      "weaknesses": ["..."],
      "best_for": "...",
      "score": 85
    }
  ],
  "recommendation": "Based on the comparison, Candidate X is recommended because..."
}"""
    user = f"Candidates:\n{json.dumps(selected, indent=2)}"
    try:
        data = llm_json(system, user, max_tokens=700)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
