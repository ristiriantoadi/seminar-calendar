from beanie import PydanticObjectId
from fastapi import APIRouter, Depends

from controllers.auth.admin import get_current_user_admin
from controllers.auth.authentication import PWDCONTEXT
from controllers.teacher.crud_helper import (
    find_all_teachers_with_pagination_on_db,
    find_teacher,
    insert_teacher_to_db,
    update_teacher_on_db,
)
from controllers.teacher.validation import (
    validate_email_is_unique,
    validate_email_is_unique_on_update,
    validate_nip_is_unique,
    validate_nip_is_unique_on_update,
    validate_nip_is_valid,
)
from controllers.util.auth import generate_random_string
from controllers.util.util import validate_email_is_valid
from models.authentication.authentication import TokenData
from models.user.teacher import GetTeachers, InputTeacher, Teacher
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


@route_admin_teacher.get("")
async def get_teachers(
    currentUser: TokenData = Depends(get_current_user_admin),
    size: int = 10,
    page: int = 0,
    sort: str = "updateTime",
    dir: int = 1,
):
    teachers, totalPages, totalElements = await find_all_teachers_with_pagination_on_db(
        criteria={}, skip=page * size, size=size, sort=sort, dir=dir
    )
    return GetTeachers(
        size=size,
        page=page,
        totalElements=totalElements,
        totalPages=totalPages,
        sortBy=sort,
        sortDir=dir,
        content=teachers,
    )


@route_admin_teacher.put("/{idTeacher}")
async def update_teacher(
    idTeacher: str,
    input: InputTeacher,
    currentUser: TokenData = Depends(get_current_user_admin),
):
    await find_teacher({"_id": PydanticObjectId(idTeacher)})

    validate_nip_is_valid(input.nip)
    validate_email_is_valid(input.email)
    await validate_nip_is_unique_on_update(nip=input.nip, idTeacher=idTeacher)
    await validate_email_is_unique_on_update(input.email, idTeacher=idTeacher)

    await update_teacher_on_db(
        updateData=input.dict(),
        currentUser=currentUser,
        criteria={"_id": PydanticObjectId(idTeacher)},
    )
    return "OK"
