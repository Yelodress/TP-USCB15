import secrets
import os

def create_secret_file(path):
    """
    Génère une clé secrète et l'écrit dans un fichier au chemin spécifié.
    Le fichier sera écrasé s'il existe déjà.
    """
    # Générer une clé sécurisée de 32 octets (64 caractères hexadécimaux)
    key = secrets.token_hex(32)

    # Écrire la clé dans le fichier .env, en l'écrasant s'il existe
    with open(path, "w") as f:
        f.write(f"SECRET_KEY=\"{key}\"\n")
if __name__ == "__main__":
    # Crée le fichier .env dans le même répertoire que ce script
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    create_secret_file(env_path)
