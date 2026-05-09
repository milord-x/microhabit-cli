from datetime import date
from unittest.mock import patch

from microhabit.notifications import get_habits_due_today, show_reminders


def test_get_habits_due_today_returns_habits_not_done():
    today_str = date.today().isoformat()
    habits = [
        {"name": "read", "created_at": "2026-05-01", "completed_dates": []},
        {"name": "code", "created_at": "2026-05-01", "completed_dates": [today_str]},
    ]
    with patch("microhabit.notifications.load_habits", return_value=habits):
        due = get_habits_due_today()
        assert len(due) == 1
        assert due[0]["name"] == "read"


def test_get_habits_due_today_empty_when_all_done():
    today_str = date.today().isoformat()
    habits = [
        {"name": "read", "created_at": "2026-05-01", "completed_dates": [today_str]},
    ]
    with patch("microhabit.notifications.load_habits", return_value=habits):
        due = get_habits_due_today()
        assert due == []


def test_get_habits_due_today_empty_when_no_habits():
    with patch("microhabit.notifications.load_habits", return_value=[]):
        due = get_habits_due_today()
        assert due == []


def test_show_reminders_output_when_habits_due(capsys):
    today_str = date.today().isoformat()
    habits = [
        {"name": "read", "created_at": "2026-05-01", "completed_dates": []},
        {"name": "code", "created_at": "2026-05-01", "completed_dates": [today_str]},
    ]
    with patch("microhabit.notifications.load_habits", return_value=habits):
        result = show_reminders()
        captured = capsys.readouterr()
        assert result == 1
        assert "Reminder: 1 habit(s) not done today:" in captured.out
        assert "  - read" in captured.out


def test_show_reminders_no_output_when_all_done(capsys):
    today_str = date.today().isoformat()
    habits = [
        {"name": "read", "created_at": "2026-05-01", "completed_dates": [today_str]},
    ]
    with patch("microhabit.notifications.load_habits", return_value=habits):
        result = show_reminders()
        captured = capsys.readouterr()
        assert result == 0
        assert captured.out == ""


def test_show_reminders_no_output_when_no_habits(capsys):
    with patch("microhabit.notifications.load_habits", return_value=[]):
        result = show_reminders()
        captured = capsys.readouterr()
        assert result == 0
        assert captured.out == ""


def test_cli_reminders_shown_on_startup(capsys):
    with (
        patch("microhabit.notifications.load_habits") as mock_load,
        patch("sys.argv", ["microhabit", "list"]),
    ):
        mock_load.return_value = [
            {"name": "read", "created_at": "2026-05-01", "completed_dates": []},
        ]
        from microhabit.cli import main

        result = main()
        captured = capsys.readouterr()
        assert "Reminder:" in captured.out
