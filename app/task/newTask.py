

from fastapi import APIRouter
from app.database import dbmodels
from app.database.dbconnection import session_start
from fastapi.params import Depends
from sqlalchemy.orm import Session
from enum import Enum

from app.schema import CreateTaskRequest, CreateTaskResponse


router=APIRouter()

def get_db():
    db=session_start()
    try:
        yield db
    finally:
        db.close()
    
    
@router.post("/addtask")
def Add_Task(task:CreateTaskRequest,
    db:Session=Depends(get_db)):
    new_task=dbmodels.Create_Task(
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        status=task.status.value   
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return CreateTaskResponse(
        id = new_task.id, 
        title = new_task.title, 
        description = new_task.description, 
        created_date=new_task.created_date, 
        due_date=new_task.due_date, 
        status=new_task.status)