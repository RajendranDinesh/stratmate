from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from models import Base
from dotenv import load_dotenv
import os

load_dotenv()

# Database connection details
DATABASE_URL = os.getenv("DATABASE_URL")

def create_tables():
    # Create engine and connect to the database
    engine = create_engine(DATABASE_URL)

    # Create tables
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully.")
    except ProgrammingError as e:
        print(f"Error creating tables: {e}")

if __name__ == "__main__":
    create_tables()
