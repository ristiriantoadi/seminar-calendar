import re

from fastapi import HTTPException

from controllers.teacher.crud_helper import find_teacher_on_db


def validate_nip_is_valid(nip: str):
    pattern = r"^\d{8}$"
    if re.match(pattern, nip) is None:
        raise HTTPException(status_code=404, detail="NIP tidak valid")


async def validate_nip_is_unique(nip: str):
    teacher = await find_teacher_on_db({"nip": nip})
    if teacher:
        raise HTTPException(status_code=400, detail="NIP duplikat")


async def validate_email_is_unique(email: str):
    teacher = await find_teacher_on_db({"email": email})
    if teacher:
        raise HTTPException(status_code=400, detail="Email duplikat")
