import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from xquik_csv import convert_file, convert_record, read_records


class XquikCsvTests(unittest.TestCase):
    def test_maps_current_xquik_author_fields(self):
        row = convert_record(
            {
                "text": "Useful launch",
                "author": {
                    "username": "builder",
                    "followers": 120,
                    "following": 45,
                    "statusesCount": 88,
                },
            }
        )

        self.assertEqual(row["username"], "builder")
        self.assertEqual(row["followers"], 120)
        self.assertEqual(row["following"], 45)
        self.assertEqual(row["posts_count"], 88)

    def test_maps_camel_case_reply_exports(self):
        row = convert_record(
            {"replyText": "A reply", "author": {"userName": "responder"}}
        )

        self.assertEqual(row["text"], "A reply")
        self.assertEqual(row["username"], "responder")

    def test_reads_paginated_xquik_tweets(self):
        with TemporaryDirectory() as directory:
            source = Path(directory) / "tweets.json"
            source.write_text(
                json.dumps({"tweets": [{"id": "1", "text": "Hello"}]}),
                encoding="utf-8",
            )

            self.assertEqual(read_records(source), [{"id": "1", "text": "Hello"}])

    def test_filters_blank_rows(self):
        with TemporaryDirectory() as directory:
            source = Path(directory) / "tweets.jsonl"
            output = Path(directory) / "output.csv"
            source.write_text('{"text": ""}\n{"text": "Kept"}\n', encoding="utf-8")

            self.assertEqual(convert_file(source, output), 1)
            self.assertIn("Kept", output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
