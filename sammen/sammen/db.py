"""SQLite storage. One local file, no external service."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from sammen.matching import Profile

DATABASE_PATH = Path(__file__).resolve().parent.parent / "data" / "sammen.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    looking_for TEXT NOT NULL,
    city TEXT NOT NULL,
    meeting_mode TEXT NOT NULL,
    about TEXT NOT NULL,
    verified INTEGER NOT NULL DEFAULT 0
);
"""


def connect(database_path: Path = DATABASE_PATH) -> sqlite3.Connection:
    """
    Open the database and create the table if it is missing.

    Parameters
    ----------
    database_path : Path, default=DATABASE_PATH
        Location of the SQLite file

    Returns
    -------
    sqlite3.Connection
        Connection with rows accessible by column name

    Raises
    ------
    sqlite3.Error
        If the file cannot be opened or created
    """
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute(SCHEMA)
    return connection


def row_to_profile(row: sqlite3.Row) -> Profile:
    """Convert a database row into a Profile."""
    return Profile(
        id=row["id"],
        name=row["name"],
        role=row["role"],
        looking_for=[role for role in row["looking_for"].split(",") if role],
        city=row["city"],
        meeting_mode=row["meeting_mode"],
        about=row["about"],
        verified=bool(row["verified"]),
    )


def add_profile(
    connection: sqlite3.Connection,
    name: str,
    role: str,
    looking_for: list[str],
    city: str,
    meeting_mode: str,
    about: str,
    verified: bool = False,
) -> int:
    """
    Store a new profile.

    Returns
    -------
    int
        Id of the new profile
    """
    cursor = connection.execute(
        "INSERT INTO profiles (name, role, looking_for, city, meeting_mode, about, verified) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (name, role, ",".join(looking_for), city, meeting_mode, about, int(verified)),
    )
    connection.commit()
    return int(cursor.lastrowid)


def get_profile(connection: sqlite3.Connection, profile_id: int) -> Profile | None:
    """Return one profile, or None if the id does not exist."""
    row = connection.execute("SELECT * FROM profiles WHERE id = ?", (profile_id,)).fetchone()
    return row_to_profile(row) if row else None


def list_profiles(connection: sqlite3.Connection) -> list[Profile]:
    """Return all profiles."""
    rows = connection.execute("SELECT * FROM profiles ORDER BY id").fetchall()
    return [row_to_profile(row) for row in rows]
