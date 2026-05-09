from datetime import date

from microhabit.storage import load_habits


def get_habits_due_today() -> list[dict]:
    today_str = date.today().isoformat()
    habits = load_habits()
    due = []
    for h in habits:
        if today_str not in h.get("completed_dates", []):
            due.append(h)
    return due


def show_reminders() -> int:
    due = get_habits_due_today()
    if not due:
        return 0
    print(f"Reminder: {len(due)} habit(s) not done today:")
    for h in due:
        print(f"  - {h['name']}")
    return 1
