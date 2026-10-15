# ============================================================
# FILE: app.py
# PROJECT: AI Resume Builder
# PURPOSE: Main application controller
# AI: Local Ollama
# ============================================================

from pathlib import Path

from ollama_client import ask_ollama
from resume_generator import generate_resume
from resume_templates import (
    get_country_rules,
    get_supported_countries,
    get_supported_templates,
    get_template_style,
    get_template_description,
)
from export_resume import (
    export_to_docx,
    export_to_pdf,
)
from ats_checker import (
    check_ats_match,
    format_ats_report,
)
from profile_parser import extract_profile_text


# ============================================================
# 1. PROJECT SETTINGS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = BASE_DIR / "generated_resumes"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

AI_PROVIDER = "Local Ollama"
AI_MODEL = "qwen2.5:0.5b"


# ============================================================
# 2. INPUT CLEANING
# ============================================================

def clean_input(value):
    """Convert an input value to clean text."""

    if value is None:
        return ""

    return str(value).strip()


# ============================================================
# 3. VALIDATE RESUME INFORMATION
# ============================================================

def validate_resume_data(data):
    """Validate the minimum information needed to generate a resume."""

    if not isinstance(data, dict):
        return False, "Resume data must be provided as a dictionary."

    required_fields = {
        "full_name": "Full name",
        "job_title": "Target job title",
        "skills": "Skills",
    }

    for field, label in required_fields.items():
        if not clean_input(data.get(field)):
            return False, f"{label} is required."

    return True, "Input validation successful."


# ============================================================
# 4. GENERATE RESUME
# ============================================================

def create_resume(data):
    """
    Generate resume content using the local AI model.

    The visual template is applied when exporting the resume.
    """

    valid, message = validate_resume_data(data)

    if not valid:
        return f"Error: {message}"

    try:
        full_name = clean_input(data.get("full_name"))
        email = clean_input(data.get("email"))
        phone = clean_input(data.get("phone"))
        location = clean_input(data.get("location"))
        target_country = clean_input(
            data.get("target_country")
        ) or "Pakistan"

        job_title = clean_input(data.get("job_title"))
        company = clean_input(data.get("company"))
        skills = clean_input(data.get("skills"))
        education = clean_input(data.get("education"))
        experience = clean_input(data.get("experience"))
        projects = clean_input(data.get("projects"))
        job_description = clean_input(
            data.get("job_description")
        )

        # Get the country-specific resume guidance.
        country_guidance = get_country_rules(target_country)

        # Combine the country guidance with the job description.
        tailored_job_description = (
            f"Target country: {target_country}\n\n"
            f"Country-specific resume guidance:\n"
            f"{country_guidance}\n\n"
            f"Target company: {company or 'Not specified'}\n\n"
            f"Original job description:\n"
            f"{job_description or 'Not provided'}"
        )

        # Call the existing resume generator.
        resume_text = generate_resume(
            full_name=full_name,
            email=email,
            phone=phone,
            location=location,
            target_country=target_country,
            job_title=job_title,
            company=company,
            skills=skills,
            education=education,
            experience=experience,
            projects=projects,
            job_description=tailored_job_description,
        )

        if not isinstance(resume_text, str):
            resume_text = str(resume_text)

        return resume_text

    except Exception as exc:
        return f"Resume generation failed: {exc}"


# ============================================================
# 5. COUNTRY OPTIONS AND GUIDANCE
# ============================================================

def get_country_options():
    """Return supported countries."""

    return get_supported_countries()


def get_country_guidance(country):
    """Return guidance for the selected country."""

    try:
        return str(get_country_rules(country))
    except Exception as exc:
        return f"Could not load country guidance: {exc}"


# ============================================================
# 6. VISUAL TEMPLATE OPTIONS
# ============================================================

def get_template_options():
    """Return the available visual resume templates."""

    return get_supported_templates()


def get_template_information(template_name):
    """Return information about a selected template."""

    return get_template_description(template_name)


def get_template_settings(template_name):
    """Return the style settings for a selected template."""

    return get_template_style(template_name)


# ============================================================
# 7. ATS KEYWORD CHECKER
# ============================================================

def check_resume_ats(resume_text, job_description):
    """Compare resume keywords with the job description."""

    if not clean_input(resume_text):
        return "Please provide resume text."

    if not clean_input(job_description):
        return "Please provide a job description."

    try:
        report = check_ats_match(
            resume_text,
            job_description,
        )

        # Some implementations return a formatted report already.
        if isinstance(report, str):
            return report

        # Otherwise use the report formatter.
        return format_ats_report(report)

    except Exception as exc:
        return f"ATS comparison failed: {exc}"


# ============================================================
# 8. IMPORT EXISTING PROFILE
# ============================================================

def parse_uploaded_profile(file_path):
    """Extract text from a PDF, DOCX, or TXT profile."""

    if not file_path:
        return "Please select a file first."

    try:
        # Gradio may pass a file path or a file-like object.
        if hasattr(file_path, "name"):
            file_path = file_path.name

        return extract_profile_text(str(file_path))

    except Exception as exc:
        return f"Profile extraction failed: {exc}"


# ============================================================
# 9. EXPORT WORD RESUME WITH SELECTED TEMPLATE
# ============================================================

def download_resume_docx(
    resume_text,
    name,
    template_name="Classic ATS",
):
    """
    Export the resume as DOCX using the chosen visual template.

    Example:
        download_resume_docx(
            resume_text,
            "Alex Morgan",
            "Modern Professional"
        )
    """

    if not clean_input(resume_text):
        return "Word export failed: Resume text is empty."

    try:
        template_name = clean_input(template_name) or "Classic ATS"

        if template_name not in get_supported_templates():
            template_name = "Classic ATS"

        file_path = export_to_docx(
            resume_text=resume_text,
            full_name=clean_input(name) or "Resume",
            template_name=template_name,
        )

        return str(file_path)

    except Exception as exc:
        return f"Word export failed: {exc}"


# ============================================================
# 10. EXPORT PDF RESUME WITH SELECTED TEMPLATE
# ============================================================

def download_resume_pdf(
    resume_text,
    name,
    template_name="Classic ATS",
):
    """
    Export the resume as PDF using the chosen visual template.

    Example:
        download_resume_pdf(
            resume_text,
            "Alex Morgan",
            "Executive"
        )
    """

    if not clean_input(resume_text):
        return "PDF export failed: Resume text is empty."

    try:
        template_name = clean_input(template_name) or "Classic ATS"

        if template_name not in get_supported_templates():
            template_name = "Classic ATS"

        file_path = export_to_pdf(
            resume_text=resume_text,
            full_name=clean_input(name) or "Resume",
            template_name=template_name,
        )

        return str(file_path)

    except Exception as exc:
        return f"PDF export failed: {exc}"


# ============================================================
# 11. EXPORT BOTH FORMATS
# ============================================================

def export_resume_files(
    resume_text,
    name,
    template_name="Classic ATS",
):
    """Export PDF and DOCX using the same selected template."""

    docx_result = download_resume_docx(
        resume_text,
        name,
        template_name,
    )

    pdf_result = download_resume_pdf(
        resume_text,
        name,
        template_name,
    )

    return {
        "template": template_name,
        "docx": docx_result,
        "pdf": pdf_result,
    }


# ============================================================
# 12. APPLICATION STATUS
# ============================================================

def get_app_status():
    """Return the basic application configuration."""

    return {
        "provider": AI_PROVIDER,
        "model": AI_MODEL,
        "output_folder": str(OUTPUT_DIR),
        "countries": get_country_options(),
        "templates": get_template_options(),
    }


# ============================================================
# 13. TEST CONTROLLER
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("AI Resume Builder - Application Controller")
    print("=" * 60)

    status = get_app_status()

    print(f"AI Provider: {status['provider']}")
    print(f"AI Model: {status['model']}")
    print(f"Output folder: {status['output_folder']}")

    print("\nSupported countries:")
    for country in status["countries"]:
        print(f"- {country}")

    print("\nAvailable visual templates:")
    for template in status["templates"]:
        print(f"- {template}: {get_template_information(template)}")

    print("\nAvailable functions:")
    print("- create_resume(data)")
    print("- get_country_options()")
    print("- get_country_guidance(country)")
    print("- get_template_options()")
    print("- get_template_information(template_name)")
    print("- check_resume_ats(resume, job_description)")
    print("- parse_uploaded_profile(file_path)")
    print("- download_resume_docx(resume, name, template_name)")
    print("- download_resume_pdf(resume, name, template_name)")
    print("- export_resume_files(resume, name, template_name)")
    print("- get_app_status()")

    print("\nApplication controller loaded successfully.")
    print("Next: connect the template selector in gui.py.")

