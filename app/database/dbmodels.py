from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String,Integer,DateTime,func,Date,ForeignKey
from enum import Enum

from app.schema import TaskStatus

Base=declarative_base()

# Entity
class Task(Base):
    __tablename__="tasks"
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey("users.user_id"),nullable=False)
    title=Column(String)
    description=Column(String)
    created_date=Column(DateTime, default=datetime.now)
    due_date=Column(Date)
    status=Column(String)
    update_date=Column(Date,default=datetime.now,onupdate=datetime.now)
    
class User(Base):
    __tablename__="users"
    user_id=Column(Integer,primary_key=True)
    username=Column(String)
    email_id=Column(String,unique=True)
    password=Column(String)
    create_date=Column(DateTime,default=datetime.now)
    update_date=Column(DateTime,default=datetime.now,onupdate=datetime.now)
    

    
