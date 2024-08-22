from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from db import Base


class Super_Admin(Base):
    __tablename__ = 'super_admin'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    token = Column(String)
    is_superadmin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    phone_number = Column(String)
    name = Column(String)
    surname = Column(String)
    token = Column(String)
    region = Column(String)
    is_add_teacher = Column(Boolean, default=False)
    is_add_tutorial = Column(Boolean, default=False)
    is_add_calendar = Column(Boolean, default=False)
    is_add_news = Column(Boolean, default=False)
    is_add_project = Column(Boolean, default=False)
    is_add_student = Column(Boolean, default=False)
    is_add_chat = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
