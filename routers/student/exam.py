from fastapi import APIRouter,Depends,HTTPException,status,Request,File, UploadFile
from sqlalchemy.orm import Session
import models.teacher.schemas as mod 
import models.superuser.schemas as login 
from db.connection import get_db
import crud.student as auth
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from typing import List

exam = APIRouter(tags=['exam'])
@exam.post("/api/add_exam", dependencies=[Depends(HTTPBearer())])
async def create_exam(header_param: Request,req: mod.Exam_Base,db: Session = Depends(get_db),):
    result = await auth.create_exam(header_param=header_param,req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
#--------------------------------------------------------------------------------------
@exam.get('/api/get_all_exam/{course_id}', dependencies=[Depends(HTTPBearer())])
async def get_exam(course_id:int,header_param: Request,db: Session = Depends(get_db)):
    result = await auth.read_exam(header_param=header_param, db=db,course_id=course_id)
    result = jsonable_encoder(result)
    print(result)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    elif result==-2:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="You dont have exam")
    elif result == None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Doesn't have exam this id")
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#--------------------------------------------------------------------------------------
@exam.get('/api/get_exam_by_id/{exam_id}', dependencies=[Depends(HTTPBearer())])
async def get_exam(exam_id:int,header_param: Request,db: Session = Depends(get_db)):
    result = await auth.read_exam_by_id(header_param=header_param, db=db,exam_id=exam_id)
    result = jsonable_encoder(result)
    print(result)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    elif result==-2:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="You dont have exam")
    elif result == None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Doesn't have exam this id")
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#----------------------------------------------------------------------------------
#update exam
@exam.put('/api/update_exam/{id}', dependencies=[Depends(HTTPBearer())])
async def update_exam(id: int, header_param: Request, req: mod.Exam_update_Base, db: Session = Depends(get_db)):
    result = await auth.update_exam(id=id, header_param=header_param, req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result:
        result = {'msg': 'Обновлено!'}
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)

#------------------------------------------------------------------------------
#delete exam
@exam.delete('/api/delete_exam/{id}', dependencies=[Depends(HTTPBearer())])
async def delete_homework( header_param: Request,id: int,db: Session = Depends(get_db)):
    result = await auth.delete_exam(id=id, header_param=header_param, db=db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
#------------------------------------------------------------------------------
#add quiz
@exam.post("/api/add_quiz", dependencies=[Depends(HTTPBearer())])
async def create_exam(header_param: Request,req: mod.Quiz_Base,db: Session = Depends(get_db),):
    result = await auth.create_quiz(header_param=header_param,req=req, db=db)
    result=await auth.update_point(exam_id=req.exam_id,db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result ==-2:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="this id doesnot have exam")
    elif result:
        return JSONResponse(content={"status":"done"}, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
#--------------------------------------------------------------------------------------
@exam.get('/api/get_all_quiz/{exam_id}', dependencies=[Depends(HTTPBearer())])
async def get_quiz(exam_id:int, header_param: Request,db: Session = Depends(get_db)):
    result = await auth.read_quiz(header_param=header_param, db=db,exam_id=exam_id)
    result = jsonable_encoder(result)
    print(result)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    elif result==-2:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="You dont have exam")
    elif result == None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Doesn't have exam this id")
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#----------------------------------------------------------------------------------
#update quiz
@exam.put('/api/update_quiz/{quiz_id}', dependencies=[Depends(HTTPBearer())])
async def update_quiz(quiz_id: int, header_param: Request, req: mod.Quiz_Base, db: Session = Depends(get_db)):
    result = await auth.update_quiz(id=quiz_id, header_param=header_param, req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result:
        result = {'msg': 'Обновлено!'}
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)

#------------------------------------------------------------------------------
#delete exam
@exam.delete('/api/delete_quiz/{quiz_id}', dependencies=[Depends(HTTPBearer())])
async def delete_homework( header_param: Request,quiz_id: int,db: Session = Depends(get_db)):
    result = await auth.delete_quiz(id=quiz_id, header_param=header_param, db=db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
#------------------------------------------------------------------------------
#add quiz answer
@exam.post("/api/add_answers", dependencies=[Depends(HTTPBearer())])
async def create_quiz_answer(header_param: Request,req: mod.Quiz_answer_Base,db: Session = Depends(get_db),):
    result = await auth.create_quiz_answer(header_param=header_param,req=req, db=db)
    
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result ==-2:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="this id doesnot have exam")
    elif result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
#--------------------------------------------------------------------------------------
@exam.get('/api/get_quiz/{quiz_id}', dependencies=[Depends(HTTPBearer())])
async def get_quiz(quiz_id:int, header_param: Request,db: Session = Depends(get_db)):
    result = await auth.read_quiz_answer(header_param=header_param, db=db,quiz_id=quiz_id)
    result = jsonable_encoder(result)
    print(result)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    elif result==-2:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="You dont have exam")
    elif result == None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Doesn't have exam this id")
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#----------------------------------------------------------------------------------
#update quiz
@exam.put('/api/update_quiz_answer/{quiz_id}', dependencies=[Depends(HTTPBearer())])
async def update_quiz(quiz_id: int, header_param: Request, req: mod.Update_Quiz_answer_Base, db: Session = Depends(get_db)):
    result = await auth.update_quiz_answer(id=quiz_id, header_param=header_param, req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result:
        result = {'msg': 'Обновлено!'}
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)

#------------------------------------------------------------------------------
#delete exam
@exam.delete('/api/delete_quiz/{quiz_answer_id}', dependencies=[Depends(HTTPBearer())])
async def delete_homework( header_param: Request,quiz_answer_id: int,db: Session = Depends(get_db)):
    result = await auth.delete_quiz_answer(id=quiz_answer_id, header_param=header_param, db=db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
#------------------------------------------------------------------------------
#add quiz answer
@exam.post("/api/add_student_answers", dependencies=[Depends(HTTPBearer())])
async def create_quiz_answer(header_param: Request,req: mod.Quiz_student_answer_Base,db: Session = Depends(get_db),):
    result = await auth.create_quiz_student_answer(header_param=header_param,req=req, db=db)
    
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result ==-2:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="you alright done exam")
    elif result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
#--------------------------------------------------------------------------------------
@exam.get('/api/get_all_result/{quiz_id}', dependencies=[Depends(HTTPBearer())])
async def get_quiz(quiz_id:int, header_param: Request,db: Session = Depends(get_db)):
    result = await auth.read_all_result(header_param=header_param, db=db,exam_id=quiz_id)
    result = jsonable_encoder(result)
    print(result)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    elif result==-2:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="You dont have exam")
    elif result == None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Doesn't have exam this id")
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#---------------------------------------------------------------------------------------
@exam.post("/api/add_question", dependencies=[Depends(HTTPBearer())])
async def create_question(header_param: Request,req: mod.Question_Base,db: Session = Depends(get_db),):
    result = await auth.create_question(header_param=header_param,req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
#--------------------------------------------------------------------------------------
@exam.get('/api/get_all_question/{exam_id}', dependencies=[Depends(HTTPBearer())])
async def get_exam(exam_id:int,header_param: Request,db: Session = Depends(get_db)):
    result = await auth.read_question(header_param=header_param, db=db,exam_id=exam_id)
    result = jsonable_encoder(result)
    print(result)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    elif result==-2:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="You dont have exam")
    elif result == None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Doesn't have exam this id")
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#----------------------------------------------------------------------------------
#update quiz
@exam.put('/api/update_question/{question_id}', dependencies=[Depends(HTTPBearer())])
async def update_question(question_id: int, header_param: Request, req: mod.Question_update_Base, db: Session = Depends(get_db)):
    result = await auth.update_question(id=question_id, header_param=header_param, req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result:
        result = {'msg': 'Обновлено!'}
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)

#------------------------------------------------------------------------------
#delete exam
@exam.delete('/api/delete_question/{question_id}', dependencies=[Depends(HTTPBearer())])
async def delete_question( header_param: Request,question_id: int,db: Session = Depends(get_db)):
    result = await auth.delete_question(id=question_id, header_param=header_param, db=db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
#---------------------------------------------------------------------------------------
@exam.post("/api/add_question_answer_student", dependencies=[Depends(HTTPBearer())])
async def create_question(header_param: Request,req: mod.Question_answer_student_Base,db: Session = Depends(get_db),):
    result = await auth.create_question_answer_student(header_param=header_param,req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
#--------------------------------------------------------------------------------------
@exam.get('/api/get_qestion_result/{exam_id}', dependencies=[Depends(HTTPBearer())])
async def get_quiz(exam_id:int, header_param: Request,db: Session = Depends(get_db)):
    result = await auth.read_question_by_id(header_param=header_param, db=db,exam_id=exam_id)
    result = jsonable_encoder(result)
    print(result)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    elif result==-2:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="You dont have exam")
    elif result == None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Doesn't have exam this id")
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#-----------------------------------------------------------------------------------

@exam.put('/api/visible_exam_result/{visible}', dependencies=[Depends(HTTPBearer())])
async def update_exam(visible: bool, header_param: Request,  db: Session = Depends(get_db)):
    result = await auth.update_visible_exam(visible=visible, header_param=header_param, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result:
        result = {'msg': 'Обновлено!'}
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
#---------------------------------------------------------------------------------------
@exam.post("/api/question_result", dependencies=[Depends(HTTPBearer())])
async def create_question(header_param: Request,req: mod.Question_result_Base,db: Session = Depends(get_db),):
    result = await auth.create_question_result(header_param=header_param,req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
#---------------------------------------------------------------------------------------
@exam.post("/api/add_project_exam", dependencies=[Depends(HTTPBearer())])
async def create_project_exam(header_param: Request,req: mod.Project_exam_Base,db: Session = Depends(get_db)):
    result = await auth.create_project_exam(header_param=header_param,req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
# ---------------------------------------------------------------------------------------
@exam.post('/api/create-project_exam_img/{project_id}', dependencies=[Depends(HTTPBearer())])
async def create_video(project_id: int, header_param: Request, db: Session = Depends(get_db), file: UploadFile = File(...)):
    result = await auth.post_project_exam(project_id, header_param, db, file)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
#--------------------------------------------------------------------------------------
@exam.get('/api/get_all_project/{exam_id}', dependencies=[Depends(HTTPBearer())])
async def get_exam(exam_id:int,header_param: Request,db: Session = Depends(get_db)):
    result = await auth.read_project(header_param=header_param, db=db,exam_id=exam_id)
    result = jsonable_encoder(result)
    print(result)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    elif result==-2:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="You dont have exam")
    elif result == None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Doesn't have exam this id")
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#----------------------------------------------------------------------------------
#update quiz
@exam.put('/api/update_project_exam/{question_id}', dependencies=[Depends(HTTPBearer())])
async def update_question(question_id: int, header_param: Request, req: mod.Project_exam_Base, db: Session = Depends(get_db)):
    result = await auth.update_project_exam(id=question_id, header_param=header_param, req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result:
        result = {'msg': 'Обновлено!'}
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)

#------------------------------------------------------------------------------
#delete exam
@exam.delete('/api/delete_project_exam/{question_id}', dependencies=[Depends(HTTPBearer())])
async def delete_question( header_param: Request,question_id: int,db: Session = Depends(get_db)):
    result = await auth.delete_project_exam(id=question_id, header_param=header_param, db=db)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
#---------------------------------------------------------------------------------------
@exam.post("/api/add_project_exam_result_student", dependencies=[Depends(HTTPBearer())])
async def create_question(header_param: Request,req: mod.Project_result_add,db: Session = Depends(get_db),):
    result = await auth.create_project_answer_student(header_param=header_param,req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
# ---------------------------------------------------------------------------------------
@exam.post('/api/add_project_exam_result_student_img/{answer_id}', dependencies=[Depends(HTTPBearer())])
async def create_video(answer_id: int, header_param: Request, db: Session = Depends(get_db), file: UploadFile = File(...)):
    result = await auth.create_project_answer_student_img(answer_id, header_param, db, file)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
#--------------------------------------------------------------------------------------
@exam.get('/api/get_project_result/{exam_id}', dependencies=[Depends(HTTPBearer())])
async def get_quiz(exam_id:int, header_param: Request,db: Session = Depends(get_db)):
    result = await auth.read_project_by_id(header_param=header_param, db=db,exam_id=exam_id)
    result = jsonable_encoder(result)
    print(result)
    if result == -1:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    elif result==-2:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="You dont have exam")
    elif result == None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Doesn't have exam this id")
    if result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#---------------------------------------------------------------------------------------
@exam.post("/api/project_result", dependencies=[Depends(HTTPBearer())])
async def create_question(header_param: Request,req: mod.Question_result_Base,db: Session = Depends(get_db),):
    result = await auth.create_project_results(header_param=header_param,req=req, db=db)
    result = jsonable_encoder(result)
    if result == -1:
        return HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    elif result:
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)