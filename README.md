# HP API Replicator

This project provides a simple FastAPI application to receive and log data from remote devices, secured with JWT authentication, and a CLI for user and token management.

## Features

*   **Data Replication Endpoint:** A `/data` endpoint to accept POST requests with arbitrary JSON data.
*   **Structured Logging:** All incoming data is timestamped, includes source IP and authenticated user, and is stored in a structured JSONL log file (`logs/replication.log`).
*   **JWT Authentication:** The `/data` endpoint is secured using JSON Web Tokens.
*   **CLI for User Management:** A command-line interface to create and delete users, and generate JWT tokens.

## Installation

1.  **Clone the repository (if applicable):**
    ```bash
    # git clone <repository_url>
    # cd hp-api-replicator
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### 1. Set up a User and Get a JWT Token

Use the CLI to create a new user. This will also provide you with a JWT token that you'll use for authenticating with the API.

```bash
python cli.py create-user <username>
# Example: python cli.py create-user mydeviceuser
```
You will be prompted to enter and confirm a password. Upon successful creation, the JWT token for the user will be displayed. Keep this token secure.

### 2. Run the API Server

Start the FastAPI application using Uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be accessible at `http://0.0.0.0:8000`.

### 3. Send Data to the API

You can send POST requests to the `/data` endpoint. You *must* include the JWT token obtained in step 1 in the `Authorization` header as a Bearer token.

Example using `curl`:

```bash
curl -X POST \
  http://0.0.0.0:8000/data \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <YOUR_JWT_TOKEN>" \
  -d '{
    "device_id": "sensor-123",
    "temperature": 25.5,
    "humidity": 60,
    "timestamp": "2023-10-27T10:00:00Z"
  }'
```

Replace `<YOUR_JWT_TOKEN>` with the actual token you received.

### 4. Check the Logs

All received data will be appended to `logs/replication.log` in JSONL format.

```bash
cat logs/replication.log
```

### CLI Commands

*   **`python cli.py create-user <username>`**: Creates a new user and generates a JWT token.
*   **`python cli.py delete-user <username>`**: Deletes an existing user.

## Configuration

The `config.py` file contains the following settings:

*   `SECRET_KEY`: Used for signing JWT tokens. **Important: Change this to a strong, random value in production and ideally load it from an environment variable (`SECRET_KEY`).**
*   `ALGORITHM`: The JWT signing algorithm (default: `HS256`).
*   `ACCESS_TOKEN_EXPIRE_MINUTES`: The validity period for JWT tokens in minutes.

## Security Considerations

*   **SECRET_KEY:** Never commit your production `SECRET_KEY` to version control. Use environment variables.
*   **User Storage:** For this prototype, user credentials are stored in `users.json`. For production, integrate with a proper database.
*   **HTTPS:** Always use HTTPS in a production environment to protect communication.

