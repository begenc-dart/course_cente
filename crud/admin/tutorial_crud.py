import models.admin as mod
import models.superuser as login
from sqlalchemy.orm import Session, joinedload
from fastapi import Request
from sqlalchemy import and_, desc
import crud.admin.auth_admin as super_admin
from fastapi.encoders import jsonable_encoder
from tokens.token import check_token, create_access_token, decode_token
from upload_depends import upload
from typing import List
from fastapi import UploadFile

async def create_tutorial(header_param: Request, req: mod.Tutorial_Base, db: Session,):
    user = await super_admin.check_admin_token(header_param=header_param, db=db)
    if not user or not user.is_add_tutorial :
        return -1
    new_add = mod.Tutorial(
        name=req.name,
        description=req.description,
    )
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    else:
        return None
# --------------------------------------------------------------------------------


async def read_all_tutorial(db: Session):
    result = (
        db.query(
            mod.Tutorial
        )

        .all()
    )
    # admin_short_list = [mod.Admin_short(id=admin.id, username=admin.username, name=admin.name,
    #                                     phone_number=admin.phone_number, surname=admin.surname) for admin in result]
    return result
# ----------------------------------------------------------------------------------


async def read_tutorial(id: int, db: Session):
    result = (
        db.query(mod.Tutorial)
        .filter(
            and_(
                mod.Tutorial.id == id,
            )
        ).options(joinedload(mod.Tutorial.folders).options(joinedload(mod.Folder.videos)))
        .first()
    )

    return result
# ------------------------------------------------------------------------------


async def create_folder_crud(header_param: Request, req: mod.Folder_Base, db: Session,):
    user = await super_admin.check_admin_token(header_param=header_param, db=db)
    if not user or not user.is_add_tutorial:
        return -1
    new_add = mod.Folder(
        folder_name=req.folder_name,
        tutorial_id=req.tutorial_id

    )
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    else:
        return None


async def post_img_tutorial(id, header_param, db: Session, file):
    user = await super_admin.check_admin_token(header_param, db)
    if not user or not user.is_add_tutorial:
        return -1
    uploaded_img = upload.upload_image(directory="tutorial_img", file=file)
    new_add = mod.Tutorial(img=uploaded_img)
    if new_add:
        req_json = jsonable_encoder(new_add)
        new_update = (
            db.query(mod.Tutorial)
            .filter(mod.Tutorial.id == id)
            .update(req_json, synchronize_session=False)
        )
        db.commit()
        
        return new_add

#--------------------------------------------------------------------------------------
async def create_video(folder_id: mod.Video_Base, header_param, db: Session, file):
    user = await super_admin.check_admin_token(header_param, db)
    if not user or not user.is_add_tutorial:
        return -1
    uploaded_img = upload.upload_image(directory="tutorial", file=file)
    new_add = mod.Video(video_name=uploaded_img, folder_id=folder_id)
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
#-----------------------------------------------------------------------------
async def create_videos(folder_id: int, header_param: Request, db: Session, files: List[UploadFile]):
    created_videos = []
    
    for file in files:
        # Example: process file (e.g., save it, extract metadata, etc.)
        # You might need to save the file or process it here.
        file_content =  upload.upload_image(directory="tutorial", file=file)
        # Create a new video instance
        new_video = mod.Video(
            video_name=file_content,  # or another attribute depending on your needs
            folder_id=folder_id,
            # Set other attributes as needed
        )
        
        # Add the new video to the session
        db.add(new_video)
        created_videos.append(new_video)
    
    # Commit all changes to the database
    db.commit()

    return created_videos
#--------------------------------------------------------------------------------------
async def delete_tutorial(id, header_param: Request, db: Session):
    user = await super_admin.check_admin_token(header_param, db)
    if not user or not user.is_add_tutorial:
        return -1
    new_delete = (
        db.query(mod.Tutorial).filter(mod.Tutorial.id == id).delete(synchronize_session=False)
    )
    db.commit()
    if new_delete:
        result = {"msg": "Удалено!"}
        return result
#-----------------------------------------------------------------------------------
async def delete_video(id, header_param: Request, db: Session):
    user = await super_admin.check_admin_token(header_param, db)
    if not user or not user.is_add_tutorial:
        return -1
    get_video = db.query(mod.Video).filter(mod.Video.id == id).first()
    if get_video.video_name is not None:
        upload.delete_uploaded_image(image_name=get_video.video_name)
    new_delete = (
        db.query(mod.Video).filter(mod.Video.id == id).delete(synchronize_session=False)
    )
    db.commit()
    if new_delete:
        result = {"msg": "Удалено!"}
        return result
#-------------------------------------------------------------------------------------
async def delete_folder(id, header_param: Request, db: Session):
    user = await super_admin.check_admin_token(header_param, db)
    if not user or not user.is_add_tutorial:
        return -1
    
    new_delete = (
        
        db.query(mod.Folder).filter(mod.Folder.id == id).delete(synchronize_session=False),
        db.query(mod.Video).filter(mod.Video.folder_id==id).delete(synchronize_session=False)
    )
    db.commit()
    if new_delete:
        result = {"msg": "Удалено!"}
        return result
#--------------------------------------------------------------------------------
async def update_tutorial(id, req: mod.Tutorial_Base, header_param: Request, db: Session):
    user = await super_admin.check_admin_token(header_param=header_param, db=db)
    if not user and not user.is_add_tutorial:
        return -1
    req_json = jsonable_encoder(req)
    user_exist = (
        db.query(mod.Tutorial).filter(
            and_(mod.Tutorial.id == id)).update(req_json, synchronize_session=False)
    )
    db.commit()
    if user_exist:
        return True
    else:
        return None
#--------------------------------------------------------------------------------
async def update_folder(id, req: mod.Folder_Base, header_param: Request, db: Session):
    user = await super_admin.check_admin_token(header_param=header_param, db=db)
    if not user and not user.is_add_tutorial:
        return -1
    req_json = jsonable_encoder(req)
    user_exist = (
        db.query(mod.Folder).filter(
            and_(mod.Folder.id == id)).update(req_json, synchronize_session=False)
    )
    db.commit()
    if user_exist:
        return True
    else:
        return None