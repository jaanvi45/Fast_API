from pydantic import BaseModel
from typing import List, Optional
from datetime import timedelta

class Blog(BaseModel):
    title: str
    body: str
    
    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True

    
class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []
    class Config:
        orm_mode = True
  
class showBlog(BaseModel):
    title: str
    body: str  
    creator: ShowUser
    class Config:
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None