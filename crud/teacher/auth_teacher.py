import models.teacher as mod
import models.superuser as login
from sqlalchemy.orm import Session
from fastapi import Request
from sqlalchemy import and_, desc
import crud.admin.auth_admin as super_admin
from fastapi.encoders import jsonable_encoder
from tokens.token import check_token, create_access_token, decode_token

async def check_teacher_token(header_param: Request, db: Session):
    token = await check_token(header_param=header_param)
    if not token:
        return None
    payload = await decode_token(token=token)
    if not payload:
        return None
    username: str = payload.get("username")
    password: str = payload.get("password")
    result = await read_teacher_by_username_password(
        username=username, password=password, db=db
    )
    print(username)
    if result:
        return result
    else:
        return None
#---------------------------------------------------------------------
async def read_teacher_by_username_password(username: str, password: str, db: Session):
    result = (
        db.query(
            mod.Teacher
        )
        .filter(
            and_(
                mod.Teacher.username == username,
                mod.Teacher.password == password,
                mod.Teacher.is_active == True
            )
        )
        .first()
    )
    
    print(password)
    if result:
        return result
    else:
        return None
#-------------------------------------------------------------------------------------------
async def create_techer_crud(header_param: Request, req: mod.CreateTeacherBase, db: Session,):
    user = await super_admin.check_admin_token(header_param=header_param, db=db)
    if not user or not user.is_add_teacher:
        return -1
    new_delete = (
        db.query(mod.Teacher)
        .filter(and_(mod.Teacher.username == req.username))
    ).first()
    if new_delete:
        return False
    new_dict = {"username": req.username, "password": req.password}
    access_token = await create_access_token(data=new_dict)
    new_add = mod.Teacher(
        username=req.username,
        password=req.password,
        token=access_token,
        phone_number=req.phone_number,
        name=req.name,
        surname=req.surname,
        region=req.region,
        is_active=True
    )
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    else:
        return None


async def teacher_login(req: login.LoginSchema, db: Session):
    result = await read_teacher_by_username_password(req.username, req.password, db)
    if result:
        return result
    else:
        return None



# read all users


async def read_all_teacher(header_param: Request, db: Session):
    user = await super_admin.check_admin_token(header_param=header_param, db=db)
   
    if not user or not user.is_add_teacher:
        return -1
    result = (
        db.query(
            mod.Teacher
        ).filter(mod.Teacher.is_active == True)
        .order_by(desc(mod.Teacher.id))
        .distinct()
        .all()
    )
    return result
# read disactive teacher


async def read_disactive_teacher(header_param: Request, db: Session):
    user = await super_admin.check_admin_token(header_param=header_param, db=db)
    if not user or not user.is_add_teacher:
        return -1
    result = (
        db.query(
            mod.Teacher
        ).filter(mod.Teacher.is_active == False)
        .order_by(desc(mod.Teacher.id))
        .distinct()
        .all()
    )
    return result
# read all same region


async def read_region_teacher(header_param: Request, region: str, db: Session):
    user = await super_admin.check_admin_token(header_param=header_param, db=db)
    if not user or not user.is_add_teacher:
        return -1

    result = (
        db.query(
            mod.Teacher
        ).filter(
            and_(
                mod.Teacher.region == region,
                mod.Teacher.is_active == True
            )

        )

        .order_by(desc(mod.Teacher.id))
        .distinct()
        .all()
    )

    return result
# read teacher with id


async def read_teacher(header_param: Request, id: int, db: Session):
    user = await super_admin.check_admin_token(header_param=header_param, db=db)
    teacher= await check_teacher_token(header_param=header_param, db=db)
    if not user  and not teacher:
        return -1
    if user:
        if not user.is_add_teacher:
            return -1

    result = (
        db.query(mod.Teacher)
        .filter(
            and_(
                mod.Teacher.id == id,
                mod.Teacher.is_active == True

            )
        )
        .first()
    )
    return result
# update teacher


async def update_teacher(id, req: mod.CreateTeacherBase, header_param: Request, db: Session):
    user = await super_admin.check_admin_token(header_param=header_param, db=db)
    if not user or not user.is_add_teacher:
        return -1
    user_exist = (
        db.query(mod.Teacher).filter(
            and_(mod.Teacher.username == req.username)).first()
    )

    if user_exist and user_exist.id != id:
        return -2
    req_json = jsonable_encoder(req)
    new_update = (
        db.query(mod.Teacher)
        .filter(mod.Teacher.id == id)
        .update(req_json, synchronize_session=False)
    )
    db.commit()
    if new_update:
        return True
    else:
        return None
# Disactive teacher


async def disactive_teacheres(id, req: mod.Disactive_teacher, header_param: Request, db: Session):
    user = await super_admin.check_admin_token(header_param=header_param, db=db)
    if not user or not user.is_add_teacher:
        return -1
    user_exist = (
        db.query(mod.Teacher).filter(and_(mod.Teacher.id == id)).first()
    )

    if not user or not user.is_add_teacher_exist:
        return -2
    req_json = jsonable_encoder(req)
    new_update = (
        db.query(mod.Teacher)
        .filter(mod.Teacher.id == id)
        .update(req_json, synchronize_session=False)
    )
    db.commit()
    if new_update:
        return True
    else:
        return None
