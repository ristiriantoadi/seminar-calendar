from fastapi import APIRouter, Depends

from controllers.auth.admin import get_current_user_admin
from controllers.auth.authentication import PWDCONTEXT
from controllers.student.crud_helper import insert_student_to_db
from controllers.student.validation import (
    validate_email_is_unique,
    validate_nim_is_unique,
    validate_nim_is_valid,
)
from controllers.util.auth import generate_random_string
from controllers.util.util import validate_email_is_valid
from models.authentication.authentication import TokenData
from models.user.student import InputStudent, Student
from models.user.user import Credential

route_admin_student = APIRouter(
    prefix="/admin/student",
    tags=["Admin Student"],
    responses={404: {"description": "Not found"}},
)


@route_admin_student.post("")
async def add_student(
    input: InputStudent, currentUser: TokenData = Depends(get_current_user_admin)
):
    validate_email_is_valid(input.email)
    validate_nim_is_valid(input.nim)
    await validate_nim_is_unique(input.nim)
    await validate_email_is_unique(input.email)

    password = generate_random_string()

    await insert_student_to_db(
        student=Student(
            name=input.name,
            email=input.email,
            nim=input.nim.upper(),
            year=input.year,
            credential=Credential(password=PWDCONTEXT.encrypt(password)),
        ),
        currentUser=currentUser,
    )
    return password


@route_admin_student.get("")
async def get_students(current_user: TokenData = Depends(get_current_user_admin)):
    pass


@route_admin_student.put("/{idStudent}")
async def update_student(
    idStudent: str, current_user: TokenData = Depends(get_current_user_admin)
):
    pass


@route_admin_student.put("/{idStudent}")
async def delete_student(
    idStudent: str, current_user: TokenData = Depends(get_current_user_admin)
):
    pass