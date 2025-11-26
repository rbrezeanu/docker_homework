from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta

from starlette.responses import PlainTextResponse

app = FastAPI()

# Secret key for JWT
SECRET_KEY = "supersecretkey"
list_of_students=["Cosmin","Edi","Andrei","Vlad","Darius"]

# Pydantic model for login
class LoginRequest(BaseModel):
    username: str
    password: str


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
def login(data: LoginRequest):
    username = data.username
    password = data.password

    # For simplicity, accept any username/password
    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password required")
    if username not in list_of_students and password not in list_of_students:
        raise HTTPException(status_code=403, detail="Parola/user gresit")
    else:
        # Create token
        payload = {
            "sub": username,
            "exp": datetime.utcnow() + timedelta(hours=1)  # token expires in 1 hour
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return {"access_token": token, "token_type": "bearer"}


@app.get("/cerinta", response_class=PlainTextResponse)
def cerinta(payload: dict = Depends(verify_token)):
    try:
        with open("server/cerinta.txt", "r", encoding="utf-8") as f:
            cerinta = f.read()
        return cerinta
    except Exception as e:
        return e
