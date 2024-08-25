import models.teacher as mod
import models.superuser as login
from sqlalchemy.orm import Session, joinedload
from fastapi import Request
from sqlalchemy import and_, desc
import crud.teacher.auth_teacher as super_admin
import crud.student.auth as student
from fastapi.encoders import jsonable_encoder
from tokens.token import check_token, create_access_token, decode_token
from upload_depends import upload
from typing import List
from fastapi import UploadFile


async def create_homework(header_param: Request, req: mod.Homework_Base, db: Session,):
    user = await super_admin.check_teacher_token(header_param=header_param, db=db)
    if not user:
        return -1
    new_add = mod.Homework(
        lesson_time=req.lesson_time,
        title=req.title,
        subtitle=req.subtitle,
        course_id=req.course_id,
        
    )
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    else:
        return None
#---------------------------------------------------------------------------------------------
async def create_homework_answer(header_param: Request, req: mod.Homework_teacher_answer_Base, db: Session,):
    user = await super_admin.check_teacher_token(header_param=header_param, db=db)
    if not user:
        return -1
    new_add = mod.HomeworkAnswer(
        comment=req.comment,
        homework_id=req.homework_id,
        student_id=req.student_id,
        is_true=req.is_true,
        
    )
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    else:
        return None
#---------------------------------------------------------------------------------------------
async def create_student_homework_answer(header_param: Request, req: mod.Homework_answer_Base, db: Session,):
    user = await student.check_student_token(header_param=header_param, db=db)
    if not user:
        return -1
    new_add = mod.HomeworkAnswer(
        comment=req.comment,
        homework_id=req.homework_id,
        student_id=user.id,
        is_student=True
        
    )
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    else:
        return None
#--------------------------------------------------------------------------------------------
async def post_img_homework(id, header_param, db: Session, file):
    user = await super_admin.check_teacher_token(header_param, db)
    if not user:
        return -1
    uploaded_img = upload.upload_image(directory="homework_img", file=file)
    new_add = mod.Homework(img=uploaded_img)
    if new_add:
        req_json = jsonable_encoder(new_add)
        new_update = (
            db.query(mod.Homework)
            .filter(mod.Homework.id == id)
            .update(req_json, synchronize_session=False)
        )
        db.commit()
        
        return new_add
#--------------------------------------------------------------------------------------------
async def post_img_homework_answer(id, header_param, db: Session, file):
    user = await student.check_student_token(header_param, db)
    if not user:
        return -1
    uploaded_img = upload.upload_image(directory="homework_img", file=file)
    new_add = mod.HomeworkAnswer(img=uploaded_img,homework_id=id,student_id=user.id,is_img=True)
    if new_add:
        req_json = jsonable_encoder(new_add)
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        
        return new_add

# -----------------------------------------------------------------------------------------


async def read_homework(header_param: Request,  db: Session):
    user = await student.check_student_token(header_param=header_param, db=db)
    teacher = await super_admin.check_teacher_token(header_param=header_param, db=db)
    if not user or not teacher:
        return -1
    course=db.query(mod.CourseToGroup).filter(mod.CourseToGroup.group_id==user.group_id).first()
    if not course:
        return -2
    result = (
        db.query(mod.Homework)
        .filter(
            and_(
                mod.Homework.course_id == course.course_id,

            )
        )
        .all()
    )
    return result
# ----------------------------------------------------------------------------------


async def read_homework_by_id(id: int, header_param: Request,db: Session):
    user = await student.check_student_token(header_param=header_param, db=db)
    teacher = await super_admin.check_teacher_token(header_param=header_param, db=db)
    if not user or not teacher:
        return -1
    result = (
        db.query(mod.Homework)
        .filter(
            and_(
                mod.Homework.id == id,
                
            )
        )
        .first()
    )

    return result
#-----------------------------------------------------------------------------------------------
async def read_answer(id: int, header_param: Request,db: Session):
    user = await student.check_student_token(header_param=header_param, db=db)
    teacher = await super_admin.check_teacher_token(header_param=header_param, db=db)
    if not user or not teacher:
        return -1
    result = (
        db.query(mod.HomeworkAnswer)
        .filter(
            and_(
                mod.HomeworkAnswer.homework_id == id,
                mod.HomeworkAnswer.student_id==user.id
            )
        )
        .all()
    )
   
    return result

#--------------------------------------------------------------------------------------
async def delete_homework(id, header_param: Request, db: Session):
    user = await super_admin.check_teacher_token(header_param, db)
    if not user:
        return -1
    get_video = db.query(mod.Homework).filter(mod.Homework.id == id).first()
    if get_video.img!="":
        upload.delete_uploaded_image(image_name=get_video.img)
    new_delete = (
        db.query(mod.Homework).filter(mod.Homework.id == id).delete(synchronize_session=False)
    )
    db.commit()
    if new_delete:
        result = {"msg": "Удалено!"}
        return result

#--------------------------------------------------------------------------------
async def update_homework(id, req: mod.Homework_update_Base, header_param: Request, db: Session):
    user = await super_admin.check_teacher_token(header_param=header_param, db=db)
    if not user:
        return -1
    req_json = jsonable_encoder(req)
    user_exist = (
        db.query(mod.Homework).filter(
            and_(mod.Homework.id == id)).update(req_json, synchronize_session=False)
    )
    db.commit()
    if user_exist:
        return True
    else:
        return None