from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from config.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from models.authentication.authentication import TokenData
from models.user.user import OutputUser

PWDCONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme_admin = OAuth2PasswordBearer(
    tokenUrl="admin/auth/login", scheme_name="admin_oauth2_schema"
)
oauth2_scheme_student = OAuth2PasswordBearer(
    tokenUrl="student/auth/login", scheme_name="student_oauth2_schema"
)


def create_token(user: OutputUser):
    data = TokenData(
        userId=str(user.id),
        exp=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    encoded_jwt = jwt.encode(data.dict(), SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        tokenData = TokenData(
            userId=payload.get("userId"),
            exp=payload.get("exp"),
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Token tidak valid")

    return tokenData
