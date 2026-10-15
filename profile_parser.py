
# ==========================================================
# FILE: profile_parser.py
# PURPOSE: Extract text from uploaded PDF, DOCX, or TXT files
# ==========================================================

from pathlib import Path
from pypdf import PdfReader
from docx import Document


def extract_pdf_text(file_path):
    """Extract selectable text from a PDF file."""

    reader = PdfReader(file_path)
    pages_text = []

    for page in reader.pages:
        # Extract text from each PDF page
        text = page.extract_text()

        if text:
            pages_text.append(text)

    return "\n".join(pages_text).strip()


def extract_docx_text(file_path):
    """Extract text from a Word document."""

    document = Document(file_path)

    # Read normal paragraphs
    lines = [
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    # Also extract text from tables
    for table in document.tables:
        for row in table.rows:
            cells = [
                cell.text.strip()
                for cell in row.cells
                if cell.text.strip()
            ]

            if cells:
                lines.append(" | ".join(cells))

    return "\n".join(lines).strip()


def extract_txt_text(file_path):
    """Read text from a TXT file."""

    # utf-8-sig handles common UTF-8 text files
    with open(
        file_path,
        "r",
        encoding="utf-8-sig"
    ) as file:
        return file.read().strip()


def extract_profile_text(file_path):
    """
    Detect the file type and extract its text.
    Supported: PDF, DOCX, TXT.
    """

    if not file_path:
        return "Error: Please provide a file path."

    path = Path(file_path)

    # Check whether the file exists
    if not path.exists() or not path.is_file():
        return "Error: The specified file was not found."

    extension = path.suffix.lower()

    try:
        if extension == ".pdf":
            text = extract_pdf_text(str(path))

        elif extension == ".docx":
            text = extract_docx_text(str(path))

        elif extension == ".txt":
            text = extract_txt_text(str(path))

        else:
            return (
                "Unsupported file type. "
                "Please upload a PDF, DOCX, or TXT file."
            )

        if not text:
            return (
                "No readable text found. The PDF may be scanned; "
                "OCR may be needed to read its images."
            )

        return text

    except Exception as error:
        return f"Could not read the file: {error}"
