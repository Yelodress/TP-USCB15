from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.routes.auth import auth_endpoint
from app.routes.call import call_endpoint
from werkzeug.security import generate_password_hash
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from app.connect import engine
import time


# Initialize rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def create_user(username, password, role='USER'):
    """
    Creates a user with a hashed password if they don't already exist.
    This is a utility function for development setup.
    """
    hashed_password = generate_password_hash(password)
    try:
        with engine.connect() as conn:
            # Check if user already exists
            result = conn.execute(
                text("SELECT id FROM users WHERE username = :username"),
                {"username": username}
            ).fetchone()

            if result:
                print(f"User '{username}' already exists. Skipping creation.")
                return

            # Insert new user
            conn.execute(
                text("INSERT INTO users (username, password, role) VALUES (:username, :password, :role)"),
                {"username": username, "password": hashed_password, "role": role}
            )
            conn.commit()
            print(f"Successfully created user '{username}'.")
    except Exception as e:
        print(f"Error creating user '{username}': {e}")

def setup_database():
    """
    Waits for the database to be ready and creates default users.
    This function implements a retry mechanism to handle race conditions during startup.
    """
    max_retries = 10
    retry_delay = 5  # seconds

    print("--- Initializing database setup ---")
    for attempt in range(max_retries):
        try:
            print(f"Attempting to connect to the database (Attempt {attempt + 1}/{max_retries})...")
            with engine.connect() as conn:
                conn.execute(text("SELECT 1")) # Simple query to test connection
            
            print("Database connection successful. Ensuring default users exist...")
            create_user('admin', 'adminpass', 'ADMIN')
            create_user('user1', 'pass1', 'USER')
            print("--- User setup complete. ---")
            return # Exit loop on success
        except OperationalError as e:
            print(f"Database connection failed: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Could not connect to the database after multiple retries. The application might not work correctly.")

def create_app():
    app = Flask(__name__)
    limiter.init_app(app)

    setup_database()

    @app.get("/")
    def index():
        return jsonify({"message": "auth service"})

    auth_endpoint(app, limiter)
    call_endpoint(app)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002)