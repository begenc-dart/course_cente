from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.superadmin import authentication_router
from routers.admin import auth_admin, tutorial
from routers.student import auth_student,course,homework,exam
from routers.teacher import auth_teacher
from db.connection import Base,engine
from fastapi.staticfiles import StaticFiles
app = FastAPI()
origins = ["*"]
methods = ["*"]
headers = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers,
)
app.mount('/uploads', StaticFiles(directory="uploads"), name="uploads")


Base.metadata.create_all(engine)

app.include_router(authentication_router)
app.include_router(auth_admin)
app.include_router(auth_teacher)
# app.include_router(tutorial)
app.include_router(auth_student)
app.include_router(course)
# app.include_router(homework)
app.include_router(exam)