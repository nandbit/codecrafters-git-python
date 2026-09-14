def config(username: str, email: str) -> None:
    if username == "":
        print("The username may not be empty.")
    if email == "":
        print("The email may not be empty.")

    with open(".git/config", "w") as config_file:
        user_info = f"[user]\n\tname = {username}\n\temail = {email}"
        config_file.write(user_info)
