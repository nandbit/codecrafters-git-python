import os
import zlib
from hashlib import sha1
from pathlib import Path

from app.commands.hash_object import hash_object
from app.utils import get_file_mode


def write_tree() -> None:
    tree_object_hash = _get_staged_targets(directory="./")
    print(tree_object_hash)


def _get_staged_targets(directory: str) -> list[str]:
    entries = dict()
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            filepath = Path(os.path.join(dirpath, f))
            mode, hash = _process_file(filepath)
            entries[f] = {"hash": hash, "mode": mode}
        for d in dirnames:
            if d == ".git":
                continue
            dirpath = Path(os.path.join(directory, d))
            hash = _get_staged_targets(dirpath)
            entries[d] = {"hash": hash, "mode": "40000"}
        break

    # for k, v in entries.items():
    #     print(f"{k}: hash: {v['hash'][:5]} mode: {v['mode']}")

    entries_sorted = {k: v for k, v in sorted(entries.items())}

    entries_list = [
        f"{v['mode']} {k}\0{v['hash'][:20]}" for k, v in entries_sorted.items()
    ]
    entries_string = "".join(entries_list)
    header = f"tree {len(entries_string)}\0"
    output = header + entries_string
    output_compressed = zlib.compress(output.encode())

    h = sha1()
    h.update(output.encode())
    new_tree_object_hash = h.hexdigest()
    new_tree_object_dir = f".git/objects/{new_tree_object_hash[:2]}"
    new_tree_object_path = f"{new_tree_object_dir}/{new_tree_object_hash[2:]}"

    os.makedirs(new_tree_object_dir, exist_ok=True)
    with open(new_tree_object_path, "wb") as f:
        f.write(output_compressed)

    return new_tree_object_hash
    # return hash_object(
    #     target=new_tree_object_path,
    #     write=False,
    #     stdin=False,
    #     content_type="tree",
    # )


def _process_file(filepath: Path) -> tuple[str, str]:
    mode = get_file_mode(filepath)
    hash = hash_object(
        target=filepath,
        write=False,
        stdin=False,
        content_type="blob",
    )

    return mode, hash
