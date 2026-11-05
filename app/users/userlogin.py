from datetime import  datetime,timezone,timedelta

from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.database import dbmodels
from app.database.dbconnection import session_start
from fastapi import APIRouter
from app.database.dbmodels import User
from app.schema import PasswordReset, UpdateRequest, UserRequest, UserResponse

import jwt
from pwdlib import PasswordHash

from app.users.login import UserLogin

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
        password_hash=PasswordHash.recommended()
        hashed_Password=password_hash.hash(login.password)
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
            

        

SECRET_KEY="my_secret_key"
ALGORITHM="HS256"
print(SECRET_KEY)
password_hash=PasswordHash.recommended()

#@myRouter.get("/login")
@router.post("/login")
def LoginRequest(
    Register:UserLogin,    
    db:Session=Depends(get_db)):
    email=Register.email
    password=Register.password

    
    db_user=db.query(dbmodels.User).filter(dbmodels.User.email_id==email).first()
    db_email=db_user.email_id
    db_password=db_user.password
    
    try:

        if db_user is None:
            raise HTTPException(status_code=500,detail="Please Enter Valid Credentails")
        if email==db_email and password_hash.verify(password,db_password):
        #if email==db_email and password_hash==db_password:
            payload={
                    "email_id":email,
                    "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
                    }
            token = jwt.encode(
                    payload,
                    key=SECRET_KEY,
                    algorithm=ALGORITHM
                    )
            print(token)
            return{
                "email":email,
                "jwt":token,
                "msg":"Login Successfull"
            }
        else:
            return{
                "msg":"Forgot Paasword"           
            }           
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500,detail="Please Enter Valid Credentails")
    
    

    
@router.post("/forgotpassword")
def forgot_password(
    Request:PasswordReset,
    db:Session=Depends(get_db)
                    ):
    email_id=Request.email_id
    new_password=Request.new_password
    Confirm_password=Request.confirm_password
    password_hash=PasswordHash.recommended()
    hashed_Password=password_hash.hash(new_password)
    try:
        db_user=db.query(dbmodels.User).filter(dbmodels.User.email_id==email_id).first()
        password=db_user.password
        print(password)
        if new_password==Confirm_password:
            db_user.password=hashed_Password
            print(db_user.password)
            db.commit()
            print("committed successfull")
            db.refresh(db_user)
            return{
                "msg":"Password Reset Successfully"
            }
        else:
            return {
                "msg":"password doesn't match"
            }
               
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500,detail="Error at db connection")
        
# decrypted_token=jwt.decode(
#     token,
#     secret_key=SECRET_KEY,
#     algorithm=ALGORITHM
# )
# print(decrypted_token)
        

#@myRouter.get("/logout")


