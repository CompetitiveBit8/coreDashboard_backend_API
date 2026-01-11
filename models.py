from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = "userdb"

    id = Column(Integer, primary_key=True)
    username = Column(String, primary_key=True, index=True)
    password = Column(String, nullable=False, index=True)
    age = Column(Integer, index=True)
    email = Column(String, index=True)
    adderss = Column(String, index=True)
    username = Column(String, ForeignKey("userdb.username"), nullable=False)
    bio = Column(String, index=True)
    memory = Column(String, index=True)
    picture = Column(String, index=True)

# class infoTable(Base):
#     __tablename__ = "info"

#     id = Column(Integer, primary_key=True)
#     age = Column(Integer, index=True)
#     email = Column(String, index=True)
#     adderss = Column(String, index=True)
#     username = Column(String, ForeignKey("userdb.username"), nullable=False)

#     users = relationship("Users", back_populates="username")


class UserInput(Base):
    __tablename__ = "usersInput"

    id = Column(String, primary_key=True)
    memory = Column(String, index=True)
    picture = Column(String, index=True)