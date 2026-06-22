import re


CUSTOMER_KEYWORDS = [
    "BILL TO",
    "CUSTOMER",
    "KEPADA",
    "SHIP TO",
    "ATTENTION",
    "ATTN"
]


def sanitize(value):

    value = re.sub(
        r'[\\/:*?"<>|]',
        '_',
        value
    )

    value = re.sub(
        r'_+',
        '_',
        value
    )

    return value.strip('_')


def clean_company(company):

    company = company.upper()

    company = re.sub(
        r'[^A-Z0-9 ]',
        '',
        company
    )

    company = "_".join(
        company.split()
    )

    return company[:100]

# def find_invoice_number(text):
#
#     if not text:
#         return "NO_INVOICE"
#
#     lines = [
#         line.strip()
#         for line in text.splitlines()
#         if line.strip()
#     ]
#
#     for i, line in enumerate(lines):
#
#         upper = line.upper()
#
#         # Invoice No:
#         if (
#             "INVOICE NO" in upper
#             or "INVOICE NUMBER" in upper
#             or "NO INVOICE" in upper
#             or "NOMOR INVOICE" in upper
#         ):
#
#             # cek 3 baris setelahnya
#             for j in range(i + 1, min(i + 4, len(lines))):
#
#                 candidate = lines[j].strip()
#
#                 # contoh:
#                 # C123-00026
#                 # 016/INV-AJN/II/2023
#                 # INV-2023-001
#
#                 if re.match(
#                     r'^[A-Z0-9][A-Z0-9\-\/]{3,}$',
#                     candidate.upper()
#                 ):
#                     return sanitize(candidate)
#
#     # fallback global search
#
#     patterns = [
#
#         r'([A-Z][0-9]{3,}\-[0-9]{3,})',
#
#         r'([0-9]{1,5}/INV[A-Z0-9/\-]+)',
#
#         r'(INV[A-Z0-9/\-]{4,})'
#     ]
#
#     upper_text = text.upper()
#
#     for pattern in patterns:
#
#         match = re.search(
#             pattern,
#             upper_text
#         )
#
#         if match:
#             return sanitize(
#                 match.group(1)
#             )
#
#     return "NO_INVOICE"
def find_invoice_number(text):

    if not text:
        return "NO_INVOICE"

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    # Cari label invoice
    for i, line in enumerate(lines):

        upper = line.upper()

        if (
            "INVOICE NO" in upper
            or "INVOICE NUMBER" in upper
            or upper == "INVOICE"
        ):

            # cek 8 baris setelahnya
            for j in range(i + 1, min(i + 8, len(lines))):

                candidate = lines[j].strip().upper()

                # abaikan kata-kata umum
                if candidate in [
                    "DATE",
                    "OFFICE",
                    "INVOICE",
                    "INVOICE NO",
                    "NUMBER"
                ]:
                    continue

                # contoh:
                # YP2207-0900
                # C123-00026
                # 005-23
                # INV-001
                if re.match(
                    r'^[A-Z0-9]{2,20}[-/][A-Z0-9]{1,20}([-/][A-Z0-9]{1,20})*$',
                    candidate
                ):
                    return sanitize(candidate)

    # fallback global
    candidates = re.findall(
        r'\b[A-Z0-9]{2,20}[-/][A-Z0-9]{1,20}(?:[-/][A-Z0-9]{1,20})*\b',
        text.upper()
    )

    blacklist = {
        "20-07-22",
        "12-01-2023",
        "13-03-2023"
    }

    for candidate in candidates:

        if candidate not in blacklist:
            return sanitize(candidate)

    return "NO_INVOICE"

def find_company(text):

    if not text:
        return "UNKNOWN_COMPANY"

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    header = lines[:50]

    for line in header:

        upper = line.upper()

        if any(
            keyword in upper
            for keyword in CUSTOMER_KEYWORDS
        ):
            break

        match = re.search(
            r'\b(PT|PI|CV|UD|PD)\b[\.\'\s]*([A-Z0-9\s&\-,]+)',
            upper
        )

        if match:

            company = (
                match.group(1)
                + " "
                + match.group(2)
            )

            company = clean_company(
                company
            )

            if len(company) > 5:
                return company

    return "UNKNOWN_COMPANY"