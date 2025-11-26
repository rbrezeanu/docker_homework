import json

from fastapi import FastAPI, HTTPException, Header, Depends, Form
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta

from starlette.responses import PlainTextResponse

from pathlib import Path

list_of_students=["Cosmin","Edi","Andrei","Vlad","Darius", "Rares"]
app = FastAPI()

# Secret key for JWT
SECRET_KEY = "supersecretkey"

BASE_DIR = Path(__file__).parent
datadir = BASE_DIR / "data"
results_dir = BASE_DIR / "results"
results_dir.mkdir(exist_ok=True)

class SaveResults(BaseModel):
    filename: str
    content: str

def verify_token(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    # Expecting: Authorization: Bearer <token>
    parts = authorization.split(" ")

    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization format")

    token = parts[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload  # You can access the username later
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.post("/login", summary="Login and receive a JWT token",
          description="Send a JSON body containing **username** and **password** to receive a JWT token."
          )
def login(username: str = Form(...), password: str = Form(...)):
    # For simplicity, accept any username/password
    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password required")
    if username not in list_of_students and password not in list_of_students:
        raise HTTPException(status_code=403, detail="Parola/user gresit")
    else:
        # Create token
        payload = {
            "sub": username,
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return {"access_token": token, "token_type": "bearer"}


@app.get("/cerinta", response_class=PlainTextResponse)
def cerinta(payload: dict = Depends(verify_token)):
    try:
        with open("second_server/cerinta.txt", "r", encoding="utf-8") as f:
            cerinta = f.read()
        return cerinta
    except Exception as e:
        return e

@app.get("/words", response_class=PlainTextResponse)
def get_words(payload: dict = Depends(verify_token)):
    try:
        file_path = datadir / "long_words.txt"
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return e


@app.get("/servers_suport", response_class=PlainTextResponse)
def servers_suport(payload: dict = Depends(verify_token)):
    try:
        with open("second_server/cerinta.txt", "r", encoding="utf-8") as f:
            servers_suport = f.read()
        return servers_suport
    except Exception as e:
        return e


@app.get("/subscriptions", response_class=PlainTextResponse)
def subscriptions(payload: dict = Depends(verify_token)):
    try:
        with open("second_server/Subscriptions.txt", "r", encoding="utf-8") as f:
            subscriptions = f.read()
        return subscriptions
    except Exception as e:
        return e


@app.get("/servers")
async def servers(payload: dict = Depends(verify_token)):
    with open("second_server/servers.json") as f:
        return json.load(f)



@app.post("/save_results")
def save_results(data: SaveResults, payload: dict = Depends(verify_token)):
    try:
        file_path = results_dir / data.filename
        with open(file_path, "w") as f:
            f.write(data.content)
        return {"status": "ok", "saved_to": str(file_path)}
    except Exception as e:
        return e