from pathlib import Path
import argparse
import shlex
import sys

from microhabit.color import bold, cyan, green, red
from microhabit.notifications import show_reminders
from microhabit.storage import (
    add_habit,
    complete_habit,
    export_habits,
    get_habits_by_category,
    get_stats,
    get_streak,
    load_habits,
    remove_habit,
    rename_habit,
    set_category,
    set_tags,
)
from microhabit.visuals import render_calendar

try:
    import readline

    HAS_READLINE = True
except ImportError:
    HAS_READLINE = False

COMMANDS: dict[str, tuple] = {}


def _cmd(name: str, help_text: str):
    def decorator(func):
        COMMANDS[name] = (func, help_text)
        return func

    return decorator


@_cmd("help", "Show this help message")
def _handle_help(args: list[str]) -> None:
    print("Available commands:")
    for name in sorted(COMMANDS):
        _, help_text = COMMANDS[name]
        print(f"  {name:<20} {help_text}")


@_cmd("exit", "Exit the interactive shell")
def _handle_exit(args: list[str]) -> None:
    print("Goodbye!")
    sys.exit(0)


@_cmd("quit", "Exit the interactive shell")
def _handle_quit(args: list[str]) -> None:
    _handle_exit(args)


@_cmd("add", "Add a new habit: add <name> [--category CAT] [--tags TAG ...]")
def _handle_add(args: list[str]) -> None:
    parser = argparse.ArgumentParser(prog="add", add_help=False)
    parser.add_argument("name")
    parser.add_argument("--category")
    parser.add_argument("--tags", nargs="*", default=None)
    try:
        parsed = parser.parse_args(args)
    except SystemExit:
        return
    result = add_habit(parsed.name, category=parsed.category, tags=parsed.tags)
    if result is None:
        print(red(f"Habit already exists: {parsed.name}"))
        return
    parts = [f"Habit added: {bold(parsed.name)}"]
    if parsed.category:
        parts.append(f"category: {cyan(parsed.category)}")
    if parsed.tags:
        parts.append(f"tags: {', '.join(parsed.tags)}")
    print(" ".join(parts))


@_cmd("done", "Mark a habit as done today: done <name>")
def _handle_done(args: list[str]) -> None:
    if not args:
        print(red("Usage: done <name>"))
        return
    name = args[0]
    result = complete_habit(name)
    if result is None:
        print(red(f"Habit not found: {name}"))
        return
    print(green(f"Habit marked done: {bold(name)}"))


@_cmd("list", "List habits: list [--category CAT]")
def _handle_list(args: list[str]) -> None:
    parser = argparse.ArgumentParser(prog="list", add_help=False)
    parser.add_argument("--category")
    try:
        parsed = parser.parse_args(args)
    except SystemExit:
        return
    habits = load_habits()
    if parsed.category:
        habits = get_habits_by_category(habits, parsed.category)
    if not habits:
        print("No habits found.")
        return
    for h in habits:
        streak = get_streak(h)
        count = len(h.get("completed_dates", []))
        streak_str = green(str(streak)) if streak > 0 else red(str(streak))
        parts = [f"{bold(h['name'])} - streak: {streak_str}, completions: {count}"]
        if h.get("category"):
            parts.append(f"category: {cyan(h['category'])}")
        if h.get("tags"):
            parts.append(f"tags: {', '.join(h['tags'])}")
        print(" | ".join(parts))


@_cmd("remove", "Remove a habit: remove <name>")
def _handle_remove(args: list[str]) -> None:
    if not args:
        print(red("Usage: remove <name>"))
        return
    name = args[0]
    result = remove_habit(name)
    if result is None:
        print(red(f"Habit not found: {name}"))
        return
    print(f"Habit removed: {bold(name)}")


@_cmd("rename", "Rename a habit: rename <old_name> <new_name>")
def _handle_rename(args: list[str]) -> None:
    if len(args) < 2:
        print(red("Usage: rename <old_name> <new_name>"))
        return
    old_name, new_name = args[0], args[1]
    result = rename_habit(old_name, new_name)
    if result is None:
        habits = load_habits()
        if any(h["name"] == old_name for h in habits):
            print(red(f"Habit already exists: {new_name}"))
        else:
            print(red(f"Habit not found: {old_name}"))
        return
    print(f"Habit renamed: {bold(old_name)} -> {bold(new_name)}")


@_cmd("stats", "Show progress summary")
def _handle_stats(args: list[str]) -> None:
    stats = get_stats()
    print(f"Total habits: {green(str(stats['total_habits']))}")
    print(f"Total completions: {green(str(stats['total_completions']))}")
    print(f"Longest streak: {green(str(stats['longest_streak']))}")


@_cmd("set-category", "Set habit category: set-category <name> <category>")
def _handle_set_category(args: list[str]) -> None:
    if len(args) < 2:
        print(red("Usage: set-category <name> <category>"))
        return
    name, category = args[0], args[1]
    result = set_category(name, category)
    if result is None:
        print(red(f"Habit not found: {name}"))
        return
    print(f"Category set: {bold(name)} -> {cyan(category)}")


@_cmd("set-tags", "Set habit tags: set-tags <name> <tag> [<tag> ...]")
def _handle_set_tags(args: list[str]) -> None:
    if len(args) < 2:
        print(red("Usage: set-tags <name> <tag> [<tag> ...]"))
        return
    name = args[0]
    tags = args[1:]
    result = set_tags(name, tags)
    if result is None:
        print(red(f"Habit not found: {name}"))
        return
    print(f"Tags set: {bold(name)} -> {', '.join(tags)}")


@_cmd("export", "Export habits: export [--format json|csv] [--output FILE]")
def _handle_export(args: list[str]) -> None:
    parser = argparse.ArgumentParser(prog="export", add_help=False)
    parser.add_argument("--format", choices=["csv", "json"], default="json")
    parser.add_argument("--output")
    try:
        parsed = parser.parse_args(args)
    except SystemExit:
        return
    data = export_habits(parsed.format)
    if parsed.output:
        Path(parsed.output).write_text(data, encoding="utf-8")
        print(f"Exported to {parsed.output}")
    else:
        print(data, end="")


@_cmd("calendar", "Show habit completion calendar: calendar [--days N]")
def _handle_calendar(args: list[str]) -> None:
    parser = argparse.ArgumentParser(prog="calendar", add_help=False)
    parser.add_argument("--days", type=int, default=30)
    try:
        parsed = parser.parse_args(args)
    except SystemExit:
        return
    calendar = render_calendar(days=parsed.days)
    print(calendar)


def _setup_completion() -> None:
    if not HAS_READLINE:
        return
    commands = sorted(COMMANDS.keys())

    def completer(text: str, state: int) -> str | None:
        options = [c for c in commands if c.startswith(text)]
        if state < len(options):
            return options[state]
        return None

    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)


def run_shell() -> None:
    _setup_completion()
    print(bold("MicroHabit Interactive Shell"))
    print("Type 'help' for commands, 'exit' to quit.")
    print()
    show_reminders()
    while True:
        try:
            line = input("microhabit> ").strip()
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print()
            continue
        if not line:
            continue
        parts = shlex.split(line)
        cmd = parts[0].lower()
        cmd_args = parts[1:]
        if cmd in COMMANDS:
            handler, _ = COMMANDS[cmd]
            try:
                handler(cmd_args)
            except SystemExit:
                break
            except Exception as e:
                print(red(f"Error: {e}"))
        else:
            print(red(f"Unknown command: {cmd}"))
