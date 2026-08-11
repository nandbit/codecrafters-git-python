import hashlib
import os
import sys
import zlib

from app.utils import blob_filepath


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
    filepath = blob_filepath(hash)

    # Create the subdirectory in objects directory
    os.mkdir(file_dir)

    # Compress contents and write
    compressed_content = zlib.compress(header + content)

    with open(filepath, "wb") as f:
        f.write(compressed_content)

    return hash


def _validate_hash_object_args(target: str, write: bool, stdin: bool) -> None:
    if target is None:
        raise ValueError("No target supplied.")
        sys.exit()

    if not os.path.exists(target):
        print(f"Error: no file {target} found.")
        sys.exit()


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
