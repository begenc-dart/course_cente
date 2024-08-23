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

# exam add


async def create_exam(header_param: Request, req: mod.Exam_Base, db: Session,):
    user = await super_admin.check_teacher_token(header_param=header_param, db=db)
    if not user:
        return -1
    new_add = mod.Exam(
        name=req.name,
        exam_duration=req.exam_duration,
        quiz_point=req.quiz_point,
        course_id=req.course_id,
        is_active=req.is_active

    )
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    else:
        return None
# -----------------------------------------------------------------------------------------

# exam get


async def read_exam(course_id:int,header_param: Request,  db: Session):
    user = await student.check_student_token(header_param=header_param, db=db)
    teacher = await super_admin.check_teacher_token(header_param=header_param, db=db)
    if not user and not teacher:
        return -1
    result = (
        db.query(mod.Exam)
        .filter(
            and_(
                mod.Exam.course_id == course_id,

            )
        ).options(joinedload(mod.Exam.exam_result))
        .all()
    )
    return result
# -----------------------------------------------------------------------------------------

# exam get


async def read_exam_by_id(exam_id:int,header_param: Request,  db: Session):
    user = await student.check_student_token(header_param=header_param, db=db)
    teacher = await super_admin.check_teacher_token(header_param=header_param, db=db)
    if not user and not teacher:
        return -1
    result = (
        db.query(mod.Exam)
        .filter(
            and_(
                mod.Exam.id==exam_id

            )
        ).options(joinedload(mod.Exam.question)).options(joinedload(mod.Exam.quiz).options(joinedload(mod.Quiz.quiz_answer)))
        .all()
    )
    return result
# --------------------------------------------------------------------------------------


async def delete_exam(id, header_param: Request, db: Session):
    user = await super_admin.check_teacher_token(header_param, db)
    if not user:
        return -1

    new_delete = (
        db.query(mod.Exam).filter(mod.Exam.id == id).delete(
            synchronize_session=False)
    )
    db.commit()
    if new_delete:
        result = {"msg": "Удалено!"}
        return result

# --------------------------------------------------------------------------------


async def update_exam(id, req: mod.Exam_update_Base, header_param: Request, db: Session):
    user = await super_admin.check_teacher_token(header_param=header_param, db=db)
    if not user:
        return -1
    req_json = jsonable_encoder(req)
    user_exist = (
        db.query(mod.Exam).filter(
            and_(mod.Exam.id == id)).update(req_json, synchronize_session=False)
    )
    db.commit()
    if user_exist:
        return True
    else:
        return None
# --------------------------------------------------------------------------------
# Quiz add


async def create_quiz(header_param: Request, req: mod.Quiz_Base, db: Session,):
    user = await super_admin.check_teacher_token(header_param=header_param, db=db)
    if not user:
        return -1
    new_add = mod.Quiz(
        quiz=req.quiz,
        exam_id=req.exam_id,
    )
    update = db.query(mod.Exam).filter(mod.Exam.id == req.exam_id).first()
    if update == None:
        return -2
    update = db.query(mod.Exam).filter(mod.Exam.id == req.exam_id).update(
        {"quiz_len": mod.Exam.quiz_len+1}, synchronize_session='evaluate')

    print(update)
    if new_add and update:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)

        return new_add
    else:
        return None
# --------------------------------------------------------------------
# exam get


async def read_quiz(exam_id: int, header_param: Request,  db: Session):
    user = await student.check_student_token(header_param=header_param, db=db)
    teacher = await super_admin.check_teacher_token(header_param=header_param, db=db)
    if not user and not teacher:
        return -1
    result = (
        db.query(mod.Quiz)
        .filter(
            and_(
                mod.Quiz.exam_id == exam_id,

            )
        ).options(joinedload(mod.Quiz.quiz_answer))
        .all()
    )
    if teacher:
        return result
    course = db.query(mod.CourseToGroup).filter(
        mod.CourseToGroup.group_id == user.group_id).first()
    if not course:
        return -2
    
    resultes = []
    for i in result:
        quiz_answer = db.query(mod.Quiz_Student_answers).filter(and_(
            mod.Quiz_Student_answers.quiz_id == i.id, mod.Quiz_Student_answers.student_id == user.id)).first()

        resultes.append({
            "quiz_answer_by_student": quiz_answer,
            "quiz": i
        })

    return resultes
# --------------------------------------------------------------------------------


async def update_point(exam_id, db: Session):
    exam_point = db.query(mod.Exam).filter(mod.Exam.id == exam_id).first()
    quiz_point = db.query(mod.Quiz).filter(mod.Quiz.exam_id == exam_id).all()

    if not exam_point:
        return -2
    quiz = exam_point.quiz_point/len(quiz_point)
    print(quiz_point)
    req_json = jsonable_encoder({
        "point": quiz
    })
    for i in quiz_point:
        user_exist = (
            db.query(mod.Quiz).filter(
                and_(mod.Quiz.exam_id == exam_id, i.id == mod.Quiz.id)).update(req_json, synchronize_session=False)

        )
    db.commit()

    if user_exist:
        return user_exist
    else:
        return None
# --------------------------------------------------------------------------------------


async def delete_quiz(id, header_param: Request, db: Session):
    user = await super_admin.check_teacher_token(header_param, db)
    if not user:
        return -1

    new_delete = (
        db.query(mod.Quiz).filter(mod.Quiz.id == id).delete(
            synchronize_session=False)
    )
    db.commit()
    if new_delete:
        result = {"msg": "Удалено!"}
        return result

# --------------------------------------------------------------------------------


async def update_quiz(id, req: mod.Quiz_Base, header_param: Request, db: Session):
    user = await super_admin.check_teacher_token(header_param=header_param, db=db)
    if not user:
        return -1
    req_json = jsonable_encoder(req)
    user_exist = (
        db.query(mod.Quiz).filter(
            and_(mod.Quiz.id == id)).update(req_json, synchronize_session=False)
    )
    db.commit()
    if user_exist:
        return True
    else:
        return None
# --------------------------------------------------------------------------------
# Quiz add


async def create_quiz_answer(header_param: Request, req: mod.Quiz_answer_Base, db: Session,):
    user = await super_admin.check_teacher_token(header_param=header_param, db=db)
    if not user:
        return -1
    new_add = mod.Quiz_answers(
        answer=req.answer,
        is_true=req.is_true,
        quiz_id=req.quiz_id
    )

    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)

        return new_add
    else:
        return None
# --------------------------------------------------------------------
# exam get


async def read_quiz_answer(quiz_id: int, header_param: Request,  db: Session):
    user = await student.check_student_token(header_param=header_param, db=db)
    teacher = await super_admin.check_teacher_token(header_param=header_param, db=db)
    if not user and not teacher:
        return -1

    result = (
        db.query(mod.Quiz)
        .filter(
            and_(
                mod.Quiz.id == quiz_id,

            )
        ).options(joinedload(mod.Quiz.quiz_answer))
        .first()
    )
    if teacher:
        return result
    if not result :
        return -2
    quiz_answer = db.query(mod.Quiz_Student_answers).filter(and_(
        mod.Quiz_Student_answers.quiz_id == result.id, mod.Quiz_Student_answers.student_id == user.id)).first()

    return {
        "quiz_answer_by_student": quiz_answer,
        "quiz": result
    }
# ---------------------------------------------------------------------------------------


async def delete_quiz_answer(id, header_param: Request, db: Session):
    user = await super_admin.check_teacher_token(header_param, db)
    if not user:
        return -1

    new_delete = (
        db.query(mod.Quiz_answers).filter(
            mod.Quiz_answers.id == id).delete(synchronize_session=False)
    )
    db.commit()
    if new_delete:
        result = {"msg": "Удалено!"}
        return result

# --------------------------------------------------------------------------------


async def update_quiz_answer(id, req: mod.Update_Quiz_answer_Base, header_param: Request, db: Session):
    user = await super_admin.check_teacher_token(header_param=header_param, db=db)
    if not user:
        return -1
    req_json = jsonable_encoder(req)
    user_exist = (
        db.query(mod.Quiz_answers).filter(
            and_(mod.Quiz_answers.id == id)).update(req_json, synchronize_session=False)
    )
    db.commit()
    if user_exist:
        return True
    else:
        return None
# --------------------------------------------------------------------------------
# Quiz add


async def create_quiz_student_answer(header_param: Request, req: mod.Quiz_student_answer_Base, db: Session,):
    user = await student.check_student_token(header_param=header_param, db=db)
    if not user:
        return -1
    check = db.query(mod.Quiz_Student_answers).filter(and_(
        mod.Quiz_Student_answers.student_id == user.id,
        mod.Quiz_Student_answers.quiz_id == req.quiz_id,
        mod.Quiz_Student_answers.quiz_answer_id == req.quiz_answer_id,
    )).first()
    if check:
        return -2
    new_add = mod.Quiz_Student_answers(
        quiz_id=req.quiz_id,
        quiz_answer_id=req.quiz_answer_id,
        student_id=user.id
    )
    quiz = db.query(mod.Quiz_answers).filter(and_(mod.Quiz_answers.id ==
                                                  req.quiz_answer_id, mod.Quiz_answers.quiz_id == req.quiz_id)).first()
    if quiz.is_true:
        result=db.query(mod.Exam_result).filter(and_(mod.Exam_result.student_id==user.id)).first()
        quiz=db.query(mod.Quiz).filter(and_(mod.Quiz.id==req.quiz_id)).first()
        if not result:
            
            exam_resu=mod.Exam_result(
                point=quiz.point,
                student_id=user.id,
                exam_id=quiz.exam_id
            )
            db.add(exam_resu)
            db.commit()
            db.refresh(exam_resu)
        else:
            req_json = jsonable_encoder({
                "point":result.point+quiz.point
            })
            user_exist = (
            db.query(mod.Exam_result).filter(
                and_(mod.Exam_result.student_id==user.id)).update(req_json, synchronize_session=False))
            db.commit()
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)

        return new_add
    else:
        return None

# ----------------------------------------------------------------------------------------
# exam get


async def read_all_result(exam_id: int, header_param: Request,  db: Session):
    user = await student.check_student_token(header_param=header_param, db=db)
    teacher = await super_admin.check_teacher_token(header_param=header_param, db=db)
    if not user and not teacher:
        return -1

    result = (
        db.query(mod.Exam)
        .filter(
            and_(
                mod.Exam.id == exam_id,

            )
        ).options(joinedload(mod.Exam.course)).options(joinedload(mod.Exam.exam_result).options(joinedload(mod.Exam_result.student)))
        .first()
    )
    return result
#-------------------------------------------------------------------------------------------

async def create_question(header_param: Request, req: mod.Question_Base, db: Session,):
    user = await super_admin.check_teacher_token(header_param=header_param, db=db)
    if not user:
        return -1
    new_add = mod.Question(
        question=req.question,
        point=req.point,
        exam_id=req.exam_id,
    )
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    else:
        return None

# -----------------------------------------------------------------------------------------

# question read


async def read_question(exam_id:int,header_param: Request,  db: Session):
    user = await student.check_student_token(header_param=header_param, db=db)
    teacher = await super_admin.check_teacher_token(header_param=header_param, db=db)
    if not user and not teacher:
        return -1
    result = (
        db.query(mod.Question)
        .filter(
            and_(
                mod.Question.exam_id == exam_id,

            )
        )
        .all()
    )
    return result
# ---------------------------------------------------------------------------------------


async def delete_question(id, header_param: Request, db: Session):
    user = await super_admin.check_teacher_token(header_param, db)
    if not user:
        return -1

    new_delete = (
        db.query(mod.Question).filter(
            mod.Question.id == id).delete(synchronize_session=False)
    )
    db.commit()
    if new_delete:
        result = {"msg": "Удалено!"}
        return result

# --------------------------------------------------------------------------------


async def update_question(id, req: mod.Question_update_Base, header_param: Request, db: Session):
    user = await super_admin.check_teacher_token(header_param=header_param, db=db)
    if not user:
        return -1
    req_json = jsonable_encoder(req)
    user_exist = (
        db.query(mod.Question).filter(
            and_(mod.Question.id == id)).update(req_json, synchronize_session=False)
    )
    db.commit()
    if user_exist:
        return True
    else:
        return None
#-------------------------------------------------------------------------------------------

async def create_question_answer_student(header_param: Request, req: mod.Question_answer_student_Base, db: Session,):
    user = await student.check_student_token(header_param=header_param, db=db)
    if not user:
        return -1
    new_add = mod.Question_answer_Student(
        answer=req.answer,
        question_id=req.question_id,
        student_id=user.id,
    )
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return new_add
    else:
        return None
# --------------------------------------------------------------------
# exam get


async def read_question_by_id(exam_id: int, header_param: Request,  db: Session):
    user = await student.check_student_token(header_param=header_param, db=db)
    teacher = await super_admin.check_teacher_token(header_param=header_param, db=db)
    if not user and not teacher:
        return -1
    result = (
        db.query(mod.Question)
        .filter(
            and_(
                mod.Question.exam_id == exam_id,

            )
        )
        .all()
    )
    if teacher:
        return result
    course = db.query(mod.CourseToGroup).filter(
        mod.CourseToGroup.group_id == user.group_id).first()
    if not course:
        return -2
    
    resultes = []
    for i in result:
        print(user.id)
        quiz_answer = db.query(mod.Question_answer_Student).filter(and_(
            mod.Question_answer_Student.question_id == i.id, mod.Question_answer_Student.student_id == user.id)).first()

        resultes.append({
            "question_answer_by_student": quiz_answer,
            "question": i
        })

    return resultes