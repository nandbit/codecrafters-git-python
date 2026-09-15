import os

from app.config import GIT_OBJECTS_DIRECTORY, GIT_ROOT_DIRECTORY


def init() -> str:
    os.mkdir(GIT_ROOT_DIRECTORY)
    os.mkdir(GIT_OBJECTS_DIRECTORY)
    os.mkdir(f"{GIT_ROOT_DIRECTORY}/refs")
    with open(f"{GIT_ROOT_DIRECTORY}/HEAD", "w") as f:
        f.write("ref: refs/heads/main\n")
    print("Initialized git directory")
