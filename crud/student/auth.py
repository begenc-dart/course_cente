import models.teacher as mod
import models.superuser as login
from sqlalchemy.orm import Session, joinedload
from fastapi import Request
from sqlalchemy import and_, desc
import crud.admin.auth_admin as super_admin
from fastapi.encoders import jsonable_encoder
from tokens.token import check_token, create_access_token, decode_token
import crud.teacher.auth_teacher as teacher
from datetime import datetime, timedelta
import models.superuser as login
import crud.teacher.auth_teacher as teacher



async def create_group_crud(header_param: Request, req: mod.Group_Base, db: Session,):
    user = await super_admin.check_admin_token(header_param=header_param, db=db)
    if not user or not user.is_add_teacher:
        return -1
    new_add = mod.Group(
        group_name=req.group_name,
        teacher_id=req.teacher_id,
        start_time=req.start_time,
        end_time=req.end_time
    )
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    else:
        return None
# ------------------------------------------------------------------------------------


async def create_group_time_crud(header_param: Request, req: mod.GroupTime_Base, db: Session,):
    user = await super_admin.check_admin_token(header_param=header_param, db=db)
    if not user or not user.is_add_teacher:
        return -1

    new_add = mod.GroupTime(
        week_number=req.week_number,
        group_id=req.group_id,

    )
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    else:
        return None
# ----------------------------------------------------------------------------------------


async def read_all_group(header_param: Request, db: Session):
    
    teache = await teacher.check_teacher_token(header_param=header_param, db=db)
    if not teache:
        return -1
    now = datetime.now()
    one_week_later = now + timedelta(weeks=1)
    result = (
        db.query(
            mod.Group
        ).filter(mod.Group.teacher_id == teache.id).all()
    )
    print(result)
    # admin_short_list = [mod.Admin_short(id=admin.id, username=admin.username, name=admin.name,
    #                                     phone_number=admin.phone_number, surname=admin.surname) for admin in result]
    return result
# --------------------------------------------------------------------------------------


async def read_one_group(id: int, db: Session):
    result = (
        db.query(mod.Group)
        .filter(
            and_(
                mod.Group.id == id,
            )
        ).options(joinedload(mod.Group.group_times)).options(joinedload(mod.Group.students)).options(joinedload(mod.Group.course_to_groups))
        .first()
    )

    return result

# -----------------------------------------------------------------------------------------------


async def create_student_crud(header_param: Request, req: mod.Student_Base, db: Session,):
    user = await super_admin.check_admin_token(header_param=header_param, db=db)
    if not user and not user.is_add_teacher:
        return -1
    new_delete = (
        db.query(mod.Student)
        .filter(and_(mod.Student.username == req.username))
    ).first()
    if new_delete:
        return False
    
    update = db.query(mod.Group).filter(mod.Group.id == req.group_id).update(
        {"child_count":mod.Group.child_count+1}, synchronize_session='evaluate')
    db.commit()
    new_dict = {"username": req.username, "password": req.password}
    access_token = await create_access_token(data=new_dict)
    new_add = mod.Student(
        name=req.name,
        surname=req.surname,
        token=access_token,
        username=req.username,
        password=req.password,
        parent_name=req.parent_name,
        phone_number=req.phone_number,
        parent_number=req.parent_number,
        group_id=req.group_id,
        is_active=True
    )
    if new_add and update:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    else:
        return None
# ---------------------------------------------------------------------------


async def disactive_students(id, req: mod.Disactive_teacher, header_param: Request, db: Session):
    user = await super_admin.check_admin_token(header_param=header_param, db=db)
    if not user:
        return -1
    user_exist = (
        db.query(mod.Student).filter(and_(mod.Student.id == id)).first()
    )

    if not user_exist:
        return -2
    req_json = jsonable_encoder(req)
    new_update = (
        db.query(mod.Student)
        .filter(mod.Student.id == id)
        .update(req_json, synchronize_session=False)
    )
    db.commit()
    if new_update:
        return True
    else:
        return None
# ----------------------------------------------------------------------


async def read_disactive_student(header_param: Request, db: Session):
    user = await super_admin.check_admin_token(header_param=header_param, db=db)
    if not user:
        return -1
    result = (
        db.query(
            mod.Student
        ).filter(mod.Student.is_active == False)
        .order_by(desc(mod.Student.id))
        .distinct()
        .all()
    )
    return result
# -------------------------------------------------------------------------------------------


async def update_student(id, req: mod.Student_Base, header_param: Request, db: Session):
    user = await super_admin.check_admin_token(header_param=header_param, db=db)
    if not user or not user.is_add_teacher:
        return -1
    user_exist = (
        db.query(mod.Student).filter(
            and_(mod.Student.username == req.username)).first()
    )

    if user_exist and user_exist.id != id:
        return -2
    req_json = jsonable_encoder(req)
    new_update = (
        db.query(mod.Student)
        .filter(mod.Student.id == id)
        .update(req_json, synchronize_session=False)
    )
    db.commit()
    if new_update:
        return True
    else:
        return None
# Disactive teacher


# ----------------------------------------------------------------------------------------------
async def read_student(header_param: Request, id: int, db: Session):
    user = await super_admin.check_admin_token(header_param=header_param, db=db)
    student = await check_student_token(header_param=header_param, db=db)
    teache = await teacher.check_teacher_token(header_param=header_param, db=db)
    if not user and not student and not teache:
        return -1

    result = (
        db.query(mod.Student)
        .filter(
            and_(
                mod.Student.id == id,
                mod.Student.is_active == True

            )
        )
        .first()
    )
    return result


async def read_student_all(header_param: Request, group_id: int, db: Session):
    user = await super_admin.check_admin_token(header_param=header_param, db=db)
    student = await check_student_token(header_param=header_param, db=db)
    teache = await teacher.check_teacher_token(header_param=header_param, db=db)
    if not user and not student and not teache:
        return -1

    result = (
        db.query(mod.Student)
        .filter(
            and_(
                mod.Student.group_id == group_id,


            )
        )
        .all()
    )
    return result
# --------------------------------------------------------------------------------------------------

async def check_student_token(header_param: Request, db: Session):
    token = await check_token(header_param=header_param)
    if not token:
        return None
    payload = await decode_token(token=token)
    if not payload:
        return None
    username: str = payload.get("username")
    password: str = payload.get("password")
    result = await read_student_by_username_password(
        username=username, password=password, db=db
    )
    print(username)
    if result:
        return result
    else:
        return None
#---------------------------------------------------------------------

    
async def student_login(req: login.LoginSchema, db: Session):
    result = await read_student_by_username_password(req.username, req.password, db)
    if result:
        return result
    else:
        return None

# -------------------------------------------------------------------------


async def read_student_by_username_password(username: str, password: str, db: Session):
    result = (
        db.query(
            mod.Student
        )
        .filter(
            and_(
                mod.Student.username == username,
                mod.Student.password == password,
                mod.Student.is_active == True
            )
        )
        .first()
    )
    print(username)
    print(password)
    if result:
        return result
    else:
        return None
