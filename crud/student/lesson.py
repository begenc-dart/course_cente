import models.teacher as mod

from sqlalchemy.orm import Session, joinedload
from fastapi import Request
from sqlalchemy import and_, desc
import crud.teacher.auth_teacher as super_admin
import crud.superuser.auth as superadmin
import crud.student.auth as student
from fastapi.encoders import jsonable_encoder
from tokens.token import check_token, create_access_token, decode_token
from upload_depends import upload
from typing import List
from fastapi import UploadFile


async def create_lesson(header_param: Request, req: mod.Lesson_Base, db: Session,):
    user = await super_admin.check_teacher_token(header_param=header_param, db=db)
    if not user:
        return -1
    new_add = mod.Lesson(
        course_id=req.course_id,
        name=req.name,
        descrition=req.descrition,
    )
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    else:
        return None
# -----------------------------------------------------------------------------


async def create_lesson_img(lesson_id: int, header_param: Request, db: Session, files: List[UploadFile]):
    created_videos = []

    for file in files:
        # Example: process file (e.g., save it, extract metadata, etc.)
        # You might need to save the file or process it here.
        file_content = upload.upload_image(directory="tutorial", file=file)
        # Create a new video instance
        new_video = mod.Lesson_img(
            img_url=file_content,  # or another attribute depending on your needs
            lesson_id=lesson_id,
            # Set other attributes as needed
        )

        # Add the new video to the session
        db.add(new_video)
        created_videos.append(new_video)

    # Commit all changes to the database
    db.commit()

    return created_videos
# -----------------------------------------------------------------------------------------

# exam get


async def read_lesson(course_id: int, header_param: Request,  db: Session):
    user = await student.check_student_token(header_param=header_param, db=db)
    teacher = await super_admin.check_teacher_token(header_param=header_param, db=db)
    super = await superadmin.check_super_admin_token(header_param=header_param, db=db)
    if not user and not teacher and not super:
        return -1
    result = (
        db.query(mod.Lesson)
        .filter(
            and_(
                mod.Lesson.course_id == course_id,

            )
        )
        .all()
    )
    return result


async def read_lesson_by_id(lesson_id: int, header_param: Request,  db: Session):
    user = await student.check_student_token(header_param=header_param, db=db)
    teacher = await super_admin.check_teacher_token(header_param=header_param, db=db)
    if not user and not teacher:
        return -1
    result = (
        db.query(mod.Lesson)
        .filter(
            and_(
                mod.Lesson.id == lesson_id

            )
        ).options(joinedload(mod.Lesson.lesson_img)).options(joinedload(mod.Lesson.lesson_comments).options(joinedload(mod.Lesson_comment.student)).options(joinedload(mod.Lesson_comment.teacher)))
        .all()
    )
    return result
# --------------------------------------------------------------------------------------


async def delete_lesson(id, header_param: Request, db: Session):
    user = await super_admin.check_teacher_token(header_param, db)
    if not user:
        return -1

    new_delete = (
        db.query(mod.Lesson).filter(mod.Lesson.id == id).delete(
            synchronize_session=False)
    )
    db.commit()
    if new_delete:
        result = {"msg": "Удалено!"}
        return result
# --------------------------------------------------------------------------------------


async def delete_lesson_img(id, header_param: Request, db: Session):
    user = await super_admin.check_teacher_token(header_param, db)
    if not user:
        return -1

    new_delete = (
        db.query(mod.Lesson_img).filter(mod.Lesson_img.id == id).delete(
            synchronize_session=False)
    )
    db.commit()
    if new_delete:
        result = {"msg": "Удалено!"}
        return result

# --------------------------------------------------------------------------------


async def update_lesson(id, req: mod.Lesson_update_base, header_param: Request, db: Session):
    user = await super_admin.check_teacher_token(header_param=header_param, db=db)
    if not user:
        return -1
    req_json = jsonable_encoder(req)
    user_exist = (
        db.query(mod.Lesson).filter(
            and_(mod.Lesson.id == id)).update(req_json, synchronize_session=False)
    )
    db.commit()
    if user_exist:
        return True
    else:
        return None
# -----------------------------------------------------------------------


async def create_lesson_comment(header_param: Request, req: mod.Lesson_Comment_base, db: Session,):
    user = await student.check_student_token(header_param=header_param, db=db)
    teacher = await super_admin.check_teacher_token(header_param=header_param, db=db)
    if not user and not teacher:
        return -1
    if teacher:
        new_add = mod.Lesson_comment(
            comment=req.comment,
            teacher_id=teacher.id,
            lesson_id=req.lesson_id
        )
    else:
        new_add = mod.Lesson_comment(
            comment=req.comment,
            student_id=user.id,
            lesson_id=req.lesson_id
        )
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    else:
        return None
