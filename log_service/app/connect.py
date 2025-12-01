from sqlalchemy import create_engine
from app.config import DATABASE_URL

# Engine seulement pour la connexion à la base de données
# pool_recycle pour éviter les erreurs de timeout de MySQL
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)