from pydantic import BaseModel
class SuperAdminBase(BaseModel):
    username        : str
    password        : str

    class Config:
        orm_mode = True
class LoginSchema(BaseModel):
    username    : str 
    password    : str 
    class Config:
        orm_mode = True
class AdminBase(BaseModel):
    username : str
    password :str
    phone_number:str
    name:str
    surname:str
    region:str
    is_add_teacher: bool= False
    is_add_tutorial:bool= False
    is_add_calendar: bool= False
    is_add_news:bool= False
    is_add_project:bool= False
    is_add_student:bool= False
    is_add_chat:bool=False
class Admin_short(BaseModel):
    id : int
    username : str
    phone_number:str
    name:str
    surname:str
