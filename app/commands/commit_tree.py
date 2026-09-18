import hashlib
import os
import time
import zlib

from app.commands.config import (
    ConfigError,
    ConfigFileMissingError,
    UserInfo,
    get_user_info,
)
from app.commands.hash_object import (
    _construct_header,
    blob_filepath,
)
from app.config import GIT_OBJECTS_DIRECTORY


def commit_tree(hash: str, parent_commit_hash: str, message: str) -> None:
    try:
        user_info = get_user_info()
    except ConfigFileMissingError or ConfigError:
        user_info = UserInfo(name="John Doe", email="john@example.com")
    timestamp = int(time.time())
    timezone_value = -int(time.timezone / 3600) * 100
    timezone = (
        str(timezone_value).zfill(4)
        if timezone_value < 0
        else "+" + str(timezone_value).zfill(4)
    )
    content = (
        f"tree {hash}\n"
        + f"parent {parent_commit_hash}\n"
        + f"author {user_info.name} <{user_info.email}> {timestamp} {timezone}\n"
        + f"committer {user_info.name} <{user_info.email}> {timestamp} {timezone}\n"
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
