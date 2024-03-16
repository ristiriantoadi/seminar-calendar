from fastapi import Depends, HTTPException

from controllers.admin.crud_helper import find_admin_on_db
from controllers.auth.authentication import (
    PWDCONTEXT,
    get_current_user,
    oauth2_scheme_admin,
)
from models.user.admin import OutputAdmin


async def authenticate_admin(username: str, password: str) -> OutputAdmin:
    admin = await find_admin_on_db(
        criteria={"$or": [{"nip": username}, {"email": username}]}
    )
    if admin is None:
        raise HTTPException(status_code=401, detail="Username atau password salah")
    if not PWDCONTEXT.verify(password.strip(), admin.credential.password):
        raise HTTPException(status_code=401, detail="Username atau password salah")
    return admin


async def get_current_user_admin(token: str = Depends(oauth2_scheme_admin)):
    return get_current_user(token)
