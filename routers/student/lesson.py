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

lesson = APIRouter(tags=['lesson'])
@lesson.post("/api/add_lesson", dependencies=[Depends(HTTPBearer())])
async def create_lesson(header_param: Request,req: mod.Lesson_Base,db: Session = Depends(get_db),):
    result = await auth.create_lesson(header_param=header_param,req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
# -----------------------------------------------------------------------------------------------
@lesson.post('/api/create_img_lesson/{lesson_id}', dependencies=[Depends(HTTPBearer())])
async def create_video(
    lesson_id: int,
    header_param: Request,
    db: Session = Depends(get_db),
    files: List[UploadFile] = File(...)
):
    # Call the CRUD function to create videos
    created_videos = await auth.create_lesson_img(lesson_id, header_param, db, files)

    if created_videos is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    if created_videos:
        result = jsonable_encoder(created_videos)

        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={"msg": "No videos created"}, status_code=status.HTTP_204_NO_CONTENT)
#--------------------------------------------------------------------------------------
@lesson.get('/api/get_all_lesson/{course_id}', dependencies=[Depends(HTTPBearer())])
async def get_exam(course_id:int,header_param: Request,db: Session = Depends(get_db)):
    result = await auth.read_lesson(header_param=header_param, db=db,course_id=course_id)
    result = jsonable_encoder(result)
    print(result)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    elif result==-2:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="You dont have exam")
    elif result == None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Doesn't have exam this id")
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#--------------------------------------------------------------------------------------
@lesson.get('/api/get_lesson_by_id/{lesson_id}', dependencies=[Depends(HTTPBearer())])
async def get_exam(lesson_id:int,header_param: Request,db: Session = Depends(get_db)):
    result = await auth.read_lesson_by_id(header_param=header_param, db=db,lesson_id=lesson_id)
    result = jsonable_encoder(result)
    print(result)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    elif result==-2:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="You dont have exam")
    elif result == None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Doesn't have exam this id")
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#----------------------------------------------------------------------------------
#update exam
@lesson.put('/api/update_lesson/{id}', dependencies=[Depends(HTTPBearer())])
async def update_exam(id: int, header_param: Request, req: mod.Lesson_update_base, db: Session = Depends(get_db)):
    result = await auth.update_lesson(id=id, header_param=header_param, req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result:
        result = {'msg': 'Обновлено!'}
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)

#------------------------------------------------------------------------------
#delete exam
@lesson.delete('/api/delete_lesson/{id}', dependencies=[Depends(HTTPBearer())])
async def delete_homework( header_param: Request,id: int,db: Session = Depends(get_db)):
    result = await auth.delete_lesson(id=id, header_param=header_param, db=db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
#------------------------------------------------------------------------------
#delete exam
@lesson.delete('/api/delete_lesson_img/{id}', dependencies=[Depends(HTTPBearer())])
async def delete_homework( header_param: Request,id: int,db: Session = Depends(get_db)):
    result = await auth.delete_lesson_img(id=id, header_param=header_param, db=db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
#--------------------------------------------------------------------------------
@lesson.post("/api/add_lesson_comment", dependencies=[Depends(HTTPBearer())])
async def create_lesson(header_param: Request,req: mod.Lesson_Comment_base,db: Session = Depends(get_db),):
    result = await auth.create_lesson_comment(header_param=header_param,req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)