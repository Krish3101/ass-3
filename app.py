"""
Job Description Simplifier - Streamlit Web Application
An intelligent GenAI tool that extracts required skills, experience,
compensation & responsibilities from messy job listings into clean, structured tables
powered by OpenRouter AI.
"""

import streamlit as st
import pandas as pd
import json
import os
from dotenv import load_dotenv
from samples import SAMPLE_JDS
from extractor import (
    simplify_job_description,
    extract_text_from_file,
    offline_mock_extractor,
    fetch_text_from_url,
    MODEL_NAME,
    MODEL_DISPLAY_NAME
)

# Load local environment variables from .env
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Job Description Simplifier",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean, minimalist, light CSS styling
st.markdown("""
<style>
    .stApp {
        background-color: #FFFFFF;
        color: #0F172A;
    }
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1E3A8A;
        letter-spacing: -0.02em;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 0.98rem;
        color: #475569;
        margin-bottom: 1.2rem;
    }
    
    /* Clean Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem;
        color: #64748B;
        font-weight: 500;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.15rem;
        color: #0F172A;
        font-weight: 700;
    }

    /* Skills badges */
    .skill-chip {
        display: inline-block;
        padding: 0.3rem 0.75rem;
        margin: 0.25rem 0.25rem 0.25rem 0;
        border-radius: 6px;
        background-color: #EFF6FF;
        color: #1D4ED8;
        border: 1px solid #BFDBFE;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .skill-chip-soft {
        background-color: #FEF9C3;
        color: #854D0E;
        border: 1px solid #FEF08A;
    }
    .not-mentioned {
        color: #DC2626;
        font-style: italic;
        font-weight: 600;
    }
    .status-badge {
        background-color: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-radius: 8px;
        padding: 0.65rem 0.9rem;
        margin-bottom: 1.2rem;
    }
    .status-badge-title {
        color: #166534;
        font-weight: 600;
        font-size: 0.85rem;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .status-badge-sub {
        color: #15803D;
        font-size: 0.75rem;
        margin-top: 2px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/briefcase.png", width=48)
    st.title("Job Simplifier")
    
    # Clean Live Engine Indicator
    st.markdown(f"""
    <div class="status-badge">
        <div class="status-badge-title">● OpenRouter AI Engine Active</div>
        <div class="status-badge-sub">{MODEL_DISPLAY_NAME}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ⚡ Pre-loaded Sample JDs")
    sample_selection = st.selectbox(
        "Select a sample to load instantly:",
        options=["None (Custom Input)"] + list(SAMPLE_JDS.keys()),
        index=0,
        help="Select any realistic sample to instantly populate the input."
    )

# ----------------- MAIN CONTENT -----------------
st.markdown('<div class="main-header">📋 Job Description Simplifier</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="sub-header">Fast, structured extraction of required skills, experience, salary & responsibilities powered by {MODEL_DISPLAY_NAME}.</div>',
    unsafe_allow_html=True
)

default_text = ""
if sample_selection != "None (Custom Input)":
    default_text = SAMPLE_JDS[sample_selection].strip()

input_tab1, input_tab2, input_tab3 = st.tabs([
    "✍️ Paste Text", 
    "🌐 Fetch from Web URL", 
    "📂 Upload File (PDF / TXT)"
])

with input_tab1:
    jd_input = st.text_area(
        "Job Description Text:",
        value=default_text,
        height=240,
        placeholder="Paste raw, unformatted job description text here..."
    )
    
with input_tab2:
    st.markdown("Enter a live job post URL to fetch its text automatically:")
    url_input = st.text_input(
        "Job Posting URL:",
        placeholder="https://boards.greenhouse.io/... or https://jobs.lever.co/..."
    )
    if st.button("📥 Fetch Web Content", use_container_width=False):
        if url_input:
            try:
                with st.spinner("Fetching job content from webpage..."):
                    fetched_text = fetch_text_from_url(url_input.strip())
                    st.success(f"Fetched {len(fetched_text)} characters from {url_input}")
                    jd_input = fetched_text
            except Exception as url_err:
                st.error(f"Failed to fetch webpage: {url_err}")
        else:
            st.warning("Please enter a valid URL starting with http:// or https://")

with input_tab3:
    uploaded_doc = st.file_uploader("Upload Job Description Document (.pdf or .txt)", type=["pdf", "txt"])
    if uploaded_doc is not None:
        try:
            extracted_doc_text = extract_text_from_file(uploaded_doc)
            st.success(f"Successfully extracted {len(extracted_doc_text)} characters from {uploaded_doc.name}")
            jd_input = extracted_doc_text
        except Exception as e:
            st.error(f"Error reading file: {e}")

run_btn = st.button("🚀 Simplify Job Description", type="primary", use_container_width=True)

# ----------------- PROCESSING & RESULTS -----------------
if run_btn:
    if not jd_input or not jd_input.strip():
        st.warning("⚠️ Please provide a job description by pasting text, entering a URL, selecting a sample, or uploading a file.")
    else:
        with st.spinner(f"Analyzing job post with {MODEL_DISPLAY_NAME}..."):
            extracted_data = None
            raw_response = ""
            
            try:
                env_api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
                if env_api_key:
                    extracted_data, raw_response = simplify_job_description(
                        jd_text=jd_input,
                        api_key=env_api_key,
                        model_name=MODEL_NAME
                    )
                else:
                    st.info("ℹ️ Running built-in intelligent heuristic extraction.")
                    extracted_data = offline_mock_extractor(jd_input)
                    raw_response = json.dumps(extracted_data, indent=2)
            except Exception as ex:
                st.warning(f"Note: Transitioned to offline heuristic engine ({ex}).")
                extracted_data = offline_mock_extractor(jd_input)
                raw_response = json.dumps(extracted_data, indent=2)

            st.session_state["extracted_result"] = extracted_data
            st.session_state["raw_response"] = raw_response

if "extracted_result" in st.session_state:
    data = st.session_state["extracted_result"]
    
    st.markdown("---")
    st.subheader("🎯 Extracted Job Intelligence Summary")
    
    summary_text = data.get("summary", "not mentioned")
    st.success(f"**Role Summary:** {summary_text}")
    
    # Top KPI Metrics Cards
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.metric("💼 Job Title", data.get("job_title", "not mentioned"))
    with m2:
        st.metric("🏢 Company", data.get("company_name", "not mentioned"))
    with m3:
        st.metric("📍 Work Mode", data.get("work_mode", "not mentioned"))
    with m4:
        st.metric("⏳ Experience", data.get("experience_required", "not mentioned"))
    with m5:
        salary_val = data.get("salary_compensation", "not mentioned")
        st.metric("💰 Salary", salary_val if salary_val != "not mentioned" else "Not Disclosed")

    # Structured Tabbed View
    tab_table, tab_skills, tab_resp, tab_json = st.tabs([
        "📊 Master Summary Table", 
        "🛠️ Skills Breakdown", 
        "📝 Key Responsibilities", 
        "🔍 Raw JSON Schema"
    ])
    
    # 1. Master Table View
    with tab_table:
        st.markdown("#### Clean Specification Table")
        table_rows = [
            {"Attribute": "Job Title", "Extracted Details": data.get("job_title", "not mentioned")},
            {"Attribute": "Company / Organization", "Extracted Details": data.get("company_name", "not mentioned")},
            {"Attribute": "Location", "Extracted Details": data.get("location", "not mentioned")},
            {"Attribute": "Work Mode", "Extracted Details": data.get("work_mode", "not mentioned")},
            {"Attribute": "Experience Required", "Extracted Details": data.get("experience_required", "not mentioned")},
            {"Attribute": "Salary / Compensation", "Extracted Details": data.get("salary_compensation", "not mentioned")},
            {"Attribute": "Educational Qualifications", "Extracted Details": data.get("educational_qualifications", "not mentioned")},
            {"Attribute": "Required Technical Skills", "Extracted Details": ", ".join(data.get("required_technical_skills", []))},
            {"Attribute": "Soft / Interpersonal Skills", "Extracted Details": ", ".join(data.get("soft_skills", []))},
            {"Attribute": "Key Responsibilities", "Extracted Details": " • " + " • ".join(data.get("core_responsibilities", []))},
            {"Attribute": "Benefits & Perks", "Extracted Details": ", ".join(data.get("benefits_and_perks", []))},
        ]
        
        df_table = pd.DataFrame(table_rows)
        st.table(df_table)

    # 2. Skills View
    with tab_skills:
        col_tech, col_soft = st.columns(2)
        with col_tech:
            st.markdown("##### 💻 Technical Skills Required")
            tech_skills = data.get("required_technical_skills", ["not mentioned"])
            if tech_skills == ["not mentioned"] or not tech_skills:
                st.markdown('<span class="not-mentioned">⚠️ No technical skills explicitly mentioned.</span>', unsafe_allow_html=True)
            else:
                badges_html = "".join([f'<span class="skill-chip">{skill}</span>' for skill in tech_skills])
                st.markdown(badges_html, unsafe_allow_html=True)

        with col_soft:
            st.markdown("##### 🤝 Soft / Collaborative Skills")
            soft_skills = data.get("soft_skills", ["not mentioned"])
            if soft_skills == ["not mentioned"] or not soft_skills:
                st.markdown('<span class="not-mentioned">⚠️ No soft skills explicitly mentioned.</span>', unsafe_allow_html=True)
            else:
                soft_badges_html = "".join([f'<span class="skill-chip skill-chip-soft">{skill}</span>' for skill in soft_skills])
                st.markdown(soft_badges_html, unsafe_allow_html=True)

    # 3. Responsibilities View
    with tab_resp:
        st.markdown("##### 🎯 Daily Responsibilities & Deliverables")
        responsibilities = data.get("core_responsibilities", ["not mentioned"])
        if responsibilities == ["not mentioned"] or not responsibilities:
            st.markdown('<span class="not-mentioned">⚠️ No responsibilities explicitly mentioned.</span>', unsafe_allow_html=True)
        else:
            for idx, resp in enumerate(responsibilities, 1):
                st.markdown(f"**{idx}.** {resp}")

    # 4. Raw JSON View
    with tab_json:
        st.markdown("##### Validated Strict JSON Schema Output")
        st.json(data)

    # Export options
    st.markdown("---")
    st.markdown("### 📥 Export & Download Results")
    exp_c1, exp_c2, exp_c3 = st.columns(3)
    
    with exp_c1:
        st.download_button(
            label="📄 Download as CSV",
            data=df_table.to_csv(index=False).encode("utf-8"),
            file_name=f"simplified_jd_{data.get('job_title', 'export').lower().replace(' ', '_')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    with exp_c2:
        st.download_button(
            label="📦 Download JSON Schema",
            data=json.dumps(data, indent=2).encode("utf-8"),
            file_name=f"simplified_jd_{data.get('job_title', 'export').lower().replace(' ', '_')}.json",
            mime="application/json",
            use_container_width=True
        )
    with exp_c3:
        tech_list = "\n".join([f"- {s}" for s in data.get("required_technical_skills", [])])
        resp_list = "\n".join([f"- {r}" for r in data.get("core_responsibilities", [])])
        md_content = f"""# Job Description Summary: {data.get('job_title')}
**Company:** {data.get('company_name')}
**Location / Mode:** {data.get('location')} ({data.get('work_mode')})
**Experience:** {data.get('experience_required')}
**Salary:** {data.get('salary_compensation')}

## Summary
{data.get('summary')}

## Technical Skills
{tech_list}

## Key Responsibilities
{resp_list}

*Extracted via Job Description Simplifier*
"""
        st.download_button(
            label="📝 Download Markdown",
            data=md_content.encode("utf-8"),
            file_name=f"simplified_jd_{data.get('job_title', 'export').lower().replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True
        )
