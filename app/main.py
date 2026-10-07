import os

from dotenv import load_dotenv
from fastapi import FastAPI
import psycopg2

from app import status

from app.register import login5
from app.register import login

app = FastAPI(title="TaskFlow API")

app.include_router(status.router)

app.include_router(login.myRouter)

app.include_router(login5.myRouter)


#postgres connection

# taskflowDatabase = "{sqlServer}://{username}:{password}@{SQLserver}:{portNumber}/{DBName}"

load_dotenv()

DB_PW = os.getenv("DB_PASSWORD")

DB_UN = os.getenv("DB_USERNAME")

print("My pw is ", DB_PW)
print("My username is ", DB_UN)

taskflowDatabase = f"postgresql://{DB_UN}:{DB_PW}@localhost:5432/taskflow"

try:
    # psycopg2 natively accepts connection URIs
    connection = psycopg2.connect(taskflowDatabase)
    
    cursor = connection.cursor()
    cursor.execute("SELECT * from users")
    db_version = cursor.fetchone()
    print("Successfully connected to 'taskflow' database!")
    print("PostgreSQL version:", db_version)
    
    # Close the connections
    cursor.close()
    connection.close()

except Exception as error:
    print("Error connecting to PostgreSQL:", error)

@app.get("/health")
def healthName():
    return {"status": "Hello world!"}

# @app.get("/isOk")
# def healthName():
#     return {"status": "I am very good from main.py"}

#Cons
# confusing
# non readable
# not maintainable
# No separation

#Better way of doing it

#by separating