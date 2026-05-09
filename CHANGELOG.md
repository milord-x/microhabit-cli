# Changelog

## 2026-05-09

- Initialized Python package structure.
- Added minimal CLI entry point with argparse.
- Added basic import test.
- Implemented JSON storage module with load, save, add, complete, streak.
- Added 16 tests covering storage operations and edge cases.
- Wired CLI add, list, done commands to storage module.
- Added 8 tests covering CLI command dispatch and output.
- Updated README to reflect working CLI commands.

## 2026-05-09 (run 4)

- Added remove_habit, rename_habit, get_stats to storage module.
- Added remove, rename, stats CLI commands.
- Added 8 storage tests for new functions.
- Added 8 CLI tests for new commands.
- All 41 tests pass.

## 2026-05-09 (run 5)

- Added notifications module with daily reminder logic.
- Integrated reminders into CLI entry point.
- Added 7 notification tests.
- All 48 tests pass.

## 2026-05-09 (run 6)

- Added optional category and tags fields to habit creation.
- Added --category and --tags options to add command.
- Added --category filter to list command.
- Added set-category and set-tags CLI commands.
- Added 12 storage tests and 5 CLI tests.
- All 65 tests pass.

## 2026-05-10

- Added colorized terminal output using ANSI codes.
- Created color module with green/red/yellow/cyan/bold helpers.
- Colors applied to list, stats, done, add, remove, rename, set-category,
  set-tags commands and reminders.
- Color auto-disabled when not a TTY or when NO_COLOR is set.
- Added 14 color module tests.
- All 79 tests pass.

## 2026-05-10 (run 8)

- Added export_habits function to storage module.
- Added export subcommand with --format (csv|json) and --output flags.
- Added 6 export tests.
- All 86 tests pass.

## 2026-05-10 (run 9)

- Added set_storage_path function to storage module.
- Added --storage-path global CLI flag.
- Added MICROHABIT_PATH env var support (flag overrides env var).
- Added 5 tests for configurable storage path.
- Updated README with storage path customization docs.
- All 91 tests pass.
