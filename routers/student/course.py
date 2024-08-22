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

course = APIRouter(tags=['course'])

@course.post("/api/add_course", dependencies=[Depends(HTTPBearer())])
async def create_course(header_param: Request,req: mod.Course_Base,db: Session = Depends(get_db),):
    result = await auth.create_course(header_param=header_param,req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
#------------------------------------------------------------------------------
@course.delete('/api/delete-course/{id}', dependencies=[Depends(HTTPBearer())])
async def delete_course(id: int, header_param: Request, db: Session = Depends(get_db)):
    result = await auth.delete_course(id, header_param, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    elif result ==-2:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="this course added one group")
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)

#-------------------------------------------------------------------------------------
@course.post("/api/add_course_to_group", dependencies=[Depends(HTTPBearer())])
async def create_course(header_param: Request,req: mod.Course_Group,db: Session = Depends(get_db),):
    result = await auth.create_course_to_group(header_param=header_param,req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result ==-2:
        return HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail="Already add to course this group")
    elif result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

#------------------------------------------------------------------------------
@course.delete('/api/delete-course_to_group/', dependencies=[Depends(HTTPBearer())])
async def delete_course_to_group( header_param: Request,req: mod.Course_Group,db: Session = Depends(get_db)):
    result = await auth.delete_course_to_group(req=req, header_param=header_param, db=db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    elif result ==-2:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="this course added one group")
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
#--------------------------------------------------------------------------------------
@course.get('/api/get-course/', dependencies=[Depends(HTTPBearer())])
async def get_admin(header_param: Request,db: Session = Depends(get_db)):
    result = await auth.read_course(header_param=header_param, db=db)
    result = jsonable_encoder(result)
    print(result)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    elif result == None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Doesn't have tutorial this id")
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#--------------------------------------------------------------------------------------
@course.get('/api/get-group-to_course/{id}', dependencies=[Depends(HTTPBearer())])
async def get_group_to_course(id:int,header_param: Request,db: Session = Depends(get_db)):
    result = await auth.read_course_group(id=id,header_param=header_param, db=db)
    result = jsonable_encoder(result)
    print(result)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    elif result == None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Doesn't have tutorial this id")
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)