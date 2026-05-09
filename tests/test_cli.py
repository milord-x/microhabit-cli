import os
import sys
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


def test_add_with_category_via_cli(capsys):
    with patch("microhabit.cli.add_habit") as mock_add:
        mock_add.return_value = {
            "name": "read",
            "created_at": "2026-05-09",
            "completed_dates": [],
            "category": "health",
        }
        with patch("sys.argv", ["microhabit", "add", "read", "--category", "health"]):
            result = main()
            captured = capsys.readouterr()
            assert result == 0
            assert "category: health" in captured.out


def test_add_with_tags_via_cli(capsys):
    with patch("microhabit.cli.add_habit") as mock_add:
        mock_add.return_value = {
            "name": "read",
            "created_at": "2026-05-09",
            "completed_dates": [],
            "tags": ["morning", "books"],
        }
        with patch(
            "sys.argv", ["microhabit", "add", "read", "--tags", "morning", "books"]
        ):
            result = main()
            captured = capsys.readouterr()
            assert result == 0
            assert "tags: morning, books" in captured.out


def test_list_with_category_filter(capsys):
    habits = [
        {
            "name": "read",
            "created_at": "2026-05-01",
            "completed_dates": [],
            "category": "health",
        },
    ]
    with (
        patch("microhabit.cli.load_habits") as mock_load,
        patch("microhabit.cli.get_streak") as mock_streak,
        patch("sys.argv", ["microhabit", "list", "--category", "health"]),
    ):
        mock_load.return_value = habits
        mock_streak.return_value = 0
        result = main()
        captured = capsys.readouterr()
        assert result == 0
        assert "read" in captured.out
        assert "category: health" in captured.out


def test_parser_has_set_category_subcommand():
    parser = build_parser()
    subs = {
        a.dest: a for a in parser._subparsers._actions if hasattr(a, "_name_parser_map")
    }
    setcat_action = subs["command"]
    assert "set-category" in setcat_action._name_parser_map


def test_parser_has_set_tags_subcommand():
    parser = build_parser()
    subs = {
        a.dest: a for a in parser._subparsers._actions if hasattr(a, "_name_parser_map")
    }
    settag_action = subs["command"]
    assert "set-tags" in settag_action._name_parser_map


def test_set_category_via_cli(capsys):
    with patch("microhabit.cli.set_category") as mock_set:
        mock_set.return_value = {"name": "read", "category": "health"}
        with patch("sys.argv", ["microhabit", "set-category", "read", "health"]):
            result = main()
            captured = capsys.readouterr()
            assert result == 0
            assert "Category set: read -> health" in captured.out


def test_parser_has_export_subcommand():
    parser = build_parser()
    subs = {
        a.dest: a for a in parser._subparsers._actions if hasattr(a, "_name_parser_map")
    }
    export_action = subs["command"]
    assert "export" in export_action._name_parser_map


def test_set_tags_via_cli(capsys):
    with patch("microhabit.cli.set_tags") as mock_set:
        mock_set.return_value = {"name": "read", "tags": ["morning"]}
        with patch("sys.argv", ["microhabit", "set-tags", "read", "morning"]):
            result = main()
            captured = capsys.readouterr()
            assert result == 0
            assert "Tags set: read -> morning" in captured.out


def test_storage_path_flag_passed_to_storage(capsys):
    with (
        patch("microhabit.cli.set_storage_path") as mock_set,
        patch("microhabit.cli.load_habits", return_value=[]),
        patch("sys.argv", ["microhabit", "--storage-path", "/tmp/test.json", "list"]),
    ):
        main()
        mock_set.assert_called_once_with("/tmp/test.json")


def test_storage_path_flag_removed_from_argv(capsys):
    with (
        patch("microhabit.cli.set_storage_path"),
        patch("microhabit.cli.load_habits", return_value=[]),
        patch("sys.argv", ["microhabit", "--storage-path", "/tmp/test.json", "list"]),
    ):
        main()
        assert "--storage-path" not in sys.argv
        assert "/tmp/test.json" not in sys.argv


def test_env_var_microhabit_path(capsys):
    with (
        patch("microhabit.cli.set_storage_path") as mock_set,
        patch("microhabit.cli.load_habits", return_value=[]),
        patch("sys.argv", ["microhabit", "list"]),
        patch.dict(os.environ, {"MICROHABIT_PATH": "/env/test.json"}),
    ):
        main()
        mock_set.assert_called_once_with("/env/test.json")


def test_cli_flag_overrides_env_var(capsys):
    with (
        patch("microhabit.cli.set_storage_path") as mock_set,
        patch("microhabit.cli.load_habits", return_value=[]),
        patch("sys.argv", ["microhabit", "--storage-path", "/cli/test.json", "list"]),
        patch.dict(os.environ, {"MICROHABIT_PATH": "/env/test.json"}),
    ):
        main()
        mock_set.assert_called_once_with("/cli/test.json")
