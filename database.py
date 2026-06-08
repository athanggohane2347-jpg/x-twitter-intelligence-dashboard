import sqlite3
from contextlib import closing
from datetime import datetime
from flask import current_app, g
from werkzeug.security import generate_password_hash, check_password_hash


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    filename TEXT,
    total_posts INTEGER NOT NULL,
    positive_count INTEGER NOT NULL,
    negative_count INTEGER NOT NULL,
    neutral_count INTEGER NOT NULL,
    spam_count INTEGER NOT NULL,
    fake_count INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
"""


def init_database(database_path):
    with closing(sqlite3.connect(database_path)) as connection:
        connection.executescript(SCHEMA)
        connection.commit()


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def create_user(name, email, password):
    db = get_db()
    db.execute(
        "INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
        (name, email.lower(), generate_password_hash(password), datetime.utcnow().isoformat()),
    )
    db.commit()


def find_user_by_email(email):
    return get_db().execute(
        "SELECT * FROM users WHERE email = ?",
        (email.lower(),),
    ).fetchone()


def find_user_by_id(user_id):
    return get_db().execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()


def verify_user(email, password):
    user = find_user_by_email(email)
    if user and check_password_hash(user["password_hash"], password):
        return user
    return None


def save_analysis(user_id, filename, summary):
    db = get_db()
    db.execute(
        """
        INSERT INTO analyses (
            user_id, filename, total_posts, positive_count, negative_count,
            neutral_count, spam_count, fake_count, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            filename,
            summary["total_posts"],
            summary["positive_count"],
            summary["negative_count"],
            summary["neutral_count"],
            summary["spam_count"],
            summary["fake_count"],
            datetime.utcnow().isoformat(),
        ),
    )
    db.commit()


def get_recent_analyses(user_id, limit=6):
    return get_db().execute(
        """
        SELECT * FROM analyses
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (user_id, limit),
    ).fetchall()
