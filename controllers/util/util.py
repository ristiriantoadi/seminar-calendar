import re

from fastapi import HTTPException


def validate_email_is_valid(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if re.match(pattern, email) is None:
        raise HTTPException(status_code=400, detail="Email tidak valid")
