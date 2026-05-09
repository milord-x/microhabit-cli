import os
import sys


def _supports_color() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    return sys.stdout.isatty()


def green(text: str) -> str:
    if _supports_color():
        return f"\033[32m{text}\033[0m"
    return text


def yellow(text: str) -> str:
    if _supports_color():
        return f"\033[33m{text}\033[0m"
    return text


def red(text: str) -> str:
    if _supports_color():
        return f"\033[31m{text}\033[0m"
    return text


def cyan(text: str) -> str:
    if _supports_color():
        return f"\033[36m{text}\033[0m"
    return text


def bold(text: str) -> str:
    if _supports_color():
        return f"\033[1m{text}\033[0m"
    return text
