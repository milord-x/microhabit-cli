# MicroHabit CLI

A terminal habit tracker with streaks, reminders, and local JSON storage.

## Status

Core features implemented: habit storage, completion tracking, streak calculation.

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
microhabit done "read 20 pages"
microhabit list
```

## Storage

Habits are stored in `~/.microhabit/habits.json` as a JSON file.
The data directory is created automatically on first use.

## Limitations

- CLI commands are not wired yet (storage module is ready).
- Single-user, local only.
