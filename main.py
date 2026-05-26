import json
import os
from datetime import datetime
from fastapi import FastAPI, Request, Depends, HTTPException, status
from auth import get_current_user

app = FastAPI()

LOG_DIR = "./logs"
LOG_FILE = os.path.join(LOG_DIR, "replication.log")

@app.on_event("startup")
async def startup_event():
    os.makedirs(LOG_DIR, exist_ok=True)

@app.post("/data")
async def replicate_data(request: Request, current_user: dict = Depends(get_current_user)):
    try:
        data = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data")

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "source_ip": request.client.host,
        "authenticated_user": current_user["username"],
        "payload": data
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    return {"message": "Data received and logged successfully!"}

