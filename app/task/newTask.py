

from fastapi import APIRouter
from app.database import dbmodels
from app.database.dbconnection import session_start
from fastapi.params import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from enum import Enum
from datetime import datetime

from app.schema import CreateTaskRequest, CreateTaskResponse,ReturnTask, UpdateTaskRequest,UpdateTaskResponse


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
        user_id=task.user_id,
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
        print("DATABASE ERROR:", repr(e))
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

#DELETE TASK
@router.delete("/deletetask/{id}")
def deletetask(id:int,
    db:Session=Depends(get_db)):
    print(id)
    try:
        get_task_from_db=db.get(dbmodels.Task,id)
        print(get_task_from_db)

        if  get_task_from_db is not None:
            db.delete(get_task_from_db)
            db.commit()
            return{
                "message":"task successfully deleted",
                "id":id
            }
        else  :
            raise HTTPException(status_code=404,detail="task id is not present")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500,detail="Something went wrong, Try again after some")
    
    



# RETURN TASKS
@router.post("/gettasks")
def gettasks(
             task:ReturnTask,
             db:Session=Depends(get_db)
             ):
    user_id=task.user_id
    page_num=task.page_num
    page_size=task.page_size
    title=task.title
    status=task.status
    response={
        "total_count":db.query(dbmodels.Task).count(),
        "data":[]
    }
    try:
        if user_id ==0:
            start=page_num*page_size
            response["data"]=db.query(dbmodels.Task).filter(dbmodels.Task.title.ilike(f"%{title}%")).order_by(dbmodels.Task.status.like(f"{status}=asc")).offset(start).limit(page_size).all()
            return response
            
        else:
            get_task_from_db= db.query(dbmodels.Task).filter(dbmodels.Task.user_id==user_id,dbmodels.Task.title.ilike(f"%{title}%")).all()
            #print(get_task_from_db)
            if get_task_from_db: # if value is present in get_task_from_db it will return the value.
                return {
                    "total_count":response["total_count"],
                    "data":get_task_from_db
                }
            else:
                raise HTTPException(
                    status_code=404,
                    detail="No tasks found for this user")
    except SQLAlchemyError as e: 
        raise HTTPException(f"error{e}",status_code=500,detail="Error at data retrivel from db ,Please try again later") from e
    
    

# #FILTER TASK
# @router.post("/filter")
# def taskfilter(task:FilterTask,
#                db:Session=Depends(get_db)):
#     title=task.title
#     try:
#         filter=db.query(dbmodels.Task).filter(dbmodels.Task.title.ilike(f"%{title}%")).all()
#         if not filter:
#             raise HTTPException(
#                             status_code=404,
#                             detail="No title found")
#         return filter
            
#     except SQLAlchemyError as e: 
#         raise HTTPException(f"error{e}",status_code=500,detail="Error at data retrivel from db ,Please try again later") from e
    