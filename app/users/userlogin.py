from datetime import  datetime

from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.database.dbconnection import session_start

from fastapi import APIRouter

from app.database.dbmodels import User
from app.schema import UserRequest, UserResponse


router = APIRouter()

def get_db():
    db=session_start()
    try:
        yield db
    finally:
        db.close()
@router.get("/login")
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
        print("there is a matching data in the database")
        db.commit()
        print("2. Data committed successfully")
        db.refresh(userlogin)
        print("3. Data refreshed successfully")
        return UserResponse(
            id=userlogin.id,
            username=userlogin.username,
            email_id=userlogin.email_id,
            create_date=userlogin.create_date,
            update_date=userlogin.update_date
        ) 
        print("4. Response created successfully")       
    except SQLAlchemyError :
        db.rollback()
        raise HTTPException(status_code=500,detail="problem at database connection")
        



#@myRouter.get("/register")

#@myRouter.get("/login")

#@myRouter.get("/logout")


