import io
try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    from pdf2image import convert_from_bytes
except ImportError:
    convert_from_bytes = None


def extract_text_from_pdf(file: io.BytesIO) -> str:
    if pdfplumber is None:
        raise RuntimeError("pdfplumber not installed.")
    text_parts = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            text_parts.append(txt)
    return "\n\n".join(text_parts).strip()


def pdf_to_images(file: io.BytesIO):
    """
    Convert PDF pages into images.
    Requires: pip install pdf2image poppler-utils
    """
    if convert_from_bytes is None:
        raise RuntimeError("pdf2image not installed.")
    images = convert_from_bytes(file.read())
    return images
