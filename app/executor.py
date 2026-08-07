import argparse

from app.commands.cat_file import cat_file
from app.commands.hash_object import hash_object
from app.commands.init import init


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
