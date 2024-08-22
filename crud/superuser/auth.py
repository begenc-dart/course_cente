import models.superuser as mod
from sqlalchemy.orm import Session
from fastapi import Request
from sqlalchemy import and_
from tokens.token import check_token, create_access_token, decode_token
# create superadmin
async def create_superadmin_crud(req: mod.SuperAdminBase, db: Session):
    new_delete = (
        db.query(mod.Super_Admin)
        .filter(and_(mod.Super_Admin.username == req.username))
    ).first()
    
    if new_delete:
        return False
    
    new_dict = {"username": req.username, "password": req.password}
    access_token = await create_access_token(data=new_dict)
    new_add = mod.Super_Admin(
        username=req.username,
        password=req.password,
        token=access_token,
        is_active=True,
        is_superadmin=True,
    )
    
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    else:
        return None
#------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------
async def super_admin_login(req: mod.LoginSchema, db: Session):
    result = await read_super_admin_by_username_password(req.username, req.password, db)
    if result:
        return result
    else:
        return None
#------------------------------------------------------------------------------------
# read admin by username and password
async def read_super_admin_by_username_password(username: str, password: str, db: Session):
    result = (
        db.query(
            mod.Super_Admin
        )
        .filter(
            and_(
                mod.Super_Admin.username == username,
                mod.Super_Admin.password == password,
                mod.Super_Admin.is_deleted == False,
                mod.Super_Admin.is_active == True,
                mod.Super_Admin.is_superadmin== True
            )
        )
        .first()
    )
   
    if result:
        return result
    else:
        return None
#--------------------------------------------------------------------------
async def check_super_admin_token(header_param: Request, db: Session):
    token = await check_token(header_param=header_param)
    if not token:
        return None
    payload = await decode_token(token=token)
    if not payload:
        return None
    username: str = payload.get("username")
    password: str = payload.get("password")
    result = await read_super_admin_by_username_password(
        username=username, password=password, db=db
    )
    if result and result.is_superadmin:
        return True
    else:
        return None