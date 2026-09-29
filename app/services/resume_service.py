import fitz

from src.data.preprocessing import clean_text
from src.skills.extractor import extract_skills


def extract_pdf_text(file_bytes: bytes) -> str:
    try:
        doc = fitz.open(
            stream=file_bytes,
            filetype="pdf"
        )
    except Exception as exc:
        raise ValueError(
            "The uploaded file is not a valid PDF"
        ) from exc

    try:
        text = "\n".join(
            page.get_text("text")
            for page in doc
        )
    finally:
        doc.close()

    text = clean_text(text)

    if len(text) < 30:
        raise ValueError(
            "No usable text could be extracted. "
            "The PDF may be scanned/image-only."
        )

    return text


def analyze_resume(text: str) -> dict:
    text = clean_text(text)

    if len(text) < 20:
        raise ValueError(
            "Resume text is too short to analyze"
        )

    return {
        "skills": extract_skills(text),
        "text_length": len(text),
        "text": text,
    }