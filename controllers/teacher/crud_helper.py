from typing import List, Tuple

from fastapi import HTTPException
from pydantic import parse_obj_as

from config.mongo_collection import TEACHER
from controllers.util.crud import (
    delete_on_db,
    find_all_data_with_pagination_on_db,
    find_one_on_db,
    insert_one_on_db,
    update_on_db,
)
from models.authentication.authentication import TokenData
from models.user.teacher import OutputTeacher, Teacher


async def find_teacher_on_db(criteria: dict) -> OutputTeacher:
    teacher = await find_one_on_db(collection=TEACHER, criteria=criteria)
    if teacher:
        return OutputTeacher(**teacher)
    return None


async def find_teacher(criteria: dict):
    teacher = await find_teacher_on_db(criteria)
    if teacher is None:
        raise HTTPException(status_code=404, detail="Dosen tidak ditemukan")


async def insert_teacher_to_db(
    teacher: Teacher,
    currentUser: TokenData,
):
    await insert_one_on_db(
        collection=TEACHER, data=teacher.dict(), currentUser=currentUser
    )


async def find_all_teachers_with_pagination_on_db(
    criteria: dict, skip: int, size: int = 10, sort: str = "updateTime", dir: int = 1
) -> Tuple[List[OutputTeacher], int, int]:
    datas, totalPages, totalElements = await find_all_data_with_pagination_on_db(
        criteria=criteria, collection=TEACHER, skip=skip, size=size, sort=sort, dir=dir
    )
    datas = parse_obj_as(List[OutputTeacher], datas)
    return datas, totalPages, totalElements


async def update_teacher_on_db(
    updateData: dict,
    currentUser: TokenData,
    criteria: dict,
):
    await update_on_db(
        updateData=updateData,
        currentUser=currentUser,
        collection=TEACHER,
        criteria=criteria,
    )


async def delete_teacher_on_db(criteria: dict, currentUser: TokenData):
    await delete_on_db(collection=TEACHER, criteria=criteria, currentUser=currentUser)
