import secrets
import os

def create_secret_file(path):
    # Generate secure 32octets secret key
    key = secrets.token_hex(32)

    # Write the key in the .env file (or replace it)
    with open(path, "w") as f:
        f.write(f"SECRET_KEY=\"{key}\"\n")
if __name__ == "__main__":
    # Create the .env file in the same path as the script
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    create_secret_file(env_path)
