"""Command-line interface for the study tracker.

Usage:
    python -m study_tracker log --subject LeetCode --minutes 45 --topic "binary search"
    python -m study_tracker today
    python -m study_tracker stats
    python -m study_tracker streak
"""

from __future__ import annotations

import argparse
from datetime import date, timedelta

from .store import StudyStore


def _fmt_minutes(minutes: int) -> str:
    hours, mins = divmod(minutes, 60)
    return f"{hours}h {mins}m" if hours else f"{mins}m"


def cmd_log(args: argparse.Namespace) -> None:
    store = StudyStore()
    session = store.log(
        subject=args.subject,
        minutes=args.minutes,
        topic=args.topic or "",
        notes=args.notes or "",
        day=args.day,
    )
    print(f"Logged {_fmt_minutes(session.minutes)} of {session.subject} on {session.day}")
    if session.topic:
        print(f"  topic: {session.topic}")


def cmd_today(args: argparse.Namespace) -> None:
    sessions = StudyStore().today()
    if not sessions:
        print("No study sessions logged today yet. Go get one in!")
        return
    total = sum(s.minutes for s in sessions)
    print(f"Today ({date.today().isoformat()}): {_fmt_minutes(total)} across {len(sessions)} sessions\n")
    for s in sessions:
        label = f"{s.subject} — {s.topic}" if s.topic else s.subject
        print(f"  • {label}: {_fmt_minutes(s.minutes)}")


def cmd_stats(args: argparse.Namespace) -> None:
    store = StudyStore()
    by_subject = store.minutes_by_subject()
    if not by_subject:
        print("No sessions logged yet. Log your first one with: python -m study_tracker log --help")
        return
    print("All-time by subject:")
    for subject, minutes in by_subject.items():
        print(f"  {subject:<20} {_fmt_minutes(minutes)}")
    print("\nLast 7 days:")
    for day, minutes in store.minutes_by_day(7).items():
        bar = "█" * max(1, minutes // 15)
        print(f"  {day}  {_fmt_minutes(minutes):>8}  {bar}")


def cmd_streak(args: argparse.Namespace) -> None:
    streak = StudyStore().streak()
    day_word = "day" if streak == 1 else "days"
    print(f"Current study streak: {streak} {day_word} 🔥" if streak else "No streak yet — log a session to start one!")


def cmd_subjects(args: argparse.Namespace) -> None:
    subjects = StudyStore().subjects()
    print("Subjects so far:" if subjects else "No subjects yet.")
    for subject in subjects:
        print(f"  • {subject}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="study_tracker", description="Track your study sessions.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_log = sub.add_parser("log", help="Log a study session.")
    p_log.add_argument("--subject", required=True, help="e.g. LeetCode, System Design, GenAI")
    p_log.add_argument("--minutes", required=True, type=int, help="How long you studied")
    p_log.add_argument("--topic", default="", help="What you covered")
    p_log.add_argument("--notes", default="", help="Optional notes")
    p_log.add_argument("--day", default=None, help="Date as YYYY-MM-DD (default: today)")
    p_log.set_defaults(func=cmd_log)

    p_today = sub.add_parser("today", help="Show today's sessions.")
    p_today.set_defaults(func=cmd_today)

    p_stats = sub.add_parser("stats", help="Show totals by subject and last 7 days.")
    p_stats.set_defaults(func=cmd_stats)

    p_streak = sub.add_parser("streak", help="Show your current study streak.")
    p_streak.set_defaults(func=cmd_streak)

    p_subjects = sub.add_parser("subjects", help="List subjects you've studied.")
    p_subjects.set_defaults(func=cmd_subjects)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
