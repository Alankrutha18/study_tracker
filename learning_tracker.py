def calculate_total_minutes(sessions):
    total_count = 0
    for session in sessions:
        total_count = total_count + session["duration_time"]
    return total_count
def get_topic():
    while True:
        topic = input("What did you study? ").strip()
        if topic != "":
            return topic
        else:
            print("Please enter a topic.")
def get_duration():
    while True:
        try:
            duration_minutes = int(input("How many minutes did you study? "))
            if duration_minutes > 0:
                return duration_minutes
            else:
                print("Study time must be greater than zero.")
        except ValueError:
            print("Please enter a whole number, such as 50.")
def get_notes():
    notes = input("any notes on the topic you studied?")
    return notes
def create_session():
    topic = get_topic()
    duration_minutes = get_duration()
    notes = get_notes()
    return{
        "topic": topic,
        "duration_time": duration_minutes,
        "notes": notes
    }

def list_sessions(sessions):
    if len(sessions) == 0:
        print("No study sessions yet.")
        return
    for session in sessions:
        print(session["topic"], ":", session["duration_time"],  "minutes","|","Notes:", session["notes"])

def show_menu():
    print("\nStudy Tracker")
    print("1. Add a session")
    print("2. View sessions")
    print("3. View total minutes")
    print("4. Exit")

session_1 = {"topic": "programming", "duration_time": 120, "notes": "Today we are learning Python Programming Language"}
session_2 = {"topic": "databases", "duration_time": 90, "notes": "Today we are learning SQL"}
sessions =[]
sessions.append(session_1)
sessions.append(session_2)
# new_session = create_session()
while True:
    show_menu()
    choice = input("Choose an option: ").strip()
    if choice == "1":
        print("Add a session selected")
        new_session = create_session()
        sessions.append(new_session)
    elif choice == "2":
        print("View sessions selected")
        list_sessions(sessions)
    elif choice == "3":
        print("View total minutes selected")
        total_minutes = calculate_total_minutes(sessions)
        print("Total minutes studied:", total_minutes)
    elif choice == "4":
        print("Goodbye!")
        break
    else:
        print("Invalid Selection , Select from menu options only")
