import csv
from io import StringIO


DANGEROUS_CELL_PREFIXES = ("=", "+", "-", "@", "\t", "\r")


def neutralize_spreadsheet_formula(value):
    text = str(value)
    if text.startswith(DANGEROUS_CELL_PREFIXES):
        return f"'{text}"
    return text


def serialize_csv_row(values):
    buffer = StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(neutralize_spreadsheet_formula(value) for value in values)
    return buffer.getvalue()
