import re
import importlib
from io import BytesIO


PREDEFINED_SKILLS = [
    "Python",
    "Java",
    "C++",
    "SQL",
    "JavaScript",
    "TypeScript",
    "React",
    "Node.js",
    "Flask",
    "Django",
    "AWS",
    "Docker",
    "Kubernetes",
    "Git",
    "HTML",
    "CSS",
    "Machine Learning",
    "Data Structures",
    "OOP",
]


def _extract_text_from_pdf(file_bytes: bytes) -> str:
    text_chunks = []
    pypdf = importlib.import_module("pypdf")
    reader = pypdf.PdfReader(BytesIO(file_bytes))
    for page in reader.pages:
        page_text = page.extract_text() or ""
        if page_text:
            text_chunks.append(page_text)
    return "\n".join(text_chunks)


def _extract_text_from_docx(file_bytes: bytes) -> str:
    text_chunks = []
    docx = importlib.import_module("docx")
    document = docx.Document(BytesIO(file_bytes))
    for paragraph in document.paragraphs:
        paragraph_text = (paragraph.text or "").strip()
        if paragraph_text:
            text_chunks.append(paragraph_text)
    return "\n".join(text_chunks)


def _extract_cgpa(text: str):
    patterns = [
        r"(?:CGPA|GPA)\s*[:=]\s*(\d+(?:\.\d+)?)",
        r"(\d+(?:\.\d+)?)\s*/\s*10(?:\.0+)?",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if not match:
            continue
        try:
            value = float(match.group(1))
            if 0 <= value <= 10:
                return value
        except (TypeError, ValueError):
            continue
    return None


def _extract_skills(text: str):
    matched = []
    for skill in PREDEFINED_SKILLS:
        if re.search(r"\b" + re.escape(skill) + r"\b", text, re.IGNORECASE):
            matched.append(skill)
    return ",".join(matched)


def _extract_phone(text: str):
    patterns = [
        r"(?:\+91[-\s]?)?[6-9]\d{9}",
        r"\b\d{3}[-\s]?\d{3}[-\s]?\d{4}\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0).strip()
    return None


def _extract_branch(text: str):
    branch_patterns = [
        (r"computer\s+science|\bcse\b", "Computer Science & Engineering"),
        (r"information\s+technology|\bit\b", "Information Technology"),
        (r"electronics\s*(?:and|&)\s*communication|\bece\b", "Electronics & Communication"),
    ]

    for pattern, label in branch_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return label
    return None


def _extract_current_year(text: str):
    explicit_patterns = [
        (r"\b1st\s+year\b|\bfirst\s+year\b", "1st Year"),
        (r"\b2nd\s+year\b|\bsecond\s+year\b", "2nd Year"),
        (r"\b3rd\s+year\b|\bthird\s+year\b", "3rd Year"),
        (r"\b4th\s+year\b|\bfourth\s+year\b", "4th Year"),
    ]

    for pattern, label in explicit_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return label

    numeric_match = re.search(r"(?:current\s+year|year)\s*[:=]?\s*([1-4])\b", text, re.IGNORECASE)
    if numeric_match:
        return f"{numeric_match.group(1)}th Year" if numeric_match.group(1) == "4" else f"{numeric_match.group(1)}rd Year" if numeric_match.group(1) == "3" else f"{numeric_match.group(1)}nd Year" if numeric_match.group(1) == "2" else "1st Year"

    return None


def parse_cv(file_storage):
    result = {"cgpa": None, "skills": "", "phone": None, "branch": None, "current_year": None}

    if not file_storage or not file_storage.filename:
        return result

    filename = file_storage.filename.lower()
    try:
        file_bytes = file_storage.read() or b""
        file_storage.stream.seek(0)
    except Exception:
        return result

    if not file_bytes:
        return result

    try:
        if filename.endswith(".pdf"):
            text = _extract_text_from_pdf(file_bytes)
        elif filename.endswith(".docx"):
            text = _extract_text_from_docx(file_bytes)
        else:
            return result
    except Exception:
        return result

    if not text:
        return result

    result["cgpa"] = _extract_cgpa(text)
    result["skills"] = _extract_skills(text)
    result["phone"] = _extract_phone(text)
    result["branch"] = _extract_branch(text)
    result["current_year"] = _extract_current_year(text)
    return result
