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


def add_habit(
    name: str, category: str | None = None, tags: list[str] | None = None
) -> dict | None:
    habits = load_habits()
    if any(h["name"] == name for h in habits):
        return None
    today_str = date.today().isoformat()
    habit = {
        "name": name,
        "created_at": today_str,
        "completed_dates": [],
    }
    if category is not None:
        habit["category"] = category
    if tags is not None:
        habit["tags"] = tags
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


def remove_habit(name: str) -> dict | None:
    habits = load_habits()
    for i, h in enumerate(habits):
        if h["name"] == name:
            removed = habits.pop(i)
            save_habits(habits)
            return removed
    return None


def rename_habit(old_name: str, new_name: str) -> dict | None:
    habits = load_habits()
    if any(h["name"] == new_name for h in habits):
        return None
    for h in habits:
        if h["name"] == old_name:
            h["name"] = new_name
            save_habits(habits)
            return h
    return None


def get_habits_by_category(habits: list[dict], category: str) -> list[dict]:
    return [h for h in habits if h.get("category") == category]


def set_category(name: str, category: str) -> dict | None:
    habits = load_habits()
    for h in habits:
        if h["name"] == name:
            h["category"] = category
            save_habits(habits)
            return h
    return None


def set_tags(name: str, tags: list[str]) -> dict | None:
    habits = load_habits()
    for h in habits:
        if h["name"] == name:
            h["tags"] = tags
            save_habits(habits)
            return h
    return None


def get_stats() -> dict:
    habits = load_habits()
    total = len(habits)
    total_completions = sum(len(h.get("completed_dates", [])) for h in habits)
    longest = 0
    for h in habits:
        s = get_streak(h)
        if s > longest:
            longest = s
    return {
        "total_habits": total,
        "total_completions": total_completions,
        "longest_streak": longest,
    }


def export_habits(fmt: str = "json") -> str:
    import io

    habits = load_habits()
    if fmt == "json":
        return json.dumps(habits, indent=2)
    elif fmt == "csv":
        import csv

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(
            ["name", "category", "tags", "created_at", "streak", "completions"]
        )
        for h in habits:
            writer.writerow(
                [
                    h["name"],
                    h.get("category", ""),
                    ", ".join(h.get("tags", [])),
                    h.get("created_at", ""),
                    get_streak(h),
                    len(h.get("completed_dates", [])),
                ]
            )
        return output.getvalue()
    else:
        raise ValueError(f"Unsupported format: {fmt}")


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
