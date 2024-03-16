from fastapi import HTTPException

from controllers.admin.crud_helper import find_admin_on_db
from controllers.auth.authentication import PWDCONTEXT
from models.user.admin import OutputAdmin


async def authenticate_admin(username: str, password: str) -> OutputAdmin:
    admin = await find_admin_on_db(criteria={"nip": username.strip()})
    if admin is None:
        raise HTTPException(status_code=401, detail="Username atau password salah")
    if not PWDCONTEXT.verify(password.strip(), admin.credential.password):
        raise HTTPException(status_code=401, detail="Username atau password salah")
    return admin
