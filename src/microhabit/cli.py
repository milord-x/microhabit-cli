from pathlib import Path
import argparse
import os
import sys

from microhabit.color import bold, cyan, green, red, yellow
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
    set_storage_path,
    set_tags,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="microhabit",
        description="A small terminal habit tracker.",
    )
    parser.add_argument(
        "--storage-path",
        help="Path to habits JSON file (overrides MICROHABIT_PATH env var)",
    )
    sub = parser.add_subparsers(dest="command")
    sub.required = True

    add_p = sub.add_parser("add", help="Add a new habit")
    add_p.add_argument("name", help="Habit name")
    add_p.add_argument("--category", help="Habit category")
    add_p.add_argument("--tags", nargs="*", default=None, help="Habit tags")
    add_p.set_defaults(func=_cmd_add)

    done_p = sub.add_parser("done", help="Mark a habit as done today")
    done_p.add_argument("name", help="Habit name")
    done_p.set_defaults(func=_cmd_done)

    list_p = sub.add_parser("list", help="List habits")
    list_p.add_argument("--category", help="Filter by category")
    list_p.set_defaults(func=_cmd_list)

    remove_p = sub.add_parser("remove", help="Remove a habit")
    remove_p.add_argument("name", help="Habit name")
    remove_p.set_defaults(func=_cmd_remove)

    rename_p = sub.add_parser("rename", help="Rename a habit")
    rename_p.add_argument("old_name", help="Current habit name")
    rename_p.add_argument("new_name", help="New habit name")
    rename_p.set_defaults(func=_cmd_rename)

    stats_p = sub.add_parser("stats", help="Show progress summary")
    stats_p.set_defaults(func=_cmd_stats)

    setcat_p = sub.add_parser("set-category", help="Set habit category")
    setcat_p.add_argument("name", help="Habit name")
    setcat_p.add_argument("category", help="Category name")
    setcat_p.set_defaults(func=_cmd_set_category)

    export_p = sub.add_parser("export", help="Export habits to CSV or JSON")
    export_p.add_argument(
        "--format", choices=["csv", "json"], default="json", help="Output format"
    )
    export_p.add_argument("--output", help="Output file path (default: stdout)")
    export_p.set_defaults(func=_cmd_export)

    settag_p = sub.add_parser("set-tags", help="Set habit tags")
    settag_p.add_argument("name", help="Habit name")
    settag_p.add_argument("tags", nargs="+", help="Tag values")
    settag_p.set_defaults(func=_cmd_set_tags)

    return parser


def _cmd_add(args: argparse.Namespace) -> int:
    result = add_habit(args.name, category=args.category, tags=args.tags)
    if result is None:
        print(red(f"Habit already exists: {args.name}"))
        return 1
    parts = [f"Habit added: {bold(args.name)}"]
    if args.category:
        parts.append(f"category: {cyan(args.category)}")
    if args.tags:
        parts.append(f"tags: {', '.join(args.tags)}")
    print(" ".join(parts))
    return 0


def _cmd_done(args: argparse.Namespace) -> int:
    result = complete_habit(args.name)
    if result is None:
        print(red(f"Habit not found: {args.name}"))
        return 1
    print(green(f"Habit marked done: {bold(args.name)}"))
    return 0


def _cmd_list(args: argparse.Namespace) -> int:
    habits = load_habits()
    if args.category:
        habits = get_habits_by_category(habits, args.category)
    if not habits:
        print("No habits found.")
        return 0
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
    return 0


def _cmd_remove(args: argparse.Namespace) -> int:
    result = remove_habit(args.name)
    if result is None:
        print(red(f"Habit not found: {args.name}"))
        return 1
    print(f"Habit removed: {bold(args.name)}")
    return 0


def _cmd_rename(args: argparse.Namespace) -> int:
    result = rename_habit(args.old_name, args.new_name)
    if result is None:
        habits = load_habits()
        if any(h["name"] == args.old_name for h in habits):
            print(red(f"Habit already exists: {args.new_name}"))
        else:
            print(red(f"Habit not found: {args.old_name}"))
        return 1
    print(f"Habit renamed: {bold(args.old_name)} -> {bold(args.new_name)}")
    return 0


def _cmd_set_category(args: argparse.Namespace) -> int:
    result = set_category(args.name, args.category)
    if result is None:
        print(red(f"Habit not found: {args.name}"))
        return 1
    print(f"Category set: {bold(args.name)} -> {cyan(args.category)}")
    return 0


def _cmd_set_tags(args: argparse.Namespace) -> int:
    result = set_tags(args.name, args.tags)
    if result is None:
        print(red(f"Habit not found: {args.name}"))
        return 1
    print(f"Tags set: {bold(args.name)} -> {', '.join(args.tags)}")
    return 0


def _cmd_export(args: argparse.Namespace) -> int:
    data = export_habits(args.format)
    if args.output:
        Path(args.output).write_text(data, encoding="utf-8")
        print(f"Exported to {args.output}")
    else:
        print(data, end="")
    return 0


def _cmd_stats(args: argparse.Namespace) -> int:
    stats = get_stats()
    print(f"Total habits: {green(str(stats['total_habits']))}")
    print(f"Total completions: {green(str(stats['total_completions']))}")
    print(f"Longest streak: {green(str(stats['longest_streak']))}")
    return 0


def _resolve_storage_path_early() -> None:
    argv = sys.argv[1:]
    new_argv = []
    skip_next = False
    found_cli_flag = False
    for i, arg in enumerate(argv):
        if skip_next:
            skip_next = False
            continue
        if arg == "--storage-path" and i + 1 < len(argv):
            set_storage_path(argv[i + 1])
            found_cli_flag = True
            skip_next = True
            continue
        if arg.startswith("--storage-path="):
            set_storage_path(arg.split("=", 1)[1])
            found_cli_flag = True
            continue
        new_argv.append(arg)
    env_path = os.environ.get("MICROHABIT_PATH")
    if env_path and not found_cli_flag:
        set_storage_path(env_path)
    sys.argv[:] = [sys.argv[0]] + new_argv


def main() -> int:
    _resolve_storage_path_early()
    show_reminders()
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
