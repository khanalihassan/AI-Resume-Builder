# ============================================================
# FILE: gui.py
# AI RESUME BUILDER PRO
# Clean SaaS UI (White + Sky Blue) + Connected Visual Templates
# NOTE: Only the interface was redesigned. All backend logic,
# function names and controller calls are unchanged.
# ============================================================

import gradio as gr
import app as controller

from resume_templates import (
    get_supported_templates,
    get_template_description,
)


# ============================================================
# 1. PREMIUM LIGHT UI THEME (WHITE + SKY BLUE)
# ============================================================

CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root,
.dark,
.gradio-container {
    --bg: #f3f9ff;
    --card: #ffffff;
    --input: #f8fbff;
    --border: #dbeafe;
    --border-strong: #bfdbfe;
    --text: #0f172a;
    --muted: #64748b;
    --sky: #0ea5e9;
    --sky-light: #e0f2fe;
    --sky-soft: #f0f9ff;
    --blue: #2563eb;
    --blue-dark: #1d4ed8;
    --green: #059669;
    --shadow: 0 4px 24px rgba(14, 165, 233, 0.10);
    --shadow-hover: 0 10px 32px rgba(14, 165, 233, 0.20);

    /* Override Gradio's own variables so dark mode can't leak in */
    --body-background-fill: #f3f9ff;
    --background-fill-primary: #ffffff;
    --background-fill-secondary: #f8fbff;
    --block-background-fill: #ffffff;
    --block-border-color: #dbeafe;
    --block-label-background-fill: #f0f9ff;
    --block-label-text-color: #334155;
    --block-title-text-color: #334155;
    --body-text-color: #0f172a;
    --body-text-color-subdued: #64748b;
    --input-background-fill: #f8fbff;
    --input-background-fill-focus: #ffffff;
    --input-border-color: #dbeafe;
    --input-border-color-focus: #0ea5e9;
    --input-placeholder-color: #94a3b8;
    --border-color-primary: #dbeafe;
    --panel-background-fill: #ffffff;
    --table-even-background-fill: #ffffff;
    --table-odd-background-fill: #f8fbff;
    --color-accent: #0ea5e9;
    --button-primary-background-fill: #0ea5e9;
    --button-primary-text-color: #ffffff;
}

body,
.gradio-container {
    background:
        radial-gradient(
            ellipse at top left,
            rgba(125, 211, 252, 0.28),
            transparent 45%
        ),
        radial-gradient(
            ellipse at bottom right,
            rgba(191, 219, 254, 0.40),
            transparent 50%
        ),
        var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', Arial, sans-serif !important;
}

.gradio-container {
    max-width: 1500px !important;
    margin: auto !important;
}

footer {
    display: none !important;
}

#app-shell {
    padding: 14px 18px 30px;
}

/* ---------- HEADER ---------- */

#top-header {
    position: relative;
    overflow: hidden;
    background:
        radial-gradient(
            circle at 85% 20%,
            rgba(255, 255, 255, 0.28),
            transparent 40%
        ),
        linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%);
    border-radius: 24px;
    padding: 32px 34px;
    margin-bottom: 22px;
    box-shadow: 0 14px 40px rgba(37, 99, 235, 0.25);
}

#top-header::after {
    content: "";
    position: absolute;
    right: -60px;
    bottom: -80px;
    width: 260px;
    height: 260px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.10);
}

.brand-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border-radius: 15px;
    background: rgba(255, 255, 255, 0.95);
    color: #0ea5e9;
    font-size: 26px;
    margin-bottom: 14px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

#top-header h1 {
    font-size: 33px;
    font-weight: 800;
    letter-spacing: -1px;
    margin: 0 0 8px;
    color: #ffffff !important;
}

#top-header h1 span {
    color: #bae6fd !important;
}

#top-header p {
    color: #e0f2fe !important;
    font-size: 14px;
    line-height: 1.8;
    margin: 0;
    max-width: 640px;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 14px;
    margin-top: 16px;
    border: 1px solid rgba(255, 255, 255, 0.45);
    background: rgba(255, 255, 255, 0.18);
    border-radius: 999px;
    color: #ffffff;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.3px;
}

.status-dot {
    width: 8px;
    height: 8px;
    background: #4ade80;
    border-radius: 50%;
    box-shadow: 0 0 0 4px rgba(74, 222, 128, 0.30);
}

/* ---------- SIDEBAR ---------- */

#sidebar {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 20px !important;
    padding: 20px !important;
    box-shadow: var(--shadow);
}

#sidebar-title {
    font-size: 19px;
    font-weight: 800;
    color: var(--blue);
    border-bottom: 1px solid var(--border);
    padding-bottom: 16px;
    margin-bottom: 14px;
}

#sidebar p,
#sidebar li,
#sidebar strong {
    color: #334155 !important;
    font-size: 13px;
    line-height: 1.9;
}

#sidebar strong {
    color: var(--blue) !important;
    font-size: 11px;
    letter-spacing: 0.8px;
}

.sidebar-note,
.info-box {
    border: 1px solid var(--border-strong);
    background: linear-gradient(135deg, #f0f9ff, #eff6ff);
    border-left: 4px solid var(--sky);
    border-radius: 13px;
    padding: 15px 16px;
    color: #475569;
    font-size: 12px;
    line-height: 1.8;
    margin-top: 16px;
}

.sidebar-note strong,
.info-box strong {
    color: var(--blue);
}

/* ---------- CARDS ---------- */

.section-card {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 20px !important;
    padding: 22px !important;
    margin-bottom: 14px;
    box-shadow: var(--shadow);
}

.section-title {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #0f172a;
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 4px;
}

.section-title .num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 28px;
    height: 28px;
    border-radius: 9px;
    background: var(--sky-light);
    color: var(--blue);
    font-size: 12px;
    font-weight: 800;
}

.section-subtitle {
    color: var(--muted);
    font-size: 12px;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px dashed var(--border);
}

/* ---------- FORM ELEMENTS ---------- */

label,
.gradio-container label,
.gradio-container label span {
    color: #334155 !important;
    font-weight: 600 !important;
    font-size: 12px !important;
}

input,
textarea,
select,
.gradio-container input,
.gradio-container textarea {
    background: var(--input) !important;
    color: var(--text) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 11px !important;
    transition: all 0.2s ease !important;
}

input:hover,
textarea:hover {
    border-color: var(--border-strong) !important;
}

input:focus,
textarea:focus {
    background: #ffffff !important;
    border-color: var(--sky) !important;
    box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.15) !important;
    outline: none !important;
}

input::placeholder,
textarea::placeholder {
    color: #94a3b8 !important;
}

textarea[disabled],
input[disabled] {
    background: #f1f5f9 !important;
    color: #475569 !important;
}

.gradio-container .block,
.gradio-container .form {
    background: transparent !important;
    border-color: transparent !important;
}

.section-card .block,
.section-card .form {
    box-shadow: none !important;
}

/* Dropdown menu */
ul.options,
.gradio-container ul.options {
    background: #ffffff !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: 12px !important;
    box-shadow: var(--shadow-hover) !important;
}

ul.options li {
    color: #0f172a !important;
}

ul.options li:hover,
ul.options li.selected,
ul.options li.active {
    background: var(--sky-light) !important;
    color: var(--blue-dark) !important;
}

/* File upload areas */
.gradio-container .file-preview,
.gradio-container [data-testid="file-upload"],
.gradio-container .upload-container {
    background: var(--sky-soft) !important;
    border: 2px dashed var(--border-strong) !important;
    border-radius: 14px !important;
    color: #334155 !important;
}

/* ---------- BUTTONS ---------- */

.gradio-container button {
    border-radius: 11px !important;
    font-weight: 700 !important;
    transition: all 0.2s ease !important;
}

.gradio-container button.primary {
    background: linear-gradient(135deg, #0ea5e9, #2563eb) !important;
    color: #ffffff !important;
    border: none !important;
    box-shadow: 0 6px 20px rgba(37, 99, 235, 0.30);
}

.gradio-container button.primary:hover {
    filter: brightness(1.08);
    transform: translateY(-2px);
    box-shadow: 0 10px 28px rgba(37, 99, 235, 0.40);
}

.gradio-container button.primary:active {
    transform: translateY(0);
}

.gradio-container button.secondary {
    background: #ffffff !important;
    color: var(--blue) !important;
    border: 1.5px solid var(--border-strong) !important;
}

.gradio-container button.secondary:hover {
    background: var(--sky-light) !important;
    border-color: var(--sky) !important;
    transform: translateY(-1px);
}

/* ---------- TABS ---------- */

.gradio-container .tab-nav,
.gradio-container div[role="tablist"] {
    background: #ffffff !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 5px !important;
    margin-bottom: 14px !important;
    box-shadow: var(--shadow);
    gap: 4px;
}

.gradio-container button[role="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    border: 1px solid transparent !important;
    border-radius: 10px !important;
    padding: 9px 16px !important;
    font-size: 13px !important;
}

.gradio-container button[role="tab"]:hover {
    color: var(--blue) !important;
    background: var(--sky-soft) !important;
}

.gradio-container button[role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #0ea5e9, #2563eb) !important;
    color: #ffffff !important;
    border-color: transparent !important;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.30);
}

.gradio-container .tabitem {
    background: transparent !important;
    border: none !important;
}

/* ---------- MARKDOWN ---------- */

.gradio-container .prose h1,
.gradio-container .md h1 {
    color: #0f172a !important;
    font-weight: 800 !important;
    font-size: 26px !important;
    letter-spacing: -0.5px;
}

.gradio-container .prose h2,
.gradio-container .md h2 {
    color: var(--blue) !important;
    font-weight: 700 !important;
    font-size: 18px !important;
}

.gradio-container .prose h3,
.gradio-container .md h3 {
    color: #0f172a !important;
    font-weight: 700 !important;
}

.gradio-container .prose p,
.gradio-container .prose li,
.gradio-container .md p,
.gradio-container .md li {
    color: #475569 !important;
    line-height: 1.8;
}

.gradio-container .prose strong,
.gradio-container .md strong {
    color: #0f172a !important;
}

/* ---------- RESUME EDITOR ---------- */

#resume-editor textarea {
    min-height: 570px !important;
    line-height: 1.7 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    background: #ffffff !important;
    border: 1.5px solid var(--border-strong) !important;
}

/* ---------- FOOTER ---------- */

#footer {
    color: var(--muted);
    text-align: center;
    font-size: 11px;
    padding: 22px 0 6px;
    letter-spacing: 0.4px;
}

#footer b {
    color: var(--blue);
}

/* ---------- SCROLLBAR ---------- */

::-webkit-scrollbar {
    width: 9px;
    height: 9px;
}

::-webkit-scrollbar-thumb {
    background: #bae6fd;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #7dd3fc;
}

/* ---------- RESPONSIVE ---------- */

@media (max-width: 768px) {
    #app-shell {
        padding: 4px;
    }

    #top-header {
        padding: 22px;
        border-radius: 18px;
    }

    #top-header h1 {
        font-size: 25px;
    }

    .section-card {
        padding: 14px !important;
    }

    .gradio-container button[role="tab"] {
        padding: 8px 10px !important;
        font-size: 12px !important;
    }
}
"""


# ============================================================
# 2. UI HELPER FUNCTIONS  (UNCHANGED)
# ============================================================

def is_error_message(value):
    """Identify common backend error messages."""

    if not isinstance(value, str):
        return False

    prefixes = (
        "Error:",
        "Resume generation failed:",
        "Word export failed:",
        "PDF export failed:",
        "ATS comparison failed:",
        "Profile extraction failed:",
    )

    return value.startswith(prefixes)


def generate_resume_ui(
    full_name,
    email,
    phone,
    location,
    target_country,
    job_title,
    company,
    skills,
    education,
    experience,
    projects,
    certifications,
    achievements,
    job_description,
    additional_profile,
):
    """Generate resume content through app.py."""

    if not full_name or not full_name.strip():
        return "", "Please enter your full name."

    if not job_title or not job_title.strip():
        return "", "Please enter your target job title."

    if not skills or not skills.strip():
        return "", "Please enter your skills."

    # Keep additional candidate information.
    extra_sections = []

    if certifications and certifications.strip():
        extra_sections.append(
            "CERTIFICATIONS PROVIDED BY USER:\n"
            + certifications.strip()
        )

    if achievements and achievements.strip():
        extra_sections.append(
            "ACHIEVEMENTS PROVIDED BY USER:\n"
            + achievements.strip()
        )

    if additional_profile and additional_profile.strip():
        extra_sections.append(
            "ADDITIONAL PROFILE INFORMATION:\n"
            + additional_profile.strip()
        )

    all_projects = (projects or "").strip()

    if extra_sections:
        all_projects += (
            "\n\n"
            + "\n\n".join(extra_sections)
        )

    data = {
        "full_name": full_name.strip(),
        "email": (email or "").strip(),
        "phone": (phone or "").strip(),
        "location": (location or "").strip(),
        "target_country": target_country or "Pakistan",
        "job_title": job_title.strip(),
        "company": (company or "").strip(),
        "skills": skills.strip(),
        "education": (education or "").strip(),
        "experience": (experience or "").strip(),
        "projects": all_projects,
        "job_description": (job_description or "").strip(),
    }

    try:
        resume = controller.create_resume(data)

        if not isinstance(resume, str):
            resume = str(resume)

        if is_error_message(resume):
            return "", resume

        return (
            resume,
            "Resume generated. Review all information before exporting.",
        )

    except Exception as exc:
        return "", f"Resume generation failed: {exc}"


def country_guidance_ui(country):
    """Show guidance for the selected country."""

    try:
        return controller.get_country_guidance(
            country or "Pakistan"
        )
    except Exception as exc:
        return f"Could not load guidance: {exc}"


def template_description_ui(template_name):
    """Show a description of the selected visual template."""

    try:
        return get_template_description(
            template_name or "Classic ATS"
        )
    except Exception as exc:
        return f"Could not load template information: {exc}"


def parse_profile_ui(uploaded_file):
    """Extract text from an uploaded PDF, DOCX, or TXT file."""

    if not uploaded_file:
        return "Please upload a PDF, DOCX, or TXT file."

    try:
        return controller.parse_uploaded_profile(uploaded_file)
    except Exception as exc:
        return f"Profile extraction failed: {exc}"


def check_ats_ui(resume_text, job_description):
    """Run the existing ATS keyword comparison."""

    if not resume_text or not resume_text.strip():
        return "Please enter or generate resume text first."

    if not job_description or not job_description.strip():
        return "Please paste a job description first."

    try:
        return controller.check_resume_ats(
            resume_text,
            job_description,
        )
    except Exception as exc:
        return f"ATS comparison failed: {exc}"


def export_docx_ui(resume_text, full_name, template_name):
    """Export DOCX using the selected visual template."""

    if not resume_text or not resume_text.strip():
        return None, "Generate or enter a resume before exporting."

    template_name = template_name or "Classic ATS"

    try:
        result = controller.download_resume_docx(
            resume_text,
            full_name or "Resume",
            template_name,
        )

        if not isinstance(result, str):
            return None, "Unexpected response from Word exporter."

        if result.startswith("Word export failed:"):
            return None, result

        return result, f"Word resume exported using {template_name}."

    except Exception as exc:
        return None, f"Word export failed: {exc}"


def export_pdf_ui(resume_text, full_name, template_name):
    """Export PDF using the selected visual template."""

    if not resume_text or not resume_text.strip():
        return None, "Generate or enter a resume before exporting."

    template_name = template_name or "Classic ATS"

    try:
        result = controller.download_resume_pdf(
            resume_text,
            full_name or "Resume",
            template_name,
        )

        if not isinstance(result, str):
            return None, "Unexpected response from PDF exporter."

        if result.startswith("PDF export failed:"):
            return None, result

        return result, f"PDF resume exported using {template_name}."

    except Exception as exc:
        return None, f"PDF export failed: {exc}"


# ============================================================
# 3. AVAILABLE OPTIONS  (UNCHANGED)
# ============================================================

COUNTRIES = controller.get_country_options()
TEMPLATES = get_supported_templates()

DEFAULT_COUNTRY = (
    "Pakistan" if "Pakistan" in COUNTRIES else COUNTRIES[0]
)

DEFAULT_TEMPLATE = (
    "Modern Professional"
    if "Modern Professional" in TEMPLATES
    else TEMPLATES[0]
)


# ============================================================
# 4. CREATE THE GRADIO APPLICATION
# ============================================================

with gr.Blocks(
    title="ResumePilot AI | Resume Builder",
    theme=gr.themes.Soft(
        primary_hue="sky",
        secondary_hue="blue",
        neutral_hue="slate",
        font=[
            gr.themes.GoogleFont("Inter"),
            "Arial",
            "sans-serif",
        ],
    ),
    css=CUSTOM_CSS,
) as demo:

    with gr.Column(elem_id="app-shell"):

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        gr.HTML(
            """
            <div id="top-header">
                <div class="brand-icon">✦</div>
                <h1>ResumePilot <span>AI</span></h1>
                <p>
                    Your career deserves a better resume.
                    Create country-specific, job-tailored resumes
                    using your local AI assistant.
                </p>
                <div class="status-pill">
                    <span class="status-dot"></span>
                    LOCAL AI · OLLAMA · PRIVATE BY DEFAULT
                </div>
            </div>
            """
        )

        with gr.Row(equal_height=False):

            # ------------------------------------------------
            # SIDEBAR
            # ------------------------------------------------

            with gr.Column(
                scale=1,
                min_width=210,
                elem_id="sidebar",
            ):

                gr.HTML(
                    """
                    <div id="sidebar-title">
                        ✦ &nbsp; ResumePilot
                    </div>
                    """
                )

                gr.Markdown(
                    """
                    **YOUR WORKSPACE**

                    Build your next resume.

                    **AVAILABLE TOOLS**

                    - Resume Builder
                    - ATS Checker
                    - Profile Import
                    - Country Guidance
                    - Visual Templates
                    """
                )

                gr.HTML(
                    """
                    <div class="sidebar-note">
                        <strong>✦ Local AI Assistant</strong>
                        <br><br>
                        Powered by your configured Ollama model.
                        No paid OpenAI API key is required.
                        <br><br>
                        <span style="color:#059669; font-weight:600;">
                            ● Local backend configured
                        </span>
                        <br><br>
                        Verify every date, qualification, and
                        achievement before applying.
                    </div>
                    """
                )

            # ------------------------------------------------
            # MAIN WORKSPACE
            # ------------------------------------------------

            with gr.Column(scale=4, min_width=300):

                with gr.Tabs():

                    # ========================================
                    # TAB 1: RESUME BUILDER
                    # ========================================

                    with gr.Tab("✦ Resume Builder"):

                        gr.Markdown(
                            """
                            # Build your resume

                            Enter your real details, choose a
                            visual template, and generate a draft.
                            """
                        )

                        # TEMPLATE SELECTOR
                        with gr.Column(
                            elem_classes=["section-card"]
                        ):

                            gr.HTML(
                                """
                                <div class="section-title">
                                    <span class="num">✦</span>
                                    Choose your resume design
                                </div>
                                <div class="section-subtitle">
                                    The selected design is applied
                                    to exported Word and PDF files.
                                </div>
                                """
                            )

                            template_selector = gr.Dropdown(
                                choices=TEMPLATES,
                                value=DEFAULT_TEMPLATE,
                                label="Visual resume template",
                                interactive=True,
                            )

                            template_description = gr.Textbox(
                                value=template_description_ui(
                                    DEFAULT_TEMPLATE
                                ),
                                label="Template description",
                                interactive=False,
                                lines=2,
                            )

                            template_selector.change(
                                fn=template_description_ui,
                                inputs=template_selector,
                                outputs=template_description,
                            )

                        with gr.Row(equal_height=False):

                            # LEFT COLUMN: FORM
                            with gr.Column(
                                scale=3,
                                elem_classes=["section-card"],
                            ):

                                gr.HTML(
                                    """
                                    <div class="section-title">
                                        <span class="num">01</span>
                                        Personal information
                                    </div>
                                    <div class="section-subtitle">
                                        Basic contact details.
                                    </div>
                                    """
                                )

                                with gr.Row():
                                    full_name = gr.Textbox(
                                        label="Full name *",
                                        placeholder="Your full name",
                                    )

                                    email = gr.Textbox(
                                        label="Email",
                                        placeholder="you@example.com",
                                    )

                                with gr.Row():
                                    phone = gr.Textbox(
                                        label="Phone number",
                                        placeholder="+92 ...",
                                    )

                                    location = gr.Textbox(
                                        label="Current location",
                                        placeholder="City, country",
                                    )

                                gr.HTML(
                                    """
                                    <div class="section-title"
                                        style="margin-top:22px">
                                        <span class="num">02</span>
                                        Target opportunity
                                    </div>
                                    <div class="section-subtitle">
                                        Tailor your content to a role.
                                    </div>
                                    """
                                )

                                with gr.Row():
                                    target_country = gr.Dropdown(
                                        choices=COUNTRIES,
                                        value=DEFAULT_COUNTRY,
                                        label="Target country",
                                    )

                                    job_title = gr.Textbox(
                                        label="Target job title *",
                                        value="Python Developer",
                                    )

                                company = gr.Textbox(
                                    label="Target company",
                                    placeholder="Company name",
                                )

                                job_description = gr.Textbox(
                                    label="Job description",
                                    placeholder=(
                                        "Paste the target job description..."
                                    ),
                                    lines=6,
                                )

                                country_guidance = gr.Textbox(
                                    label="Country-specific guidance",
                                    value=country_guidance_ui(
                                        DEFAULT_COUNTRY
                                    ),
                                    lines=4,
                                    interactive=False,
                                )

                                target_country.change(
                                    fn=country_guidance_ui,
                                    inputs=target_country,
                                    outputs=country_guidance,
                                )

                                gr.HTML(
                                    """
                                    <div class="section-title"
                                        style="margin-top:22px">
                                        <span class="num">03</span>
                                        Qualifications
                                    </div>
                                    <div class="section-subtitle">
                                        Include only information that
                                        accurately describes you.
                                    </div>
                                    """
                                )

                                skills = gr.Textbox(
                                    label="Skills *",
                                    placeholder=(
                                        "Python, SQL, NumPy, Pandas, Git..."
                                    ),
                                    lines=3,
                                )

                                education = gr.Textbox(
                                    label="Education",
                                    placeholder=(
                                        "Degree, institution, dates, "
                                        "relevant coursework"
                                    ),
                                    lines=3,
                                )

                                experience = gr.Textbox(
                                    label="Work experience",
                                    placeholder=(
                                        "Role, company, dates, "
                                        "responsibilities, achievements"
                                    ),
                                    lines=4,
                                )

                                projects = gr.Textbox(
                                    label="Projects",
                                    placeholder=(
                                        "Project name, technologies, "
                                        "and actual contributions"
                                    ),
                                    lines=4,
                                )

                                with gr.Row():
                                    certifications = gr.Textbox(
                                        label="Certifications",
                                        placeholder="Your certifications",
                                        lines=3,
                                    )

                                    achievements = gr.Textbox(
                                        label="Achievements",
                                        placeholder="Verified achievements",
                                        lines=3,
                                    )

                                additional_profile = gr.Textbox(
                                    label="Additional profile details",
                                    placeholder=(
                                        "Optional: paste details from "
                                        "your own profile or export."
                                    ),
                                    lines=3,
                                )

                                gr.HTML(
                                    """
                                    <div class="info-box">
                                        <strong>Before generating</strong>
                                        <br>
                                        Review all AI-generated claims.
                                        Never submit invented qualifications
                                        or achievements to an employer.
                                    </div>
                                    """
                                )

                                generate_button = gr.Button(
                                    "✦ Generate my resume",
                                    variant="primary",
                                    size="lg",
                                )

                                generation_status = gr.Textbox(
                                    label="Generation status",
                                    interactive=False,
                                )

                            # RIGHT COLUMN: EDITOR + EXPORT
                            with gr.Column(
                                scale=2,
                                elem_classes=["section-card"],
                            ):

                                gr.HTML(
                                    """
                                    <div class="section-title">
                                        <span class="num">✎</span>
                                        Resume workspace
                                    </div>
                                    <div class="section-subtitle">
                                        Edit your generated content before
                                        exporting the selected design.
                                    </div>
                                    """
                                )

                                resume_output = gr.Textbox(
                                    label="Editable resume text",
                                    placeholder=(
                                        "Your AI-generated resume "
                                        "will appear here..."
                                    ),
                                    lines=25,
                                    elem_id="resume-editor",
                                )

                                gr.Markdown("### Export your resume")

                                export_word_button = gr.Button(
                                    "⇩ Download Word (.docx)",
                                    variant="secondary",
                                )

                                word_file = gr.File(
                                    label="Word document download",
                                )

                                export_pdf_button = gr.Button(
                                    "⇩ Download PDF (.pdf)",
                                    variant="primary",
                                )

                                pdf_file = gr.File(
                                    label="PDF document download",
                                )

                                export_status = gr.Textbox(
                                    label="Export status",
                                    interactive=False,
                                )

                        # ------------------------------------
                        # GENERATE RESUME EVENT
                        # ------------------------------------

                        generate_button.click(
                            fn=generate_resume_ui,
                            inputs=[
                                full_name,
                                email,
                                phone,
                                location,
                                target_country,
                                job_title,
                                company,
                                skills,
                                education,
                                experience,
                                projects,
                                certifications,
                                achievements,
                                job_description,
                                additional_profile,
                            ],
                            outputs=[
                                resume_output,
                                generation_status,
                            ],
                        )

                        # ------------------------------------
                        # EXPORT DOCX WITH SELECTED TEMPLATE
                        # ------------------------------------

                        export_word_button.click(
                            fn=export_docx_ui,
                            inputs=[
                                resume_output,
                                full_name,
                                template_selector,
                            ],
                            outputs=[
                                word_file,
                                export_status,
                            ],
                        )

                        # ------------------------------------
                        # EXPORT PDF WITH SELECTED TEMPLATE
                        # ------------------------------------

                        export_pdf_button.click(
                            fn=export_pdf_ui,
                            inputs=[
                                resume_output,
                                full_name,
                                template_selector,
                            ],
                            outputs=[
                                pdf_file,
                                export_status,
                            ],
                        )

                    # ========================================
                    # TAB 2: ATS CHECKER
                    # ========================================

                    with gr.Tab("◎ ATS Checker"):

                        gr.Markdown(
                            """
                            # ATS keyword analysis

                            Compare a resume with a job description
                            to identify relevant keywords.
                            """
                        )

                        with gr.Row():

                            with gr.Column(
                                elem_classes=["section-card"]
                            ):
                                ats_resume = gr.Textbox(
                                    label="Resume text",
                                    placeholder="Paste your resume...",
                                    lines=15,
                                )

                            with gr.Column(
                                elem_classes=["section-card"]
                            ):
                                ats_job_description = gr.Textbox(
                                    label="Job description",
                                    placeholder=(
                                        "Paste the target job description..."
                                    ),
                                    lines=15,
                                )

                        ats_button = gr.Button(
                            "◎ Analyze keyword match",
                            variant="primary",
                        )

                        ats_report = gr.Textbox(
                            label="ATS report",
                            lines=15,
                            interactive=False,
                        )

                        ats_button.click(
                            fn=check_ats_ui,
                            inputs=[
                                ats_resume,
                                ats_job_description,
                            ],
                            outputs=ats_report,
                        )

                        gr.HTML(
                            """
                            <div class="info-box">
                                This is a basic keyword comparison,
                                not an official ATS score or a guarantee
                                of getting an interview.
                            </div>
                            """
                        )

                    # ========================================
                    # TAB 3: PROFILE IMPORT
                    # ========================================

                    with gr.Tab("⇧ Profile Import"):

                        gr.Markdown(
                            """
                            # Import an existing resume

                            Extract text from PDF, DOCX, and TXT files.
                            """
                        )

                        with gr.Column(
                            elem_classes=["section-card"]
                        ):

                            profile_file = gr.File(
                                label="Upload your resume",
                                file_types=[
                                    ".pdf",
                                    ".docx",
                                    ".txt",
                                ],
                                type="filepath",
                            )

                            parse_button = gr.Button(
                                "⇧ Extract profile text",
                                variant="primary",
                            )

                            parsed_profile = gr.Textbox(
                                label="Extracted profile text",
                                lines=20,
                                placeholder=(
                                    "Extracted text appears here..."
                                ),
                            )

                            parse_button.click(
                                fn=parse_profile_ui,
                                inputs=profile_file,
                                outputs=parsed_profile,
                            )

                        gr.HTML(
                            """
                            <div class="info-box">
                                Scanned PDFs may need OCR. Imported
                                text is not automatically verified or
                                inserted into all resume fields.
                            </div>
                            """
                        )

                    # ========================================
                    # TAB 4: ABOUT
                    # ========================================

                    with gr.Tab("ⓘ About"):

                        gr.Markdown(
                            """
                            # About ResumePilot AI

                            A resume generation prototype powered
                            by a locally running Ollama model.

                            ## Features

                            - Local AI resume generation
                            - Country-specific resume guidance
                            - Job and company tailoring
                            - Three selectable visual templates
                            - PDF and DOCX export with selected styling
                            - Editable resume text
                            - Basic ATS keyword comparison
                            - PDF, DOCX, and TXT profile extraction

                            ## Visual templates

                            **Classic ATS:** Minimal black-and-white style.

                            **Modern Professional:** Purple accents and
                            contemporary headings.

                            **Executive:** Teal accents and centered name.

                            ## Current limitations

                            - No login or registration.
                            - No database-backed resume storage.
                            - No direct LinkedIn scraping.
                            - No OCR for scanned PDFs.
                            - No automatic job applications.
                            - ATS keyword matching is not a full ATS simulation.

                            ## Privacy

                            This interface is configured for a local
                            Ollama backend. Check your backend settings
                            before entering sensitive information.
                            """
                        )

        # ----------------------------------------------------
        # FOOTER
        # ----------------------------------------------------

        gr.HTML(
            """
            <div id="footer">
                <b>RESUMEPILOT AI</b> · GRADIO + LOCAL OLLAMA
                <br><br>
                Your information. Your resume. Your career.
            </div>
            """
        )


# ============================================================
# 5. LAUNCH APPLICATION
# ============================================================

if __name__ == "__main__":
    demo.queue().launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
    )