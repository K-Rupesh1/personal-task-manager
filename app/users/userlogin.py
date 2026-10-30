from datetime import  datetime,timezone,timedelta
import os

from dotenv import load_dotenv
from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.database import dbmodels
from app.database.dbconnection import session_start
from fastapi import APIRouter
from app.database.dbmodels import User
from app.schema import LoginRequest, LoginResponse, UpdateRequest, UserRequest, UserResponse

import jwt
from pwdlib import PasswordHash

router = APIRouter()

load_dotenv()

#1
SECRET_KEY=os.getenv("SECRET_KEY")

#2
ALGORITHM = "HS256"

#3
EXPIRY = 30


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
        
        password_hash=PasswordHash.recommended()
        hashed_Password=password_hash.hash(login.password)
        print(hash)
        userlogin=User(
                username=login.username,
                email_id=login.email_id,
                password=hashed_Password
                )
        print("1. User object created")
        db.add(userlogin)
        
    
        db.commit()
        print("2. Data Committed Successfully")
        db.refresh(userlogin)
        print("3. Data refreshed successfully")
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
            

@router.post("/login")
def UserLoginRequest(loginRequest:LoginRequest,
                    db:Session=Depends(get_db)):
    
    try:

        #4
        payload={
                "sub":loginRequest.username,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=EXPIRY)
                }

        dbUser = db.query(dbmodels.User).filter_by(username=loginRequest.username).first()

        print(dbUser.password);

        password_hash=PasswordHash.recommended()

        isAuhorized= password_hash.verify(loginRequest.password, dbUser.password)

        print(isAuhorized)

        if isAuhorized:
            
            token = jwt.encode(
                payload,
                SECRET_KEY,
                algorithm=ALGORITHM
                )
            return LoginResponse(
                token = token,
                type = "bearer"
            )
        else:
            return "Username or Password is wrong!"
        
    except SQLAlchemyError :
        db.rollback()
        raise HTTPException(status_code=500,detail="problem at database connection")



#@myRouter.get("/register")

#@myRouter.get("/login")

#@myRouter.get("/logout")


