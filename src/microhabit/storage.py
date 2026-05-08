from datetime import date, datetime, timedelta
from pathlib import Path
import json

HABIT_FILE = Path.home() / ".microhabit" / "habits.json"


def _ensure_dir() -> None:
    HABIT_FILE.parent.mkdir(parents=True, exist_ok=True)


def _habit_file_path() -> Path:
    return HABIT_FILE


def load_habits() -> list[dict]:
    path = _habit_file_path()
    if not path.exists():
        return []
    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
        if not isinstance(data, list):
            return []
        return data
    except (json.JSONDecodeError, OSError):
        return []


def save_habits(habits: list[dict]) -> None:
    _ensure_dir()
    path = _habit_file_path()
    path.write_text(json.dumps(habits, indent=2), encoding="utf-8")


def add_habit(name: str) -> dict | None:
    habits = load_habits()
    if any(h["name"] == name for h in habits):
        return None
    today_str = date.today().isoformat()
    habit = {
        "name": name,
        "created_at": today_str,
        "completed_dates": [],
    }
    habits.append(habit)
    save_habits(habits)
    return habit


def complete_habit(name: str) -> dict | None:
    habits = load_habits()
    for h in habits:
        if h["name"] == name:
            today_str = date.today().isoformat()
            if today_str not in h["completed_dates"]:
                h["completed_dates"].append(today_str)
            save_habits(habits)
            return h
    return None


def get_streak(habit: dict) -> int:
    dates = sorted(set(habit.get("completed_dates", [])), reverse=True)
    if not dates:
        return 0
    today = date.today()
    last = datetime.strptime(dates[0], "%Y-%m-%d").date()
    if last != today and last != today - timedelta(days=1):
        return 0
    streak = 0
    check = last
    for d_str in dates:
        current = datetime.strptime(d_str, "%Y-%m-%d").date()
        if current != check:
            break
        streak += 1
        check -= timedelta(days=1)
    return streak
