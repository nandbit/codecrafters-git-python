import os
from hashlib import sha1
from pathlib import Path

from app.commands.hash_object import hash_object
from app.utils import get_file_mode


def write_tree() -> None:
    tree_object_hash = _get_staged_targets(directory="./")
    print(tree_object_hash)


def _get_staged_targets(directory: str) -> list[str]:
    output = ""
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            output += _create_file_string(Path(os.path.join(dirpath, f)))
        for d in dirnames:
            if d == ".git":
                continue
            output += _get_staged_targets(Path(os.path.join(directory, d)))
        break

    h = sha1()
    h.update(output.encode())
    new_tree_object_hash = h.hexdigest()
    new_tree_object_dir = f".git/objects/{new_tree_object_hash[:2]}"
    new_tree_object_path = f"{new_tree_object_dir}/{new_tree_object_hash[2:]}"

    print(f"creating directory {new_tree_object_dir}")
    os.makedirs(new_tree_object_dir, exist_ok=True)

    print(f"writing to file {new_tree_object_path}")
    with open(new_tree_object_path, "w") as f:
        f.write(output)

    print(output)

    return hash_object(
        target=new_tree_object_path,
        write=False,
        stdin=False,
        content_type="tree",
    )


def _create_file_string(filepath: Path) -> str:
    mode = get_file_mode(filepath)
    hash = hash_object(
        target=filepath,
        write=False,
        stdin=False,
        content_type="blob",
    )

    return f"{mode} {filepath.name}\0{hash}"
