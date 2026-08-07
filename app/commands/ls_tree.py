import os
import sys
import zlib

from app.utils import blob_filepath


def ls_tree(target: str, name_only: bool) -> None:
    filepath = blob_filepath(target)
    _validate_ls_tree_args(target, filepath)

    file_bytes = _extract_file_bytes(filepath)
    decompressed_bytes = zlib.decompress(file_bytes)
    _parse_tree_object_bytes(decompressed_bytes)
    # lines = decoded_data.split("\n")


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

    header = b""
    for int_byte in object_bytes:
        b = bytes([int_byte])
        if b.hex() == "00":
            break
        header += b

    print(header)
    object_type, size = header.split(b" ")

    objects_data = []
    for int_byte in object_bytes:
        object_data = b""
        b = bytes([int_byte])
        if b.hex() == "00":
            objects_data.append(object_data)
            object_data = b""

    return

    chunks = object_bytes.split(b"\0")
    print(f"Got {len(chunks)} chunks:")
    for chunk in chunks:
        print(chunk)
    header_bytes = chunks[0]
    header_object, size = header_bytes.split(b" ")

    object_bytes = []
    for idx in range(1, len(chunks) - 1, 2):
        mode_name = chunks[idx]
        sha = chunks[idx + 1]
        mode, name = mode_name.split(b" ")
        object_type = b"tree" if mode == b"40000" else b"blob"
        line = b" ".join([mode, object_type, sha, name])
        object_bytes.append(line)

    for ob in object_bytes:
        print(ob)
