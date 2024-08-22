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
tutorial = APIRouter(tags=['tutorial'])


@tutorial.post('/api/create-tutorial/', dependencies=[Depends(HTTPBearer())])
async def create_tutorial(tutorial: mod.Tutorial_Base, header_param: Request, db: Session = Depends(get_db),):
    result = await crud.create_tutorial(header_param, req=tutorial, db=db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        result['msg'] = 'Создано!'
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
# -----------------------------------------------------------------------------------
@tutorial.post('/api/post_image_tutorial/{id}', dependencies=[Depends(HTTPBearer())])
async def post_img_tutorial(id: int, header_param: Request, db: Session = Depends(get_db), file: UploadFile = File(...)):
    result = await crud.post_img_tutorial(id, header_param, db, file)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        result['msg'] = 'Создано!'
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
# -----------------------------------------------------------------------------------
@tutorial.get('/api/read_tutorial', )
async def get_all_tutorial(db: Session = Depends(get_db),):
    result = await crud.read_all_tutorial(db=db)

    result = jsonable_encoder(result)

    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
# -------------------------------------------------------------------------------------
@tutorial.get('/api/get-tutorial/{id}')
async def get_admin(id: int, db: Session = Depends(get_db)):
    result = await crud.read_tutorial(id=id, db=db)
    result = jsonable_encoder(result)
    print(result)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    elif result == None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Doesn't have tutorial this id")
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
# ----------------------------------------------------------------------------
@tutorial.post('/api/create-folder/', dependencies=[Depends(HTTPBearer())])
async def create_folder(tutorial: mod.Folder_Base, header_param: Request, db: Session = Depends(get_db),):
    result = await crud.create_folder_crud(header_param, req=tutorial, db=db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        result['msg'] = 'Создано!'
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
# ---------------------------------------------------------------------------------------
@tutorial.post('/api/create-video/{folder_id}', dependencies=[Depends(HTTPBearer())])
async def create_video(folder_id: int, header_param: Request, db: Session = Depends(get_db), file: UploadFile = File(...)):
    result = await crud.create_video(folder_id, header_param, db, file)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        result['msg'] = 'Создано!'
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
# -----------------------------------------------------------------------------------------------
@tutorial.post('/api/create-video_list/{folder_id}', dependencies=[Depends(HTTPBearer())])
async def create_video(
    folder_id: int,
    header_param: Request,
    db: Session = Depends(get_db),
    files: List[UploadFile] = File(...)
):
    # Call the CRUD function to create videos
    created_videos = await crud.create_videos(folder_id, header_param, db, files)

    if created_videos is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    if created_videos:
        result = jsonable_encoder(created_videos)

        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={"msg": "No videos created"}, status_code=status.HTTP_204_NO_CONTENT)
# ---------------------------------------------------------------------------------


@tutorial.delete('/api/delete-tutorial/{id}', dependencies=[Depends(HTTPBearer())])
async def delete_tutorial(id: int, header_param: Request, db: Session = Depends(get_db)):
    result = await crud.delete_tutorial(id, header_param, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
#-------------------------------------------------------------------------------
@tutorial.delete('/api/delete-video/{id}', dependencies=[Depends(HTTPBearer())])
async def delete_videos(id: int, header_param: Request, db: Session = Depends(get_db)):
    result = await crud.delete_video(id, header_param, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
#---------------------------------------------------------------------------------
@tutorial.delete('/api/delete-folder/{id}', dependencies=[Depends(HTTPBearer())])
async def delete_videos(id: int, header_param: Request, db: Session = Depends(get_db)):
    result = await crud.delete_folder(id, header_param, db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
#----------------------------------------------------------------------------------
@tutorial.put('/api/update-tutorial/{id}', dependencies=[Depends(HTTPBearer())])
async def update_tutorial(id: int, header_param: Request, req: mod.Tutorial_Base, db: Session = Depends(get_db)):
    result = await crud.update_tutorial(id=id, header_param=header_param, req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result:
        result = {'msg': 'Обновлено!'}
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
#----------------------------------------------------------------------------------
@tutorial.put('/api/update-folder/{id}', dependencies=[Depends(HTTPBearer())])
async def update_folder(id: int, header_param: Request, req: mod.Folder_Base, db: Session = Depends(get_db)):
    result = await crud.update_folder(id=id, header_param=header_param, req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result:
        result = {'msg': 'Обновлено!'}
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


