from config.mongo_collection import TEACHER
from controllers.util.crud import find_one_on_db, insert_one_on_db
from models.authentication.authentication import TokenData
from models.user.teacher import OutputTeacher, Teacher


async def find_teacher_on_db(criteria: dict) -> OutputTeacher:
    teacher = await find_one_on_db(collection=TEACHER, criteria=criteria)
    if teacher:
        return OutputTeacher(**teacher)
    return None


async def insert_teacher_to_db(
    teacher: Teacher,
    currentUser: TokenData,
):
    await insert_one_on_db(
        collection=TEACHER, data=teacher.dict(), currentUser=currentUser
    )
