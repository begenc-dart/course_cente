from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class Tutorial_Base(BaseModel):
    name: str
    description: str


class Folder_Base(BaseModel):
    folder_name: str
    tutorial_id: int


class Video_Base(BaseModel):
    folder_id: int
class News_Base(BaseModel):
    title:str
    subtitle:str
    
