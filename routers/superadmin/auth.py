from fastapi import APIRouter,Depends,HTTPException,status,Request
from sqlalchemy.orm import Session
import models.superuser.schemas as mod 
from db.connection import get_db
import crud.superuser as auth
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
authentication_router = APIRouter(tags=['super_admin'])


@authentication_router.post("/api/create-superadmin",status_code=status.HTTP_200_OK)
async def create_superadmin(req: mod.SuperAdminBase,db: Session = Depends(get_db)):
    result = await auth.create_superadmin_crud(req=req, db=db)
    if not result:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Your username already have!!!")
    result = jsonable_encoder(result)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
#----------------------------------------------------------------------------------
@authentication_router.post('/api/login-superadmin')
async def login_admin(req: mod.LoginSchema, db: Session = Depends(get_db)):
    result = await auth.super_admin_login(req, db)
    # print(result)
    result = jsonable_encoder(result)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Логин или пароль неверный!')
#-------------------------------------------------------------------------------------
