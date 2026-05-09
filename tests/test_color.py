from unittest.mock import patch

from microhabit.color import _supports_color, bold, cyan, green, red, yellow


def test_supports_color_false_when_not_tty():
    with patch("sys.stdout.isatty", return_value=False):
        assert _supports_color() is False


def test_supports_color_false_when_no_color():
    with patch("sys.stdout.isatty", return_value=True):
        with patch.dict("os.environ", {"NO_COLOR": "1"}):
            assert _supports_color() is False


def test_supports_color_true_when_tty():
    with patch("sys.stdout.isatty", return_value=True):
        assert _supports_color() is True


def test_green_wraps_when_color_supported():
    with patch("sys.stdout.isatty", return_value=True):
        assert green("ok") == "\033[32mok\033[0m"


def test_green_plain_when_no_color():
    with patch("sys.stdout.isatty", return_value=False):
        assert green("ok") == "ok"


def test_red_wraps_when_color_supported():
    with patch("sys.stdout.isatty", return_value=True):
        assert red("err") == "\033[31merr\033[0m"


def test_red_plain_when_no_color():
    with patch("sys.stdout.isatty", return_value=False):
        assert red("err") == "err"


def test_yellow_wraps_when_color_supported():
    with patch("sys.stdout.isatty", return_value=True):
        assert yellow("warn") == "\033[33mwarn\033[0m"


def test_yellow_plain_when_no_color():
    with patch("sys.stdout.isatty", return_value=False):
        assert yellow("warn") == "warn"


def test_cyan_wraps_when_color_supported():
    with patch("sys.stdout.isatty", return_value=True):
        assert cyan("info") == "\033[36minfo\033[0m"


def test_cyan_plain_when_no_color():
    with patch("sys.stdout.isatty", return_value=False):
        assert cyan("info") == "info"


def test_bold_wraps_when_color_supported():
    with patch("sys.stdout.isatty", return_value=True):
        assert bold("name") == "\033[1mname\033[0m"


def test_bold_plain_when_no_color():
    with patch("sys.stdout.isatty", return_value=False):
        assert bold("name") == "name"


def test_empty_string_handling():
    with patch("sys.stdout.isatty", return_value=True):
        assert green("") == "\033[32m\033[0m"
