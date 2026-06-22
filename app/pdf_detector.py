import fitz

from app.config import MIN_TEXT_LENGTH


def is_scanned_pdf(pdf_path):

    try:

        doc = fitz.open(pdf_path)

        text = ""

        for page in doc:
            text += page.get_text()

        doc.close()

        return len(text.strip()) < MIN_TEXT_LENGTH

    except Exception:
        return True