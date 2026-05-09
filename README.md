# MicroHabit CLI

A terminal habit tracker with streaks, reminders, and local JSON storage.

## Status

Core features implemented: habit storage, completion tracking, streak calculation, CLI commands.

## Quick Start

```bash
pip install -e .
microhabit --help
```

## Requirements

- Python 3.11+

## Usage

```bash
microhabit --help
microhabit add "read 20 pages"
microhabit add "meditate" --category health --tags morning
microhabit done "read 20 pages"
microhabit list
microhabit list --category health
microhabit remove "read 20 pages"
microhabit rename "read 20 pages" "read 30 pages"
microhabit stats
microhabit set-category "read 20 pages" learning
microhabit set-tags "read 20 pages" evening
```

## Reminders

Each time you run `microhabit`, it checks which habits are not yet completed today
and prints a colored reminder if any are due.

## Export

Habits can be exported to CSV or JSON:

```bash
microhabit export                    # JSON to stdout
microhabit export --format csv       # CSV to stdout
microhabit export --format json --output habits.json  # JSON to file
microhabit export --format csv --output habits.csv    # CSV to file
```

CSV columns: name, category, tags, created_at, streak, completions.

## Colorized Output

MicroHabit CLI uses ANSI color codes to highlight output in supported terminals:

- **Green** for completed habits and positive stats
- **Yellow** for reminders
- **Red** for errors and zero streaks
- **Cyan** for categories
- **Bold** for habit names

Color is automatically disabled when output is not a TTY or when the `NO_COLOR`
environment variable is set.

## Storage

Habits are stored in `~/.microhabit/habits.json` as a JSON file.
The data directory is created automatically on first use.

## Limitations

- Single-user, local only.
