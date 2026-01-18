from sqlalchemy import create_engine
import os
import urllib.request
import json
import time

# --- Configuration Loading ---
# In a Docker environment, all these variables are provided by docker-compose.

SECRET_KEY = os.getenv("SECRET_KEY")
VAULT_ADDR = os.getenv("VAULT_ADDR", "http://vault:8200")
VAULT_TOKEN = os.getenv("VAULT_TOKEN", "root")

def get_secret_from_vault():
    """Tente de récupérer la SECRET_KEY depuis Vault."""
    url = f"{VAULT_ADDR}/v1/secret/data/tp-uscb15"
    req = urllib.request.Request(url, headers={"X-Vault-Token": VAULT_TOKEN})
    
    # On réessaie plusieurs fois car Vault peut être plus lent à démarrer que ce service
    for _ in range(5):
        try:
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status == 200:
                    data = json.loads(response.read())
                    # Structure de réponse Vault KV v2 : data -> data -> key
                    return data["data"]["data"].get("SECRET_KEY")
        except Exception:
            time.sleep(1)
    return None

SECRET_KEY = get_secret_from_vault() or os.getenv("SECRET_KEY")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# The application will fail to start if one is missing.
if not all([SECRET_KEY, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS]):
    raise ValueError("One or more environment variables are missing (SECRET_KEY, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS).")

connection_string = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(connection_string)