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

def find_invoice_number(text):

    if not text:
        return "NO_INVOICE"

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    candidates = []

    patterns = [

        # YP2207-0900
        r'\b[A-Z]{1,10}[0-9]{2,10}-[0-9]{2,10}\b',

        # C123-00026
        r'\b[A-Z][0-9]{2,10}-[0-9]{2,10}\b',

        # 005-23
        r'\b[0-9]{2,10}-[0-9]{1,10}\b',

        # 016/INV-AJN/II/2023
        r'\b[0-9]{1,10}/INV[A-Z0-9/\-]+\b',

        # INV-001
        r'\bINV[-/A-Z0-9]+\b'
    ]

    upper_text = text.upper()

    for pattern in patterns:

        matches = re.findall(
            pattern,
            upper_text
        )

        for match in matches:

            # skip tanggal
            if re.match(
                r'^\d{2}-\d{2}-\d{2,4}$',
                match
            ):
                continue

            if re.match(
                r'^\d{2}/\d{2}/\d{2,4}$',
                match
            ):
                continue

            candidates.append(match)

    if not candidates:
        return "NO_INVOICE"

    # prioritas yang mengandung INV
    inv_candidates = [
        x for x in candidates
        if "INV" in x
    ]

    if inv_candidates:
        inv_candidates.sort(
            key=len,
            reverse=True
        )
        return sanitize(inv_candidates[0])

    # selain INV ambil yang paling panjang
    candidates.sort(
        key=len,
        reverse=True
    )

    return sanitize(candidates[0])

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