"""
Generates a formal 2-page Technical Academic Report (Report.pdf) for PS #44
Job Description Simplifier using ReportLab.
- Typography: Times New Roman throughout (Times-Roman, Times-Bold, Times-Italic).
- Color: Solid black text throughout (#000000).
- Alignment: Cleanly justified body text, centered headers, aligned tables.
- Spacing: Balanced content distribution filling both A4 pages naturally without gaps.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)


def build_pdf(filename="Report.pdf"):
    # Margins: 36pt (0.5 inch) left/right, 34pt top/bottom
    # Printable area: 523.28pt wide x 773.89pt high
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=34,
        bottomMargin=34
    )

    styles = getSampleStyleSheet()

    # Pure Black, Times New Roman Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.black,
        alignment=1, # Centered
        spaceAfter=3
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=14,
        textColor=colors.black,
        alignment=1 # Centered
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=11,
        leading=14.5,
        textColor=colors.black,
        spaceBefore=8,
        spaceAfter=3.5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9.8,
        leading=13.6,
        textColor=colors.black,
        alignment=4, # Justified
        spaceAfter=3.5
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9.5,
        leading=13.2,
        textColor=colors.black,
        alignment=4, # Justified
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.black,
        backColor=colors.HexColor("#F9FAFB"),
        borderColor=colors.HexColor("#D1D5DB"),
        borderWidth=0.5,
        borderPadding=3.5,
        spaceBefore=4,
        spaceAfter=4
    )

    table_header_style = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.black,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TC',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8,
        leading=10.5,
        textColor=colors.black
    )

    story = []

    # =========================================================================
    # PAGE 1
    # =========================================================================
    story.append(Paragraph("<b>Job Description Simplifier</b>", title_style))
    story.append(Spacer(1, 2))
    header_meta = "<b>Name:</b> Krish Kalya &nbsp;|&nbsp; <b>Roll No:</b> 44 &nbsp;|&nbsp; <b>Class:</b> LY Core 1"
    story.append(Paragraph(header_meta, meta_style))
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width="100%", thickness=0.75, color=colors.black, spaceBefore=2, spaceAfter=6))

    # Section 1
    story.append(Paragraph("<b>1. Introduction & Problem Statement</b>", h1_style))
    p1_text = (
        "Job listings published across modern hiring platforms and career portals are predominantly verbose, unformatted, "
        "and inundated with boilerplate corporate descriptions. As a consequence, candidates encounter significant cognitive "
        "friction when reviewing dozens of postings to discern whether their technical capabilities, qualifications, and compensation "
        "expectations align with the hiring organization. Problem Statement #44 mandates the engineering of an automated system that "
        "ingests raw, unstructured job advertisements and extracts the essential criteria into a standardized schema and tabular interface. "
        "The primary extracted parameters comprise required technical skills, soft skills, required experience levels, salary/compensation, "
        "and primary responsibilities. A pivotal constraint governing this assignment is that any detail omitted by the employer in the job "
        "text—such as unstated salary bands, absent educational degrees, or undefined location policies—must be explicitly and strictly "
        "populated as <b>'not mentioned'</b> rather than hallucinated, inferred, or left blank."
    )
    story.append(Paragraph(p1_text, body_style))

    # Section 2
    story.append(Paragraph("<b>2. System Architecture & Component Design</b>", h1_style))
    arch_intro = (
        "The software architecture is decoupled into four modular subsystems to ensure high throughput, deterministic accuracy, and "
        "a responsive user experience:"
    )
    story.append(Paragraph(arch_intro, body_style))
    
    arch_points = [
        "• <b>Multi-Source Ingestion Pipeline:</b> Provides three flexible ingestion modes: direct text pasting via a multiline text area, "
        "automated URL web scraping for live job postings (utilizing a custom HTML parser that discards script, style, and navigation tags), "
        "and document file uploading supporting both <code>.pdf</code> and <code>.txt</code> formats with automated textual extraction.",
        
        "• <b>Large Language Model (LLM) Inference Engine:</b> Interfaces with the OpenRouter API (<code>https://openrouter.ai/api/v1</code>) "
        "utilizing the <code>openrouter/free</code> auto-router endpoint. The engine issues zero-shot prompt instructions with the decoding "
        "temperature set to 0.1 to maximize factual determinism and eliminate model creativity or speculative assumptions.",
        
        "• <b>Schema Validation & Normalization Pipeline:</b> Evaluates raw model outputs, strips optional markdown code block enclosures "
        "(<code>```json ... ```</code>), executes strict JSON parsing, and passes the parsed payload through a dictionary normalizer that "
        "iterates over twelve canonical schema keys to guarantee strict adherence and apply 'not mentioned' fallback values.",
        
        "• <b>Interactive Light-Mode Dashboard:</b> Developed in Streamlit 1.67, presenting summary metric cards, tabbed views for "
        "the master summary table, interactive skills breakdown chips, key responsibilities, raw JSON schema, and one-click export handlers "
        "for CSV, JSON, and Markdown formats."
    ]
    for pt in arch_points:
        story.append(Paragraph(pt, bullet_style))

    # Section 3
    story.append(Paragraph("<b>3. Ingestion & Pre-processing Methodology</b>", h1_style))
    p3_text = (
        "Because raw job listings contain diverse forms of formatting noise, specialized pre-processing routines were constructed. "
        "For web URLs, a custom subclass of Python's built-in <code>html.parser.HTMLParser</code> extracts only human-readable text "
        "while systematically filtering out script blocks, stylesheet rules, document headers, metadata, SVG elements, and navigational footers. "
        "Whitespace is condensed to eliminate consecutive blank lines. For document uploads, <code>pypdf</code> traverses all pages to assemble "
        "the full textual stream into a unified string, ensuring that multi-page job descriptions are processed with complete context."
    )
    story.append(Paragraph(p3_text, body_style))

    # Section 4
    story.append(Paragraph("<b>4. Prompt Engineering & JSON Schema Design</b>", h1_style))
    p4_text = (
        "During initial experimentation, unconstrained prompts such as <i>'Extract skills, experience, salary and responsibilities into JSON'</i> "
        "exhibited two recurrent flaws: first, models frequently hallucinated plausible salaries (e.g., generating '$90k-$120k' for software "
        "engineer postings where compensation was unstated); second, models altered key names unpredictably across runs. "
        "To resolve this, the system prompt was engineered with explicit boundary rules and a fixed JSON schema template:"
    )
    story.append(Paragraph(p4_text, body_style))

    code_snippet = (
        "SYSTEM PROMPT DIRECTIVES:\n"
        "1. Extract ONLY facts explicitly stated in the job posting. Do NOT assume unstated details.\n"
        "2. If any field, skill, requirement, salary, or experience is NOT explicitly mentioned,\n"
        "   you MUST write \"not mentioned\" for strings, or [\"not mentioned\"] for lists.\n"
        "3. Return ONLY a valid JSON object matching the 12-key schema template without prose.\n"
        "SCHEMA KEYS: ['job_title', 'company_name', 'location', 'work_mode', 'experience_required',\n"
        "              'salary_compensation', 'required_technical_skills', 'soft_skills',\n"
        "              'core_responsibilities', 'educational_qualifications', 'benefits_and_perks', 'summary']"
    )
    story.append(Paragraph(code_snippet.replace("\n", "<br/>"), code_style))

    # Force Page Break to cleanly begin Page 2
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2
    # =========================================================================
    # Section 5
    story.append(Paragraph("<b>5. Step-by-Step Implementation Procedure</b>", h1_style))
    steps = [
        "<b>Step 1: Workspace & Virtual Environment Setup:</b> Established project repository <code>llm-ps44-ADT23SOCB0536</code>, initialized "
        "an isolated Python virtual environment (<code>python3 -m venv venv</code>), and configured <code>.gitignore</code> to safeguard "
        "sensitive local environment files (<code>.env</code>) and build artifacts.",
        
        "<b>Step 2: API Integration & Ingestion Pipeline:</b> Developed <code>extractor.py</code> to handle live API requests against OpenRouter "
        "using Python's <code>requests</code> library. Constructed the URL scraper using standard library components and integrated <code>pypdf</code> "
        "for document ingestion.",
        
        "<b>Step 3: Response Normalization & Fallback Engine:</b> Implemented <code>clean_json_response()</code> utilizing regular expressions "
        "to strip surrounding markdown backticks. Added an automated dictionary normalizer that verifies all 12 schema keys and enforces the "
        "'not mentioned' fallback rule whenever a field is omitted, empty, or null. Added an offline heuristic fallback parser for demo resilience.",
        
        "<b>Step 4: Streamlit Dashboard Construction:</b> Developed <code>app.py</code> with a light-mode layout. Designed metric summary "
        "cards, tabbed panels for the specification table, technical skills, daily responsibilities, raw JSON schema, and three export formats.",
        
        "<b>Step 5: Rigorous Test Suite Execution:</b> Packaged 5 comprehensive test job descriptions in <code>samples.py</code> representing "
        "diverse employment categories to validate deterministic parsing and verify strict 'not mentioned' enforcement."
    ]
    for step in steps:
        story.append(Paragraph(step, bullet_style))

    # Section 6
    story.append(Paragraph("<b>6. Test Cases and Experimental Evaluation Results</b>", h1_style))
    p6_intro = (
        "The system was evaluated against five representative job postings with varying structural complexities and missing attributes. "
        "The experimental results demonstrate zero-shot extraction fidelity and consistent enforcement of the 'not mentioned' mandate:"
    )
    story.append(Paragraph(p6_intro, body_style))

    # Academic Results Table
    table_data = [
        [
            Paragraph("<b>Test Case</b>", table_header_style),
            Paragraph("<b>Role & Organization</b>", table_header_style),
            Paragraph("<b>Experience</b>", table_header_style),
            Paragraph("<b>Extracted Salary</b>", table_header_style),
            Paragraph("<b>Validation of 'not mentioned' Rule</b>", table_header_style)
        ],
        [
            Paragraph("1. Startup Posting", table_cell_style),
            Paragraph("Full Stack Engineer<br/>NovaPay", table_cell_style),
            Paragraph("3 to 5 years", table_cell_style),
            Paragraph("not mentioned", table_cell_style),
            Paragraph("Salary omitted in source text; strictly and correctly assigned 'not mentioned'.", table_cell_style)
        ],
        [
            Paragraph("2. Enterprise Posting", table_cell_style),
            Paragraph("Senior Data Scientist<br/>Apex Global Analytics", table_cell_style),
            Paragraph("Minimum 5+ years", table_cell_style),
            Paragraph("INR 28L - 38L + 15% bonus", table_cell_style),
            Paragraph("Explicit compensation and full ML stack (PyTorch, PySpark) parsed accurately.", table_cell_style)
        ],
        [
            Paragraph("3. Product Role", table_cell_style),
            Paragraph("Technical Product Manager<br/>ByteFlow Labs", table_cell_style),
            Paragraph("At least 4 years", table_cell_style),
            Paragraph("not mentioned", table_cell_style),
            Paragraph("Informal text stated 'Not Disclosed'; correctly normalized to 'not mentioned'.", table_cell_style)
        ],
        [
            Paragraph("4. DevOps Role", table_cell_style),
            Paragraph("DevOps / SRE Engineer<br/>CloudMatrix Technologies", table_cell_style),
            Paragraph("Minimum 3 years", table_cell_style),
            Paragraph("not mentioned", table_cell_style),
            Paragraph("Degree criteria omitted; educational qualification defaulted to 'not mentioned'.", table_cell_style)
        ],
        [
            Paragraph("5. AI Internship", table_cell_style),
            Paragraph("GenAI Research Intern<br/>CognitiveMind AI Labs", table_cell_style),
            Paragraph("Freshers / 0-1 year", table_cell_style),
            Paragraph("INR 40,000 / month stipend", table_cell_style),
            Paragraph("Fixed monthly stipend and degree eligibility (B.Tech/M.Tech) extracted cleanly.", table_cell_style)
        ]
    ]

    result_table = Table(table_data, colWidths=[68, 106, 74, 108, 167])
    result_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F3F4F6")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(result_table)
    story.append(Spacer(1, 4))

    # Section 7
    story.append(Paragraph("<b>7. Technical Challenges & Architectural Solutions</b>", h1_style))
    challenges = [
        "• <b>Markdown Enclosure Elimination:</b> Generative LLMs frequently enclose JSON data inside markdown delimiters (<code>```json ... ```</code>). "
        "A robust regex sanitization pass strips these delimiters before executing <code>json.loads()</code>, preventing runtime decoding exceptions.",
        
        "• <b>Guaranteeing Schema Completeness:</b> Unstructured job postings occasionally lead models to omit specific dictionary keys entirely. "
        "A post-processing normalizer iterates over <code>FIXED_SCHEMA_KEYS</code>, populating absent keys with <code>\"not mentioned\"</code>.",
        
        "• <b>HTML Noise Suppression:</b> Career websites contain extensive boilerplate navigation and style code. The custom HTML parser "
        "strips non-content tags and consolidates whitespace to avoid wasting token context during model ingestion.",

        "• <b>Zero-Cost API Availability:</b> Direct platform quota constraints were mitigated by leveraging OpenRouter's dynamic free router, "
        "which routes queries to available high-speed models without requiring local GPU compute."
    ]
    for ch in challenges:
        story.append(Paragraph(ch, bullet_style))

    # Section 8
    story.append(Paragraph("<b>8. Conclusion & Future Scope</b>", h1_style))
    p8_text = (
        "The developed Job Description Simplifier fulfills all technical and functional requirements specified in Problem Statement #44. "
        "By synthesizing prompt engineering, deterministic low-temperature decoding, automated pre-processing, and strict post-processing "
        "normalization, the system consistently formats messy job advertisements into structured tables while strictly enforcing the "
        "'not mentioned' fallback rule for unstated attributes. Future extensions could incorporate resume-to-JD semantic similarity scoring "
        "to identify skill gaps directly from the extracted specification table."
    )
    story.append(Paragraph(p8_text, body_style))

    doc.build(story)
    print(f"Report built successfully at {filename}")


if __name__ == "__main__":
    build_pdf("Report.pdf")
