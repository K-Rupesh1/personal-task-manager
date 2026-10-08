from fastapi import FastAPI
import os
import psycopg2
from dotenv import load_dotenv

from app.register import login

app = FastAPI(title="TaskFlow API")

# For loading the which is present in .env file
load_dotenv()


#postgres connection

db_username=os.getenv("db_username")
db_password=os.getenv("db_password")

print(f"db_username : {db_username}")
print(f"db_password : {db_password}")


# taskflowDatabase = "{sqlServer}://{username}:{password}@{SQLserver}:{portNumber}/{DBName}"
db_url=f"postgresql://{db_username}:{db_password}@localhost:5432/ptm_db"

#db connection
try:
    connection = psycopg2.connect(db_url)

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users")

    rows = cursor.fetchall()

    print("Data in users table:")

    for row in rows:
        print(row)

    cursor.close()
    connection.close()

except Exception as error:
    print("Error connecting to PostgreSQL:", error)


# routing login.py file methods into main file
app.include_router(login.router,
                   prefix="/register",
                   tags=["authentication"])


@app.get("/health")
def health():
    return {"status": "ok"}