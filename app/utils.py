import os


def blob_filepath(name: str) -> str:
    subdir = name[:2]
    filename = name[2:]
    return os.path.join(f".git/objects/{subdir}/{filename}")


def get_file_mode(filepath: str) -> str:
    if os.path.isfile(filepath) and os.access(filepath, os.X_OK):
        return "100755"
    elif os.path.islink(filepath):
        return "120000"
    elif os.path.isfile(filepath):
        return "100644"
    else:
        raise ValueError(
            f"Error obtaining mode of file {filepath}. "
            "The file must be either a regular file"
            "an executable, or a symbolic link.",
        )
