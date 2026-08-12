import os
import sys
import zlib

from app.utils import blob_filepath


def ls_tree(target: str, name_only: bool) -> None:
    filepath = blob_filepath(target)
    _validate_ls_tree_args(target, filepath)

    file_bytes = _extract_file_bytes(filepath)
    decompressed_bytes = zlib.decompress(file_bytes)
    # entries = _parse_tree_object_bytes(decompressed_bytes)

    header_bytes = decompressed_bytes.split(b"\0")[0]
    object_type_bytes, size_bytes = header_bytes.split(b" ")
    object_type = object_type_bytes.decode()

    if object_type == "tree":
        entries = _parse_tree_object_bytes(decompressed_bytes)

    elif object_type == "commit":
        return _parse_commit_object_bytes(decompressed_bytes)

        if name_only:
            names = [e[1] for e in entries]

            return "\n".join(names)
    else:
        sys.exit("fatal: not a tree object")


def _validate_ls_tree_args(target: str, filepath: str) -> None:
    if target is None:
        raise ValueError("No target supplied.")
        sys.exit()

    if not os.path.exists(filepath):
        print(f"Error: no file {target} found.")
        sys.exit()


def _extract_file_bytes(target: str) -> bytes:
    with open(target, "rb") as f:
        return f.read()


def _parse_tree_object_bytes(object_bytes: bytes) -> list[str]:

    entries = []
    for idx in range(len(object_bytes) - 1):
        if idx == 0:
            mode, name = object_bytes[idx].split(b" ")
            continue
        print(object_bytes[idx])
        mode, name = object_bytes[idx][20:].split(b" ")
        sha = object_bytes[idx + 1][:20]
        entries.append((mode.decode(), name.decode(), sha.hex()))

    return entries


def _parse_commit_object_bytes(object_bytes: bytes) -> list[str]:
    split_bytes = object_bytes.split(b"\0")
    header_bytes = split_bytes[0]
    # Content in a commit object is NOT binary
    content = split_bytes[1].decode()

    split_content = str(content).split("\n")
    tree, tree_sha = split_content[0].split(" ")
    parent, parent_sha = split_content[1].split(" ")
    (
        author,
        author_name,
        author_email,
        author_timestamp,
        author_timezone,
    ) = split_content[2].split(" ")

    (
        commiter,
        commiter_name,
        commiter_email,
        commiter_timestamp,
        commiter_timezone,
    ) = split_content[3].split(" ")

    commit_message = split_content[4]

    return "\n".join(
        [
            f"{tree} {tree_sha}",
            f"{parent} {parent_sha}",
            f"{author} {author_name} {author_email} {author_timestamp} {author_timezone}",
            f"{commiter} {commiter_name} {commiter_email} {commiter_timestamp} {commiter_timezone}",
            "",
            f"{commit_message}",
        ]
    )
