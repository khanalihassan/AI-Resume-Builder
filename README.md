# AI Resume Builder Pro 🚀

An AI-powered resume builder built with Python, Gradio, and Ollama. Create professional resumes, check ATS keyword compatibility, import existing resumes, and export your resume as PDF or DOCX.

## ✨ Features

- **AI Resume Generation:** Generate resume content using a locally running Ollama model.
- **Multiple Resume Templates:** Choose from six resume templates.
- **ATS Checker:** Compare your resume against job description keywords.
- **Profile Import:** Import existing resumes from PDF, DOCX, or TXT files.
- **PDF & DOCX Export:** Export resumes in commonly used document formats.
- **Modern Web Interface:** User-friendly interface built with Gradio.
- **Local AI Support:** Uses Ollama, avoiding a paid OpenAI API dependency.

## 🛠️ Tech Stack

- Python
- Gradio
- Ollama
- Qwen 2.5 (0.5B)
- python-docx
- ReportLab
- PyPDF

## 📋 Requirements

- Python 3.10 or later
- [Ollama](https://ollama.com/)
- Git (optional, for cloning the repository)

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/khanalihassan/AI-Resume-Builder.git
cd AI-Resume-Builder
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Install and start Ollama

Install Ollama from [ollama.com](https://ollama.com/).

Download the model:

```bash
ollama pull qwen2.5:0.5b
```

Make sure Ollama is running locally.

### 5. Run the application

```bash
python app.py
```

If your project uses `gui.py` as the main entry point instead, run:

```bash
python gui.py
```

Open the local URL shown in the terminal if the application does not open automatically.

## 📁 Project Structure

```text
AI-Resume-Builder/
├── app.py
├── gui.py
├── ollama_client.py
├── resume_generator.py
├── resume_templates.py
├── export_resume.py
├── ats_checker.py
├── profile_parser.py
├── test_ats_checker.py
├── test_export.py
├── test_ollama.py
├── test_profile_parser.py
├── test_resume_generator.py
├── test_templates.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🧪 Testing

Run the tests with Python's unittest framework if the test files are compatible with it:

```bash
python -m unittest discover -v
```

## 🔒 Privacy

The application is designed to use a local Ollama model for AI generation. Resume files may contain personal information, so avoid uploading real resumes, private data, API keys, or environment files to a public repository.

## 🎯 Project Goal

The goal of this project is to make professional resume creation easier through AI-assisted writing, ATS keyword checking, multiple templates, and convenient document exports.

## 👨‍💻 Author

**Ali Hassan**

GitHub: [@khanalihassan](https://github.com/khanalihassan)

---

⭐ If you find this project useful, consider giving the repository a star!
