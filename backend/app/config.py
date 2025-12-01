import os
from sqlalchemy import create_engine

# Variable d'environnement pour la configuration de la base de données
# TODO enlever les valeurs par défaut pour la production
DB_USER = os.getenv("DB_USER", "tp_user")
DB_PASS = os.getenv("DB_PASS", "tp_pass")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "tp_uscb15")

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
)
engine = create_engine(DATABASE_URL)
