
"""Store monitoring measurements in a SQLite database."""

import sqlite3
from pathlib import Path


DATABASE_FILE = Path(__file__).resolve().parent / "monitoring.db"


def create_database():
    """Create the measurements table if it does not exist."""
    with sqlite3.connect(DATABASE_FILE) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS measurements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                hostname TEXT NOT NULL,
                metric TEXT NOT NULL,
                value REAL NOT NULL,
                unit TEXT NOT NULL
            )
        """)


def save_measurements(measurements):
    """Add measurements to the database without deleting old data."""
    create_database()

    with sqlite3.connect(DATABASE_FILE) as connection:
        for item in measurements:
            connection.execute(
                """
                INSERT INTO measurements
                (timestamp, hostname, metric, value, unit)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    item["timestamp"],
                    item["hostname"],
                    item["metric"],
                    item["value"],
                    item["unit"],
                ),
            )


def load_measurements():
    """Read all measurements from the database."""
    create_database()

    with sqlite3.connect(DATABASE_FILE) as connection:
        connection.row_factory = sqlite3.Row

        rows = connection.execute(
            """
            SELECT timestamp, hostname, metric, value, unit
            FROM measurements
            ORDER BY timestamp
            """
        ).fetchall()

    return [dict(row) for row in rows]
