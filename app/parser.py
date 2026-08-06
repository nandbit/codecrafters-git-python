import argparse


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pit",
        description="A toy implementation of a subset of git in Python.",
    )
    subparsers = parser.add_subparsers(dest="command")

    _setup_cat_file_parser(subparsers)
    _setup_init_parser(subparsers)

    return parser


def _setup_init_parser(subparsers: argparse._SubParsersAction) -> None:
    init_parser = subparsers.add_parser("init")
    init_parser.add_argument(
        dest="init_dest",
        help="Specify the name of the repository to initialize.",
        type=str,
        nargs="?",
        action="store",
    )


def _setup_cat_file_parser(subparsers: argparse._SubParsersAction) -> None:
    cat_file_parser = subparsers.add_parser("cat-file")
    cat_file_parser.add_argument(
        dest="cat_file_dest",
        help="Supply the hash of the file to print its contents.",
        type=str,
        nargs="?",
        action="store",
    )
    cat_file_parser.add_argument(
        "-p",
        dest="cat_file_pretty",
        help="Whether to pretty print the contents of the object based on its type.",
        action="store_true",
    )
