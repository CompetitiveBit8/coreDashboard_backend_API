from pydantic import BaseModel
from typing import Optional


class signupDetails(BaseModel):
    username: str
    password: str

class UserDetails(BaseModel):
    age: Optional[int] = None
    email: Optional[str] = None
    adderss: Optional[str] = None
    bio: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    username: str
    password: str
    age: int
    email: str
    adderss: str
    bio: str
    images: str

    
class userInfo(BaseModel):
    email: str
    password: str
    email: str
    bio: Optional[str] = None


class userInputs(BaseModel):
    memoTitle: Optional[str] = None
    memo: str