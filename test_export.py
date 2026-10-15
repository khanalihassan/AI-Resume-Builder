
from export_resume import export_to_docx, export_to_pdf

# Sample resume text
sample_resume = """
## Professional Summary
Python developer learning AI and machine learning.

## Skills
- Python
- NumPy
- Pandas
- SQL

## Education
- BS Computer Science

## Projects
- Student Management System using Python
"""

# Export the resume to Word and PDF
word_file = export_to_docx(
    sample_resume,
    "Ali Hassan"
)

pdf_file = export_to_pdf(
    sample_resume,
    "Ali Hassan"
)

# Show the generated file locations
print("Word file created:", word_file)
print("PDF file created:", pdf_file)
