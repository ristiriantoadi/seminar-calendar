import re

from fastapi import HTTPException

from controllers.student.crud_helper import find_student_on_db


async def validate_nim_is_unique(nim: str):
    student = await find_student_on_db({"nim": nim})
    if student:
        raise HTTPException(status_code=400, detail="NIM duplikat")


async def validate_email_is_unique(email: str):
    student = await find_student_on_db({"email": email})
    if student:
        raise HTTPException(status_code=400, detail="Email duplikat")


def validate_nim_is_valid(nim: str):
    pattern = r"^F1D\d{6}$"
    if re.match(pattern, nim, re.IGNORECASE) is None:
        raise HTTPException(status_code=400, detail="NIM tidak valid")
