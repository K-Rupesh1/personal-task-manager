
from datetime import date
from fastapi import APIRouter
from app.database import dbmodels
from app.database.dbconnection import session_start
from pydantic import BaseModel,Field
from fastapi.params import Depends
from sqlalchemy.orm import Session


router=APIRouter()

def get_db():
    db=session_start()
    try:
        yield db
    finally:
        db.close()
    

class CreateTask(BaseModel):
    id:int
    title:str=Field(min_length=3)
    description:str=Field(...,min_length=7,description="Description must have morethan 6 characters")
    created_date:date 
    due_date:date 
    status: dbmodels.TaskStatus = dbmodels.TaskStatus.PENDING
    
@router.post("/addtask")
def Add_Task(task:CreateTask,
    db:Session=Depends(get_db)):
    new_task=dbmodels.Create_Task(
        id=task.id,
        title=task.title,
        description=task.description,
        created_date=task.created_date,
        due_date=task.due_date,
        status=task.status.value   
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    {
        "message": "Task Added Successfull",
        "id":new_task.id,
        "title":new_task.title,
        "description":new_task.description,
        "created_date":new_task.created_date,
        "due_date":new_task.due_date,
        "status":new_task.status
    }