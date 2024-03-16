from beanie import PydanticObjectId
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from controllers.auth.authentication import create_token
from controllers.auth.student import authenticate_student, get_current_user_student
from controllers.student.crud_helper import find_student_on_db
from models.authentication.auth_dto import OutputCheckToken, OutputLogin
from models.authentication.authentication import TokenData

route_student_auth = APIRouter(
    prefix="/student/auth",
    tags=["Student Auth"],
    responses={404: {"description": "Not found"}},
)


@route_student_auth.post("/login", response_model=OutputLogin)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    student = await authenticate_student(
        username=form_data.username, password=form_data.password
    )
    access_token = create_token(student)
    return OutputLogin(access_token=access_token)


@route_student_auth.get("/check_token", response_model=OutputCheckToken)
async def check_token(current_user: TokenData = Depends(get_current_user_student)):
    student = await find_student_on_db({"_id": PydanticObjectId(current_user.userId)})
    return OutputCheckToken(
        name=student.name, isFirstLogin=student.credential.isFirstLogin
    )
