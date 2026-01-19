from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = "userdb"

    id = Column(Integer, primary_key=True)
    username = Column(String, index=True)
    password = Column(String, index=True)
    age = Column(Integer, index=True)
    email = Column(String, index=True)
    adderss = Column(String, index=True)
    bio = Column(String, index=True)
    picture = Column(String, index=True)
    
    info = relationship("memoTable", back_populates="user")

class memoTable(Base):
    __tablename__ = "memos"

    id = Column(Integer, primary_key=True)
    username = Column(String, ForeignKey("userdb.id"), index=True) 
    title = Column(String, index=True)
    memo = Column(String, index=True)
    memoTime = Column(String, index=True)

    user = relationship("Users", back_populates="info")


class UserInput(Base):
    __tablename__ = "usersInput"

    id = Column(String, primary_key=True)
    memory = Column(String, index=True)
    picture = Column(String, index=True)