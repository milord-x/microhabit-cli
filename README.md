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
and prints a reminder if any are due.

## Storage

Habits are stored in `~/.microhabit/habits.json` as a JSON file.
The data directory is created automatically on first use.

## Limitations

- Single-user, local only.
