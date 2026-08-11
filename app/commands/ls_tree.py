import os
import sys
import zlib

from app.utils import blob_filepath


def ls_tree(target: str, name_only: bool) -> None:
    filepath = blob_filepath(target)
    _validate_ls_tree_args(target, filepath)

    file_bytes = _extract_file_bytes(filepath)
    decompressed_bytes = zlib.decompress(file_bytes)
    entries = _parse_tree_object_bytes(decompressed_bytes)

    names = entries
    if name_only:
        names = [e[1] for e in entries]

    return "\n".join(names)


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


def _parse_tree_object_bytes(object_bytes: bytes) -> str:
    split_bytes = object_bytes.split(b"\0")
    header_bytes = split_bytes[0]
    content_bytes = split_bytes[1:]

    object_type, size = header_bytes.split(b" ")

    # print(object_bytes)
    # print(content_bytes)

    entries = []
    for idx in range(len(content_bytes) - 1):
        # print(f"loop {idx} of {len(content_bytes) - 1}")
        # print(content_bytes[idx])
        if idx == 0:
            mode, name = content_bytes[idx].split(b" ")
        else:
            # print(content_bytes[idx][20:])
            mode, name = content_bytes[idx][20:].split(b" ")
        sha = content_bytes[idx + 1][:20]
        entries.append((mode.decode(), name.decode(), sha.hex()))

    return entries
