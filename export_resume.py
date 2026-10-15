
# ============================================================
# AI RESUME BUILDER
# Complete PDF and DOCX Export System
# Features:
# 1. Six Resume Templates
# 2. Markdown Cleanup (##, **, etc.)
# 3. PDF Export
# 4. Word DOCX Export
# 5. Separate Filename for Each Template
# ============================================================

import re
from pathlib import Path
from xml.sax.saxutils import escape

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
)

from resume_templates import (
    get_supported_templates,
    get_template_style,
)


# ============================================================
# OUTPUT FOLDER
# ============================================================

OUTPUT_DIR = Path(__file__).resolve().parent / "generated_resumes"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# TEMPLATE COLORS AND SETTINGS
# ============================================================

DEFAULT_STYLE = {
    "layout": "single",
    "primary": "#222222",
    "font": "Arial",
}

SECTION_NAMES = {
    "professional summary": "Professional Summary",
    "summary": "Professional Summary",
    "career summary": "Professional Summary",
    "objective": "Career Objective",
    "career objective": "Career Objective",
    "work experience": "Work Experience",
    "professional experience": "Work Experience",
    "experience": "Work Experience",
    "employment history": "Work Experience",
    "education": "Education",
    "academic background": "Education",
    "skills": "Skills",
    "technical skills": "Technical Skills",
    "core skills": "Core Skills",
    "key skills": "Key Skills",
    "projects": "Projects",
    "personal projects": "Projects",
    "certifications": "Certifications",
    "certificates": "Certifications",
    "languages": "Languages",
    "achievements": "Achievements",
    "awards": "Awards",
    "interests": "Interests",
    "publications": "Publications",
    "references": "References",
}

SIDEBAR_SECTIONS = {
    "skills",
    "technical skills",
    "core skills",
    "key skills",
    "education",
    "certifications",
    "languages",
    "interests",
    "achievements",
    "awards",
}


# ============================================================
# FILE NAME HELPERS
# ============================================================

def safe_filename(name):
    """Make a string safe for use in a filename."""
    name = str(name or "Resume")
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "", name)
    name = re.sub(r"\s+", "_", name.strip())
    return name or "Resume"


def safe_template_filename(template_name):
    """Convert a template name to a filename-safe string."""
    return safe_filename(template_name).replace("_", "-")


def output_path_for(full_name, template_name, extension):
    """Create a separate output path for each template."""
    person = safe_filename(full_name)
    template = safe_template_filename(template_name)

    filename = f"{person}_{template}_Resume.{extension}"
    return OUTPUT_DIR / filename


# ============================================================
# MARKDOWN CLEANUP
# ============================================================

def clean_markdown(text):
    """
    Remove common Markdown syntax produced by an AI model.

    Examples:
        ## PROFESSIONAL SUMMARY -> PROFESSIONAL SUMMARY
        **Python** -> Python
        *Python* -> Python
        - Skill -> Skill
        ```python -> removed
    """
    text = str(text or "")

    # Remove Markdown heading symbols at the start of a line.
    text = re.sub(r"(?m)^\s{0,3}#{1,6}\s*", "", text)

    # Remove code-fence markers.
    text = re.sub(
        r"(?m)^\s*```[^\n]*$",
        "",
        text,
    )

    # Remove bold and italic markers while preserving their text.
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"__(.*?)__", r"\1", text)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"\1", text)
    text = re.sub(r"(?<!_)_([^_\n]+)_(?!_)", r"\1", text)

    # Remove inline code markers.
    text = re.sub(r"`([^`\n]+)`", r"\1", text)

    # Remove Markdown link syntax but keep the link label.
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)

    # Remove horizontal Markdown separators.
    text = re.sub(r"(?m)^\s*[-*_]{3,}\s*$", "", text)

    return text.strip()


def get_resume_lines(resume_text):
    """Clean resume text and return non-empty lines."""
    cleaned = clean_markdown(resume_text)

    return [
        line.strip()
        for line in cleaned.splitlines()
        if line.strip()
    ]


# ============================================================
# RESUME TEXT PARSING
# ============================================================

def normalize_heading(line):
    """Normalize a heading for matching."""
    line = clean_markdown(line)
    line = re.sub(r"^[\s:|]+|[\s:|]+$", "", line)
    return re.sub(r"\s+", " ", line).lower()


def is_section_heading(line):
    """Check whether a line is a known resume section heading."""
    normalized = normalize_heading(line)
    return normalized in SECTION_NAMES


def section_title(line):
    """Return a standard heading title."""
    normalized = normalize_heading(line)
    return SECTION_NAMES.get(normalized, line.strip())


def is_bullet(line):
    """Identify common bullet-list markers."""
    return bool(
        re.match(
            r"^\s*(?:[-*•▪◦‣]|\d+[.)])\s+",
            line,
        )
    )


def clean_bullet(line):
    """Remove a bullet marker from a line."""
    return re.sub(
        r"^\s*(?:[-*•▪◦‣]|\d+[.)])\s+",
        "",
        line,
    ).strip()


def is_contact_line(line):
    """Identify likely contact information lines."""
    low = line.lower()

    return (
        "@" in line
        or bool(re.search(r"\+?\d[\d\s().-]{7,}\d", line))
        or low.startswith(("phone:", "email:", "location:", "linkedin:", "github:"))
        or "linkedin.com/" in low
        or "github.com/" in low
    )


def split_resume(resume_text):
    """
    Parse resume into:
        name
        contact lines
        sidebar sections
        main sections

    Unknown lines before a recognized section go into the summary.
    """
    lines = get_resume_lines(resume_text)

    name = "Resume"
    contact = []
    sidebar = []
    main = []

    current_section = "Professional Summary"
    current_items = []

    def save_section():
        nonlocal current_items

        if current_items:
            section = {
                "title": current_section,
                "items": current_items[:],
            }

            if current_section.lower() in SIDEBAR_SECTIONS:
                sidebar.append(section)
            else:
                main.append(section)

            current_items = []

    if not lines:
        return name, contact, sidebar, main

    # First line is usually the person's name.
    name = clean_markdown(lines[0]).strip() or "Resume"

    for line in lines[1:]:
        line = clean_markdown(line)

        if not line:
            continue

        # Contact details are collected separately.
        if is_contact_line(line):
            contact.append(line)
            continue

        if is_section_heading(line):
            save_section()
            current_section = section_title(line)
            continue

        # Preserve content under the current section.
        current_items.append(line)

    save_section()

    return name, contact, sidebar, main


# ============================================================
# TEMPLATE STYLE HELPERS
# ============================================================

def get_style(template_name):
    """Load the selected template style with safe defaults."""
    try:
        style = get_template_style(template_name) or {}
    except (KeyError, TypeError, AttributeError):
        style = {}

    result = DEFAULT_STYLE.copy()
    result.update(style)

    return result


def hex_rgb(hex_color):
    """Convert #RRGGBB into RGB values between 0 and 255."""
    value = str(hex_color or "#222222").strip().lstrip("#")

    if len(value) != 6:
        value = "222222"

    try:
        return tuple(
            int(value[index:index + 2], 16)
            for index in (0, 2, 4)
        )
    except ValueError:
        return (34, 34, 34)


def report_color(hex_color):
    """Convert a hex color to a ReportLab color."""
    r, g, b = hex_rgb(hex_color)

    return colors.Color(
        r / 255,
        g / 255,
        b / 255,
    )


def word_rgb(hex_color):
    """Convert a hex color to a python-docx RGBColor."""
    r, g, b = hex_rgb(hex_color)
    return RGBColor(r, g, b)


# ============================================================
# WORD DOCUMENT HELPERS
# ============================================================

def shade_cell(cell, fill):
    """Apply background color to a Word table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()

    shd = tc_pr.find(qn("w:shd"))

    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)

    shd.set(qn("w:fill"), fill.lstrip("#"))


def set_cell_margins(
    cell,
    top=120,
    start=150,
    bottom=120,
    end=150,
):
    """Set internal cell margins in twentieths of a point."""
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()

    margins = tc_pr.first_child_found_in("w:tcMar")

    if margins is None:
        margins = OxmlElement("w:tcMar")
        tc_pr.append(margins)

    for margin_name, value in [
        ("top", top),
        ("start", start),
        ("bottom", bottom),
        ("end", end),
    ]:
        node = margins.find(qn(f"w:{margin_name}"))

        if node is None:
            node = OxmlElement(f"w:{margin_name}")
            margins.append(node)

        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def remove_table_borders(table):
    """Remove visible borders from a Word table."""
    tbl_pr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")

    for edge in (
        "top",
        "left",
        "bottom",
        "right",
        "insideH",
        "insideV",
    ):
        element = OxmlElement(f"w:{edge}")
        element.set(qn("w:val"), "nil")
        borders.append(element)

    tbl_pr.append(borders)


def set_cell_width(cell, width):
    """Set a cell width in inches."""
    cell.width = Inches(width)

    tc_pr = cell._tc.get_or_add_tcPr()
    tc_w = tc_pr.find(qn("w:tcW"))

    if tc_w is None:
        tc_w = OxmlElement("w:tcW")
        tc_pr.append(tc_w)

    tc_w.set(qn("w:w"), str(int(width * 1440)))
    tc_w.set(qn("w:type"), "dxa")


def set_paragraph_spacing(paragraph, before=0, after=3):
    """Set paragraph spacing in points."""
    paragraph.paragraph_format.space_before = Pt(before)
    paragraph.paragraph_format.space_after = Pt(after)


def add_word_heading(container, title, color, font_name="Arial"):
    """Add a styled section heading to a Word document."""
    paragraph = container.add_paragraph()
    set_paragraph_spacing(paragraph, before=8, after=4)

    run = paragraph.add_run(title.upper())
    run.bold = True
    run.font.name = font_name
    run.font.size = Pt(11)
    run.font.color.rgb = word_rgb(color)

    return paragraph


def add_word_body(container, text, color="#222222", font_name="Arial"):
    """Add a clean content line to a Word document."""
    paragraph = container.add_paragraph()
    set_paragraph_spacing(paragraph, before=0, after=3)

    if is_bullet(text):
        text = clean_bullet(text)
        paragraph.style = "List Bullet"

    run = paragraph.add_run(text)
    run.font.name = font_name
    run.font.size = Pt(9.5)
    run.font.color.rgb = word_rgb(color)

    return paragraph


def add_word_sections(
    container,
    sections,
    heading_color,
    font_name="Arial",
    body_color="#222222",
):
    """Write sections and their content into Word."""
    for section in sections:
        add_word_heading(
            container,
            section["title"],
            heading_color,
            font_name,
        )

        for item in section["items"]:
            add_word_body(
                container,
                item,
                body_color,
                font_name,
            )


# ============================================================
# DOCX EXPORT
# ============================================================

def export_to_docx(resume_text, full_name, template_name):
    """Export resume to a formatted DOCX file."""
    style = get_style(template_name)
    primary = style.get("primary", "#222222")
    layout = style.get("layout", "single")
    font_name = style.get("font", "Arial")

    name, contact, sidebar, main = split_resume(resume_text)

    output_path = output_path_for(
        full_name,
        template_name,
        "docx",
    )

    document = Document()
    section = document.sections[0]

    section.top_margin = Inches(0.55)
    section.bottom_margin = Inches(0.55)
    section.left_margin = Inches(0.6)
    section.right_margin = Inches(0.6)

    normal = document.styles["Normal"]
    normal.font.name = font_name
    normal.font.size = Pt(9.5)

    if layout == "single":
        heading = document.add_paragraph()
        heading.alignment = WD_ALIGN_PARAGRAPH.CENTER

        run = heading.add_run(name.upper())
        run.bold = True
        run.font.name = font_name
        run.font.size = Pt(21)
        run.font.color.rgb = word_rgb(primary)

        for line in contact:
            paragraph = document.add_paragraph()
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            paragraph.paragraph_format.space_after = Pt(2)

            run = paragraph.add_run(line)
            run.font.size = Pt(8.5)

        add_word_sections(
            document,
            main + sidebar,
            primary,
            font_name,
        )

    else:
        # Two-column design.
        table = document.add_table(rows=1, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        left_cell = table.cell(0, 0)
        right_cell = table.cell(0, 1)

        left_cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
        right_cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP

        set_cell_width(left_cell, 2.15)
        set_cell_width(right_cell, 4.65)

        shade_cell(left_cell, primary)
        set_cell_margins(left_cell, 220, 220, 220, 220)
        set_cell_margins(right_cell, 180, 240, 180, 160)

        # Remove the default empty paragraph from each cell.
        left_cell.paragraphs[0].text = ""
        right_cell.paragraphs[0].text = ""

        p = left_cell.add_paragraph()
        set_paragraph_spacing(p, after=8)

        run = p.add_run(name.upper())
        run.bold = True
        run.font.name = font_name
        run.font.size = Pt(17)
        run.font.color.rgb = RGBColor(255, 255, 255)

        for line in contact:
            p = left_cell.add_paragraph()
            set_paragraph_spacing(p, after=4)

            run = p.add_run(line)
            run.font.name = font_name
            run.font.size = Pt(8)
            run.font.color.rgb = RGBColor(255, 255, 255)

        for item in sidebar:
            add_word_heading(
                left_cell,
                item["title"],
                "#FFFFFF",
                font_name,
            )

            # Ensure sidebar headings stay white on colored background.
            for run in left_cell.paragraphs[-1].runs:
                run.font.color.rgb = RGBColor(255, 255, 255)

            for text_line in item["items"]:
                p = left_cell.add_paragraph()
                set_paragraph_spacing(p, after=3)

                if is_bullet(text_line):
                    text_line = clean_bullet(text_line)

                run = p.add_run(text_line)
                run.font.name = font_name
                run.font.size = Pt(8.5)
                run.font.color.rgb = RGBColor(255, 255, 255)

        add_word_sections(
            right_cell,
            main,
            primary,
            font_name,
        )

        remove_table_borders(table)

    document.save(output_path)

    return str(output_path)


# ============================================================
# PDF HELPERS
# ============================================================

def make_pdf_styles(primary, font_name):
    """Create PDF paragraph styles."""
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="ResumeName",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=report_color(primary),
            alignment=TA_CENTER,
            spaceAfter=6,
        )
    )

    styles.add(
        ParagraphStyle(
            name="ResumeContact",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#555555"),
            alignment=TA_CENTER,
            spaceAfter=2,
        )
    )

    styles.add(
        ParagraphStyle(
            name="ResumeHeading",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=13,
            textColor=report_color(primary),
            spaceBefore=8,
            spaceAfter=4,
            keepWithNext=True,
        )
    )

    styles.add(
        ParagraphStyle(
            name="ResumeBody",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8.8,
            leading=12,
            textColor=colors.HexColor("#222222"),
            spaceAfter=3,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SidebarHeading",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.5,
            leading=12,
            textColor=colors.white,
            spaceBefore=8,
            spaceAfter=4,
            keepWithNext=True,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SidebarBody",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=11,
            textColor=colors.white,
            spaceAfter=3,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SidebarName",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=18,
            textColor=colors.white,
            spaceAfter=8,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SidebarContact",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=10,
            textColor=colors.white,
            spaceAfter=4,
        )
    )

    return styles


def pdf_paragraph_text(text):
    """Escape text safely for ReportLab's paragraph parser."""
    text = clean_markdown(text)
    text = escape(text)

    # Convert ampersands and angle brackets safely.
    return text.replace("\n", "<br/>")


def add_pdf_sections(story, sections, styles):
    """Append resume sections to a PDF story."""
    for section in sections:
        heading = Paragraph(
            pdf_paragraph_text(section["title"].upper()),
            styles["ResumeHeading"],
        )

        story.append(heading)

        for line in section["items"]:
            if is_bullet(line):
                line = clean_bullet(line)
                prefix = "&#8226;&nbsp;"
            else:
                prefix = ""

            story.append(
                Paragraph(
                    prefix + pdf_paragraph_text(line),
                    styles["ResumeBody"],
                )
            )


def draw_sidebar(canvas, doc, primary, sidebar_width):
    """Draw a colored sidebar on each page."""
    canvas.saveState()

    page_width, page_height = A4

    canvas.setFillColor(report_color(primary))
    canvas.rect(
        0,
        0,
        sidebar_width,
        page_height,
        fill=1,
        stroke=0,
    )

    canvas.restoreState()


# ============================================================
# PDF EXPORT
# ============================================================

def export_to_pdf(resume_text, full_name, template_name):
    """Export resume to a formatted PDF file."""
    style = get_style(template_name)
    primary = style.get("primary", "#222222")
    layout = style.get("layout", "single")

    name, contact, sidebar, main = split_resume(resume_text)

    output_path = output_path_for(
        full_name,
        template_name,
        "pdf",
    )

    pdf_styles = make_pdf_styles(primary, style.get("font", "Arial"))

    if layout == "single":
        story = [
            Paragraph(
                pdf_paragraph_text(name.upper()),
                pdf_styles["ResumeName"],
            )
        ]

        for line in contact:
            story.append(
                Paragraph(
                    pdf_paragraph_text(line),
                    pdf_styles["ResumeContact"],
                )
            )

        story.append(Spacer(1, 8))
        add_pdf_sections(story, main + sidebar, pdf_styles)

        document = SimpleDocTemplate(
            str(output_path),
            pagesize=A4,
            rightMargin=0.55 * inch,
            leftMargin=0.55 * inch,
            topMargin=0.45 * inch,
            bottomMargin=0.45 * inch,
            title=f"{name} Resume",
            author=name,
        )

        document.build(story)

    else:
        # Two-column PDF with colored sidebar.
        page_width, page_height = A4
        sidebar_width = 2.05 * inch
        margin = 0.4 * inch

        from reportlab.platypus import (
            BaseDocTemplate,
            Frame,
            PageTemplate,
        )

        document = BaseDocTemplate(
            str(output_path),
            pagesize=A4,
            leftMargin=sidebar_width + 0.3 * inch,
            rightMargin=margin,
            topMargin=0.45 * inch,
            bottomMargin=0.45 * inch,
            title=f"{name} Resume",
            author=name,
        )

        left_frame = Frame(
            0.18 * inch,
            0.35 * inch,
            sidebar_width - 0.28 * inch,
            page_height - 0.7 * inch,
            leftPadding=0.12 * inch,
            rightPadding=0.12 * inch,
            topPadding=0.1 * inch,
            bottomPadding=0.1 * inch,
            id="sidebar",
            showBoundary=0,
        )

        right_frame = Frame(
            sidebar_width + 0.25 * inch,
            0.45 * inch,
            page_width - sidebar_width - margin - 0.25 * inch,
            page_height - 0.9 * inch,
            leftPadding=0.04 * inch,
            rightPadding=0.04 * inch,
            topPadding=0.02 * inch,
            bottomPadding=0.02 * inch,
            id="main",
            showBoundary=0,
        )

        def on_page(canvas, doc):
            draw_sidebar(canvas, doc, primary, sidebar_width)

        document.addPageTemplates(
            [
                PageTemplate(
                    id="ResumeTwoColumn",
                    frames=[left_frame, right_frame],
                    onPage=on_page,
                )
            ]
        )

        sidebar_story = [
            Paragraph(
                pdf_paragraph_text(name.upper()),
                pdf_styles["SidebarName"],
            )
        ]

        for line in contact:
            sidebar_story.append(
                Paragraph(
                    pdf_paragraph_text(line),
                    pdf_styles["SidebarContact"],
                )
            )

        for section in sidebar:
            sidebar_story.append(
                Paragraph(
                    pdf_paragraph_text(section["title"].upper()),
                    pdf_styles["SidebarHeading"],
                )
            )

            for line in section["items"]:
                if is_bullet(line):
                    line = clean_bullet(line)

                sidebar_story.append(
                    Paragraph(
                        pdf_paragraph_text(line),
                        pdf_styles["SidebarBody"],
                    )
                )

        main_story = []
        add_pdf_sections(main_story, main, pdf_styles)

        # The first frame is the sidebar; the second is the main column.
        # Keep both stories in one document using explicit frame actions.
        from reportlab.platypus import FrameBreak

        story = sidebar_story + [FrameBreak()] + main_story
        document.build(story)

    return str(output_path)


# ============================================================
# TEST ALL TEMPLATES
# ============================================================

if __name__ == "__main__":

    sample_resume = """
Ali Hassan
ali@example.com | +92 300 1234567 | Pakistan

## PROFESSIONAL SUMMARY
Python developer learning machine learning and AI.

## TECHNICAL SKILLS
- Python
- NumPy
- Pandas
- Scikit-learn

## EDUCATION
Bachelor's degree in Computer Science

## PROJECTS
**AI Resume Builder**
Created a resume generation project using Python and Ollama.

## CERTIFICATIONS
Python Programming
"""

    print("\nTesting Markdown cleanup...")
    print("----------------------------------")

    cleaned = clean_markdown(sample_resume)
    print(cleaned)

    print("\nTesting all resume templates...")
    print("----------------------------------")

    try:
        templates = get_supported_templates()
    except Exception as error:
        print("Could not load templates:", error)
        raise

    for template_name in templates:
        print(f"\nTemplate: {template_name}")

        try:
            docx_path = export_to_docx(
                sample_resume,
                "Ali Hassan",
                template_name,
            )
            print("DOCX:", docx_path)

            pdf_path = export_to_pdf(
                sample_resume,
                "Ali Hassan",
                template_name,
            )
            print("PDF:", pdf_path)

        except Exception as error:
            print("ERROR:", error)
            raise

    print("\nAll template export tests completed.")
    print("Output folder:", OUTPUT_DIR)
