from fastapi import APIRouter,Depends,HTTPException,status,Request
from sqlalchemy.orm import Session
import models.teacher.schemas as mod 
import models.superuser.schemas as login 
from db.connection import get_db
import crud.student as auth
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from typing import List

auth_student = APIRouter(tags=['student_auth'])

@auth_student.post("/api/add_group", dependencies=[Depends(HTTPBearer())])
async def create_group(header_param: Request,req: mod.Group_Base,db: Session = Depends(get_db),):
    result = await auth.create_group_crud(header_param=header_param,req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
@auth_student.post("/api/add_group_time", dependencies=[Depends(HTTPBearer())])
async def create_group(header_param: Request,req: mod.GroupTime_Base,db: Session = Depends(get_db),):
    result = await auth.create_group_time_crud(header_param=header_param,req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
@auth_student.get('/api/read_group',  dependencies=[Depends(HTTPBearer())])
async def get_all_tutorial(header_param: Request,db: Session = Depends(get_db),):
    result = await auth.read_all_group(header_param=header_param,db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#------------------------------------------------------------------------------------------
@auth_student.get('/api/get-group/{id}')
async def get_admin(id: int, db: Session = Depends(get_db)):
    result = await auth.read_one_group(id=id, db=db)
    result = jsonable_encoder(result)
    print(result)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    elif result == None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Doesn't have tutorial this id")
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#-------------------------------------------------------------------------------------
@auth_student.post("/api/add_student", dependencies=[Depends(HTTPBearer())])
async def create_student(header_param: Request, req: mod.Student_Base, db: Session = Depends(get_db),):
    result = await auth.create_student_crud(header_param=header_param,req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
#------------------------------------------------------------------------------
@auth_student.post('/api/login-student')
async def login_admin(req: login.LoginSchema, db: Session = Depends(get_db)):
    result = await auth.student_login(req, db)
    # print(result)
    result = jsonable_encoder(result)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Логин или пароль неверный!')
#----------------------------------------------------------------------------------
@auth_student.put('/api/update_disactive_student/{id}', dependencies=[Depends(HTTPBearer())])
async def update_teacher(id: int, header_param: Request, req: mod.Disactive_teacher, db: Session = Depends(get_db)):
    result = await auth.disactive_students(id=id, header_param=header_param, req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result == -2:
        result = {'msg': 'Этот пользователь уже существует!'}
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    elif result:
        result = {'msg': 'Обновлено!'}
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
#--------------------------------------------------------------------------------------
@auth_student.get('/api/get-disactive-student', dependencies=[Depends(HTTPBearer())])
async def get_users(header_param: Request,db: Session = Depends(get_db),):
    result = await auth.read_disactive_student(header_param=header_param,db=db)
   
    result = jsonable_encoder(result)
    
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#--------------------------------------------------------------------------------------
@auth_student.get('/api/get-student/{id}', dependencies=[Depends(HTTPBearer())])
async def get_user(header_param: Request,id: int, db: Session = Depends(get_db)):
    result = await auth.read_student(header_param=header_param,id=id, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#--------------------------------------------------------------------------------------
@auth_student.get('/api/get-student_all/{group_id}', dependencies=[Depends(HTTPBearer())])
async def get_user(header_param: Request,group_id: int, db: Session = Depends(get_db)):
    result = await auth.read_student_all(header_param=header_param,group_id=group_id, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#--------------------------------------------------------------------------------------
@auth_student.get('/api/get-student/{id}', dependencies=[Depends(HTTPBearer())])
async def get_user(header_param: Request,id: int, db: Session = Depends(get_db)):
    result = await auth.read_student(header_param=header_param,id=id, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#---------------------------------------------------------------------------------
@auth_student.put('/api/update-student/{id}', dependencies=[Depends(HTTPBearer())])
async def update_teacher(id: int, header_param: Request, req: mod.Student_Base, db: Session = Depends(get_db)):
    result = await auth.update_student(id=id, header_param=header_param, req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result == -2:
        result = {'msg': 'Этот пользователь уже существует!'}
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    elif result:
        result = {'msg': 'Обновлено!'}
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)