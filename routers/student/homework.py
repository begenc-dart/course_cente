from fastapi import APIRouter,Depends,HTTPException,status,Request,File, UploadFile
from sqlalchemy.orm import Session
import models.teacher.schemas as mod 
import models.superuser.schemas as login 
from db.connection import get_db
import crud.student as auth
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from typing import List

homework = APIRouter(tags=['homework'])
@homework.post("/api/add_homework", dependencies=[Depends(HTTPBearer())])
async def create_course(header_param: Request,req: mod.Homework_Base,db: Session = Depends(get_db),):
    result = await auth.create_homework(header_param=header_param,req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
# -----------------------------------------------------------------------------------
@homework.post('/api/post_image_student_answer/{homeworkd_id}', dependencies=[Depends(HTTPBearer())])
async def post_img_tutorial(homeworkd_id: int, header_param: Request, db: Session = Depends(get_db), file: UploadFile = File(...)):
    result = await auth.post_img_homework_answer(homeworkd_id, header_param, db, file)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        result['msg'] = 'Создано!'
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
# -----------------------------------------------------------------------------------
@homework.post('/api/post_image_homework/{id}', dependencies=[Depends(HTTPBearer())])
async def post_img_tutorial(id: int, header_param: Request, db: Session = Depends(get_db), file: UploadFile = File(...)):
    result = await auth.post_img_homework(id, header_param, db, file)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        result['msg'] = 'Создано!'
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
#--------------------------------------------------------------------------------------
@homework.get('/api/get-homework/', dependencies=[Depends(HTTPBearer())])
async def get_admin(header_param: Request,db: Session = Depends(get_db)):
    result = await auth.read_homework(header_param=header_param, db=db)
    result = jsonable_encoder(result)
    print(result)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    elif result==-2:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="You dont have homework")
    elif result == None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Doesn't have tutorial this id")
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#-----------------------------------------------------------------------------------
@homework.post("/api/add_homework_answer", dependencies=[Depends(HTTPBearer())])
async def create_course(header_param: Request,req: mod.Homework_teacher_answer_Base,db: Session = Depends(get_db),):
    result = await auth.create_homework_answer(header_param=header_param,req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
#-----------------------------------------------------------------------------------
@homework.post("/api/add_student_homework_answer", dependencies=[Depends(HTTPBearer())])
async def create_course(header_param: Request,req: mod.Homework_answer_Base,db: Session = Depends(get_db),):
    result = await auth.create_student_homework_answer(header_param=header_param,req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
#--------------------------------------------------------------------------------------
@homework.get('/api/get-homework/{id}', dependencies=[Depends(HTTPBearer())])
async def get_admin(header_param: Request,id:int,db: Session = Depends(get_db)):
    result = await auth.read_homework_by_id(id,header_param=header_param, db=db)
    result = jsonable_encoder(result)
    print(result)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    elif result==-2:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="You dont have homework")
    elif result == None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Doesn't have homework this id")
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#--------------------------------------------------------------------------------------
@homework.get('/api/get-answer/{homework_id}', dependencies=[Depends(HTTPBearer())])
async def get_admin(header_param: Request,homework_id:int,db: Session = Depends(get_db)):
    result = await auth.read_answer(homework_id,header_param=header_param, db=db)
    result = jsonable_encoder(result)
    print(result)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    elif result==-2:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="You dont have homework")
    elif result == None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Doesn't have answer this id")
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#------------------------------------------------------------------------------
@homework.delete('/api/delete-homework/{id}', dependencies=[Depends(HTTPBearer())])
async def delete_homework( header_param: Request,id: int,db: Session = Depends(get_db)):
    result = await auth.delete_homework(id=id, header_param=header_param, db=db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    elif result ==-2:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="this course added one group")
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
#----------------------------------------------------------------------------------
@homework.put('/api/update-homework/{id}', dependencies=[Depends(HTTPBearer())])
async def update_homework(id: int, header_param: Request, req: mod.Homework_update_Base, db: Session = Depends(get_db)):
    result = await auth.update_homework(id=id, header_param=header_param, req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result:
        result = {'msg': 'Обновлено!'}
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)

