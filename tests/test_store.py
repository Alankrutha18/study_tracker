"""Basic tests for the study store."""

import tempfile
import unittest
from pathlib import Path

from study_tracker.store import StudyStore


class TestStudyStore(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = StudyStore(Path(self.tmp.name) / "sessions.json")

    def tearDown(self):
        self.tmp.cleanup()

    def test_log_and_reload(self):
        self.store.log("LeetCode", 45, topic="binary search")
        fresh = StudyStore(self.store.path)
        sessions = fresh.all()
        self.assertEqual(len(sessions), 1)
        self.assertEqual(sessions[0].subject, "LeetCode")
        self.assertEqual(sessions[0].minutes, 45)

    def test_log_rejects_non_positive_minutes(self):
        with self.assertRaises(ValueError):
            self.store.log("LeetCode", 0)

    def test_minutes_by_subject(self):
        self.store.log("LeetCode", 30)
        self.store.log("LeetCode", 15)
        self.store.log("System Design", 60)
        self.assertEqual(self.store.minutes_by_subject(), {"LeetCode": 45, "System Design": 60})

    def test_streak(self):
        from datetime import date, timedelta

        today = date.today()
        self.store.log("LeetCode", 20, day=(today - timedelta(days=1)).isoformat())
        self.store.log("LeetCode", 20, day=today.isoformat())
        self.assertEqual(self.store.streak(), 2)


if __name__ == "__main__":
    unittest.main()
