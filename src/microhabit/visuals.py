from datetime import date, timedelta

from microhabit.color import bold, green, red
from microhabit.storage import get_streak, load_habits

WEEKDAYS = ["M", "T", "W", "T", "F", "S", "S"]


def _day_block(date_str: str, completed_set: set[str]) -> str:
    if date_str in completed_set:
        return green("\u2588")
    return red("\u2591")


def render_calendar(days: int = 30) -> str:
    habits = load_habits()
    if not habits:
        return "No habits found."

    today = date.today()
    start = today - timedelta(days=days - 1)
    date_strs = [(start + timedelta(days=i)).isoformat() for i in range(days)]

    lines: list[str] = []
    lines.append(f"Habit Calendar (last {days} days)")
    lines.append("")

    header = "      " + " ".join(
        WEEKDAYS[(start + timedelta(days=i)).weekday()] for i in range(days)
    )
    lines.append(header)

    for h in habits:
        completed = set(h.get("completed_dates", []))
        blocks = "".join(_day_block(d, completed) for d in date_strs)
        streak = get_streak(h)
        name = h["name"]
        if len(name) > 8:
            name = name[:7] + "\u2026"
        padded_name = name.ljust(6)
        line = f"{padded_name} {blocks}  (streak: {streak})"
        lines.append(line)

    return "\n".join(lines)
