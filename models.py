import datetime
import uuid

from typing import List
from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, Text


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    username: str | None = Field(default=None, max_length=255)
    
class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    username: str | None = Field(default=None, max_length=255)

class UserLogin(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    is_verified: bool = Field(default=False)
    verification_code: str | None = Field(default=None, index=True)
    code_expires_at: datetime.datetime | None = Field(default=None)
    api_key: str | None = Field(default=None)
    language: str | None = Field(default="English")
    essays: List["Essay"] = Relationship(back_populates="author")

class Essay(SQLModel, table=True):
    essay_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    author: "User" = Relationship(back_populates="essays")
    published_date: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

    Overall_score: float
    TR:float
    LR:float
    CC:float
    GRA:float
    reason:str = Field(sa_column=Column(Text)) # The default str limits is VARCHAR(255), must use TEXT
    improvement:str = Field(sa_column=Column(Text)) 
    content:str = Field(sa_column=Column(Text)) 
    
    topic_id: uuid.UUID = Field(foreign_key="topic.topic_id")   
    topic: "Topic" = Relationship(back_populates="essays")

class Topic(SQLModel, table=True):
    topic_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    topic: str
    essays: List["Essay"] = Relationship(back_populates="topic")




