from datetime import date, timedelta
from pathlib import Path
from unittest.mock import patch
import json
import tempfile

from microhabit.storage import (
    load_habits,
    save_habits,
    add_habit,
    complete_habit,
    get_streak,
)


def _test_path(tmp_path: Path) -> Path:
    return tmp_path / ".microhabit" / "habits.json"


def test_load_habits_empty_when_no_file(tmp_path: Path):
    with patch("microhabit.storage.HABIT_FILE", _test_path(tmp_path)):
        assert load_habits() == []


def test_save_and_load_habits(tmp_path: Path):
    habits = [{"name": "test", "created_at": "2026-05-09", "completed_dates": []}]
    with patch("microhabit.storage.HABIT_FILE", _test_path(tmp_path)):
        save_habits(habits)
        loaded = load_habits()
        assert loaded == habits


def test_add_habit(tmp_path: Path):
    with patch("microhabit.storage.HABIT_FILE", _test_path(tmp_path)):
        result = add_habit("read")
        assert result is not None
        assert result["name"] == "read"
        assert result["completed_dates"] == []
        habits = load_habits()
        assert len(habits) == 1


def test_add_duplicate_habit_returns_none(tmp_path: Path):
    with patch("microhabit.storage.HABIT_FILE", _test_path(tmp_path)):
        add_habit("read")
        result = add_habit("read")
        assert result is None
        habits = load_habits()
        assert len(habits) == 1


def test_complete_habit(tmp_path: Path):
    with patch("microhabit.storage.HABIT_FILE", _test_path(tmp_path)):
        add_habit("read")
        today_str = date.today().isoformat()
        result = complete_habit("read")
        assert result is not None
        assert today_str in result["completed_dates"]


def test_complete_habit_appends_date_once(tmp_path: Path):
    with patch("microhabit.storage.HABIT_FILE", _test_path(tmp_path)):
        add_habit("read")
        complete_habit("read")
        complete_habit("read")
        habits = load_habits()
        assert habits[0]["completed_dates"].count(date.today().isoformat()) == 1


def test_complete_nonexistent_habit_returns_none(tmp_path: Path):
    with patch("microhabit.storage.HABIT_FILE", _test_path(tmp_path)):
        result = complete_habit("nonexistent")
        assert result is None


def test_load_corrupted_json_returns_empty(tmp_path: Path):
    test_file = _test_path(tmp_path)
    test_file.parent.mkdir(parents=True, exist_ok=True)
    test_file.write_text("not json", encoding="utf-8")
    with patch("microhabit.storage.HABIT_FILE", test_file):
        assert load_habits() == []


def test_load_invalid_type_returns_empty(tmp_path: Path):
    test_file = _test_path(tmp_path)
    test_file.parent.mkdir(parents=True, exist_ok=True)
    test_file.write_text('{"not": "a list"}', encoding="utf-8")
    with patch("microhabit.storage.HABIT_FILE", test_file):
        assert load_habits() == []


def test_get_streak_zero_when_no_dates():
    habit = {"name": "test", "created_at": "2026-05-01", "completed_dates": []}
    assert get_streak(habit) == 0


def test_get_streak_today_only():
    today_str = date.today().isoformat()
    habit = {"name": "test", "created_at": "2026-05-01", "completed_dates": [today_str]}
    assert get_streak(habit) == 1


def test_get_streak_consecutive_days():
    today = date.today()
    dates = [(today - timedelta(days=i)).isoformat() for i in range(3)]
    habit = {"name": "test", "created_at": "2026-05-01", "completed_dates": dates}
    assert get_streak(habit) == 3


def test_get_streak_broken_streak():
    today = date.today()
    dates = [
        today.isoformat(),
        (today - timedelta(days=1)).isoformat(),
        (today - timedelta(days=3)).isoformat(),
    ]
    habit = {"name": "test", "created_at": "2026-05-01", "completed_dates": dates}
    assert get_streak(habit) == 2


def test_get_streak_yesterday_only():
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    habit = {"name": "test", "created_at": "2026-05-01", "completed_dates": [yesterday]}
    assert get_streak(habit) == 1


def test_get_streak_old_date_returns_zero():
    old = (date.today() - timedelta(days=5)).isoformat()
    habit = {"name": "test", "created_at": "2026-05-01", "completed_dates": [old]}
    assert get_streak(habit) == 0
