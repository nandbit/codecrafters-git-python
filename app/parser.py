import argparse


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pit",
        description="A toy implementation of a subset of git in Python.",
    )
    subparsers = parser.add_subparsers(dest="command")

    _setup_cat_file_parser(subparsers)
    _setup_init_parser(subparsers)
    _setup_hash_object_parser(subparsers)
    _setup_ls_tree_parser(subparsers)
    _setup_write_tree_parser(subparsers)

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
        dest="cat_file_target",
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


def _setup_hash_object_parser(
    subparsers: argparse._SubParsersAction,
) -> None:
    hash_object_parser = subparsers.add_parser("hash-object")
    hash_object_parser.add_argument(
        dest="hash_object_target",
        help="Content to hash.",
        type=str,
        nargs="?",
        action="store",
    )
    hash_object_parser.add_argument(
        "-w",
        "--write",
        dest="hash_object_write",
        help="Whether to write the hashed object into the objects directory.",
        action="store_true",
    )
    hash_object_parser.add_argument(
        "--stdin",
        dest="hash_object_stdin",
        help="Whether the content to be hashed comes from stdin.",
        action="store_true",
    )


def _setup_ls_tree_parser(
    subparsers: argparse._SubParsersAction,
) -> None:
    ls_tree_parser = subparsers.add_parser("ls-tree")
    ls_tree_parser.add_argument(
        dest="ls_tree_target",
        help="Tree object to inspect.",
        type=str,
        nargs="?",
        action="store",
    )
    ls_tree_parser.add_argument(
        "--name-only",
        dest="ls_tree_name_only",
        help='List only filenames (instead of the "long" output), one per line.',
        action="store_true",
    )


def _setup_write_tree_parser(
    subparsers: argparse.ArgumentParser,
) -> None:
    write_tree_parser = subparsers.add_parser("write-tree")
