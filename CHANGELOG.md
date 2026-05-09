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
