import sys
import json
import os
from auth import get_password_hash

USERS_FILE = "users.json"

def add_user_directly(username, password):
    if not os.path.exists(USERS_FILE):
        users = {}
    else:
        with open(USERS_FILE, "r") as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                users = {}

    if username in users:
        print(f"User '{username}' already exists.")
        return

    hashed_password = get_password_hash(password)
    users[username] = {"password": hashed_password}

    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)
    
    print(f"Successfully added user '{username}' to {USERS_FILE}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <username> <password>")
        sys.exit(1)
    
    user_name = sys.argv[1]
    user_pass = sys.argv[2]
    add_user_directly(user_name, user_pass)
