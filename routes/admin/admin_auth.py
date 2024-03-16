from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from config.config import INIT_KEY
from controllers.admin.crud_helper import find_admin_on_db
from controllers.admin.init import insert_first_admin_to_db, validate_no_admin_on_db
from controllers.auth.admin import authenticate_admin, get_current_user_admin
from controllers.auth.authentication import create_token
from models.authentication.auth_dto import OutputCheckToken, OutputLogin
from models.authentication.authentication import TokenData

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
    return "OK"


@route_admin_auth.post("/login", response_model=OutputLogin)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    admin = await authenticate_admin(
        username=form_data.username, password=form_data.password
    )
    access_token = create_token(admin)
    return OutputLogin(access_token=access_token)


@route_admin_auth.get("/check_token", response_model=OutputCheckToken)
async def check_token(current_user: TokenData = Depends(get_current_user_admin)):
    admin = await find_admin_on_db({"_id": PydanticObjectId(current_user.userId)})
    return OutputCheckToken(name=admin.name, isFirstLogin=admin.credential.isFirstLogin)
