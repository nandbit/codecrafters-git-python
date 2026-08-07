import os
import sys
import zlib

from app.utils import blob_filepath


def cat_file(target: str) -> str:
    filepath = blob_filepath(target)
    _validate_cat_file_args(target, filepath)

    with open(filepath, "rb") as file:
        byte_data = file.read()
        decompressed_data = zlib.decompress(byte_data)
        stripped_data = decompressed_data.split(b"\0")[1]
        decoded_data = stripped_data.decode("utf-8")

        return decoded_data


def _validate_cat_file_args(target: str, filepath: str) -> None:
    if target is None:
        raise ValueError("No target supplied.")
        sys.exit()

    if not os.path.exists(filepath):
        print(f"Error: no file {filepath} found.")
        sys.exit()
