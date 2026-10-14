

from fastapi import APIRouter
from app.database import dbmodels
from app.database.dbconnection import session_start
from fastapi.params import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from enum import Enum
from datetime import datetime

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
    new_task=dbmodels.Task(
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
@router.put("/updatetask")
def UpdateTask(id:int,
               task:UpdateTaskRequest,
               db:Session=Depends(get_db)):
    try:
        # task entity object created by using api user request
        taskEntityObj=dbmodels.Task(
                                    title=task.title,
                                    description=task.description,
                                    due_date=task.due_date,
                                    status=task.status,
                                    update_date=datetime.now()
                                )
        
        # getting existing task fromt he db
        # taskFromDB holds db data directly
        taskFromDB = db.get(dbmodels.Task, id); #database row

        # raise SQLAlchemyError("Simulated database failure")

        if taskFromDB is not None:
            try:
                taskFromDB.title = taskEntityObj.title;
                taskFromDB.status = taskFromDB.status;
                taskFromDB.due_date = taskEntityObj.due_date;
                taskFromDB.description = taskEntityObj.description;
                taskFromDB.update_date = taskEntityObj.update_date;

                db.commit()
                db.refresh(taskFromDB)

                return UpdateTaskResponse(
                            id = taskFromDB.id, 
                            title = taskFromDB.title, 
                            description = taskFromDB.description, 
                            created_date=taskFromDB.created_date, 
                            due_date=taskFromDB.due_date, 
                            update_date=taskFromDB.update_date,
                            status=taskFromDB.status)
            
            except SQLAlchemyError as e :
                    db.rollback()
                    raise HTTPException(status_code=500,detail="Failed to update task")from e
        else:
            raise HTTPException(
                status_code=404,
                detail="Task id is not present"
            )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500,detail="Something went wrong, Try again after some")