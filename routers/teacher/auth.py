from fastapi import APIRouter,Depends,HTTPException,status,Request
from sqlalchemy.orm import Session
import models.teacher.schemas as mod 
import models.superuser.schemas as login 
from db.connection import get_db
import crud.teacher as auth
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from typing import List
auth_teacher = APIRouter(tags=['teacher_auth'])

@auth_teacher.post("/api/add_teacher", dependencies=[Depends(HTTPBearer())])
async def create_admin(header_param: Request,req: mod.CreateTeacherBase,db: Session = Depends(get_db),):
    result = await auth.create_techer_crud(header_param=header_param,req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
#-----------------------------------------------------------------------------------
@auth_teacher.post('/api/login-teacher')
async def login_admin(req: login.LoginSchema, db: Session = Depends(get_db)):
    result = await auth.teacher_login(req, db)
    # print(result)
    result = jsonable_encoder(result)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Логин или пароль неверный!')
# #------------------------------------------------------------------------------------
@auth_teacher.get('/api/get-teacher', dependencies=[Depends(HTTPBearer())])
async def get_users(header_param: Request,db: Session = Depends(get_db),):
    result = await auth.read_all_teacher(header_param=header_param,db=db)
   
    result = jsonable_encoder(result)
    
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#-------------------------------------------------------------------------------------
@auth_teacher.get('/api/get-disactive-teacher', dependencies=[Depends(HTTPBearer())])
async def get_users(header_param: Request,db: Session = Depends(get_db),):
    result = await auth.read_disactive_teacher(header_param=header_param,db=db)
   
    result = jsonable_encoder(result)
    
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#------------------------------------------------------------------------------------
@auth_teacher.get('/api/get-region-teacher/{region}', dependencies=[Depends(HTTPBearer())])
async def get_users(header_param: Request,region:str,db: Session = Depends(get_db),):
    result = await auth.read_region_teacher(header_param=header_param,region=region,db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
# #--------------------------------------------------------------------------------
@auth_teacher.get('/api/get-teacher/{id}', dependencies=[Depends(HTTPBearer())])
async def get_user(header_param: Request,id: int, db: Session = Depends(get_db)):
    result = await auth.read_teacher(header_param=header_param,id=id, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#-----------------------------------------------------------------------------------
@auth_teacher.put('/api/update-teacher/{id}', dependencies=[Depends(HTTPBearer())])
async def update_teacher(id: int, header_param: Request, req: mod.CreateTeacherBase, db: Session = Depends(get_db)):
    result = await auth.update_teacher(id=id, header_param=header_param, req=req, db=db)
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
#-------------------------------------------------------------------------------------
@auth_teacher.put('/api/update_disactive_teacher/{id}', dependencies=[Depends(HTTPBearer())])
async def update_teacher(id: int, header_param: Request, req: mod.Disactive_teacher, db: Session = Depends(get_db)):
    result = await auth.disactive_teacheres(id=id, header_param=header_param, req=req, db=db)
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
