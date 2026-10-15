
from profile_parser import extract_profile_text

# Read the sample resume from our project folder
file_path = "sample_resume.txt"

# Extract the resume text
result = extract_profile_text(file_path)

# Display the result
print(result)