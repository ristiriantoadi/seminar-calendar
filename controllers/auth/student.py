from fastapi import Depends, HTTPException

from controllers.auth.authentication import (
    PWDCONTEXT,
    get_current_user,
    oauth2_scheme_student,
)
from controllers.student.crud_helper import find_student_on_db


async def authenticate_student(username: str, password: str):
    student = await find_student_on_db(
        criteria={"$or": [{"nim": username}, {"email": username}]}
    )
    if student is None:
        raise HTTPException(status_code=401, detail="Username atau password salah")
    if not PWDCONTEXT.verify(password.strip(), student.credential.password):
        raise HTTPException(status_code=401, detail="Username atau password salah")
    return student


async def get_current_user_student(token: str = Depends(oauth2_scheme_student)):
    return get_current_user(token)
