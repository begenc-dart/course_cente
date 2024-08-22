import models.superuser as mod
import models.teacher as disavtive
from sqlalchemy.orm import Session
from fastapi import Request
from sqlalchemy import and_, desc
import crud.superuser.auth as super_admin
from fastapi.encoders import jsonable_encoder
from tokens.token import check_token, create_access_token, decode_token


async def create_admin_crud(header_param: Request, req: mod.AdminBase, db: Session,):
    user = await super_admin.check_super_admin_token(header_param=header_param, db=db)
    if not user:
        return -1

    new_delete = (
        db.query(mod.Admin)
        .filter(and_(mod.Admin.username == req.username))
    ).first()
    if new_delete:
        return None
    new_dict = {"username": req.username, "password": req.password}
    access_token = await create_access_token(data=new_dict)
    new_add = mod.Admin(
        username=req.username,
        password=req.password,
        token=access_token,
        phone_number=req.phone_number,
        name=req.name,
        region=req.region,
        surname=req.surname,
        is_add_teacher=req.is_add_teacher,
        is_add_tutorial=req.is_add_tutorial,
        is_add_calendar=req.is_add_calendar,
        is_add_news=req.is_add_news,
        is_add_project=req.is_add_project,
        is_add_student=req.is_add_student,
        is_active=True,
    )
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    else:
        return None

# ------------------------------------------------------------


async def admin_login(req: mod.LoginSchema, db: Session):
    result = await read_admin_by_username_password(req.username, req.password, db)
    if result:
        return result
    else:
        return None
# -------------------------------------------------------------------------


async def read_admin_by_username_password(username: str, password: str, db: Session):
    result = (
        db.query(
            mod.Admin
        )
        .filter(
            and_(
                mod.Admin.username == username,
                mod.Admin.password == password,
                mod.Admin.is_active == True
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
# read all users


async def read_all_admin(header_param: Request, db: Session):
    user = await super_admin.check_super_admin_token(header_param=header_param, db=db)
    if not user:
        return -1

    result = (
        db.query(
            mod.Admin
        )
        .filter(mod.Admin.is_active == True)
        .order_by(desc(mod.Admin.id))
        .distinct()
        .all()
    )
    admin_short_list = [mod.Admin_short(id=admin.id, username=admin.username, name=admin.name,
                                        phone_number=admin.phone_number, surname=admin.surname) for admin in result]
    return admin_short_list
# read user


async def read_admin(header_param: Request, id: int, db: Session):
    user = await super_admin.check_super_admin_token(header_param=header_param, db=db)
    if not user:
        return -1

    result = (
        db.query(mod.Admin)
        .filter(
            and_(
                mod.Admin.id == id,
                mod.Admin.is_active == True
            )
        )
        .first()
    )
    return result
# ------------------------------------------------------------------------------


async def read_region_admin(header_param: Request, region: str, db: Session):
    user = await super_admin.check_super_admin_token(header_param=header_param, db=db)
    if not user:
        return -1

    result = (
        db.query(
            mod.Admin
        ).filter(
            and_(
                mod.Admin.region == region,
                mod.Admin.is_active == True
            )

        )

        .order_by(desc(mod.Admin.id))
        .distinct()
        .all()
    )

    return result
# ----------------------------------------------------------------------


async def read_disactive_admin(header_param: Request, db: Session):
    user = await super_admin.check_super_admin_token(header_param=header_param, db=db)
    if not user:
        return -1
    result = (
        db.query(
            mod.Admin
        ).filter(mod.Admin.is_active == False)
        .order_by(desc(mod.Admin.id))
        .distinct()
        .all()
    )
    return result
# update admin


async def update_admin(id, req: mod.AdminBase, header_param: Request, db: Session):
    user = await super_admin.check_super_admin_token(header_param=header_param, db=db)
    if not user:
        return -1
    user_exist = (
        db.query(mod.Admin).filter(
            and_(mod.Admin.username == req.username)).first()
    )

    if user_exist and user_exist.id != id:
        return -2
    req_json = jsonable_encoder(req)
    new_update = (
        db.query(mod.Admin)
        .filter(mod.Admin.id == id)
        .update(req_json, synchronize_session=False)
    )
    db.commit()
    if new_update:
        return True
    else:
        return None
# --------------------------------------------------------------------------


async def check_admin_token(header_param: Request, db: Session):
    token = await check_token(header_param=header_param)
    if not token:
        return None
    payload = await decode_token(token=token)
    if not payload:
        return None
    username: str = payload.get("username")
    password: str = payload.get("password")
    result = await read_admin_by_username_password(
        username=username, password=password, db=db
    )
    print(username)
    if result:
        return result
    else:
        return None

#---------------------------------------------------------------------------
async def disactive_admines(id, req: disavtive.Disactive_teacher, header_param: Request, db: Session):
    user = await super_admin.check_super_admin_token(header_param=header_param, db=db)
    if not user:
        return -1
    user_exist = (
        db.query(mod.Admin).filter(and_(mod.Admin.id == id)).first()
    )

    if not user_exist:
        return -2
    req_json = jsonable_encoder(req)
    new_update = (
        db.query(mod.Admin)
        .filter(mod.Admin.id == id)
        .update(req_json, synchronize_session=False)
    )
    db.commit()
    if new_update:
        return True
    else:
        return None
