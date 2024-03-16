from fastapi import APIRouter

route_member_auth = APIRouter(
    prefix="/teacher/auth",
    tags=["Teacher auth"],
    responses={404: {"description": "Not found"}},
)
