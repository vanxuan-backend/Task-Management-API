from pydantic import BaseModel, EmailStr, Field
from typing import List
from datetime import datetime
from app.schemas.task import TaskResponse

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    tasks: List[TaskResponse] = Field(default_factory=list)

    model_config = {"from_attributes": True}