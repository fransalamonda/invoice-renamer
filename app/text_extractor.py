import fitz
import tempfile
import easyocr

reader = easyocr.Reader(['en'])

def extract_text_pdf(pdf_path):
    text = ""

    doc = fitz.open(pdf_path)

    try:
        for page in doc:
            text += page.get_text()
            text += "\n"
    finally:
        doc.close()

    return text


def extract_text_ocr(pdf_path):
    text = ""

    doc = fitz.open(pdf_path)

    try:
        for page in doc:

            pix = page.get_pixmap(
                matrix=fitz.Matrix(2, 2),
                alpha=False
            )

            with tempfile.NamedTemporaryFile(
                suffix=".png",
                delete=True
            ) as temp:

                pix.save(temp.name)

                result = reader.readtext(
                    temp.name,
                    detail=0
                )

                for line in result:
                    text += line + "\n"

    finally:
        doc.close()

    return text


def extract_text(pdf_path):

    # Prioritas 1: coba baca text layer
    try:

        text = extract_text_pdf(pdf_path)

        if len(text.strip()) > 100:
            print(f"[TEXT] {pdf_path}")
            return text

    except Exception as e:
        print(f"PDF TEXT ERROR: {e}")

    # Prioritas 2: OCR jika tidak ada text
    try:

        print(f"[OCR] {pdf_path}")

        text = extract_text_ocr(pdf_path)

        return text

    except Exception as e:

        print(f"OCR ERROR: {e}")

        return ""