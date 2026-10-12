
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

username=os.getenv("DB_USERNAME")
password=os.getenv("DB_PASSWORD")
db_url=f"postgresql+psycopg2://{username}:{password}@localhost:5432/ptm_db"
engine=create_engine(db_url)
session_start=sessionmaker(autocommit=False,autoflush=False,bind=engine)