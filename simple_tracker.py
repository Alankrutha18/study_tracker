"""A simple, beginner-friendly study tracker using plain dictionaries.

Run it with: python simple_tracker.py
"""

# Step 1: Create dictionaries for study sessions
session1 = {
    "topic": "Python Basics",
    "duration": 45,
    "notes": "Learned variables, data types, and operators",
}

session2 = {
    "topic": "Python Dictionaries",
    "duration": 60,
    "notes": "Practiced dictionary methods and loops",
}

# Step 2: Store all sessions in a list
sessions = [session1, session2]


# Step 3: Helper functions
def add_session(sessions, topic, duration, notes=""):
    sessions.append({"topic": topic, "duration": duration, "notes": notes})


def total_study_time(sessions):
    return sum(s["duration"] for s in sessions)


# Step 4: Print a summary
if __name__ == "__main__":
    print(f"Sessions: {len(sessions)}")
    print(f"Total study time: {total_study_time(sessions)} minutes")
    for s in sessions:
        print(f"- {s['topic']}: {s['duration']} min \u2014 {s['notes']}")
