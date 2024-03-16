from fastapi import HTTPException

from controllers.admin.crud_helper import find_admin_on_db, insert_admin_to_db
from controllers.auth.authentication import PWDCONTEXT
from models.user.admin import Admin
from models.user.user import Credential


async def validate_no_admin_on_db():
    admin = await find_admin_on_db(criteria={})
    if admin:
        raise HTTPException(status_code=400, detail="Admin sudah dibuat")


async def insert_first_admin_to_db():
    await insert_admin_to_db(
        admin=Admin(
            name="Admin 1",
            nip="001",
            email="admin1@gmail.com",
            credential=Credential(password=PWDCONTEXT.encrypt("Pass1234")),
        )
    )
