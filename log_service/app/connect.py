from sqlalchemy import create_engine
from app.config import DATABASE_URL

# Engine only for DB connection
# pool_recycle to avoid MySQL timeout errors.
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)