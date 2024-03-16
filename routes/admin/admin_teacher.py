from fastapi import APIRouter, Depends

from controllers.auth.admin import get_current_user_admin
from controllers.auth.authentication import PWDCONTEXT
from controllers.teacher.crud_helper import insert_teacher_to_db
from controllers.teacher.validation import (
    validate_email_is_unique,
    validate_nip_is_unique,
    validate_nip_is_valid,
)
from controllers.util.auth import generate_random_string
from controllers.util.util import validate_email_is_valid
from models.authentication.authentication import TokenData
from models.user.teacher import InputTeacher, Teacher
from models.user.user import Credential

route_admin_teacher = APIRouter(
    prefix="/admin/teacher",
    tags=["Admin Teacher"],
    responses={404: {"description": "Not found"}},
)


@route_admin_teacher.post("")
async def add_teacher(
    input: InputTeacher, currentUser: TokenData = Depends(get_current_user_admin)
):
    validate_nip_is_valid(input.nip)
    validate_email_is_valid(input.email)
    await validate_nip_is_unique(input.nip)
    await validate_email_is_unique(input.email)

    password = generate_random_string()

    await insert_teacher_to_db(
        teacher=Teacher(
            name=input.name,
            email=input.email,
            nip=input.nip,
            credential=Credential(password=PWDCONTEXT.encrypt(password)),
        ),
        currentUser=currentUser,
    )
    return password
