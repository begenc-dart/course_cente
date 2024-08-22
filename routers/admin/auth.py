from fastapi import APIRouter,Depends,HTTPException,status,Request
from sqlalchemy.orm import Session
import models.superuser.schemas as mod 
import models.teacher.schemas as disactive
from db.connection import get_db
import crud.admin as auth
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from typing import List
auth_admin = APIRouter(tags=['admin_auth'])

@auth_admin.post("/api/add_admin", dependencies=[Depends(HTTPBearer())])
async def create_admin(header_param: Request,req: mod.AdminBase,db: Session = Depends(get_db),):
    result = await auth.create_admin_crud(header_param=header_param,req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result ==-2:
        return HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    elif result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
#-----------------------------------------------------------------------------------
@auth_admin.post('/api/login-admin')
async def login_admin(req: mod.LoginSchema, db: Session = Depends(get_db)):
    result = await auth.admin_login(req, db)
    # print(result)
    result = jsonable_encoder(result)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Логин или пароль неверный!')
#------------------------------------------------------------------------------------
@auth_admin.get('/api/get-admin', dependencies=[Depends(HTTPBearer())],response_model=List[mod.Admin_short])
async def get_admins(header_param: Request,db: Session = Depends(get_db),):
    result = await auth.read_all_admin(header_param=header_param,db=db)
   
    result = jsonable_encoder(result)
    
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#-------------------------------------------------------------------------------
@auth_admin.get('/api/get-region-admin/{region}', dependencies=[Depends(HTTPBearer())])
async def get_region_admin(header_param: Request,region:str,db: Session = Depends(get_db),):
    result = await auth.read_region_admin(header_param=header_param,region=region,db=db)
   
    result = jsonable_encoder(result)
    
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#--------------------------------------------------------------------------------------
@auth_admin.get('/api/get-disactive-admin', dependencies=[Depends(HTTPBearer())])
async def get_users(header_param: Request,db: Session = Depends(get_db),):
    result = await auth.read_disactive_admin(header_param=header_param,db=db)
   
    result = jsonable_encoder(result)
    
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#--------------------------------------------------------------------------------
@auth_admin.get('/api/get-admin/{id}', dependencies=[Depends(HTTPBearer())])
async def get_admin(header_param: Request,id: int, db: Session = Depends(get_db)):
    result = await auth.read_admin(header_param=header_param,id=id, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#----------------------------------------------------------------------------------
@auth_admin.put('/api/update-admin/{id}', dependencies=[Depends(HTTPBearer())])
async def update_admin(id: int, header_param: Request, req: mod.AdminBase, db: Session = Depends(get_db)):
    result = await auth.update_admin(id=id, header_param=header_param, req=req, db=db)
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
#----------------------------------------------------------------------------------
@auth_admin.put('/api/update_disactive_admin/{id}', dependencies=[Depends(HTTPBearer())])
async def update_teacher(id: int, header_param: Request, req: disactive.Disactive_teacher, db: Session = Depends(get_db)):
    result = await auth.disactive_admines(id=id, header_param=header_param, req=req, db=db)
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


