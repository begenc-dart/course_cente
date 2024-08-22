import models.teacher as mod
import models.superuser as login
from sqlalchemy.orm import Session, joinedload
from fastapi import Request
from sqlalchemy import and_, desc
import crud.teacher.auth_teacher as super_admin
from fastapi.encoders import jsonable_encoder
from tokens.token import check_token, create_access_token, decode_token
from upload_depends import upload
from typing import List
from fastapi import UploadFile


async def create_course(header_param: Request, req: mod.Course_Base, db: Session,):
    user = await super_admin.check_teacher_token(header_param=header_param, db=db)
    if not user:
        return -1
    new_add = mod.Course(
        teacher_id=user.id,
        course_name=req.name
    )
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    else:
        return None
# -----------------------------------------------------------------------------------------


async def delete_course(id, header_param: Request, db: Session):
    user = await super_admin.check_teacher_token(header_param, db)
    if not user:
        return -1
    is_group = db.query(mod.CourseToGroup).filter(
        mod.CourseToGroup.course_id == id).first()
    if is_group:
        return -2
    new_delete = (

        db.query(mod.Course).filter(mod.Course.id ==
                                    id).delete(synchronize_session=False),

    )
    db.commit()
    if new_delete:
        result = {"msg": "Удалено!"}
        return result
# -----------------------------------------------------------------------------------------


async def delete_course_to_group(req: mod.Course_Group, header_param: Request, db: Session):
    user = await super_admin.check_teacher_token(header_param, db)
    if not user:
        return -1
    new_delete = (

        db.query(mod.CourseToGroup).filter(and_(mod.CourseToGroup.group_id == req.group_id,
                                                mod.CourseToGroup.course_id == req.course_id)).delete(synchronize_session=False),

    )
    db.commit()
    if new_delete:
        result = {"msg": "Удалено!"}
        return result
# -----------------------------------------------------------------------------------------


async def read_course(header_param: Request,  db: Session):
    user = await super_admin.check_teacher_token(header_param=header_param, db=db)
    if not user:
        return -1

    result = (
        db.query(mod.Course)
        .filter(
            and_(
                mod.Course.teacher_id == user.id,

            )
        ).options(joinedload(mod.Course.course_to_groups))
        .all()
    )
    return result
# ----------------------------------------------------------------------------------------


async def create_course_to_group(header_param: Request, req: mod.Course_Group, db: Session,):
    user = await super_admin.check_teacher_token(header_param=header_param, db=db)
    if not user:
        return -1
    is_groups = db.query(mod.CourseToGroup).filter(
        mod.CourseToGroup.group_id == req.group_id).first()
    if is_groups:
        return -2
    new_add = mod.CourseToGroup(
        group_id=req.group_id,
        course_id=req.course_id,

    )
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    else:
        return None


async def read_course_group(id: int, header_param: Request,  db: Session):
    user = await super_admin.check_teacher_token(header_param=header_param, db=db)
    if not user:
        return -1

    result = (
        db.query(mod.CourseToGroup)
        .filter(

            mod.CourseToGroup.group_id == id,

        ).options(joinedload(mod.CourseToGroup.course))
        .all()
    )
    return result
