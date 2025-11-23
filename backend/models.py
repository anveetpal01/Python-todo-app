# here we define relationship between User and Task

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True) # email should be unique
    hashed_password = Column(String) # hashed password

    #relationship: One use can contain many tasks
    tasks = relationship("Task", back_populates="owner")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    is_completed = Column(Boolean, default=False)

    # foreign key: ye batata hai ki task kis user ka hai
    owner_id = Column(Integer, ForeignKey("users.id"))

    # relationship: ye task wapas User se juda hua hai
    owner = relationship("User", back_populates="tasks")