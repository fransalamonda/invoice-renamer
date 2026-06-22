import os
import shutil
import traceback

from app.config import (
    INPUT_FOLDER,
    OUTPUT_FOLDER,
    FAILED_FOLDER
)

from app.text_extractor import extract_text

import app.invoice_parser

from app.invoice_parser import (
    find_invoice_number,
    find_company
)

from app.renamer import move_and_rename
from app.logger import write_log


def process_pdf(filename):

    pdf_path = os.path.join(
        INPUT_FOLDER,
        filename
    )

    try:

        print("\n" + "=" * 80)
        print(f"PROCESSING : {filename}")
        print("=" * 80)

        text = extract_text(pdf_path)

        if not text.strip():
            raise Exception(
                "No text extracted from PDF"
            )

        print("\nTEXT SAMPLE")
        print("-" * 80)
        print(text[:3000])
        print("-" * 80)

        # ======================
        # COMPANY
        # ======================

        company = find_company(text)

        print(
            f"COMPANY : {company}"
        )

        # ======================
        # INVOICE
        # ======================

        invoice = find_invoice_number(text)

        print(
            f"INVOICE : {invoice}"
        )

        print(
            f"INVOICE TYPE : {type(invoice)}"
        )

        print(
            f"INVOICE REPR : {repr(invoice)}"
        )

        # ======================
        # NEW FILE
        # ======================

        new_filename = (
            f"{company}_{invoice}.pdf"
        )

        print(
            f"NEW FILE : {new_filename}"
        )

        move_and_rename(
            pdf_path,
            OUTPUT_FOLDER,
            company,
            new_filename
        )

        write_log(
            filename,
            new_filename,
            "SUCCESS"
        )

        print(
            f"SUCCESS : {new_filename}"
        )

    except Exception as e:

        print("\n" + "=" * 80)
        print(
            f"FAILED : {filename}"
        )

        print(
            f"ERROR : {str(e)}"
        )

        traceback.print_exc()

        print("=" * 80)

        try:

            os.makedirs(
                FAILED_FOLDER,
                exist_ok=True
            )

            shutil.move(
                pdf_path,
                os.path.join(
                    FAILED_FOLDER,
                    filename
                )
            )

        except Exception:
            pass

        write_log(
            filename,
            "",
            f"FAILED: {str(e)}"
        )


def main():

    print("\n")
    print("=" * 80)
    print("INVOICE RENAMER")
    print("=" * 80)

    print(
        "PARSER FILE :",
        app.invoice_parser.__file__
    )

    os.makedirs(
        INPUT_FOLDER,
        exist_ok=True
    )

    os.makedirs(
        OUTPUT_FOLDER,
        exist_ok=True
    )

    os.makedirs(
        FAILED_FOLDER,
        exist_ok=True
    )

    pdf_files = [
        f
        for f in os.listdir(INPUT_FOLDER)
        if f.lower().endswith(".pdf")
    ]

    print(
        f"INPUT FOLDER : {os.path.abspath(INPUT_FOLDER)}"
    )

    print(
        f"PDF FOUND    : {len(pdf_files)}"
    )

    if not pdf_files:

        print(
            "No PDF files found."
        )

        return

    for pdf_file in pdf_files:

        process_pdf(
            pdf_file
        )

    print("\n")
    print("=" * 80)
    print("FINISHED")
    print("=" * 80)


if __name__ == "__main__":
    main()