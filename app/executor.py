import argparse

from app.commands.cat_file import cat_file
from app.commands.hash_object import hash_object
from app.commands.init import init
from app.commands.ls_tree import ls_tree


def execute_command(namespace: argparse.Namespace) -> None:
    command = namespace.command

    if command == "init":
        init()
    elif command == "cat-file":
        output = cat_file(target=namespace.cat_file_target)

        print(output, end="")

    elif command == "hash-object":
        hash = hash_object(
            target=namespace.hash_object_target,
            write=namespace.hash_object_write,
            stdin=namespace.hash_object_stdin,
            # TODO: use this?
            content_type="blob",
        )
        print(hash)

    elif command == "ls-tree":
        output = ls_tree(
            target=namespace.ls_tree_target,
            name_only=namespace.ls_tree_name_only,
        )
        print(output)
