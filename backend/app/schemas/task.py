from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

TaskStatus = Literal["Todo", "In Progress", "Done"]

def _normalize_title(value: object) -> object:
    if isinstance(value, str):
        value = value.strip()
        
        if not value:
            raise ValueError("Title tidak boleh kosong atau hanya berisi whitespace.")
        
    return value

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str
    status: TaskStatus

    @field_validator("title", mode="before")
    @classmethod
    def normalize_title(cls, value: object) -> object:
        return _normalize_title(value)

class TaskUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str
    status: TaskStatus
    
    @field_validator("title", mode="before")
    @classmethod
    def normalize_title(cls, value: object) -> object:
        return _normalize_title(value)

class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    description: str
    status: TaskStatus