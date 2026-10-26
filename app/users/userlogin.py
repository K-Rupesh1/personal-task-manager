from datetime import  datetime

from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.database import dbmodels
from app.database.dbconnection import session_start

from fastapi import APIRouter

from app.database.dbmodels import User
from app.schema import UpdateRequest, UserRequest, UserResponse


router = APIRouter()

def get_db():
    db=session_start()
    try:
        yield db
    finally:
        db.close()
@router.post("/register")
def UserLoginRequest(login:UserRequest,
                    db:Session=Depends(get_db)):
    
    try:
        userlogin=User(
                username=login.username,
                email_id=login.email_id,
                password=login.password
                )
        print("1. User object created")
        db.add(userlogin)
        
        db.commit()
        
        db.refresh(userlogin)
        print("3. Data refreshed successfully")
        print("there is a matching data in the database")
        print("2. Data committed successfully")
        # return userlogin;
        return UserResponse(
            user_id=userlogin.user_id,
            username=userlogin.username,
            email_id=userlogin.email_id,
            create_date=userlogin.create_date,
            update_date=userlogin.update_date
        )
        print("4. Response created successfully")       
    except SQLAlchemyError :
        db.rollback()
        raise HTTPException(status_code=500,detail="problem at database connection")
    
@router.put("/update")
def UpdateDetails(id:int,
                  update:UpdateRequest,
                  db:Session=Depends(get_db)):
    try:
        dbentityobj=dbmodels.User(
            username=update.username,
            email_id=update.email_id,
            password=update.password
            )
        print("hiiiiiiiiiiiiii")
        taskfromdb=db.get(dbmodels.User,id)
        print("task from databse",taskfromdb)
        if taskfromdb is not None:
            try:
                
                taskfromdb.username=dbentityobj.username,
                taskfromdb.email_id=dbentityobj.email_id,
                taskfromdb.password=dbentityobj.password
                print("object created successfully")
                db.commit()
                print("object commited successfully")
                db.refresh(taskfromdb)
                print("database refresed successfully")
                return UserResponse(
                    id=taskfromdb.id,
                    username=taskfromdb.username,
                    email_id=taskfromdb.email_id,
                    password=taskfromdb.password,
                    create_date=taskfromdb.create_date,
                    update_date=taskfromdb.update_date
                    
                )
            except SQLAlchemyError as e:
                raise HTTPException(status_code=500,detail="problem at updating task to db") 
               
        else:
            raise HTTPException(status_code=500,detail="the user is not present in database")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500,detail="Something went wrong, Try again after some")  
            

        



#@myRouter.get("/register")

#@myRouter.get("/login")

#@myRouter.get("/logout")


