from fastapi import APIRouter


myRouter = APIRouter(prefix="/loginAPIs/1")

@myRouter.get("/login")
def myLogin():
    return { "message": "login is working"}

#@myRouter.get("/register")

#@myRouter.get("/login")

#@myRouter.get("/logout")


