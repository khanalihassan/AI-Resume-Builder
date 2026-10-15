# Import the resume generator
from resume_generator import generate_resume

# Sample candidate information for testing
resume = generate_resume(
    full_name="Ali Hassan",
    email="ali@example.com",
    phone="03001234567",
    location="Lahore, Pakistan",
    target_country="Pakistan",
    job_title="Python Developer",
    company="Example Software Company",
    skills="Python, NumPy, Pandas, SQL, Git",
    education="BS Computer Science",
    experience="Beginner Python developer; personal coding practice",
    projects="Student Management System using Python",
    job_description=(
        "Looking for a Python developer with Python fundamentals, "
        "problem-solving skills, SQL knowledge, and Git experience."
    )
)

# Print the generated resume
print(resume)