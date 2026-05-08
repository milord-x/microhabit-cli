from microhabit.cli import build_parser


def test_build_parser():
    parser = build_parser()
    assert parser.prog == "microhabit"
