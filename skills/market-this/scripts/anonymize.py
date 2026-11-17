#!/usr/bin/env python3
"""Remove personal data from a CSV export before analysis.

Usage:
    python3 anonymize.py input.csv output.csv [--keep COLUMN ...]

Drops columns whose header looks personal (name, email, phone, address, IBAN,
birth date, in English and Dutch) and masks email addresses and phone numbers
found in any remaining cell. Prints a short report. Standard library only.
"""
import argparse
import csv
import re
import sys

PERSONAL_HEADER = re.compile(
    r"(^|[\s_\-])(first ?name|last ?name|full ?name|name|naam|voornaam|achternaam|"
    r"contact|e-?mail|mail|phone|telefoon|tel|mobile|mobiel|gsm|address|adres|street|straat|"
    r"postcode|zip|iban|bank|bsn|ssn|birth|geboorte|dob|klant|klantnaam|customer|client|cliënt|patient|patiënt|relatie|lid|member|deelnemer|participant|medewerker|employee|werknemer)([\s_\-]|$)",
    re.IGNORECASE,
)
EMAIL = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"(?<!\d)(\+?\d[\d\s\-().]{7,}\d)(?!\d)")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}([ T]\d{2}:\d{2}(:\d{2})?)?|\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4}([ T]\d{2}:\d{2}(:\d{2})?)?")


def mask_phone(match):
    text = match.group(0)
    if DATE.fullmatch(text.strip()) or sum(c.isdigit() for c in text) < 9:
        return text
    return "[phone]"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--keep", nargs="*", default=[],
                        help="column names to keep even if they look personal")
    args = parser.parse_args()

    with open(args.input, newline="", encoding="utf-8-sig") as fh:
        sample = fh.read(4096)
        fh.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        except csv.Error:
            dialect = csv.excel
        reader = csv.DictReader(fh, dialect=dialect)
        headers = reader.fieldnames or []
        keep_set = {k.lower() for k in args.keep}
        dropped = [h for h in headers if PERSONAL_HEADER.search(h or "") and h.lower() not in keep_set]
        kept = [h for h in headers if h not in dropped]

        masked = 0
        rows = []
        for row in reader:
            out = {}
            for h in kept:
                value = row.get(h) or ""
                new = EMAIL.sub("[email]", value)
                dates = []
                new = DATE.sub(lambda m: dates.append(m.group(0)) or f"\x00{len(dates) - 1}\x00", new)
                new = PHONE.sub(mask_phone, new)
                new = re.sub("\x00(\\d+)\x00", lambda m: dates[int(m.group(1))], new)
                if new != value:
                    masked += 1
                out[h] = new
            rows.append(out)

    with open(args.output, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=kept, dialect=dialect)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Rows: {len(rows)}")
    print(f"Dropped columns: {', '.join(dropped) if dropped else 'none'}")
    print(f"Cells with masked email or phone: {masked}")
    print("Check the output before sharing: free-text fields can still contain names.", file=sys.stderr)


if __name__ == "__main__":
    main()
