import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "ds_prep.db"

CREATE_CARDS_TABLE = """
CREATE TABLE IF NOT EXISTS cards (
    id            TEXT PRIMARY KEY,
    category      TEXT NOT NULL,
    question      TEXT NOT NULL,
    answer        TEXT NOT NULL,
    language      TEXT DEFAULT 'none',
    ease_factor   REAL DEFAULT 2.5,
    interval_days INTEGER DEFAULT 0,
    repetitions   INTEGER DEFAULT 0,
    next_review   TEXT NOT NULL,
    last_reviewed TEXT,
    created_at    TEXT NOT NULL,
    updated_at    TEXT NOT NULL
);
"""


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(CREATE_CARDS_TABLE)
        conn.commit()
