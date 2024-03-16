from typing import List, Tuple

from fastapi import HTTPException
from pydantic import parse_obj_as

from config.mongo_collection import STUDENT
from controllers.util.crud import (
    find_all_data_with_pagination_on_db,
    find_one_on_db,
    insert_one_on_db,
    update_on_db,
)
from models.authentication.authentication import TokenData
from models.user.student import OutputStudent, Student


async def insert_student_to_db(student: Student, currentUser: TokenData):
    await insert_one_on_db(
        collection=STUDENT, data=student.dict(), currentUser=currentUser
    )


async def find_student_on_db(criteria: dict) -> OutputStudent:
    student = await find_one_on_db(criteria=criteria, collection=STUDENT)
    if student:
        return OutputStudent(**student)
    return None


async def find_student(criteria: dict) -> OutputStudent:
    student = await find_student_on_db(criteria)
    if student is None:
        raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan")
    return student


async def find_all_students_with_pagination_on_db(
    criteria: dict, skip: int, size: int = 10, sort: str = "updateTime", dir: int = 1
) -> Tuple[List[OutputStudent], int, int]:
    datas, totalPages, totalElements = await find_all_data_with_pagination_on_db(
        criteria=criteria, collection=STUDENT, skip=skip, size=size, sort=sort, dir=dir
    )
    datas = parse_obj_as(List[OutputStudent], datas)
    return datas, totalPages, totalElements


async def update_student_on_db(
    updateData: dict, currentUser: TokenData, criteria: dict
):
    await update_on_db(
        updateData=updateData,
        currentUser=currentUser,
        collection=STUDENT,
        criteria=criteria,
    )
