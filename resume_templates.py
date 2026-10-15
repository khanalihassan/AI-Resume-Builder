
# ============================================================
# FILE: resume_templates.py
# Country-specific rules + 6 visual resume styles
# ============================================================

COUNTRY_RULES = {
    "USA": """
Use a US-style resume.
Usually 1-2 pages.
Do not include a photograph, date of birth,
marital status, or nationality unless specifically required.
Use concise achievement-focused bullet points.
""",
    "UK": """
Use a UK-style CV.
Usually 1-2 pages for most professional roles.
Focus on skills, experience and measurable achievements.
A photograph is generally unnecessary.
""",
    "Canada": """
Use a Canadian-style resume.
Usually 1-2 pages.
Avoid photographs, age, marital status and other
unnecessary personal information.
Use clear sections and achievement-focused bullets.
""",
    "Australia": """
Use an Australian-style resume.
Usually 2-3 pages depending on experience and industry.
Include relevant qualifications and professional experience.
A photograph is generally unnecessary.
""",
    "Germany": """
Use a German-style CV.
Include clear education and employment dates.
A professional photograph may be used but is optional.
Avoid inventing personal details or qualifications.
""",
    "Pakistan": """
Use a professional Pakistani CV.
Include contact details, education, skills and experience.
Keep the layout clear and appropriate for the target job.
Only include a photograph or personal details if appropriate.
""",
    "UAE": """
Use a UAE-style CV suitable for the target role.
Include relevant qualifications, skills and experience.
Nationality, visa status and photograph should only be
included when relevant or requested by the employer.
""",
}


def get_supported_countries():
    """Return all supported countries."""
    return list(COUNTRY_RULES.keys())


def get_country_rules(country):
    """Return country-specific resume guidance."""
    return COUNTRY_RULES.get(
        country,
        "Use a clean, professional and ATS-friendly resume."
    )


# ------------------------------------------------------------
# VISUAL RESUME STYLES
# ------------------------------------------------------------

TEMPLATE_STYLES = {
    "Classic ATS": {
        "description": "Simple one-column, black-and-white ATS-friendly resume.",
        "primary": "#222222",
        "heading": "#222222",
        "body": "#222222",
        "font": "Arial",
        "header_alignment": "left",
        "divider": False,
        "layout": "single",
        "sidebar_text": "#FFFFFF",
    },

    "Modern Professional": {
        "description": "Modern two-column design with purple accents.",
        "primary": "#6D4AFF",
        "heading": "#243B64",
        "body": "#283449",
        "font": "Calibri",
        "header_alignment": "left",
        "divider": True,
        "layout": "two_column",
        "sidebar_text": "#FFFFFF",
    },

    "Executive": {
        "description": "Elegant two-column executive design with teal accents.",
        "primary": "#147D92",
        "heading": "#12304A",
        "body": "#263746",
        "font": "Georgia",
        "header_alignment": "center",
        "divider": True,
        "layout": "two_column",
        "sidebar_text": "#FFFFFF",
    },

    "Emerald Modern": {
        "description": "Emerald-green sidebar with a fresh professional layout.",
        "primary": "#176B52",
        "heading": "#176B52",
        "body": "#26352F",
        "font": "Arial",
        "header_alignment": "left",
        "divider": True,
        "layout": "two_column",
        "sidebar_text": "#FFFFFF",
    },

    "Minimal Elegant": {
        "description": "Minimal charcoal design with refined typography.",
        "primary": "#374151",
        "heading": "#222222",
        "body": "#3F4650",
        "font": "Georgia",
        "header_alignment": "left",
        "divider": True,
        "layout": "two_column",
        "sidebar_text": "#FFFFFF",
    },

    "Corporate Blue": {
        "description": "Corporate navy sidebar with blue accents.",
        "primary": "#174A7E",
        "heading": "#174A7E",
        "body": "#26384A",
        "font": "Calibri",
        "header_alignment": "left",
        "divider": True,
        "layout": "two_column",
        "sidebar_text": "#FFFFFF",
    },
}


def get_supported_templates():
    """Return the available visual resume templates."""
    return list(TEMPLATE_STYLES.keys())


def get_template_style(template_name):
    """Return the settings for the selected template."""
    return TEMPLATE_STYLES.get(
        template_name,
        TEMPLATE_STYLES["Classic ATS"]
    )


def get_template_description(template_name):
    """Return a short description of a template."""
    return get_template_style(template_name)["description"]
