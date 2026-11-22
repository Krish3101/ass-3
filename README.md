# 📋 Job Description Simplifier

[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Model](https://img.shields.io/badge/LLM-OpenRouter%20Free%20Tier-blueviolet.svg)](https://openrouter.ai/)

> An intelligent GenAI application that parses messy, verbose, and unformatted job advertisements and extracts critical hiring criteria (skills, experience, compensation & responsibilities) into clean, standardized specifications. Missing fields are strictly audited and marked as `"not mentioned"`.

---

## 📌 Problem Overview
Job advertisements today are bloated with corporate jargon, boilerplate descriptions, and ambiguous qualification criteria. Job seekers waste hours parsing dense postings across multiple job boards to understand basic requirements. 

**Job Description Simplifier** automates this by passing raw job postings (from direct text, web URLs, or uploaded PDF/TXT files) through an instruction-tuned prompt to an OpenRouter LLM (defaulting to the dynamic zero-cost `openrouter/free` router or selected models like LLaMA 3.3 70B / Gemma 4 / Nemotron). The system extracts critical hiring criteria into a validated JSON schema and renders them into clear, actionable tables and dashboard metrics. If any criterion (such as salary or education) is omitted in the posting, it is strictly flagged as `"not mentioned"`.

---

## 🏗️ System Architecture

```
┌───────────────────────┐      ┌─────────────────────────┐      ┌──────────────────────────┐
│   User Input Options  │ ───► │  Prompt & Preprocessor  │ ───► │      OpenRouter API      │
│  - Paste raw JD       │      │  - Web URL HTML Scraper │      │  - openrouter/free       │
│  - Live Web URL fetch │      │  - PDF/TXT text parsing │      │  - Zero-shot JSON schema │
│  - Upload PDF/TXT     │      │  - Schema enforcement   │      │  - Temperature: 0.1      │
│  - 5 Built-in presets │      │                         │      │                          │
└───────────────────────┘      └─────────────────────────┘      └──────────────────────────┘
                                                                              │
                                                                              ▼
┌───────────────────────┐      ┌─────────────────────────┐      ┌──────────────────────────┐
│ Export & Downloads    │ ◄─── │ Streamlit Dashboard UI  │ ◄─── │ Post-Processing Engine   │
│  - Export to CSV      │      │  - Master Summary Table │      │  - json.loads validation │
│  - Export to JSON     │      │  - Interactive Badges   │      │  - Missing keys fallback │
│  - Export Markdown    │      │  - Role KPI Cards       │      │    to "not mentioned"    │
└───────────────────────┘      └─────────────────────────┘      └──────────────────────────┘
```

---

## 🔑 Strict JSON Schema
The model adheres to a deterministic output format:
```json
{
  "job_title": "<Job Title or 'not mentioned'>",
  "company_name": "<Company Name or 'not mentioned'>",
  "location": "<Location or 'not mentioned'>",
  "work_mode": "<Remote | Hybrid | On-site | not mentioned>",
  "experience_required": "<e.g., '3-5 years' or 'not mentioned'>",
  "salary_compensation": "<e.g., '₹28-38 LPA' or 'not mentioned'>",
  "required_technical_skills": ["Skill 1", "Skill 2"],
  "soft_skills": ["Skill 1", "Skill 2"],
  "core_responsibilities": ["Duty 1", "Duty 2"],
  "educational_qualifications": "<Degree or 'not mentioned'>",
  "benefits_and_perks": ["Perk 1", "Perk 2"],
  "summary": "<2-sentence role summary>"
}
```

---

## 🚀 Key Features
1. **Multi-source Ingestion**: Paste raw job post text directly, fetch automatically from live career Web URLs, or upload `.pdf` / `.txt` files.
2. **5 Built-in Presets**: 1-click loading of realistic test JDs across different career domains (Full Stack, Data Science, Product Management, Cloud DevOps, AI Intern).
3. **Missing Field Auditing**: Missing parameters are rigorously labeled `"not mentioned"`.
4. **Clean Light Theme**: Minimalist, distraction-free interface with KPI cards, master summary tables, and skills badges.
5. **OpenRouter API Integration**: Features automatic routing via `openrouter/free` to currently active zero-cost models, plus direct support for top open-weight models.
6. **Multi-Format Export**: One-click download of simplified summaries as CSV, JSON, or Markdown.
7. **Offline Heuristic Fallback**: Features a built-in fallback parser for demonstrations even without an immediate API key or when offline.

---

## 🛠️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/Krish3101/ass-3.git
cd ass-3
```

### 2. Create and activate a virtual environment
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Key
Get your free API key from [OpenRouter](https://openrouter.ai/keys).  
You can either:
- Create a `.env` file in the project root:
  ```env
  OPENROUTER_API_KEY="sk-or-v1-your-key-here"
  ```
- Or enter your key directly into the sidebar text field in the web app.

### 5. Run the Streamlit application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501` or `http://localhost:8502`.

---

## 🧪 Pre-loaded Samples
The application comes pre-packaged with 5 comprehensive sample job postings:
- **Sample 1**: Full Stack Software Engineer (Fintech Startup) — Tests missing salary handling.
- **Sample 2**: Senior Data Scientist (Enterprise) — Tests explicit salary range (₹28–38 LPA) and advanced ML stack extraction.
- **Sample 3**: Technical Product Management (Platform) — Tests informal JD parsing with "Not Disclosed" compensation.
- **Sample 4**: Cloud DevOps & SRE Engineer — Tests infrastructure requirements with unstated education credentials.
- **Sample 5**: AI Research Intern — Tests fixed monthly stipend (₹40,000/mo) and academic eligibility extraction.

---

## 📁 Repository Layout
```
├── app.py                 # Streamlit UI & interactive dashboard
├── extractor.py           # OpenRouter API integration & schema normalization
├── samples.py             # 5 pre-loaded sample job postings
├── generate_report.py     # Evaluation report generator (PDF)
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── .gitignore             # Secrets & cache protection
├── .env.example           # API key template
├── .streamlit/            # Light theme configuration
│   └── config.toml
└── screenshots/           # Output demo captures
```
