from beanie import PydanticObjectId
from fastapi import APIRouter, Depends

from controllers.auth.admin import get_current_user_admin
from controllers.auth.authentication import PWDCONTEXT
from controllers.student.crud_helper import (
    delete_student_on_db,
    find_all_students_with_pagination_on_db,
    find_student,
    insert_student_to_db,
    update_student_on_db,
)
from controllers.student.validation import (
    validate_email_is_unique,
    validate_email_is_unique_on_update,
    validate_nim_is_unique,
    validate_nim_is_unique_on_update,
    validate_nim_is_valid,
)
from controllers.util.auth import generate_random_string
from controllers.util.util import validate_email_is_valid
from models.authentication.authentication import TokenData
from models.user.student import GetStudents, InputStudent, OutputStudentPage, Student
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


@route_admin_student.get("", response_model=GetStudents)
async def get_students(
    currentUser: TokenData = Depends(get_current_user_admin),
    size: int = 10,
    page: int = 0,
    sort: str = "updateTime",
    dir: int = 1,
):
    students, totalPages, totalElements = await find_all_students_with_pagination_on_db(
        criteria={}, skip=page * size, size=size, sort=sort, dir=dir
    )
    return OutputStudentPage(
        size=size,
        page=page,
        totalElements=totalElements,
        totalPages=totalPages,
        sortBy=sort,
        sortDir=dir,
        content=students,
    )


@route_admin_student.put("/{idStudent}")
async def update_student(
    idStudent: str,
    input: InputStudent,
    currentUser: TokenData = Depends(get_current_user_admin),
):
    validate_email_is_valid(input.email)
    validate_nim_is_valid(input.nim)
    await validate_email_is_unique_on_update(
        email=input.email, idStudent=PydanticObjectId(idStudent)
    )
    await validate_nim_is_unique_on_update(
        nim=input.nim, idStudent=PydanticObjectId(idStudent)
    )

    await find_student({"_id": PydanticObjectId(idStudent)})
    await update_student_on_db(
        updateData=input.dict(),
        currentUser=currentUser,
        criteria={"_id": PydanticObjectId(idStudent)},
    )
    return "OK"


@route_admin_student.delete("/{idStudent}")
async def delete_student(
    idStudent: str, currentUser: TokenData = Depends(get_current_user_admin)
):
    await find_student({"_id": PydanticObjectId(idStudent)})
    await delete_student_on_db(
        criteria={"_id": PydanticObjectId(idStudent)}, currentUser=currentUser
    )
    return "OK"
