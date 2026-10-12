# study_tracker

A tiny, zero-dependency Python CLI to track your study sessions: log what you
studied and for how long, then review totals by subject, daily history, and
your current streak.

## Quick start

```bash
# log a session
python -m study_tracker log --subject LeetCode --minutes 45 --topic "binary search"

# see today's sessions
python -m study_tracker today

# totals by subject + last 7 days chart
python -m study_tracker stats

# current streak
python -m study_tracker streak
```

## How it works

Sessions are stored as JSON in `~/.study_tracker/sessions.json` (override with
the `STUDY_TRACKER_DATA` env var). No database, no setup.

## Commands

| Command | What it does |
| --- | --- |
| `log --subject S --minutes M [--topic T] [--notes N] [--day YYYY-MM-DD]` | Log a study session |
| `today` | List today's sessions |
| `stats` | All-time totals by subject + last 7 days |
| `streak` | Consecutive study days |
| `subjects` | List subjects studied so far |

## Run tests

```bash
python -m unittest discover tests
```
