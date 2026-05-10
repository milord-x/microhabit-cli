from unittest.mock import patch

from microhabit.shell import COMMANDS, _setup_completion
from microhabit.cli import build_parser


def test_shell_has_all_commands():
    expected = {
        "help",
        "exit",
        "quit",
        "add",
        "done",
        "list",
        "remove",
        "rename",
        "stats",
        "set-category",
        "set-tags",
        "export",
        "calendar",
    }
    assert expected.issubset(set(COMMANDS.keys()))


def test_shell_help_output(capsys):
    handler, _ = COMMANDS["help"]
    handler([])
    captured = capsys.readouterr()
    assert "Available commands:" in captured.out
    assert "add" in captured.out
    assert "exit" in captured.out
    assert "help" in captured.out


def test_shell_unknown_command(capsys):
    from microhabit.shell import _cmd

    builtins = {"unknown": (lambda x: None, "test")}
    with patch.dict("microhabit.shell.COMMANDS", builtins, clear=False):
        pass
    handler, _ = COMMANDS["help"]
    handler([])
    captured = capsys.readouterr()
    assert "Available commands:" in captured.out


def test_shell_add_habit(capsys):
    with patch("microhabit.shell.add_habit") as mock_add:
        mock_add.return_value = {
            "name": "read",
            "created_at": "2026-05-10",
            "completed_dates": [],
        }
        handler, _ = COMMANDS["add"]
        handler(["read"])
        captured = capsys.readouterr()
        assert "Habit added: read" in captured.out


def test_shell_add_duplicate(capsys):
    with patch("microhabit.shell.add_habit") as mock_add:
        mock_add.return_value = None
        handler, _ = COMMANDS["add"]
        handler(["read"])
        captured = capsys.readouterr()
        assert "already exists" in captured.out


def test_shell_done_habit(capsys):
    with patch("microhabit.shell.complete_habit") as mock_done:
        mock_done.return_value = {
            "name": "read",
            "created_at": "2026-05-10",
            "completed_dates": ["2026-05-10"],
        }
        handler, _ = COMMANDS["done"]
        handler(["read"])
        captured = capsys.readouterr()
        assert "Habit marked done: read" in captured.out


def test_shell_done_no_args(capsys):
    handler, _ = COMMANDS["done"]
    handler([])
    captured = capsys.readouterr()
    assert "Usage: done" in captured.out


def test_shell_list_empty(capsys):
    with patch("microhabit.shell.load_habits") as mock_load:
        mock_load.return_value = []
        handler, _ = COMMANDS["list"]
        handler([])
        captured = capsys.readouterr()
        assert "No habits found" in captured.out


def test_shell_list_with_habits(capsys):
    habits = [
        {"name": "read", "created_at": "2026-05-01", "completed_dates": ["2026-05-10"]},
        {"name": "code", "created_at": "2026-05-01", "completed_dates": []},
    ]
    with (
        patch("microhabit.shell.load_habits") as mock_load,
        patch("microhabit.shell.get_streak") as mock_streak,
    ):
        mock_load.return_value = habits
        mock_streak.side_effect = [1, 0]
        handler, _ = COMMANDS["list"]
        handler([])
        captured = capsys.readouterr()
        assert "read" in captured.out
        assert "code" in captured.out


def test_shell_remove_habit(capsys):
    with patch("microhabit.shell.remove_habit") as mock_remove:
        mock_remove.return_value = {
            "name": "read",
            "created_at": "2026-05-01",
            "completed_dates": [],
        }
        handler, _ = COMMANDS["remove"]
        handler(["read"])
        captured = capsys.readouterr()
        assert "Habit removed: read" in captured.out


def test_shell_remove_no_args(capsys):
    handler, _ = COMMANDS["remove"]
    handler([])
    captured = capsys.readouterr()
    assert "Usage: remove" in captured.out


def test_shell_rename_habit(capsys):
    with patch("microhabit.shell.rename_habit") as mock_rename:
        mock_rename.return_value = {
            "name": "reading",
            "created_at": "2026-05-01",
            "completed_dates": [],
        }
        handler, _ = COMMANDS["rename"]
        handler(["read", "reading"])
        captured = capsys.readouterr()
        assert "Habit renamed: read -> reading" in captured.out


def test_shell_rename_too_few_args(capsys):
    handler, _ = COMMANDS["rename"]
    handler(["read"])
    captured = capsys.readouterr()
    assert "Usage: rename" in captured.out


def test_shell_stats(capsys):
    with patch("microhabit.shell.get_stats") as mock_stats:
        mock_stats.return_value = {
            "total_habits": 3,
            "total_completions": 7,
            "longest_streak": 5,
        }
        handler, _ = COMMANDS["stats"]
        handler([])
        captured = capsys.readouterr()
        assert "Total habits: 3" in captured.out
        assert "Total completions: 7" in captured.out
        assert "Longest streak: 5" in captured.out


def test_shell_set_category(capsys):
    with patch("microhabit.shell.set_category") as mock_set:
        mock_set.return_value = {"name": "read", "category": "health"}
        handler, _ = COMMANDS["set-category"]
        handler(["read", "health"])
        captured = capsys.readouterr()
        assert "Category set: read -> health" in captured.out


def test_shell_set_category_too_few_args(capsys):
    handler, _ = COMMANDS["set-category"]
    handler(["read"])
    captured = capsys.readouterr()
    assert "Usage: set-category" in captured.out


def test_shell_set_tags(capsys):
    with patch("microhabit.shell.set_tags") as mock_set:
        mock_set.return_value = {"name": "read", "tags": ["morning"]}
        handler, _ = COMMANDS["set-tags"]
        handler(["read", "morning"])
        captured = capsys.readouterr()
        assert "Tags set: read -> morning" in captured.out


def test_shell_set_tags_too_few_args(capsys):
    handler, _ = COMMANDS["set-tags"]
    handler(["read"])
    captured = capsys.readouterr()
    assert "Usage: set-tags" in captured.out


def test_shell_export_json(capsys):
    with patch("microhabit.shell.export_habits") as mock_export:
        mock_export.return_value = '{"habits": []}'
        handler, _ = COMMANDS["export"]
        handler([])
        captured = capsys.readouterr()
        assert '{"habits": []}' in captured.out


def test_shell_calendar(capsys):
    with patch("microhabit.shell.render_calendar") as mock_cal:
        mock_cal.return_value = "Habit Calendar (last 30 days)"
        handler, _ = COMMANDS["calendar"]
        handler([])
        captured = capsys.readouterr()
        assert "Habit Calendar" in captured.out


def test_shell_exit_prints_goodbye(capsys):
    import sys

    handler, _ = COMMANDS["exit"]
    with patch.object(sys, "exit") as mock_exit:
        handler([])
        captured = capsys.readouterr()
        assert "Goodbye!" in captured.out
        mock_exit.assert_called_once_with(0)


def test_shell_quit_aliases_exit():
    import sys

    handler_q, _ = COMMANDS["quit"]
    handler_e, _ = COMMANDS["exit"]
    with patch.object(sys, "exit") as mock_exit:
        handler_q([])
        handler_e([])
        assert mock_exit.call_count == 2
        assert mock_exit.call_args_list[0] == mock_exit.call_args_list[1]


def test_parser_has_shell_subcommand():
    parser = build_parser()
    subs = {
        a.dest: a for a in parser._subparsers._actions if hasattr(a, "_name_parser_map")
    }
    shell_action = subs["command"]
    assert "shell" in shell_action._name_parser_map


def test_shell_setup_completion_no_readline():
    orig = __import__("microhabit.shell", fromlist=["HAS_READLINE"]).HAS_READLINE
    with patch("microhabit.shell.HAS_READLINE", False):
        result = _setup_completion()
        assert result is None
