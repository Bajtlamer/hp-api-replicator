# AGENTS.md

Guidelines for running, testing, and extending this FastAPI + CLI project.

## Setup

```bash
python -m venv venv               # Create isolated environment
source venv/bin/activate          # Activate it
pip install -r requirements.txt   # Install deps
```

*Avoid* creating a global `pyproject.toml` – the repo uses a plain `requirements.txt`.

## User & Token Management

**Create a user** (`cli.py`):

```bash
python cli.py create-user <username>
```

You’ll be prompted for a password; the script prints a JWT token you’ll use to authenticate.

**Delete a user**:

```bash
python cli.py delete-user <username>
```

## Running the API

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The app automatically creates `logs/` and appends each request to `logs/replication.log`.

### Making a request

```bash
curl -X POST \
  http://0.0.0.0:8000/data \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"device_id":"sensor","temperature":25.5}'
```

## Configuration

*`config.py`* reads `SECRET_KEY` from the environment. In production, set a strong key. The default is insecure and must be overridden.

```bash
export SECRET_KEY=$(openssl rand -base64 32)
```

## Common Gotchas

* Forgetting the `--host 0.0.0.0` flag will bind to localhost only.
* The `Authorization` header must be exactly `Bearer <token>`; extra spaces or missing `Bearer` will cause a `401`.
* `logs/` is created lazily on first server start; delete it manually if you need to clear history.

Nothing else is required. The project has no tests or linters configured, so any Python environment that can run `uvicorn` and `click` will work.
