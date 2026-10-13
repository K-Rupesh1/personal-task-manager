from datetime import date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String,Integer,Date, func
from enum import Enum

from app.schema import TaskStatus

Base=declarative_base()
class Create_Task(Base):
    __tablename__="tasks"
    id=Column(Integer,primary_key=True)
    title=Column(String)
    description=Column(String)
    created_date=Column(Date, default=date.today)
    due_date=Column(Date)
    status=Column(String)
    update_date=Column(Date,onupdate=func.now())
    

    
