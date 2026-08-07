import argparse
import hashlib
import os
import sys
import zlib


def parse_command(namespace: argparse.Namespace) -> None:
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


def init() -> str:
    os.mkdir(".git")
    os.mkdir(".git/objects")
    os.mkdir(".git/refs")
    with open(".git/HEAD", "w") as f:
        f.write("ref: refs/heads/main\n")
    print("Initialized git directory")


def _validate_cat_file_args(target: str, filepath: str) -> None:
    if target is None:
        raise ValueError("No target supplied.")
        sys.exit()

    if not os.path.exists(filepath):
        print(f"Error: no file {filepath} found.")
        sys.exit()


def cat_file(target: str) -> str:
    subdir = target[:2]
    filename = target[2:]
    filepath = os.path.join(f".git/objects/{subdir}/{filename}")

    _validate_cat_file_args(target, filepath)

    with open(filepath, "rb") as file:
        byte_data = file.read()
        decompressed_data = zlib.decompress(byte_data)
        stripped_data = decompressed_data.split(b"\0")[1]
        decoded_data = stripped_data.decode("utf-8")

        return decoded_data


def _validate_hash_object_args(target: str, write: bool, stdin: bool) -> None:
    if target is None:
        raise ValueError("No target supplied.")
        sys.exit()

    if not os.path.exists(target):
        print(f"Error: no file {target} found.")
        sys.exit()


def hash_object(
    target: str,
    write: bool,
    stdin: bool,
    content_type: str,
) -> str:
    _validate_hash_object_args(target, write, stdin)

    content = _extract_file_bytes(target)
    header = _construct_header(content, "blob")
    hash = _create_hash(
        content,
        header,
    )

    if not write:
        return hash

    # Create file to write to
    file_dir = os.path.join(".git/objects/", hash[:2])
    filepath = os.path.join(".git/objects/", hash[:2], hash[2:])

    # Create the subdirectory in objects directory
    os.mkdir(file_dir)

    # Compress contents and write
    compressed_content = zlib.compress(header + content)

    with open(filepath, "wb") as f:
        f.write(compressed_content)

    return hash


def _create_hash(content: bytes, header: bytes) -> str:
    store = header + content
    h = hashlib.sha1()
    h.update(store)

    return h.hexdigest()[:40]


def _extract_file_bytes(target: str) -> bytes:
    with open(target, "rb") as f:
        return f.read()


def _construct_header(content: bytes, content_type: str) -> bytes:
    # Content type can be blob, tree, commit, tag
    header = content_type + " " + str(len(content)) + "\0"

    return bytes(header, encoding="utf-8")
