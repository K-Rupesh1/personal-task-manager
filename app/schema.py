from datetime import datetime
from enum import Enum

from pydantic import BaseModel,Field

class TaskStatus(str,Enum):
    ToDo="todo"
    PENDING="pending"
    INPROGRESS="inprogress"
    DONE="done"
    CANCELLED="cancelled"  

class CreateTaskRequest(BaseModel):
    user_id:str
    title:str=Field(min_length=3)
    description:str=Field(...,min_length=7,description="Description must have morethan 6 characters")
    due_date:datetime 
    status: TaskStatus = TaskStatus.DONE


class CreateTaskResponse(BaseModel):
    id:int
    title:str=Field(min_length=3)
    description:str=Field(...,min_length=7,description="Description must have morethan 6 characters")
    created_date:datetime
    due_date:datetime
    status: TaskStatus = TaskStatus.DONE

class UpdateTaskRequest(BaseModel):
    title:str=Field(min_length=3)
    description:str=Field(...,min_length=7,description="Description must have morethan 6 characters")
    due_date:datetime
    status:str
    
class UpdateTaskResponse(BaseModel):
    id:int
    title:str
    description:str
    created_date:datetime 
    due_date:datetime 
    update_date:datetime
    status: TaskStatus = TaskStatus.DONE


class UserRequest(BaseModel):
    username:str
    email_id:str
    password:str
    
class UserResponse(BaseModel):
    user_id:int
    username:str
    email_id:str
    create_date:datetime
    update_date:datetime
    
class UpdateRequest(BaseModel):
    username:str
    email_id:str
    password:str
    
class UpdateResponse(BaseModel):
    id:int
    username:str
    email_id:str
    update_time:datetime
    
# class ReturnTask(BaseModel):
#     user_id:int=0
#     page_num:int=0
#     page_size:int=1
#     title:str
#     status:str

class TaskFilters(BaseModel):
    user_id: int
    title:str
    due_date:datetime | None = None
    status:str

class ReturnTask(BaseModel):
    page_num:int=0
    page_size:int=1
    filters:TaskFilters
    column:str
    order:str



# class FilterTask(BaseModel):
#     title:str
    