from datetime import date, timedelta
from unittest.mock import patch

from microhabit.visuals import render_calendar


SAMPLE_HABITS = [
    {
        "name": "read",
        "created_at": "2026-05-01",
        "completed_dates": [],
    },
    {
        "name": "meditate",
        "created_at": "2026-05-01",
        "completed_dates": [
            (date.today() - timedelta(days=i)).isoformat() for i in range(3)
        ],
    },
]


def test_calendar_no_habits():
    with patch("microhabit.visuals.load_habits") as mock:
        mock.return_value = []
        result = render_calendar()
        assert result == "No habits found."


def test_calendar_with_habits():
    with patch("microhabit.visuals.load_habits") as mock:
        mock.return_value = SAMPLE_HABITS
        result = render_calendar(days=7)
        assert "Habit Calendar (last 7 days)" in result
        assert "read" in result
        assert "meditate" in result
        assert "streak:" in result


def test_calendar_custom_days():
    with patch("microhabit.visuals.load_habits") as mock:
        mock.return_value = SAMPLE_HABITS
        result = render_calendar(days=14)
        assert "Habit Calendar (last 14 days)" in result


def test_calendar_header_length():
    with patch("microhabit.visuals.load_habits") as mock:
        mock.return_value = SAMPLE_HABITS
        result = render_calendar(days=7)
        lines = result.split("\n")
        today = date.today()
        start = today - timedelta(days=6)
        expected_headers = " ".join(
            ["M", "T", "W", "T", "F", "S", "S"][(start + timedelta(days=i)).weekday()]
            for i in range(7)
        )
        assert expected_headers in lines[2]
