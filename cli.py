import json
import click
import os
from auth import get_password_hash, create_access_token, verify_password

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

@click.group()
def cli():
    pass

@cli.command()
@click.argument("username")
@click.password_option()
def create_user(username, password):
    users = load_users()
    if username in users:
        click.echo(f"Error: User '{username}' already exists.")
        return

    hashed_password = get_password_hash(password)
    users[username] = {"password": hashed_password}
    save_users(users)
    
    # Generate token immediately for the user
    token = create_access_token(data={"sub": username})

    click.echo(f"User '{username}' created successfully.")
    click.echo(f"JWT Token for '{username}': {token}")

@cli.command()
@click.argument("username")
def delete_user(username):
    users = load_users()
    if username not in users:
        click.echo(f"Error: User '{username}' not found.")
        return

    del users[username]
    save_users(users)
    click.echo(f"User '{username}' deleted successfully.")

if __name__ == "__main__":
    cli()
