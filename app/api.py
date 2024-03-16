from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.admin.admin_auth import route_admin_auth
from routes.admin.admin_student import route_admin_student
from routes.student.student_auth import route_student_auth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*", "*"],
    allow_methods=["*", "*"],
    allow_headers=["*", "*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(route_admin_auth)
app.include_router(route_student_auth)
app.include_router(route_admin_student)
