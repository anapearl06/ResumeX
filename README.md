# 🚀 ResumeX

### AI-Powered Career Intelligence & Recruitment Platform

ResumeX is an AI-powered career intelligence and recruitment platform designed to help **job seekers understand their career potential** and help **HR professionals identify the right candidates efficiently**.

The platform combines intelligent resume parsing, AI-powered job recommendations, skill gap analysis, interview preparation, job description matching, and candidate comparison into a unified experience.

Built as a full-stack MVP using **Python, Flask, Vanilla JavaScript, and Groq LLM**, ResumeX demonstrates how Large Language Models can transform traditional recruitment workflows into intelligent, personalized experiences.

---

## ✨ What is ResumeX?

ResumeX is a dual-portal career and recruitment platform built for two primary users:

👤 **Candidates** — People looking to understand their resume, discover suitable job roles, identify missing skills, prepare for interviews, and evaluate their fit for job descriptions.

🏢 **HR & Recruiters** — Professionals who want to create job openings, manage candidate profiles, intelligently rank candidates, and compare applicants.

Instead of treating a resume as just a document, ResumeX transforms it into **structured career intelligence** using AI.

---

# 🎯 The Problem ResumeX Solves

The traditional recruitment process has several challenges.

### For Candidates

Job seekers often struggle with questions such as:

- Which job roles are actually suitable for my skills?
- What skills am I missing for my target role?
- How well does my resume match a job description?
- What interview questions should I prepare for?
- How can I understand the strengths and weaknesses of my profile?

Most candidates have access to their resume but lack **actionable career insights**.

---

### For Recruiters

Recruiters face a different set of problems:

- Reviewing large numbers of resumes manually takes time.
- Comparing candidates can be inconsistent.
- Identifying the best candidate for a job can be difficult.
- Candidate ranking often requires repetitive manual evaluation.

ResumeX aims to reduce this friction by using AI to analyze candidate information and provide structured insights.

---

# 💡 Why ResumeX Was Built

ResumeX was built to explore how **Generative AI and Large Language Models can improve career intelligence and recruitment workflows**.

The core idea behind the project is simple:

> A resume contains valuable information, but raw text alone does not provide meaningful career insights.

ResumeX converts resume data into structured information and uses AI to answer questions such as:

- What job roles are suitable for this candidate?
- What skills are missing for a specific role?
- How well does the candidate match a job description?
- What interview questions should the candidate prepare for?
- Which candidate is the strongest match for a particular job?

The goal is not just to parse resumes, but to build an **intelligent layer on top of resume data**.

---

# 🌟 Key Features

## 👤 Candidate Portal

The Candidate Portal provides AI-powered tools to help users understand and improve their career profile.

### 📤 Resume Upload

Candidates can upload their resumes in supported formats:

- PDF
- DOCX

The system extracts the resume text and validates whether the uploaded document is likely to be a resume before sending it to the AI model.

---

### 📊 Resume Analysis

The uploaded resume is processed and transformed into structured information.

The system extracts and analyzes information such as:

- Personal information
- Education
- Skills
- Work experience
- Projects
- Certifications
- Career summary

The structured data is validated before being used throughout the platform.

---

### 🎯 AI Job Matching

ResumeX analyzes the candidate's skills and experience to recommend suitable job roles.

The AI generates job recommendations based on:

- Skills
- Experience
- Education
- Projects
- Overall profile

The platform recommends multiple potential career paths instead of limiting the candidate to a single role.

---

### 📈 Skill Gap Analysis

Candidates can select a target role and analyze the difference between their current profile and the requirements of that role.

The system identifies:

- Existing strengths
- Relevant skills
- Missing skills
- Recommended skills to learn
- Areas for improvement

This helps users create a more focused learning roadmap.

---

### 🎤 AI Interview Preparation

ResumeX generates personalized interview preparation questions based on the candidate's profile.

Questions are generated across multiple categories:

- Technical questions
- Resume-based questions
- Project-based questions
- HR questions

This creates a more personalized interview preparation experience compared to generic question lists.

---

### 📄 Job Description Matcher

Candidates can paste a job description and compare it with their resume.

The system evaluates:

- Skill alignment
- Experience relevance
- Missing requirements
- Overall compatibility

This helps candidates understand how well their profile matches a particular job opportunity.

---

# 🏢 HR & Recruiter Portal

The HR portal focuses on helping recruiters manage jobs and evaluate candidates more efficiently.

---

### 💼 Job Creation

Recruiters can create and manage job openings.

Each job can include relevant details and requirements that can later be used for candidate matching.

---

### 👥 Candidate Pool

Recruiters can upload and manage multiple candidate resumes.

The system builds a candidate pool that can be used for:

- Candidate evaluation
- Job matching
- Ranking
- Comparison

---

### 🤖 AI Candidate Matching

ResumeX can analyze candidates against job requirements and rank them based on their compatibility.

The ranking process considers factors such as:

- Skills
- Experience
- Resume information
- Job requirements

This provides recruiters with an AI-assisted starting point for candidate evaluation.

---

### 🔍 Candidate Details

Recruiters can view detailed information about individual candidates.

The system provides structured insights from the uploaded resume, making candidate information easier to review.

---

### ⚖️ Candidate Comparison

Recruiters can compare candidates side-by-side.

This allows HR professionals to evaluate multiple candidates based on relevant factors and make more informed decisions.

---

# 🧠 AI Intelligence Engine

The intelligence layer of ResumeX is powered by the **Groq API and Qwen language model**.

The AI is responsible for generating structured insights for multiple features, including:

- Resume parsing
- Job recommendations
- Skill gap analysis
- Interview preparation
- Job description matching
- Candidate ranking
- Candidate comparison

However, working with LLM-generated output introduces an important challenge:

> Large Language Models do not always return perfectly formatted JSON.

To solve this problem, ResumeX implements a structured JSON extraction system.

---

## 🔧 `llm_json()` — Structured LLM Output Handling

One of the core architectural components of ResumeX is the `llm_json()` pattern.

The system:

1. Sends a structured system prompt to the LLM.
2. Instructs the model to return JSON.
3. Removes Markdown code fences if present.
4. Uses brace-matching logic to locate valid JSON.
5. Extracts the structured JSON object.
6. Returns the parsed result to the application.

This makes the application more resilient to common LLM formatting problems.

### Why is this important?

Without structured output handling, an LLM response such as:

```text
Here is the analysis:

```json
{
  "skills": ["Python", "Flask"]
}
```
```

could break a normal JSON parser.

ResumeX handles these situations before passing the response into the application.

---

# 📄 Resume Processing Pipeline

The resume upload process follows the pipeline below:

```text
Candidate Uploads Resume
        │
        ▼
PDF / DOCX Validation
        │
        ▼
File Size Validation
        │
        ▼
Extract Resume Text
        │
        ▼
Resume Keyword Validation
        │
        ▼
Send Resume Data to AI
        │
        ▼
Structured JSON Response
        │
        ▼
Pydantic Validation
        │
        ▼
Store Structured Resume Data
        │
        ▼
Candidate Dashboard
```

---

## 📥 Supported Resume Formats

ResumeX currently supports:

- `.pdf`
- `.docx`

---

## 📑 PDF Parsing

PDF files are processed using:

**PyMuPDF (`fitz`)**

The library extracts readable text from uploaded PDF resumes.

---

## 📄 DOCX Parsing

DOCX files are processed using:

**python-docx**

The application reads text content from Microsoft Word documents and prepares it for analysis.

---

## 🛡️ Resume Validation

Before sending the extracted text to the AI model, ResumeX checks whether the uploaded document is likely to be a resume.

The application searches for common resume-related indicators.

This helps prevent unnecessary AI API calls for invalid uploads.

### Benefits:

- Reduces unnecessary API usage
- Saves LLM tokens
- Improves user experience
- Prevents invalid documents from entering the AI pipeline

---

# 🔄 End-to-End Data Flow

The complete candidate workflow looks like this:

```text
User
 │
 │ Upload Resume
 ▼
Resume Parser
 │
 ├── PDF → PyMuPDF
 │
 └── DOCX → python-docx
 │
 ▼
Resume Validation
 │
 ▼
Groq LLM
 │
 ▼
Structured JSON
 │
 ▼
Pydantic Validation
 │
 ▼
Session Storage
 │
 ▼
Candidate Dashboard
 │
 ├── Job Matching
 ├── Skill Gap Analysis
 ├── Interview Preparation
 └── JD Matching
```

The same structured resume data is reused across multiple AI features.

This avoids repeatedly parsing the same resume and helps reduce unnecessary API usage.

---

# 🏗️ Application Architecture

ResumeX follows a simple full-stack architecture.

```text
                    ┌───────────────────────┐
                    │       ResumeX UI      │
                    │ HTML / CSS / JS       │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │     Flask Backend     │
                    │       app.py          │
                    └───────────┬───────────┘
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
        Resume Parser       AI Engine       HR Services
        PDF / DOCX          Groq LLM       Jobs/Candidates
                │               │
                ▼               ▼
           PyMuPDF          Structured
           python-docx         JSON
                                │
                                ▼
                           Pydantic
                           Validation
                                │
                                ▼
                          Session Store
```

---

# 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.14 |
| Web Framework | Flask 3.1 |
| AI Engine | Groq API |
| Language Model | Qwen 3 27B |
| PDF Parsing | PyMuPDF (`fitz`) |
| DOCX Parsing | python-docx |
| Data Validation | Pydantic v2 |
| Frontend | HTML5 |
| Templating | Jinja2 |
| Styling | Custom CSS |
| Client-Side Logic | Vanilla JavaScript |
| Data Storage | In-Memory Python Dictionary |

---

# 🎨 Frontend & Design System

The ResumeX frontend is built using:

- Jinja2 Templates
- Vanilla JavaScript
- Custom CSS

The design system takes inspiration from modern SaaS products and interfaces such as:

- Vercel
- Linear

---

## 🎨 Design Characteristics

The UI focuses on:

- Clean layouts
- Minimal visual noise
- Soft backgrounds
- White information cards
- Hairline borders
- Subtle gradients
- Responsive navigation
- Clear typography

---

## 🎨 Color Palette

```text
Background     → #F9F8F6
Primary Accent → #4F46E5
Cards          → #FFFFFF
```

The design prioritizes readability and a professional SaaS-style appearance.

---

# 📂 Project Structure

```text
ResumeX/
│
├── app.py
│   └── Main Flask application
│
├── resume_parser.py
│   └── Resume extraction and AI parsing logic
│
├── templates/
│   │
│   ├── index.html
│   │
│   ├── candidate/
│   │   ├── sidebar.html
│   │   ├── dashboard.html
│   │   ├── upload.html
│   │   ├── analysis.html
│   │   ├── jobs.html
│   │   ├── skills.html
│   │   ├── interview.html
│   │   └── jd_matcher.html
│   │
│   └── hr/
│       ├── sidebar.html
│       ├── dashboard.html
│       ├── jobs.html
│       ├── job_create.html
│       ├── candidates.html
│       ├── candidate_detail.html
│       ├── compare.html
│       └── shortlist.html
│
├── static/
│   │
│   ├── css/
│   │   └── main.css
│   │
│   ├── js/
│   │   └── main.js
│   │
│   └── logo.png
│
├── resumes/
│   └── Sample resumes for testing
│
├── pyproject.toml
│
├── uv.lock
│
└── .gitignore
```

---

# 🔌 API Overview

ResumeX provides multiple API endpoints for candidate and recruiter workflows.

---

## 👤 Candidate APIs

### Upload Resume

```http
POST /api/upload
```

Uploads a resume and processes it through the parsing pipeline.

---

### Get Resume

```http
GET /api/resume
```

Returns the structured resume information stored for the current session.

---

### AI Job Matching

```http
POST /api/job-match
```

Analyzes the candidate profile and recommends suitable job roles.

---

### Skill Gap Analysis

```http
POST /api/skill-gap
```

Compares the candidate's skills against a selected target role.

---

### Interview Preparation

```http
POST /api/interview-prep
```

Generates personalized interview questions.

Question categories include:

- Technical
- Resume-based
- Project-based
- HR

---

### Job Description Matcher

```http
POST /api/jd-matcher
```

Matches the candidate's resume against a pasted job description.

---

# 🏢 HR APIs

### Create Job

```http
POST /api/hr/job
```

---

### Get Jobs

```http
GET /api/hr/jobs
```

---

### Upload Candidate

```http
POST /api/hr/upload-candidate
```

---

### Get Candidates

```http
GET /api/hr/candidates
```

---

### Match Candidates

```http
POST /api/hr/match
```

Ranks candidates against a selected job.

---

### Candidate Details

```http
GET /api/hr/candidate/<id>
```

---

### Compare Candidates

```http
POST /api/hr/compare
```

Provides a side-by-side comparison of candidates.

---

# 🧩 Key Engineering Decisions

## 1️⃣ Structured AI Output

Instead of directly trusting LLM responses, ResumeX extracts and processes structured JSON responses.

This improves reliability when working with generative AI.

---

## 2️⃣ Validation Before AI Processing

Resume files are checked before sending them to the AI model.

This helps reduce:

- Invalid uploads
- Unnecessary API requests
- Token usage

---

## 3️⃣ Resume Reuse

The resume is parsed once and reused across multiple features.

Instead of repeatedly sending the entire resume to the AI model, ResumeX stores the structured result and uses it throughout the candidate workflow.

---

## 4️⃣ Pydantic Validation

AI-generated resume information is validated using Pydantic models.

This adds an additional validation layer between:

```text
LLM Output → Application Data
```

---

## 5️⃣ Lightweight Architecture

The project intentionally uses:

- Flask
- Vanilla JavaScript
- Jinja2 templates

This keeps the application lightweight and easy to understand.

---

# ⚡ Application Features Summary

| Feature | Candidate | HR |
|---|:---:|:---:|
| Resume Upload | ✅ | ✅ |
| Resume Parsing | ✅ | ✅ |
| AI Job Matching | ✅ | ❌ |
| Skill Gap Analysis | ✅ | ❌ |
| Interview Preparation | ✅ | ❌ |
| JD Matching | ✅ | ❌ |
| Job Management | ❌ | ✅ |
| Candidate Pool | ❌ | ✅ |
| Candidate Ranking | ❌ | ✅ |
| Candidate Comparison | ❌ | ✅ |

---

# ⚙️ Installation & Setup

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/anapearl06/ResumeX.git
```

Navigate into the project:

```bash
cd ResumeX
```

---

## 2️⃣ Install Dependencies

This project uses Python and the `uv` package manager.

Install dependencies using:

```bash
uv sync
```

Alternatively, install the required dependencies using pip if needed.

---

## 3️⃣ Configure Environment Variables

Create a `.env` file in the project root.

```text
ResumeX/
│
├── .env
├── app.py
└── ...
```

Add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

⚠️ Never commit your `.env` file or API keys to GitHub.

---

# ▶️ Running ResumeX Locally

After installing dependencies and configuring environment variables:

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

---

# 🔐 Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | API key used to access Groq's LLM API |

---

# ⚠️ Current MVP Architecture

ResumeX is currently designed as an **AI-powered MVP and portfolio project**.

The application currently uses an in-memory data store.

```python
_store = {}
```

This means:

- Data exists only while the server is running.
- Restarting the server clears stored data.
- The application is not currently designed for persistent multi-user data.

This approach keeps the MVP architecture simple and allows rapid development.

---

# 🚧 Production Considerations

To evolve ResumeX into a production-ready application, the following improvements would be recommended.

---

## 🗄️ Persistent Database

Replace in-memory storage with a persistent database.

Possible options:

- PostgreSQL
- SQLite
- MongoDB
- Redis

---

## 🔐 Authentication & Authorization

Future versions could include:

- Candidate accounts
- Recruiter accounts
- Secure authentication
- Role-based access
- Protected recruiter portal

---

## ⚡ Rate Limiting

Since AI features depend on a shared API key, rate limiting could help:

- Prevent abuse
- Control API usage
- Protect API quotas

---

## 🔄 Centralized AI Service

Currently, LLM-related parsing logic exists in more than one location.

A future improvement would be:

```text
AI Service Layer
       │
       ├── Resume Parsing
       ├── Job Matching
       ├── Skill Analysis
       ├── Interview Generation
       └── Candidate Ranking
```

This would improve maintainability as the application grows.

---

# 🗺️ Future Roadmap

### 🔹 Phase 1 — MVP

- [x] Resume Upload
- [x] PDF Parsing
- [x] DOCX Parsing
- [x] AI Resume Analysis
- [x] Job Matching
- [x] Skill Gap Analysis
- [x] Interview Preparation
- [x] Job Description Matching
- [x] HR Candidate Management
- [x] Candidate Comparison

---

### 🔹 Phase 2 — Persistence

- [ ] Database integration
- [ ] Persistent user data
- [ ] Persistent job listings
- [ ] Candidate history

---

### 🔹 Phase 3 — Authentication

- [ ] Candidate authentication
- [ ] Recruiter authentication
- [ ] Role-based access
- [ ] Secure sessions

---

### 🔹 Phase 4 — Production Features

- [ ] Rate limiting
- [ ] AI usage monitoring
- [ ] API security improvements
- [ ] Error monitoring
- [ ] Production logging

---

### 🔹 Phase 5 — Advanced AI Features

- [ ] Resume scoring
- [ ] ATS compatibility analysis
- [ ] Personalized learning roadmap
- [ ] Career progression suggestions
- [ ] Job market insights
- [ ] Semantic candidate matching

---

# 🌍 Deployment

ResumeX is designed to be deployable as a Python web application.

For the current architecture, the application should be deployed with a platform capable of running a persistent Python web service.

Before production deployment, the following configuration should be reviewed:

- Production server configuration
- `debug=False`
- Host configuration
- Environment variables
- API key security
- Persistent storage requirements

---

# 🎓 What This Project Demonstrates

ResumeX demonstrates practical experience with:

- Full-stack web development
- Python backend development
- Flask applications
- REST API design
- Generative AI integration
- Large Language Models
- Prompt engineering
- Structured LLM output handling
- PDF parsing
- DOCX parsing
- Pydantic validation
- Frontend development
- Responsive web design
- AI-powered workflows

---

# 💭 Key Learning

One of the most important lessons from building ResumeX was understanding that:

> Integrating an LLM into an application is not only about sending a prompt and displaying the response.

A reliable AI application also requires:

- Input validation
- Output validation
- Structured data handling
- Error handling
- API usage control
- User experience considerations

ResumeX explores these challenges through a practical career and recruitment use case.

---

# 👩‍💻 Author

**Ananya Shukla**

Aspiring Full-Stack Developer & AI Engineer.

---

# ⭐ If You Like This Project

If you find ResumeX interesting, consider giving the repository a ⭐.

It helps support the project and motivates future development.

---

<div align="center">

### 🚀 ResumeX

**Turning Resumes into Career Intelligence.**

Built with ❤️ using Python, Flask, Groq AI, and Vanilla JavaScript.

</div>
