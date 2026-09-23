"""A small SQLite exercise for checking appointment state consistency."""

import sqlite3
import unittest
from contextlib import closing

CHECK_SQL = """
SELECT
    slots.id,
    slots.capacity,
    slots.remaining,
    COUNT(appointments.id) AS reserved_count
FROM slots
LEFT JOIN appointments
    ON appointments.slot_id = slots.id
    AND appointments.status = 'reserved'
GROUP BY slots.id, slots.capacity, slots.remaining
HAVING slots.remaining + COUNT(appointments.id) != slots.capacity
    OR slots.remaining < 0
"""


def make_database(remaining):
    connection = sqlite3.connect(":memory:")
    connection.executescript(
        """
        CREATE TABLE slots (
            id TEXT PRIMARY KEY,
            capacity INTEGER NOT NULL,
            remaining INTEGER NOT NULL
        );
        CREATE TABLE appointments (
            id TEXT PRIMARY KEY,
            slot_id TEXT NOT NULL,
            status TEXT NOT NULL
        );
        INSERT INTO appointments VALUES ('appointment-01', 'slot-01', 'reserved');
        INSERT INTO appointments VALUES ('appointment-02', 'slot-01', 'cancelled');
        """
    )
    connection.execute(
        "INSERT INTO slots VALUES (?, ?, ?)",
        ("slot-01", 2, remaining),
    )
    return connection


def inconsistent_rows(connection):
    return connection.execute(CHECK_SQL).fetchall()


class StateCheckTests(unittest.TestCase):
    def test_consistent_state_has_no_inconsistent_rows(self):
        with closing(make_database(remaining=1)) as connection:
            self.assertEqual(inconsistent_rows(connection), [])

    def test_wrong_remaining_count_is_detected(self):
        with closing(make_database(remaining=2)) as connection:
            self.assertEqual(inconsistent_rows(connection), [("slot-01", 2, 2, 1)])


if __name__ == "__main__":
    unittest.main()
