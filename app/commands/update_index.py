from app.commands.hash_object import hash_object


def update_index(filepath: str) -> None:
    create_entry(target=filepath)
    update_index_checksum()


def create_entry(target: str) -> None:
    new_object_hash = hash_object(
        target=filepath,
        write=True,
        stdin=False,
        content_type="blob",
    )

    metadata_bytes = _create_entry_metadata()
    filename_bytes = _get_filename()
    padding_bytes = _get_filename_padding()


def _create_entry_metadata(target: str) -> dict[str, bytes]:
    ctime = os.stat()

    ctime_sec: int = bytes_to_int(metadata[0:4])
    ctime_ns: int = bytes_to_int(metadata[4:8])
    mtime_sec: int = bytes_to_int(metadata[8:12])
    mtime_ns: int = bytes_to_int(metadata[12:16])
    dev: int = bytes_to_int(metadata[16:20])
    ino: int = bytes_to_int(metadata[20:24])
    type_and_permissions: bytes = metadata[24:28]
    mode: str = _parse_mode(metadata[24:28])
    uid: int = bytes_to_int(metadata[28:32])
    gid: int = bytes_to_int(metadata[32:36])
    file_size: int = bytes_to_int(metadata[36:40])
    sha1: str = metadata[40:60].hex()
    flags: int = bytes_to_int(metadata[60:62])
    assume_valid: int = (flags & 0x00FF) >> 15
    extended: int = (flags >> 14) & 1
    stage: int = (flags >> 12) & 3
    name_len: int = flags & 4095
    skip_worktree: int | None = None
    intend_to_add: int | None = None
