from unittest.mock import patch

from microhabit.cli import build_parser, main


def test_parser_has_add_subcommand():
    parser = build_parser()
    subs = {
        a.dest: a for a in parser._subparsers._actions if hasattr(a, "_name_parser_map")
    }
    add_action = subs["command"]
    assert "add" in add_action._name_parser_map


def test_parser_has_done_subcommand():
    parser = build_parser()
    subs = {
        a.dest: a for a in parser._subparsers._actions if hasattr(a, "_name_parser_map")
    }
    done_action = subs["command"]
    assert "done" in done_action._name_parser_map


def test_parser_has_list_subcommand():
    parser = build_parser()
    subs = {
        a.dest: a for a in parser._subparsers._actions if hasattr(a, "_name_parser_map")
    }
    list_action = subs["command"]
    assert "list" in list_action._name_parser_map


def test_add_habit_via_cli(capsys):
    with patch("microhabit.cli.add_habit") as mock_add:
        mock_add.return_value = {
            "name": "read",
            "created_at": "2026-05-09",
            "completed_dates": [],
        }
        with patch("sys.argv", ["microhabit", "add", "read"]):
            result = main()
            captured = capsys.readouterr()
            assert result == 0
            assert "Habit added: read" in captured.out


def test_add_duplicate_via_cli(capsys):
    with patch("microhabit.cli.add_habit") as mock_add:
        mock_add.return_value = None
        with patch("sys.argv", ["microhabit", "add", "read"]):
            result = main()
            captured = capsys.readouterr()
            assert result == 1
            assert "already exists" in captured.out


def test_done_habit_via_cli(capsys):
    with patch("microhabit.cli.complete_habit") as mock_done:
        mock_done.return_value = {
            "name": "read",
            "created_at": "2026-05-01",
            "completed_dates": ["2026-05-09"],
        }
        with patch("sys.argv", ["microhabit", "done", "read"]):
            result = main()
            captured = capsys.readouterr()
            assert result == 0
            assert "Habit marked done: read" in captured.out


def test_done_nonexistent_via_cli(capsys):
    with patch("microhabit.cli.complete_habit") as mock_done:
        mock_done.return_value = None
        with patch("sys.argv", ["microhabit", "done", "read"]):
            result = main()
            captured = capsys.readouterr()
            assert result == 1
            assert "not found" in captured.out


def test_list_empty(capsys):
    with patch("microhabit.cli.load_habits") as mock_load:
        mock_load.return_value = []
        with patch("sys.argv", ["microhabit", "list"]):
            result = main()
            captured = capsys.readouterr()
            assert result == 0
            assert "No habits found" in captured.out


def test_parser_has_remove_subcommand():
    parser = build_parser()
    subs = {
        a.dest: a for a in parser._subparsers._actions if hasattr(a, "_name_parser_map")
    }
    remove_action = subs["command"]
    assert "remove" in remove_action._name_parser_map


def test_parser_has_rename_subcommand():
    parser = build_parser()
    subs = {
        a.dest: a for a in parser._subparsers._actions if hasattr(a, "_name_parser_map")
    }
    rename_action = subs["command"]
    assert "rename" in rename_action._name_parser_map


def test_parser_has_stats_subcommand():
    parser = build_parser()
    subs = {
        a.dest: a for a in parser._subparsers._actions if hasattr(a, "_name_parser_map")
    }
    stats_action = subs["command"]
    assert "stats" in stats_action._name_parser_map


def test_remove_habit_via_cli(capsys):
    with patch("microhabit.cli.remove_habit") as mock_remove:
        mock_remove.return_value = {
            "name": "read",
            "created_at": "2026-05-01",
            "completed_dates": [],
        }
        with patch("sys.argv", ["microhabit", "remove", "read"]):
            result = main()
            captured = capsys.readouterr()
            assert result == 0
            assert "Habit removed: read" in captured.out


def test_remove_nonexistent_via_cli(capsys):
    with patch("microhabit.cli.remove_habit") as mock_remove:
        mock_remove.return_value = None
        with patch("sys.argv", ["microhabit", "remove", "read"]):
            result = main()
            captured = capsys.readouterr()
            assert result == 1
            assert "not found" in captured.out


def test_rename_habit_via_cli(capsys):
    with patch("microhabit.cli.rename_habit") as mock_rename:
        mock_rename.return_value = {
            "name": "reading",
            "created_at": "2026-05-01",
            "completed_dates": [],
        }
        with patch("sys.argv", ["microhabit", "rename", "read", "reading"]):
            result = main()
            captured = capsys.readouterr()
            assert result == 0
            assert "Habit renamed: read -> reading" in captured.out


def test_rename_nonexistent_via_cli(capsys):
    with patch("microhabit.cli.rename_habit") as mock_rename:
        mock_rename.return_value = None
        mock_rename.side_effect = None
        with (
            patch("microhabit.cli.load_habits") as mock_load,
            patch("sys.argv", ["microhabit", "rename", "read", "reading"]),
        ):
            mock_load.return_value = []
            result = main()
            captured = capsys.readouterr()
            assert result == 1
            assert "not found" in captured.out


def test_rename_to_existing_via_cli(capsys):
    with patch("microhabit.cli.rename_habit") as mock_rename:
        mock_rename.return_value = None
        with (
            patch("microhabit.cli.load_habits") as mock_load,
            patch("sys.argv", ["microhabit", "rename", "read", "code"]),
        ):
            mock_load.return_value = [
                {"name": "read", "created_at": "2026-05-01", "completed_dates": []},
                {"name": "code", "created_at": "2026-05-01", "completed_dates": []},
            ]
            result = main()
            captured = capsys.readouterr()
            assert result == 1
            assert "already exists" in captured.out


def test_stats_via_cli(capsys):
    with patch("microhabit.cli.get_stats") as mock_stats:
        mock_stats.return_value = {
            "total_habits": 3,
            "total_completions": 7,
            "longest_streak": 5,
        }
        with patch("sys.argv", ["microhabit", "stats"]):
            result = main()
            captured = capsys.readouterr()
            assert result == 0
            assert "Total habits: 3" in captured.out
            assert "Total completions: 7" in captured.out
            assert "Longest streak: 5" in captured.out


def test_list_with_habits(capsys):
    habits = [
        {"name": "read", "created_at": "2026-05-01", "completed_dates": ["2026-05-09"]},
        {"name": "code", "created_at": "2026-05-01", "completed_dates": []},
    ]
    with (
        patch("microhabit.cli.load_habits") as mock_load,
        patch("microhabit.cli.get_streak") as mock_streak,
    ):
        mock_load.return_value = habits
        mock_streak.side_effect = [1, 0]
        with patch("sys.argv", ["microhabit", "list"]):
            result = main()
            captured = capsys.readouterr()
            assert result == 0
            assert "read" in captured.out
            assert "streak: 1" in captured.out
            assert "completions: 1" in captured.out
            assert "code" in captured.out
            assert "streak: 0" in captured.out
            assert "completions: 0" in captured.out
