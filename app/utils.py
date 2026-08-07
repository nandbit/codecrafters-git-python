import os


def blob_filepath(name: str) -> str:
    subdir = name[:2]
    filename = name[2:]
    return os.path.join(f".git/objects/{subdir}/{filename}")
