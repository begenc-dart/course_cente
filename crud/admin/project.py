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


async def create_project(header_param: Request, req: mod.Project_Base, db: Session,):
    user = await super_admin.check_admin_token(header_param=header_param, db=db)
    if not user or not user.is_add_project:
        return -1
    new_add = mod.Project(
        url_project=req.url_project,
        name=req.name,
        description=req.description
    )
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    else:
        return None
#---------------------------------------------------------------------------
async def post_img_project(project_id, header_param, db: Session, file):
    user = await super_admin.check_admin_token(header_param, db)
    if not user or not user.is_add_project:
        return -1
    uploaded_img = upload.upload_image(directory="project_img", file=file)
    new_add = mod.Project(img_url=uploaded_img)
    if new_add:
        req_json = jsonable_encoder(new_add)
        new_update = (
            db.query(mod.Project)
            .filter(mod.Project.id == project_id)
            .update(req_json, synchronize_session=False)
        )
        db.commit()
        
        return new_add
#-----------------------------------------------------------------------------

async def read_all_project(db: Session):
    result = (
        db.query(
            mod.Project
        )
        .all()
    )
    # admin_short_list = [mod.Admin_short(id=admin.id, username=admin.username, name=admin.name,
    #                                     phone_number=admin.phone_number, surname=admin.surname) for admin in result]
    return result
#-------------------------------------------------------------------------
async def delete_project(id, header_param: Request, db: Session):
    user = await super_admin.check_admin_token(header_param, db)
    if not user or not user.is_add_project:
        return -1
    new_delete = (
        db.query(mod.Project).filter(mod.Project.id == id).delete(synchronize_session=False)
    )
    db.commit()
    if new_delete:
        result = {"msg": "Удалено!"}
        return result
#--------------------------------------------------------------------------------
async def update_project(id, req: mod.Project_Base, header_param: Request, db: Session):
    user = await super_admin.check_admin_token(header_param=header_param, db=db)
    if not user and not user.is_add_project:
        return -1
    req_json = jsonable_encoder(req)
    user_exist = (
        db.query(mod.Project).filter(
            and_(mod.Project.id == id)).update(req_json, synchronize_session=False)
    )
    db.commit()
    if user_exist:
        return True
    else:
        return None