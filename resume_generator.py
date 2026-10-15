
# ==========================================================
# FILE: resume_generator.py
# PURPOSE: Generate country-specific, company-tailored resumes
# ==========================================================

from ollama_client import ask_ollama


def generate_resume(
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
    job_description
):
    """
    Generate a resume using the user's information
    and target job description.
    """

    # Check the essential fields
    if not full_name.strip():
        return "Error: Please enter your full name."

    if not job_title.strip():
        return "Error: Please enter the target job title."

    if not skills.strip():
        return "Error: Please enter your skills."

    # Build a detailed instruction for the AI
    prompt = f"""
You are a professional resume writer and ATS resume specialist.

Create a professional, ATS-friendly resume using ONLY
the information provided below.

CANDIDATE INFORMATION
Name: {full_name}
Email: {email}
Phone: {phone}
Current Location: {location}

TARGET JOB
Target Country: {target_country}
Job Title: {job_title}
Company: {company}

SKILLS
{skills}

EDUCATION
{education}

WORK EXPERIENCE
{experience}

PROJECTS
{projects}

JOB DESCRIPTION
{job_description}

INSTRUCTIONS

1. Write a professional resume tailored to the target job.
2. Use the target country's usual resume conventions.
3. Match relevant skills and keywords from the job description.
4. Write a concise professional summary.
5. Organize sections with clear headings.
6. Improve the wording of experience and project descriptions
   without changing their meaning.
7. Use plain text formatting suitable for ATS software.
8. Do not invent qualifications, employers, degrees, dates,
   certifications, achievements, or experience.
9. If information is missing, omit that detail instead of
   making it up.
10. Do not claim that the resume guarantees an interview
    or passes every ATS system.
11. Return the resume only, with clear section headings.

Generate the resume now.
"""

    # Send the resume instructions to our local AI
    result = ask_ollama(prompt)

    # Return the generated resume
    return result
