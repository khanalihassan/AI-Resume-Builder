
# ==========================================================
# FILE: ats_checker.py
# PURPOSE: Compare resume keywords with job requirements
# ==========================================================

import re


def extract_keywords(text):
    """
    Extract useful words and technical terms from text.
    """

    if not text or not text.strip():
        return set()

    # Convert text to lowercase
    text = text.lower()

    # Extract words and common technical terms
    words = re.findall(
        r"[a-zA-Z][a-zA-Z0-9+#.]*",
        text
    )

    # Common words that do not describe job skills
    stop_words = {
        "the", "and", "for", "with", "from", "that",
        "this", "are", "was", "were", "will", "you",
        "your", "our", "their", "have", "has", "had",
        "job", "work", "working", "ability", "strong",
        "good", "using", "use", "years", "year",
        "required", "requirements", "candidate"
    }

    # Keep meaningful words
    keywords = {
        word for word in words
        if word not in stop_words and len(word) > 1
    }

    return keywords


def check_ats_match(resume_text, job_description):
    """
    Compare resume text against the job description.
    Return matching keywords and missing keywords.
    """

    # Validate the input
    if not resume_text or not resume_text.strip():
        return {
            "match_percentage": 0,
            "matched_keywords": [],
            "missing_keywords": [],
            "message": "Please provide resume text."
        }

    if not job_description or not job_description.strip():
        return {
            "match_percentage": 0,
            "matched_keywords": [],
            "missing_keywords": [],
            "message": "Please provide a job description."
        }

    # Extract keywords from both texts
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_description)

    # Avoid division by zero
    if not job_keywords:
        return {
            "match_percentage": 0,
            "matched_keywords": [],
            "missing_keywords": [],
            "message": "No useful job keywords were found."
        }

    # Compare the two keyword sets
    matched = resume_keywords.intersection(job_keywords)
    missing = job_keywords.difference(resume_keywords)

    # Calculate the keyword coverage percentage
    percentage = round(
        len(matched) / len(job_keywords) * 100,
        2
    )

    # Return the report
    return {
        "match_percentage": percentage,
        "matched_keywords": sorted(matched),
        "missing_keywords": sorted(missing),
        "message": (
            "Keyword comparison completed. "
            "Review missing keywords and add them only "
            "when they accurately describe your experience."
        )
    }


def format_ats_report(resume_text, job_description):
    """
    Convert the ATS comparison into a readable report.
    """

    report = check_ats_match(resume_text, job_description)

    # Show errors if required input is missing
    if report["message"].startswith("Please") or \
       report["message"].startswith("No useful"):
        return report["message"]

    # Build the report text
    output = [
        "ATS KEYWORD MATCH REPORT",
        "=" * 30,
        f"Keyword coverage: {report['match_percentage']}%",
        "",
        "MATCHED KEYWORDS:"
    ]

    output.extend(
        f"- {word}" for word in report["matched_keywords"]
    )

    output.extend(["", "MISSING KEYWORDS:"])

    output.extend(
        f"- {word}" for word in report["missing_keywords"]
    )

    output.extend([
        "",
        report["message"],
        "",
        "Note: This is a basic keyword comparison, not an",
        "official ATS score or a guarantee of selection."
    ])

    return "\n".join(output)
