from fastapi import APIRouter, Depends, HTTPException, status, Request, File, UploadFile
from sqlalchemy.orm import Session
import models.admin.schemas as mod
import models.teacher.schemas as disactive
from db.connection import get_db
import crud.admin as crud
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from typing import List
project = APIRouter(tags=['project'])


@project.post('/api/create-project/', dependencies=[Depends(HTTPBearer())])
async def create_tutorial(tutorial: mod.Project_Base, header_param: Request, db: Session = Depends(get_db),):
    result = await crud.create_project(header_param, req=tutorial, db=db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        result['msg'] = 'Создано!'
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
# ---------------------------------------------------------------------------------------
@project.post('/api/create_project_img/{project_id}', dependencies=[Depends(HTTPBearer())])
async def create_video(project_id: int, header_param: Request, db: Session = Depends(get_db), file: UploadFile = File(...)):
    result = await crud.post_img_project(project_id, header_param, db, file)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        result['msg'] = 'Создано!'
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
# -----------------------------------------------------------------------------------
@project.get('/api/read_project', )
async def get_all_tutorial(db: Session = Depends(get_db),):
    result = await crud.read_all_project(db=db)

    result = jsonable_encoder(result)

    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#----------------------------------------------------------------------------
@project.delete('/api/delete-project/{project_id}', dependencies=[Depends(HTTPBearer())])
async def delete_tutorial(project_id: int, header_param: Request, db: Session = Depends(get_db)):
    result = await crud.delete_project(project_id, header_param, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)

#----------------------------------------------------------------------------------
@project.put('/api/update-project/{id}', dependencies=[Depends(HTTPBearer())])
async def update_tutorial(id: int, header_param: Request, req: mod.Tutorial_Base, db: Session = Depends(get_db)):
    result = await crud.update_project(id=id, header_param=header_param, req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result:
        result = {'msg': 'Обновлено!'}
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)