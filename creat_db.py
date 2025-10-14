"""Database initialization script.

Creates required tables if they do not already exist:
 - users: stores registered user meta data
 - attendance: (optional future use) normalized attendance log table

This script is idempotent (safe to run multiple times). It no longer drops
tables automatically to avoid accidental data loss.
"""

from __future__ import annotations
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'usersdatabase.db')

USER_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    major TEXT,
    sex TEXT CHECK(sex IN ('M','F') ) ,
    reg_time TEXT
);
"""

ATTENDANCE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    timestamp TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
"""

def init_db(path: str = DB_PATH) -> None:
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(USER_TABLE_SQL)
    cur.execute(ATTENDANCE_TABLE_SQL)
    conn.commit()
    conn.close()
    print(f"[OK] Database initialized at {path}")


if __name__ == "__main__":
    init_db()

