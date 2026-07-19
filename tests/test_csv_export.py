import csv
from io import StringIO
import unittest

from csv_export import serialize_csv_row


class CsvExportTests(unittest.TestCase):
    def test_neutralizes_spreadsheet_formulas(self):
        row = serialize_csv_row(["@user", "=1+1", "+cmd", "-2", "safe"])

        self.assertEqual(
            next(csv.reader(StringIO(row))),
            ["'@user", "'=1+1", "'+cmd", "'-2", "safe"],
        )

    def test_quotes_commas_quotes_and_newlines(self):
        values = ["person", 'A comma, a "quote", and\nnewline']

        self.assertEqual(next(csv.reader(StringIO(serialize_csv_row(values)))), values)

    def test_uses_one_line_terminator(self):
        self.assertEqual(serialize_csv_row(["a", "b"]), "a,b\n")


if __name__ == "__main__":
    unittest.main()
