
from datetime import datetime, timedelta, timezone
import os

from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt


load_dotenv()

#1
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY must be configured in .env")

#2
ALGORITHM = "HS256"

#3
TOKEN_EXPIRE_MINUTES = 30

#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#4
def create_access_token(username: str):
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": username,
        "exp": expires_at
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


#5
def get_current_user(token:str):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM],)

        username = payload.get("sub")

        if not username:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid token",
                )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

        user = users_db.get(username)

        return user