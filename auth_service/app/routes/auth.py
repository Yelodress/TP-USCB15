from flask import request, jsonify
from sqlalchemy import text
from app.connect import engine
import jwt
from datetime import datetime, timedelta
import os

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")

def auth_endpoint(app):
    @app.post("/auth")
    def login():
        data = request.get_json() or {}
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "username and password required"}), 400

        try:
            with engine.connect() as conn:
                result = conn.execute(
                    text("""
                        SELECT id, username, password FROM users
                        WHERE username = :username
                    """),
                    {"username": username}
                ).fetchone()

            if not result:
                return jsonify({"error": "Invalid credentials"}), 401

            user_id, db_username, db_password = result

            # NOTE: remplacer par un vrai hachage (bcrypt) en prod
            if db_password != password:
                return jsonify({"error": "Invalid credentials"}), 401

            payload = {
                "user_id": user_id,
                "username": username,
                "exp": datetime.utcnow() + timedelta(hours=24)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

            return jsonify({"token": token, "user_id": user_id, "username": username}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500