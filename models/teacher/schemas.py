from datetime import date
from pydantic import BaseModel
from typing import List
from datetime import time
class CreateTeacherBase(BaseModel):
    username: str
    password: str
    name: str
    surname: str
    phone_number: str
    region: str

    class Config:
        orm_mode = True
class Disactive_teacher(BaseModel):
    is_active: bool
class Group_Base(BaseModel):
    group_name: str
    teacher_id:int
    start_time: date
    end_time: date


class GroupTime_Base(BaseModel):
    week_number: str
    group_id:int

class Student_Base(BaseModel):
    group_id:int
    name:str
    surname:str
    username:str
    password:str
    parent_name:str
    phone_number:str
    parent_number:str
class Course_Base(BaseModel):
    name:str
class Course_Group(BaseModel):
    group_id:int
    course_id:int
class Homework_Base(BaseModel):
    lesson_time:date
    title:str
    subtitle:str
    course_id:int
class Homework_teacher_answer_Base(BaseModel):
    comment:str
    homework_id:int
    student_id:int
    is_true:bool
class Homework_update_Base(BaseModel):
    title:str
    subtitle:str
class Homework_answer_Base(BaseModel):
    comment:str
    homework_id:int
class Exam_Base(BaseModel):
    name:str
    exam_duration:time
    is_active:bool
    quiz_point:int
    course_id:int
class Exam_update_Base(BaseModel):
    name:str
    is_active:bool
    quiz_point:int
    course_id:int    
class Quiz_Base(BaseModel):
    quiz:str
    exam_id:int
class Quiz_answer_Base(BaseModel):
    answer:str
    is_true:bool
    quiz_id:int
class Update_Quiz_answer_Base(BaseModel):
    answer:str
    is_true:bool
class Quiz_student_answer_Base(BaseModel):
    quiz_id:int
    quiz_answer_id:int
    
    