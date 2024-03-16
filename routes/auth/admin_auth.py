from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from config.config import INIT_KEY
from controllers.admin.init import insert_first_admin_to_db, validate_no_admin_on_db

route_admin_auth = APIRouter(
    prefix="/admin/auth",
    tags=["Admin auth"],
    responses={404: {"description": "Not found"}},
)


@route_admin_auth.get("/init_first_admin/{key}")
async def init_first_admin(key: str):
    if key != INIT_KEY:
        raise HTTPException(status_code=401, detail="Init key salah")

    await validate_no_admin_on_db()
    await insert_first_admin_to_db()


@route_admin_auth.get("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    pass


# @route_admin_auth.get("/check_token")
# async def check_token(current_user: TokenData = Depends(get_current_user_member)):
#     member = await find_member_on_db({"_id": PydanticObjectId(current_user.userId)})
#     return member
