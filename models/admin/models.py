from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from db import Base
from sqlalchemy.orm import relationship


class Tutorial(Base):
    __tablename__ = 'tutorial'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    img = Column(String, default="")
    folders = relationship('Folder', back_populates='tutorial')


class Folder(Base):
    __tablename__ = 'folder'

    id = Column(Integer, primary_key=True, index=True)
    folder_name = Column(String)
    tutorial_id = Column(Integer, ForeignKey(
        'tutorial.id', ondelete='CASCADE'))

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    videos = relationship('Video', back_populates='folder')
    tutorial = relationship('Tutorial', back_populates='folders')


class Video(Base):
    __tablename__ = 'video'

    id = Column(Integer, primary_key=True, index=True)
    video_name = Column(String)
    folder_id = Column(Integer, ForeignKey('folder.id', ondelete='CASCADE'))
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    folder = relationship('Folder', back_populates='videos')
class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True, index=True)
    url_project=Column(String)
    name=Column(String)
    description=Column(String)
    img_url=Column(String)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

