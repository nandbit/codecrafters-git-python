import os
from dataclasses import dataclass

from app.config import GIT_ROOT_DIRECTORY


@dataclass
class UserInfo:
    name: str
    email: str


class ConfigFileMissingError(Exception):
    pass


class ConfigError(Exception):
    pass


def config(username: str, email: str) -> None:
    if username == "":
        print("The username may not be empty.")
    if email == "":
        print("The email may not be empty.")

    with open(f"{GIT_ROOT_DIRECTORY}/config", "w") as config_file:
        user_info = f"[user]\n\tname = {username}\n\temail = {email}"
        config_file.write(user_info)


def get_user_info() -> UserInfo:
    name = ""
    email = ""
    config_filepath = f"{GIT_ROOT_DIRECTORY}/config"

    if not os.path.exists(config_filepath):
        raise ConfigFileMissingError("No config file found.")

    with open(config_filepath, "r") as config_file:
        for line in config_file:
            if name and email:
                break
            if "name" in line:
                name = line.strip().split("=")[1]
            if "email" in line:
                email = line.strip().split("=")[1]
        if not (name and email):
            raise ConfigError(
                "Could not find name or email in the git config file.",
            )

    return UserInfo(name, email)
