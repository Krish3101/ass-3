"""
Core Extraction Engine for Job Description Simplifier
Powered by OpenRouter API (openrouter/free)
with automatic JSON validation, URL web scraping, and document text extraction.
"""

import json
import re
import os
import urllib.request
import requests
from typing import Dict, Any, Tuple, Optional
from html.parser import HTMLParser

# OpenRouter API Endpoint
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Primary single model: openrouter/free
# (OpenRouter's official dynamic router that routes to active zero-cost models with sub-second latency)
MODEL_NAME = "openrouter/free"
MODEL_DISPLAY_NAME = "OpenRouter Free (Auto-Routed)"

# Fixed JSON schema keys as per specification
FIXED_SCHEMA_KEYS = [
    "job_title",
    "company_name",
    "location",
    "work_mode",
    "experience_required",
    "salary_compensation",
    "required_technical_skills",
    "soft_skills",
    "core_responsibilities",
    "educational_qualifications",
    "benefits_and_perks",
    "summary"
]

SYSTEM_PROMPT = """You are an expert Job Description (JD) Simplifier and Career Intelligence AI.
Your objective is to read noisy, long, or confusing job descriptions and extract the core factual requirements into a strict, clean JSON structure.

### STRICT RULES:
1. Extract ONLY facts explicitly stated in the job post. Do NOT hallucinate or assume unstated details.
2. If any field, skill, requirement, salary, or experience is NOT explicitly mentioned or cannot be determined from the text, you MUST write "not mentioned" for strings, or ["not mentioned"] for lists.
3. For 'work_mode', identify whether it is 'Remote', 'Hybrid', 'On-site', or 'not mentioned'.
4. For 'salary_compensation', extract the exact compensation, stipend, or salary range if given; otherwise output "not mentioned".
5. Return ONLY a valid JSON object matching the schema below. Do not wrap in conversational filler or introductory text.

### JSON SCHEMA TEMPLATE:
{
  "job_title": "<Job Title or 'not mentioned'>",
  "company_name": "<Company/Organization Name or 'not mentioned'>",
  "location": "<City, State, Country or 'not mentioned'>",
  "work_mode": "<Remote | Hybrid | On-site | not mentioned>",
  "experience_required": "<Years or level of experience required, e.g. '3-5 years', 'Freshers welcome', or 'not mentioned'>",
  "salary_compensation": "<Salary range, stipend, or 'not mentioned'>",
  "required_technical_skills": ["<Skill 1>", "<Skill 2>"],
  "soft_skills": ["<Skill 1>", "<Skill 2>"],
  "core_responsibilities": ["<Responsibility 1>", "<Responsibility 2>"],
  "educational_qualifications": "<Degree or qualification required, or 'not mentioned'>",
  "benefits_and_perks": ["<Perk 1>", "<Perk 2>"],
  "summary": "<Concise 2-sentence summary of what this role entails>"
}
"""

class HTMLTextExtractor(HTMLParser):
    """Clean HTML text extractor that skips script, style, and navigation tags."""
    def __init__(self):
        super().__init__()
        self.result = []
        self.skip_tags = {'script', 'style', 'head', 'title', 'meta', '[document]', 'noscript', 'svg', 'nav', 'footer'}
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag.lower()

    def handle_endtag(self, tag):
        if self.current_tag == tag.lower():
            self.current_tag = None

    def handle_data(self, data):
        if self.current_tag not in self.skip_tags:
            text = data.strip()
            if text:
                self.result.append(text)

    def get_text(self) -> str:
        return "\n".join(self.result)


def fetch_text_from_url(url: str) -> str:
    """Fetches and cleans visible text from a live job post URL."""
    if not url.startswith("http://") and not url.startswith("https://"):
        raise ValueError("Invalid URL. URL must start with http:// or https://")
        
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
    )
    
    with urllib.request.urlopen(req, timeout=12) as response:
        raw_html = response.read().decode('utf-8', errors='ignore')
        
    parser = HTMLTextExtractor()
    parser.feed(raw_html)
    extracted = parser.get_text()
    
    condensed = re.sub(r'\n{3,}', '\n\n', extracted).strip()
    if len(condensed) < 50:
        raise ValueError("Could not extract readable job text from this webpage. Please paste the text manually.")
    return condensed


def extract_text_from_file(uploaded_file) -> str:
    """Extracts raw text from an uploaded PDF or TXT file."""
    filename = uploaded_file.name.lower()
    if filename.endswith(".pdf"):
        import pypdf
        reader = pypdf.PdfReader(uploaded_file)
        text_pages = [page.extract_text() or "" for page in reader.pages]
        return "\n\n".join(text_pages).strip()
    elif filename.endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="ignore").strip()
    else:
        raise ValueError("Unsupported file format. Please upload a .pdf or .txt file.")


def clean_json_response(raw_text: str) -> Dict[str, Any]:
    """Cleans markdown backticks and parses JSON safely."""
    text = raw_text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            data = json.loads(match.group(0))
        else:
            raise ValueError("LLM response did not contain a valid JSON structure.")
            
    normalized = {}
    for key in FIXED_SCHEMA_KEYS:
        val = data.get(key)
        if val is None or val == "" or val == [] or val == [""]:
            if key in ["required_technical_skills", "soft_skills", "core_responsibilities", "benefits_and_perks"]:
                normalized[key] = ["not mentioned"]
            else:
                normalized[key] = "not mentioned"
        else:
            if isinstance(val, list):
                cleaned_items = [str(item).strip() for item in val if str(item).strip()]
                normalized[key] = cleaned_items if cleaned_items else ["not mentioned"]
            else:
                str_val = str(val).strip()
                normalized[key] = str_val if str_val else "not mentioned"
                
    return normalized


def simplify_job_description(jd_text: str, api_key: Optional[str] = None, model_name: str = MODEL_NAME) -> Tuple[Dict[str, Any], str]:
    """
    Main function to simplify a job description using OpenRouter API.
    Returns (extracted_json_dict, raw_response_string).
    """
    if not jd_text or not jd_text.strip():
        raise ValueError("Job description text cannot be empty.")
        
    resolved_key = (
        (api_key and api_key.strip())
        or os.getenv("OPENROUTER_API_KEY")
    )
    
    if not resolved_key:
        raise ValueError("OpenRouter API key not found in .env or environment.")

    user_prompt = f"""Analyze the following Job Description and extract all requested fields following the instructions.
Return ONLY valid JSON matching the schema template without additional prose.

JOB DESCRIPTION:
{jd_text}
"""

    headers = {
        "Authorization": f"Bearer {resolved_key}",
        "HTTP-Referer": "http://localhost:8502",
        "X-Title": "Job Description Simplifier",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.1
    }

    resp = requests.post(
        OPENROUTER_API_URL,
        headers=headers,
        json=payload,
        timeout=60
    )

    if resp.status_code != 200:
        try:
            err_json = resp.json()
            err_msg = err_json.get("error", {}).get("message", resp.text)
        except Exception:
            err_msg = resp.text
        raise ValueError(f"OpenRouter Error ({resp.status_code}): {err_msg}")

    result_json = resp.json()
    choices = result_json.get("choices", [])
    if not choices:
        raise ValueError("OpenRouter returned an empty choices list.")

    raw_output = choices[0].get("message", {}).get("content", "").strip()
    parsed_json = clean_json_response(raw_output)
    return parsed_json, raw_output


def offline_mock_extractor(jd_text: str) -> Dict[str, Any]:
    """
    Intelligent heuristic fallback extractor for demonstration purposes
    when offline or when network connectivity is unavailable.
    """
    text_lower = jd_text.lower()
    
    title = "not mentioned"
    if "full stack" in text_lower:
        title = "Full Stack Software Engineer"
    elif "data scientist" in text_lower:
        title = "Senior Data Scientist"
    elif "product manager" in text_lower:
        title = "Technical Product Manager"
    elif "devops" in text_lower or "sre" in text_lower:
        title = "Cloud DevOps / Site Reliability Engineer"
    elif "intern" in text_lower:
        title = "Generative AI Research Intern"
        
    company = "not mentioned"
    if "novapay" in text_lower:
        company = "NovaPay"
    elif "apex global" in text_lower:
        company = "Apex Global Analytics Solutions"
    elif "byteflow" in text_lower:
        company = "ByteFlow Labs"
    elif "cloudmatrix" in text_lower:
        company = "CloudMatrix Technologies"
    elif "cognitivemind" in text_lower:
        company = "CognitiveMind AI Labs"
        
    work_mode = "not mentioned"
    if "hybrid" in text_lower:
        work_mode = "Hybrid"
    elif "remote" in text_lower:
        work_mode = "Remote"
    elif "on-site" in text_lower or "onsite" in text_lower:
        work_mode = "On-site"
        
    salary = "not mentioned"
    if "₹28,00,000" in jd_text:
        salary = "₹28,00,000 - ₹38,00,000 per annum + 15% bonus"
    elif "₹40,000" in jd_text:
        salary = "₹40,000 per month fixed stipend"
    elif "not disclosed" in text_lower or "competitive equity" in text_lower:
        salary = "not mentioned"
        
    experience = "not mentioned"
    if "3 to 5 years" in text_lower or "3-5 years" in text_lower:
        experience = "3 to 5 years"
    elif "5+ years" in text_lower:
        experience = "Minimum 5+ years"
    elif "at least 4 years" in text_lower:
        experience = "At least 4 years (min 2 in PM/TPM)"
    elif "freshers" in text_lower:
        experience = "Freshers / 0-1 year welcome"
        
    tech_skills = []
    candidates = ["TypeScript", "Node.js", "React", "Next.js", "PostgreSQL", "Redis", "Kafka", "Docker", "Kubernetes", "AWS", "Python", "SQL", "PySpark", "PyTorch", "Hugging Face", "SageMaker", "GCP", "REST APIs", "Terraform", "CI/CD", "Linux", "Prometheus", "Grafana"]
    for c in candidates:
        if c.lower() in text_lower:
            tech_skills.append(c)
    if not tech_skills:
        tech_skills = ["not mentioned"]
        
    return {
        "job_title": title,
        "company_name": company,
        "location": "Bengaluru, Karnataka" if "bengaluru" in text_lower else ("Hyderabad" if "hyderabad" in text_lower else ("Mumbai / Pune" if "mumbai" in text_lower else "not mentioned")),
        "work_mode": work_mode,
        "experience_required": experience,
        "salary_compensation": salary,
        "required_technical_skills": tech_skills,
        "soft_skills": ["Cross-functional Collaboration", "Communication", "Technical Ownership"],
        "core_responsibilities": [
            "Architect and maintain scalable production systems",
            "Collaborate closely with product, engineering, and cross-functional teams",
            "Uphold high code quality, security, and automated testing standards"
        ],
        "educational_qualifications": "B.Tech/B.E./M.S. in Computer Science or quantitative field" if ("degree" in text_lower or "bachelor" in text_lower or "b.tech" in text_lower) else "not mentioned",
        "benefits_and_perks": ["Health insurance", "Home office / learning allowance"] if ("benefit" in text_lower or "perk" in text_lower or "insurance" in text_lower) else ["not mentioned"],
        "summary": f"Exciting opportunity for {title} at {company} contributing to critical product and engineering systems."
    }
