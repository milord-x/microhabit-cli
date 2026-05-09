from pathlib import Path
from unittest.mock import patch

from microhabit.storage import export_habits


SAMPLE_HABITS = [
    {
        "name": "read",
        "created_at": "2026-05-01",
        "completed_dates": ["2026-05-09", "2026-05-10"],
        "category": "health",
        "tags": ["morning", "books"],
    },
    {
        "name": "code",
        "created_at": "2026-05-01",
        "completed_dates": [],
    },
]


def test_export_json(tmp_path: Path):
    with patch("microhabit.storage.load_habits") as mock:
        mock.return_value = SAMPLE_HABITS
        result = export_habits("json")
        assert '"name": "read"' in result
        assert '"name": "code"' in result


def test_export_json_default(tmp_path: Path):
    with patch("microhabit.storage.load_habits") as mock:
        mock.return_value = SAMPLE_HABITS
        result = export_habits()
        assert '"name": "read"' in result


def test_export_csv(tmp_path: Path):
    with patch("microhabit.storage.load_habits") as mock:
        mock.return_value = SAMPLE_HABITS
        result = export_habits("csv")
        assert "name,category,tags,created_at,streak,completions" in result
        assert 'read,health,"morning, books",2026-05-01' in result
        assert "code,,,2026-05-01" in result


def test_export_csv_empty(tmp_path: Path):
    with patch("microhabit.storage.load_habits") as mock:
        mock.return_value = []
        result = export_habits("csv")
        lines = result.strip().split("\n")
        assert len(lines) == 1
        assert lines[0] == "name,category,tags,created_at,streak,completions"


def test_export_json_empty(tmp_path: Path):
    with patch("microhabit.storage.load_habits") as mock:
        mock.return_value = []
        result = export_habits("json")
        assert result == "[]"


def test_export_invalid_format(tmp_path: Path):
    with patch("microhabit.storage.load_habits") as mock:
        mock.return_value = []
        try:
            export_habits("xml")
            assert False, "expected ValueError"
        except ValueError as e:
            assert "Unsupported format" in str(e)
