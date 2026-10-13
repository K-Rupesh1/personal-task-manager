from datetime import date
from enum import Enum

from pydantic import BaseModel,Field

class TaskStatus(str,Enum):
    ToDo="todo"
    PENDING="Pending"
    INPROGRESS="Inprogress"
    DONE="Done"
    CANCELLED="Cancelled"  

class CreateTaskRequest(BaseModel):
    title:str=Field(min_length=3)
    description:str=Field(...,min_length=7,description="Description must have morethan 6 characters")
    due_date:date 
    status: TaskStatus = TaskStatus.DONE


class CreateTaskResponse(BaseModel):
    id:int
    title:str=Field(min_length=3)
    description:str=Field(...,min_length=7,description="Description must have morethan 6 characters")
    created_date:date 
    due_date:date 
    status: TaskStatus = TaskStatus.DONE

class UpdateTaskRequest(BaseModel):
    title:str=Field(min_length=3)
    description:str=Field(...,min_length=7,description="Description must have morethan 6 characters")
    due_date:date
    status:str
    
class UpdateTaskResponse(BaseModel):
    id:int
    title:str
    description:str
    created_date:date 
    due_date:date 
    update_date:date
    status: TaskStatus = TaskStatus.DONE
