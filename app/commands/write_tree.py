import os
import zlib
from hashlib import sha1
from pathlib import Path

from app.commands.hash_object import _construct_header
from app.config import GIT_OBJECTS_DIRECTORY, GIT_ROOT_DIRECTORY
from app.utils import get_file_mode


def write_tree(directory: str = "./") -> None:
    tree_object_bytes_hash = _get_staged_targets(directory)
    print(tree_object_bytes_hash.hex())


def _get_staged_targets(directory: str) -> list[str]:
    entries = {}
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            filepath = Path(os.path.join(dirpath, f))
            mode, hash = _process_file(filepath)
            entries[f] = {"hash": hash, "mode": mode}
        for d in dirnames:
            if d == GIT_ROOT_DIRECTORY:
                continue
            dirpath = Path(os.path.join(directory, d))
            hash = _get_staged_targets(dirpath)
            entries[d] = {"hash": hash, "mode": "40000"}
        break

    entries_sorted = dict(sorted(entries.items()))
    entries_list = [
        bytes(v["mode"], "utf-8")
        + b" "
        + bytes(k, "utf-8")
        + b"\x00"
        + v["hash"]
        for k, v in entries_sorted.items()
    ]

    entries_bytes = b"".join(entries_list)
    header = bytes(f"tree {len(entries_bytes)}\x00", "utf-8")
    output = header + entries_bytes
    output_compressed = zlib.compress(output)

    h = sha1()
    h.update(output)
    new_tree_object_hex_hash = h.hexdigest()[:40]
    new_tree_object_bytes_hash = h.digest()[:20]
    new_tree_object_dir = (
        f"{GIT_OBJECTS_DIRECTORY}/{new_tree_object_hex_hash[:2]}"
    )
    new_tree_object_path = (
        f"{new_tree_object_dir}/{new_tree_object_hex_hash[2:]}"
    )

    os.makedirs(new_tree_object_dir, exist_ok=True)
    with open(new_tree_object_path, "wb") as f:
        f.write(output_compressed)

    return new_tree_object_bytes_hash


def _process_file(filepath: Path) -> tuple[str, str]:
    mode = get_file_mode(filepath)
    hash = None
    h = sha1()
    with open(filepath, "rb") as f:
        content = f.read()
        h.update(_construct_header(content, "blob"))
        h.update(content)
        hash = h.digest()[:20]

    return mode, hash
