from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String,Integer,Date
from enum import Enum

class TaskStatus(str,Enum):
    ToDo="todo"
    PENDING="Pending"
    INPROGRESS="Inprogress"
    DONE="Done"
    CANCELLED="Cancelled"

Base=declarative_base()
class Create_Task(Base):
    __tablename__="TASKS"
    id=Column(Integer,primary_key=True)
    title=Column(String)
    description=Column(String)
    created_date=Column(Date)
    due_date=Column(Date)
    status=TaskStatus