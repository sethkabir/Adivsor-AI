import fitz
from docx import Document

def load_news(path: str) -> str:
    if path.endswith(".txt"):
        return open(path, encoding="utf-8").read()
    if path.endswith(".pdf"):
        return " ".join(p.get_text() for p in fitz.open(path))
    if path.endswith(".docx"):
        return " ".join(p.text for p in Document(path).paragraphs)
    raise ValueError("Unsupported file")
