

from fastapi import APIRouter
from app.database import dbmodels
from app.database.dbconnection import session_start
from fastapi.params import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from enum import Enum

from app.schema import CreateTaskRequest, CreateTaskResponse, UpdateTaskRequest,UpdateTaskResponse


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
    try:
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
    except SQLAlchemyError as e :
        db.rollback()
        raise HTTPException(status_code=500,detail="Failed to save task")from e

    return CreateTaskResponse(
        id = new_task.id, 
        title = new_task.title, 
        description = new_task.description, 
        created_date=new_task.created_date, 
        due_date=new_task.due_date, 
        status=new_task.status)
    
#endpoint for update task
@router.put("/updatetask/{id}")
def UpdateTask(id:int,
               task:UpdateTaskRequest,
               db:Session=Depends(get_db)):
    try :
        if db.get(task):
            task_update=UpdateTask(
                id=task.id,
                title=task.title,
                description=task.description,
                duedate=task.due_date,
                status=task.status
            )
            try:
                db.add(task_update)
                db.commit()
                db.refresh(task_update)
            except SQLAlchemyError as e :
                db.rollback()
                raise HTTPException(status_code=500,detail="Failed to update task")from e
            return UpdateTaskResponse(
                    id = task_update.id, 
                    title = task_update.title, 
                    description = task_update.description, 
                    created_date=task_update.created_date, 
                    due_date=task_update.due_date, 
                    updated_date=task_update.updated_date,
                    status=task_update.status)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500,detail="Task id is not present")from e