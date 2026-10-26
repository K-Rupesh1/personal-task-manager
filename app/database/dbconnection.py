
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")

if not username or not password:
	raise RuntimeError(
		"Database credentials are missing. Set DB_USERNAME and DB_PASSWORD "
		"in a .env file; see .env.example."
	)

db_url = URL.create(
	"postgresql+psycopg2",
	username=username,
	password=password,
	host=os.getenv("DB_HOST", "localhost"),
	port=int(os.getenv("DB_PORT", "5432")),
	database=os.getenv("DB_NAME", "ptm_db"),
)
engine = create_engine(db_url)
session_start = sessionmaker(autocommit=False, autoflush=False, bind=engine)