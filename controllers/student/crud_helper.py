from config.mongo_collection import STUDENT
from controllers.util.crud import find_one_on_db, insert_one_on_db
from models.authentication.authentication import TokenData
from models.user.student import OutputStudent, Student


async def insert_student_to_db(student: Student, currentUser: TokenData):
    await insert_one_on_db(
        collection=STUDENT, data=student.dict(), currentUser=currentUser
    )


async def find_student_on_db(criteria: dict):
    student = await find_one_on_db(criteria=criteria, collection=STUDENT)
    if student:
        return OutputStudent(**student)
    return None
