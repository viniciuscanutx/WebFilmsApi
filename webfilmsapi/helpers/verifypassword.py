from dotenv import load_dotenv
import os
from fastapi import HTTPException, Query, status

load_dotenv()
SECRET_PASSWORD = os.getenv("SECRET_KEY")


def verify_password(password: str = Query(...)):
    if password != SECRET_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha incorreta",
            headers={"WWW-Authenticate": "Bearer"},
        )