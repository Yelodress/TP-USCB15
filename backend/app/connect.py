from sqlalchemy import create_engine
import os

# --- Configuration Loading ---
# In a Docker environment, all these variables are provided by docker-compose.

SECRET_KEY = os.getenv("SECRET_KEY")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# It's critical to ensure all required variables are set.
if not all([SECRET_KEY, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS]):
    raise ValueError("One or more environment variables are missing (SECRET_KEY, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS).")

connection_string = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# pool_recycle to avoid MySQL 'gone away' errors
engine = create_engine(connection_string, pool_pre_ping=True, pool_recycle=3600)
