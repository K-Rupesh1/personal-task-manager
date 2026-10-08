from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


@router.get("/userregister")
def userregister(user: UserRegister):
    return {
        "username": user.username,
        "message": "user registration successful"
    }


@router.get("/userlogin")
def userlogin(user: UserLogin):
    return {
        "email": user.email,
        "message": "user login successful"
    }