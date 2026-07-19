import argparse
import csv
import json
from pathlib import Path


OUTPUT_FIELDS = ["username", "text", "followers", "following", "account_age_days", "posts_count"]


def read_records(path):
    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))

    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []

    if suffix == ".json":
        payload = json.loads(text)
        if isinstance(payload, list):
            return payload
        if isinstance(payload, dict):
            for key in ("tweets", "posts", "items", "data", "results"):
                value = payload.get(key)
                if isinstance(value, list):
                    return value
            return [payload]

    return [json.loads(line) for line in text.splitlines() if line.strip()]


def nested_get(record, path):
    value = record
    for part in path.split("."):
        if not isinstance(value, dict):
            return None
        value = value.get(part)
    return value


def first_value(record, paths, default=""):
    for path in paths:
        value = nested_get(record, path)
        if value not in (None, ""):
            return value
    return default


def to_int(value, default=0):
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def convert_record(record):
    text = first_value(
        record,
        [
            "text",
            "tweet",
            "tweetText",
            "full_text",
            "reply_text",
            "replyText",
            "content",
            "caption",
        ],
    )
    username = first_value(
        record,
        [
            "username",
            "userName",
            "author.username",
            "author.userName",
            "authorUsername",
            "user.screen_name",
            "user.username",
        ],
        "unknown",
    )
    followers = first_value(
        record,
        [
            "followers",
            "followersCount",
            "author.followers",
            "author.followersCount",
            "user.followers_count",
        ],
        0,
    )
    following = first_value(
        record,
        [
            "following",
            "followingCount",
            "author.following",
            "author.followingCount",
            "user.friends_count",
        ],
        0,
    )
    posts_count = first_value(
        record,
        [
            "posts_count",
            "statusesCount",
            "author.statusesCount",
            "user.statuses_count",
        ],
        1,
    )

    return {
        "username": str(username).lstrip("@") or "unknown",
        "text": str(text).replace("\n", " ").strip(),
        "followers": to_int(followers),
        "following": to_int(following),
        "account_age_days": to_int(record.get("account_age_days"), 30),
        "posts_count": max(1, to_int(posts_count, 1)),
    }


def convert_file(input_path, output_path):
    rows = [convert_record(record) for record in read_records(input_path)]
    rows = [row for row in rows if row["text"]]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    return len(rows)


def main():
    parser = argparse.ArgumentParser(
        description="Convert reviewed Xquik X/Twitter exports into the dashboard CSV upload schema."
    )
    parser.add_argument("input", type=Path, help="Xquik JSON, JSONL, NDJSON, or CSV export")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("uploads/xquik_posts.csv"),
        help="Destination CSV path for dashboard upload",
    )
    args = parser.parse_args()

    count = convert_file(args.input, args.output)
    print(f"Wrote {count} rows to {args.output}")


if __name__ == "__main__":
    main()
