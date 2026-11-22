"""
Sample Job Descriptions for Job Description Simplifier.
Contains 5 diverse, realistic job postings covering varied roles, formatting styles,
and edge cases (e.g. missing salary, vague experience, unformatted text).
"""

SAMPLE_JDS = {
    "1. Full Stack Software Engineer (Startup - Missing Salary)": """
We are looking for a Full Stack Software Engineer to join our fast-growing fintech team at NovaPay!
Role: Full Stack Engineer
Location: Bengaluru, Karnataka (Hybrid - 3 days in office)

About NovaPay:
NovaPay is reinventing cross-border B2B payments across APAC. We're backed by Tier 1 VCs and scaling rapidly.

What you will do:
- Design, build, and maintain high-performance, fault-tolerant REST and GraphQL APIs.
- Develop responsive, accessible web frontends using modern React and TypeScript.
- Collaborate with product managers, UX designers, and QA engineers in an agile sprint cadence.
- Write unit, integration, and end-to-end tests to maintain >85% code coverage.
- Monitor production services using Datadog and participate in on-call rotations.

What we are looking for:
- 3 to 5 years of professional software engineering experience.
- Strong proficiency in TypeScript, Node.js, and modern React (Next.js experience is a plus).
- Hands-on experience with PostgreSQL, Redis, and message brokers like RabbitMQ or Kafka.
- Familiarity with Docker, Kubernetes, and AWS deployment pipelines.
- Bachelor's or Master's degree in Computer Science, Information Technology, or equivalent practical experience.
- Excellent communication skills and a strong sense of ownership.

Compensation: Competitive equity and benefits package including comprehensive health insurance, annual learning stipend, and wellness allowance.
    """,

    "2. Senior Data Scientist (Enterprise - Explicit Salary & Structured)": """
Organization: Apex Global Analytics Solutions
Title: Senior Data Scientist
Job ID: AGAS-2026-DS88
Work Mode: 100% Remote (Candidates must be based in India)
Base Salary: ₹28,00,000 - ₹38,00,000 per annum + 15% annual performance bonus

Role Overview:
Apex Global is seeking a Senior Data Scientist to spearhead our predictive analytics and GenAI customer intelligence initiatives.

Key Responsibilities:
- Lead the architecture and deployment of enterprise-scale machine learning models for customer churn, lifetime value, and recommendation engines.
- Conduct exploratory data analysis on multi-terabyte data lakes using PySpark and SQL.
- Implement LLM fine-tuning and Retrieval-Augmented Generation (RAG) pipelines for internal document synthesis.
- Mentor junior data scientists and establish MLOps best practices using MLflow and Kubeflow.
- Present quarterly model performance and business impact metrics to executive stakeholders.

Mandatory Requirements & Skills:
- Minimum 5+ years of hands-on data science experience in a production environment.
- Expert-level Python programming and SQL.
- Deep mathematical foundation in statistics, probability, and hypothesis testing.
- Hands-on expertise in PyTorch, scikit-learn, XGBoost, and Hugging Face Transformers.
- Proven track record deploying models to AWS SageMaker or GCP Vertex AI.
- Education: M.Tech / M.S. or Ph.D. in Computer Science, Data Science, Statistics, or related quantitative field.

Perks: 30 days paid time off, home office setup budget of ₹50,000, private medical insurance covering family.
    """,

    "3. Technical Product Manager (Informal / Modern Tech JD)": """
Company: ByteFlow Labs
Role: Technical Product Manager (TPM) - Developer Platforms
Location: Mumbai / Pune (On-site)

Who we need:
We're on the hunt for a Technical Product Manager who bridges the gap between deep infrastructure engineering and developer experience. If you love clean APIs, seamless SDKs, and developer workflows, this is for you.

Responsibilities:
• Own the product roadmap for our developer APIs, CLI tooling, and SDK documentation.
• Interview developer customers, gather feedback, and turn messy feedback into crisp PRDs and user stories.
• Partner closely with our core backend engineering team to prioritize technical debt vs new feature velocity.
• Define and track key platform metrics: Time-to-First-Hello-World, API latency, and monthly active API keys.
• Coordinate release notes, developer webinars, and migration guides.

Requirements:
• At least 4 years of experience working closely with software teams, with at least 2 years in product management or technical program management.
• Prior background as a software developer or solutions architect is strongly preferred.
• Deep understanding of REST APIs, webhook architectures, and developer authentication (OAuth2, API tokens).
• Exceptional written communication and ability to say "no" with data-driven rationale.
• B.Tech/B.E. in Computer Science or related degree.

Salary: Not disclosed by recruiter.
Benefits: Flexible working hours, catered lunches at the office, unlimited coffee, sponsored attendance at global tech conferences.
    """,

    "4. Cloud DevOps & SRE Engineer (Strict Tech Stack - Missing Education & Salary)": """
Position: Cloud DevOps / Site Reliability Engineer (SRE)
Employer: CloudMatrix Technologies
Employment Type: Full-time
Location: Remote (Worldwide)

About the Job:
CloudMatrix is expanding our Cloud Reliability division. You will ensure 99.99% uptime across our multi-cloud infrastructure supporting 10M+ daily active transactions.

Core Duties:
1. Build, maintain, and audit Terraform and Pulumi Infrastructure as Code (IaC) modules.
2. Manage multi-region Kubernetes clusters (EKS and GKE) across production and staging environments.
3. Configure automated CI/CD pipelines using GitHub Actions, GitLab CI, and ArgoCD.
4. Establish observability standards: Prometheus metrics, Grafana dashboards, and OpenTelemetry distributed tracing.
5. Lead incident post-mortems and automate self-healing infrastructure remediation scripts in Python and Bash.

Required Skills:
- Linux systems administration and network fundamentals (TCP/IP, DNS, SSL/TLS, BGP).
- Containerization and orchestration: Docker, Kubernetes, Helm.
- IaC tools: Terraform (mandatory).
- Cloud platforms: In-depth expertise in AWS or GCP.
- Scripting proficiency in Python or Go.
- Experience with zero-downtime deployment strategies (Canary, Blue/Green).
- Minimum 3 years in a dedicated DevOps/SRE capacity.
    """,

    "5. AI Research Intern (College / Junior Level - Stipend Specified)": """
Hiring Announcement: Generative AI Research Intern (6 Months)
Organization: CognitiveMind AI Labs
Location: Hyderabad (Hybrid - 2 days per week in office)
Stipend: ₹40,000 per month fixed + certificate of completion and pre-placement offer (PPO) potential.
Target Audience: Pre-final and final year undergraduate / postgraduate students (Batches 2026/2027).

About the Internship:
CognitiveMind AI Labs is working on novel reasoning paradigms for compact open-weights language models. We are looking for curious research interns passionate about LLM architecture, synthetic data generation, and evaluation benchmarks.

Responsibilities:
- Assist research scientists in setting up synthetic data generation pipelines for multi-step reasoning.
- Evaluate model checkpoints on standard benchmarks (GSM8K, HumanEval, MMLU).
- Implement parameter-efficient fine-tuning (PEFT, LoRA, QLoRA) on open models.
- Document experimental findings and help draft workshop papers.

Qualifications & Skills Needed:
- Currently enrolled in B.Tech/M.Tech/MCA in Computer Science, Artificial Intelligence, or Electrical Engineering.
- Solid Python proficiency and experience with PyTorch.
- Familiarity with Hugging Face transformers, datasets, and accelerate libraries.
- Strong understanding of transformer self-attention mechanisms and loss functions.
- Prior academic project or contribution to open-source GenAI projects is a big plus!
- Experience: Freshers / 0-1 year experience welcome.
    """
}
