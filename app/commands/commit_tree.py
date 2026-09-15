import hashlib
import os
import zlib

from app.commands.hash_object import (
    _construct_header,
    blob_filepath,
)
from app.config import GIT_OBJECTS_DIRECTORY


def commit_tree(hash: str, parent_commit_hash: str, message: str) -> None:
    content = (
        f"tree {hash}\n"
        + f"parent {parent_commit_hash}\n"
        + "author John Doe <john@example.com> 1234567890 +0000\n"
        + "committer John Doe <john@example.com> 1234567890 +0000\n"
        + "\n"
        + message
        + "\n"
    )
    content_bytes = bytes(content, "utf-8")
    header_bytes = _construct_header(content_bytes, "commit")

    store = header_bytes + content_bytes
    h = hashlib.sha1()
    h.update(store)

    object_hash = h.hexdigest()[:40]
    file_dir = os.path.join(GIT_OBJECTS_DIRECTORY, object_hash[:2])
    filepath = blob_filepath(object_hash)

    os.makedirs(file_dir, exist_ok=True)

    compressed_header = zlib.compress(header_bytes + content_bytes)
    with open(filepath, "wb") as f:
        f.write(compressed_header)

    return object_hash
