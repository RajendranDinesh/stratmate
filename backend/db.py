from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session

import os
from dotenv import load_dotenv

load_dotenv()

# Define SQLAlchemy models
Base = declarative_base()

# Initialize database connection
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()