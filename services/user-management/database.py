from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Define the database URL
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_ROOT_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_DATABASE = os.getenv("DB_DATABASE")

required_env_vars = ["DB_USER", "DB_ROOT_PASSWORD", "DB_HOST", "DB_PORT", "DB_DATABASE"]
missing_env_vars = [var for var in required_env_vars if os.getenv(var) is None]

if missing_env_vars:
    raise EnvironmentError(f"Missing environment variables: {', '.join(missing_env_vars)}")

# Construct the database URL
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

# Create a SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
