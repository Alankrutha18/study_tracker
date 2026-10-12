"""JSON-backed storage for study sessions.

Sessions are kept in a single JSON file (default: ~/.study_tracker/sessions.json,
overridable with the STUDY_TRACKER_DATA env var) so the whole thing works with
zero setup and no database.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path


def _default_data_path() -> Path:
    env = os.environ.get("STUDY_TRACKER_DATA")
    if env:
        return Path(env).expanduser()
    return Path.home() / ".study_tracker" / "sessions.json"


@dataclass
class StudySession:
    """One study session."""

    subject: str
    minutes: int
    topic: str = ""
    notes: str = ""
    day: str = field(default_factory=lambda: date.today().isoformat())
    created_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "StudySession":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


class StudyStore:
    """Load, append, and query study sessions from a JSON file."""

    def __init__(self, path: Path | str | None = None) -> None:
        self.path = Path(path).expanduser() if path else _default_data_path()
        self._sessions: list[StudySession] | None = None

    # -- persistence -----------------------------------------------------
    def _load(self) -> list[StudySession]:
        if self._sessions is None:
            if self.path.exists():
                with self.path.open() as f:
                    raw = json.load(f)
                self._sessions = [StudySession.from_dict(item) for item in raw]
            else:
                self._sessions = []
        return self._sessions

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w") as f:
            json.dump([s.to_dict() for s in self._load()], f, indent=2)

    # -- writes ----------------------------------------------------------
    def log(self, subject: str, minutes: int, topic: str = "", notes: str = "", day: str | None = None) -> StudySession:
        if minutes <= 0:
            raise ValueError("minutes must be positive")
        session = StudySession(
            subject=subject.strip(),
            minutes=minutes,
            topic=topic.strip(),
            notes=notes.strip(),
            day=day or date.today().isoformat(),
        )
        self._load().append(session)
        self._save()
        return session

    # -- reads -----------------------------------------------------------
    def all(self) -> list[StudySession]:
        return list(self._load())

    def on_day(self, day: str | date) -> list[StudySession]:
        day_str = day.isoformat() if isinstance(day, date) else day
        return [s for s in self._load() if s.day == day_str]

    def today(self) -> list[StudySession]:
        return self.on_day(date.today())

    def subjects(self) -> list[str]:
        return sorted({s.subject for s in self._load()})

    def minutes_by_subject(self, since: str | None = None) -> dict[str, int]:
        totals: dict[str, int] = {}
        for s in self._load():
            if since and s.day < since:
                continue
            totals[s.subject] = totals.get(s.subject, 0) + s.minutes
        return dict(sorted(totals.items(), key=lambda kv: kv[1], reverse=True))

    def minutes_by_day(self, days: int = 7) -> dict[str, int]:
        cutoff = (date.today() - timedelta(days=days - 1)).isoformat()
        totals: dict[str, int] = {}
        for s in self._load():
            if s.day >= cutoff:
                totals[s.day] = totals.get(s.day, 0) + s.minutes
        return dict(sorted(totals.items()))

    def streak(self) -> int:
        """Consecutive days with at least one session, ending today or yesterday."""
        studied = {s.day for s in self._load()}
        if not studied:
            return 0
        cursor = date.today()
        if cursor.isoformat() not in studied:
            cursor -= timedelta(days=1)
        count = 0
        while cursor.isoformat() in studied:
            count += 1
            cursor -= timedelta(days=1)
        return count
