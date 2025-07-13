from pydantic import BaseModel, Field
from typing import Optional

class TaskCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str = Field(min_length=5, max_length=500)
    priority: int = Field(ge=1, le=25)
    class Config:
        from_attributes = True

class Tasks(BaseModel):
    id: int
    name: str
    description: str
    priority: int

    class Config:
        from_attributes = True

class TaskUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, min_length=5, max_length=500)
    priority: Optional[int] = Field(None, ge=1, le=25)

class UserCreate(BaseModel):
    name:str = Field(min_length=1,max_length=100)
    grade:str = Field(min_length=3,max_length=150)
    password:str = Field(min_length=3,max_length=100)

class UserUpdate(BaseModel):
    name:Optional[str] = Field(min_length=1,max_length=100)
    grade:Optional[str] = Field(min_length=3,max_length=150),
    password:Optional[str] = Field(min_length=3,max_length=100)