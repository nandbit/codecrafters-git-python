import argparse
import os
import zlib


def parse_command(namespace: argparse.Namespace) -> None:
    command = namespace.command

    if command == "init":
        init()
    elif command == "cat-file":
        target = namespace.cat_file_dest
        if target is None:
            raise ValueError("Error: no object found.")
        cat_file(target)


def init() -> str:
    os.mkdir(".git")
    os.mkdir(".git/objects")
    os.mkdir(".git/refs")
    with open(".git/HEAD", "w") as f:
        f.write("ref: refs/heads/main\n")
    print("Initialized git directory")


def cat_file(name: str) -> str:
    subdir = name[:2]
    filename = name[2:]
    filepath = os.path.join(f".git/objects/{subdir}/{filename}")

    with open(filepath, "rb") as file:
        byte_data = file.read()
        decompressed_data = zlib.decompress(byte_data)
        stripped_data = decompressed_data.split(b"\0")[1]
        decoded_data = stripped_data.decode("utf-8")

        print(decoded_data, end="")
