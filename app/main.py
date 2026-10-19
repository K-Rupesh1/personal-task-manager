from fastapi import FastAPI

import os
import psycopg2
from dotenv import load_dotenv

from app.database.dbmodels import Base
from app.database.dbconnection import engine
from app.users import userlogin
from app.task import newTask

app = FastAPI(title="TaskFlow API")
Base.metadata.create_all(bind=engine)


# routing login.py file methods into main file
app.include_router(userlogin.router,
                   prefix="/login",
                   tags=["authentication"])

app.include_router(newTask.router,
                   prefix="/task",
                   tags=["Adding Task"])


@app.get("/health")
def health():
    return {"status": "ok"}