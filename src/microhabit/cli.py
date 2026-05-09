import argparse
import sys

from microhabit.notifications import show_reminders
from microhabit.storage import (
    add_habit,
    complete_habit,
    get_habits_by_category,
    get_stats,
    get_streak,
    load_habits,
    remove_habit,
    rename_habit,
    set_category,
    set_tags,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="microhabit",
        description="A small terminal habit tracker.",
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

    settag_p = sub.add_parser("set-tags", help="Set habit tags")
    settag_p.add_argument("name", help="Habit name")
    settag_p.add_argument("tags", nargs="+", help="Tag values")
    settag_p.set_defaults(func=_cmd_set_tags)

    return parser


def _cmd_add(args: argparse.Namespace) -> int:
    result = add_habit(args.name, category=args.category, tags=args.tags)
    if result is None:
        print(f"Habit already exists: {args.name}")
        return 1
    parts = [f"Habit added: {args.name}"]
    if args.category:
        parts.append(f"category: {args.category}")
    if args.tags:
        parts.append(f"tags: {', '.join(args.tags)}")
    print(" ".join(parts))
    return 0


def _cmd_done(args: argparse.Namespace) -> int:
    result = complete_habit(args.name)
    if result is None:
        print(f"Habit not found: {args.name}")
        return 1
    print(f"Habit marked done: {args.name}")
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
        parts = [f"{h['name']} - streak: {streak}, completions: {count}"]
        if h.get("category"):
            parts.append(f"category: {h['category']}")
        if h.get("tags"):
            parts.append(f"tags: {', '.join(h['tags'])}")
        print(" | ".join(parts))
    return 0


def _cmd_remove(args: argparse.Namespace) -> int:
    result = remove_habit(args.name)
    if result is None:
        print(f"Habit not found: {args.name}")
        return 1
    print(f"Habit removed: {args.name}")
    return 0


def _cmd_rename(args: argparse.Namespace) -> int:
    result = rename_habit(args.old_name, args.new_name)
    if result is None:
        habits = load_habits()
        if any(h["name"] == args.old_name for h in habits):
            print(f"Habit already exists: {args.new_name}")
        else:
            print(f"Habit not found: {args.old_name}")
        return 1
    print(f"Habit renamed: {args.old_name} -> {args.new_name}")
    return 0


def _cmd_set_category(args: argparse.Namespace) -> int:
    result = set_category(args.name, args.category)
    if result is None:
        print(f"Habit not found: {args.name}")
        return 1
    print(f"Category set: {args.name} -> {args.category}")
    return 0


def _cmd_set_tags(args: argparse.Namespace) -> int:
    result = set_tags(args.name, args.tags)
    if result is None:
        print(f"Habit not found: {args.name}")
        return 1
    print(f"Tags set: {args.name} -> {', '.join(args.tags)}")
    return 0


def _cmd_stats(args: argparse.Namespace) -> int:
    stats = get_stats()
    print(f"Total habits: {stats['total_habits']}")
    print(f"Total completions: {stats['total_completions']}")
    print(f"Longest streak: {stats['longest_streak']}")
    return 0


def main() -> int:
    show_reminders()
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
