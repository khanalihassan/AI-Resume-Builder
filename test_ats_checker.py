
# Import the ATS report function
from ats_checker import format_ats_report

# Sample resume
resume = """
Python Developer
Skills: Python, SQL, Git, NumPy, Pandas
Projects: Student Management System using Python
"""

# Sample job description
job_description = """
We need a Python Developer with Python, SQL, Git,
FastAPI, REST API, Docker, and problem-solving skills.
"""

# Generate and print the keyword report
report = format_ats_report(resume, job_description)

print(report)
