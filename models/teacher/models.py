from sqlalchemy import Column, Integer, String, Boolean, DateTime,Time, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db import Base

class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)  # Consider hashing passwords
    phone_number = Column(String)
    name = Column(String)
    surname = Column(String)
    token = Column(String)  # Ensure tokens are managed securely
    region = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Define the relationships
    groups = relationship('Group', back_populates='teacher')
    courses = relationship('Course', back_populates='teacher')

class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String)
    child_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    is_active = Column(Boolean, default=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete='CASCADE'))

    # Define the relationships
    students = relationship('Student', back_populates='group')
    group_times = relationship('GroupTime', back_populates='group')
    course_to_groups = relationship('CourseToGroup', back_populates='group')
    teacher = relationship('Teacher', back_populates='groups')

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    name = Column(String)
    surname = Column(String)
    password = Column(String)  # Consider hashing passwords
    parent_name = Column(String)
    phone_number = Column(String)
    token = Column(String)  # Ensure tokens are managed securely
    parent_number = Column(String)
    is_active = Column(Boolean, default=True)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE'))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Define the relationships
    group = relationship('Group', back_populates='students')
    quiz_student_answers = relationship('Quiz_Student_answers', back_populates='student')
    homework_answers = relationship('HomeworkAnswer', back_populates='student')
    exams = relationship('Exam_result', back_populates='student')
    question_answer = relationship('Question_answer_Student', back_populates='student')

class GroupTime(Base):
    __tablename__ = 'group_times'

    id = Column(Integer, primary_key=True, index=True)
    week_number = Column(String)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE'))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Define the relationship to Group
    group = relationship('Group', back_populates='group_times')

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete='CASCADE'))

    # Define the relationships
    course_to_groups = relationship('CourseToGroup', back_populates='course')
    homeworks = relationship('Homework', back_populates='course')
    teacher = relationship('Teacher', back_populates='courses')
    exam = relationship('Exam', back_populates='course')

class CourseToGroup(Base):
    __tablename__ = 'course_group'

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE'))
    course_id = Column(Integer, ForeignKey('courses.id', ondelete='CASCADE'))

    # Define the relationships
    group = relationship('Group', back_populates='course_to_groups')
    course = relationship('Course', back_populates='course_to_groups')

class Homework(Base):
    __tablename__ = 'homeworks'

    id = Column(Integer, primary_key=True, index=True)
    lesson_time = Column(DateTime)
    title = Column(String)
    subtitle = Column(String)
    img = Column(String, default="")
    course_id = Column(Integer, ForeignKey('courses.id', ondelete='CASCADE'))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Define the relationships
    course = relationship('Course', back_populates='homeworks')
    answers = relationship('HomeworkAnswer', back_populates='homework')

class HomeworkAnswer(Base):
    __tablename__ = 'homework_answer'

    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String)
    homework_id = Column(Integer, ForeignKey('homeworks.id', ondelete='CASCADE'))
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'))
    img = Column(String,)
    is_img=Column(Boolean,default=False)
    is_student = Column(Boolean, default=False)
    is_true = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Define the relationships
    homework = relationship('Homework', back_populates='answers')
    student = relationship('Student', back_populates='homework_answers')
class Exam(Base):
    __tablename__ = 'exam'

    id = Column(Integer, primary_key=True, index=True)
    name=Column(String)
    exam_duration=Column(Time)
    is_active=Column(Boolean,default=False)
    see_result=Column(Boolean,default=False)
    quiz_point=Column(Integer,default=0)
    quiz_len=Column(Integer,default=0)
    course_id = Column(Integer, ForeignKey('courses.id', ondelete='CASCADE'))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    course = relationship('Course', back_populates='exam')
    quiz = relationship('Quiz', back_populates='exams')
    exam_result = relationship('Exam_result', back_populates='exams')
    question = relationship('Question', back_populates='exams')
class Quiz(Base):
    __tablename__="quiz"
    id = Column(Integer, primary_key=True, index=True)
    quiz=Column(String)
    exam_id = Column(Integer, ForeignKey('exam.id', ondelete='CASCADE'))
    point=Column(Integer,default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    exams = relationship('Exam', back_populates='quiz')
    quiz_answer = relationship('Quiz_answers', back_populates='quiz')
    quiz_student_answer = relationship('Quiz_Student_answers', back_populates='quiz')
class Quiz_answers(Base):
    __tablename__="quiz_answer"
    id = Column(Integer, primary_key=True, index=True)
    answer=Column(String)
    is_true=Column(Boolean)
    quiz_id = Column(Integer, ForeignKey('quiz.id', ondelete='CASCADE'))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    quiz = relationship('Quiz', back_populates='quiz_answer')
    quiz_student_answer = relationship('Quiz_Student_answers', back_populates='quiz_answer')
class Quiz_Student_answers(Base):
    __tablename__="quiz_student_answer"
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey('quiz.id', ondelete='CASCADE'))
    quiz_answer_id = Column(Integer, ForeignKey('quiz_answer.id', ondelete='CASCADE'))
    student_id=Column(Integer, ForeignKey('students.id', ondelete='CASCADE'))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    quiz = relationship('Quiz', back_populates='quiz_student_answer')
    quiz_answer = relationship('Quiz_answers', back_populates='quiz_student_answer')
    student = relationship('Student', back_populates='quiz_student_answers')
class Exam_result(Base):
    __tablename__="exam_result"
    id = Column(Integer, primary_key=True, index=True)
    point=Column(Integer,default=0)
    created_at = Column(DateTime, default=func.now())
    
    student_id=Column(Integer, ForeignKey('students.id', ondelete='CASCADE'))
    exam_id = Column(Integer, ForeignKey('exam.id', ondelete='CASCADE'))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    student = relationship('Student', back_populates='exams')
    exams = relationship('Exam', back_populates='exam_result')
class Question(Base):
    __tablename__="question"
    id = Column(Integer, primary_key=True, index=True)
    question=Column(String)
    point=Column(Integer,default=0)
    exam_id = Column(Integer, ForeignKey('exam.id', ondelete='CASCADE'))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    exams = relationship('Exam', back_populates='question')
    question_answer = relationship('Question_answer_Student', back_populates='question')
class Question_answer_Student(Base):
    __tablename__="question_answer"
    id = Column(Integer, primary_key=True, index=True)
    answer=Column(String)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'))
    question_id = Column(Integer, ForeignKey('question.id', ondelete='CASCADE'))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    question = relationship('Question', back_populates='question_answer')
    student = relationship('Student', back_populates='question_answer')