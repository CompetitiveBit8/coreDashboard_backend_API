from pydantic import BaseModel
from typing import Optional


class signupDetails(BaseModel):
    username: str
    password: str
    # age: Optional[int] = None
    # email: Optional[str] = None
    # adderss: Optional[str] = None

class UserDetails(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None
    adderss: Optional[str] = None
    memories: Optional[str] = None
    images: Optional[str] = None
    bio: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    
class userEdit(BaseModel):
    email: str
    password: str
    email: str

class userInputs(BaseModel):
    bio: Optional[str] = None