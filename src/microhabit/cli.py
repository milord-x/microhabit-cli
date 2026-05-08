import argparse
import sys

from microhabit.storage import (
    add_habit,
    complete_habit,
    get_streak,
    load_habits,
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
    add_p.set_defaults(func=_cmd_add)

    done_p = sub.add_parser("done", help="Mark a habit as done today")
    done_p.add_argument("name", help="Habit name")
    done_p.set_defaults(func=_cmd_done)

    list_p = sub.add_parser("list", help="List all habits")
    list_p.set_defaults(func=_cmd_list)

    return parser


def _cmd_add(args: argparse.Namespace) -> int:
    result = add_habit(args.name)
    if result is None:
        print(f"Habit already exists: {args.name}")
        return 1
    print(f"Habit added: {args.name}")
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
    if not habits:
        print("No habits found.")
        return 0
    for h in habits:
        streak = get_streak(h)
        count = len(h.get("completed_dates", []))
        print(f"{h['name']} - streak: {streak}, completions: {count}")
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
