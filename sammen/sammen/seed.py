"""Fill the database with invented demo profiles: python -m sammen.seed"""

from __future__ import annotations

import sqlite3

from sammen import db

# All people and organisations below are invented for the demo.
DEMO_PROFILES = [
    ("Freja Lind", "cofounder", ["cofounder", "investor"], "Copenhagen", "either",
     "Biochemist building lab automation software. Need a technical co-founder with robotics and python experience.", True),
    ("Mikkel Aagaard", "cofounder", ["cofounder"], "Copenhagen", "in_person",
     "Robotics engineer, python and hardware. Want to start a company in lab automation or biotech.", True),
    ("Nordlys Ventures", "investor", ["cofounder", "company"], "Copenhagen", "either",
     "Pre-seed fund for European biotech and lab automation startups.", True),
    ("Clara Voss", "job_seeker", ["company"], "Munich", "video",
     "Data scientist with healthcare experience, looking for a role in a European health startup.", True),
    ("Alpenblick Health", "company", ["job_seeker", "investor"], "Munich", "either",
     "Health startup hiring a data scientist to build patient analytics.", True),
    ("Jonas Berg", "job_seeker", ["company"], "Stockholm", "either",
     "Product designer focused on privacy and trust in consumer apps.", False),
]


def seed(connection: sqlite3.Connection) -> int:
    """
    Insert the demo profiles if the database is empty.

    Returns
    -------
    int
        Number of profiles inserted
    """
    if db.list_profiles(connection):
        return 0
    for name, role, looking_for, city, meeting_mode, about, verified in DEMO_PROFILES:
        db.add_profile(connection, name, role, looking_for, city, meeting_mode, about, verified)
    return len(DEMO_PROFILES)


if __name__ == "__main__":
    try:
        with db.connect() as connection:
            print(f"Inserted {seed(connection)} demo profiles")
    except sqlite3.Error as error:
        raise SystemExit(f"Could not seed the database: {error}")
