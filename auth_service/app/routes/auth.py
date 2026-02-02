from flask import request, jsonify
from sqlalchemy import text
from app.connect import engine, SECRET_KEY
import jwt
import uuid
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash

def auth_endpoint(app, limiter):
    @app.post("/auth")
    @limiter.limit("5 per minute")
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
                        SELECT id, username, password, role FROM users
                        WHERE username = :username
                    """),
                    {"username": username}
                ).fetchone()

            if not result:
                return jsonify({"error": "Invalid credentials"}), 401

            user_id, db_username, db_password, role = result

            # Verify password using Werkzeug, which matches the hash format in the database
            if not check_password_hash(db_password, password):
                return jsonify({"error": "Invalid credentials"}), 401

            # --- LOGIQUE DU REFRESH TOKEN A LA CONNEXION ---
            # 1. Chercher un refresh token existant et valide pour cet utilisateur
            refresh_token = None
            with engine.connect() as conn:
                existing_token_result = conn.execute(
                    text("""
                        SELECT token FROM refresh_tokens
                        WHERE user_id = :user_id AND expires_at > :now AND is_revoked = FALSE
                        ORDER BY created_at DESC
                        LIMIT 1
                    """),
                    {"user_id": user_id, "now": datetime.utcnow()}
                ).fetchone()

            if existing_token_result:
                # 2a. Si un token valide existe, on le réutilise
                refresh_token = existing_token_result[0]
            else:
                # 2b. Sinon (s'il n'y en a pas, ou s'ils sont tous expirés/révoqués), on en crée un nouveau
                refresh_token = str(uuid.uuid4())
                refresh_token_expiry = datetime.utcnow() + timedelta(days=7)
                with engine.connect() as conn:
                    # On insère le nouveau token
                    conn.execute(
                        text("""
                            INSERT INTO refresh_tokens (user_id, token, expires_at)
                            VALUES (:user_id, :token, :expires_at)
                        """),
                        {
                            "user_id": user_id,
                            "token": refresh_token,
                            "expires_at": refresh_token_expiry
                        }
                    )
                    conn.commit()

            # --- Création de l'Access Token (JWT de courte durée) ---
            # Cet access token est TOUJOURS nouveau, avec une durée de vie de 15 minutes
            access_token_payload = {
                "user_id": user_id,
                "username": username,
                "role": role,
                "exp": datetime.utcnow() + timedelta(minutes=15)
            }
            access_token = jwt.encode(access_token_payload, SECRET_KEY, algorithm="HS256")

            # Créer la réponse JSON sans le refresh token
            response_data = {
                "access_token": access_token,
                "user_id": user_id,
                "username": username,
                "role": role
            }
            response = jsonify(response_data)

            # Placer le refresh token dans un cookie HttpOnly, Secure.
            # C'est la méthode sécurisée pour le stocker côté client.
            response.set_cookie('refresh_token', refresh_token,
                                httponly=True, secure=True, samesite='Lax',
                                max_age=timedelta(days=7))
            return response, 200

        except Exception as e:
            print(f"Login error: {e}")
            return jsonify({"error": "Authentication failed"}), 500
        
    @app.post("/refresh")
    @limiter.limit("10 per minute")
    def refresh():
        # Lire le refresh token depuis le cookie au lieu du corps de la requête
        refresh_token = request.cookies.get("refresh_token")

        if not refresh_token:
            return jsonify({"error": "Missing or invalid refresh token"}), 401

        try:
            with engine.connect() as conn:
                db_token = conn.execute(
                    text("""
                        SELECT user_id, expires_at, is_revoked FROM refresh_tokens
                        WHERE token = :token
                    """),
                    {"token": refresh_token}
                ).fetchone()

            if not db_token:
                return jsonify({"error": "Invalid refresh token"}), 401

            user_id, expires_at, is_revoked = db_token

            if is_revoked or datetime.utcnow() > expires_at:
                return jsonify({"error": "Refresh token is invalid or expired"}), 401

            # Récupérer le nom d'utilisateur pour le nouveau payload
            with engine.connect() as conn:
                user_data = conn.execute(text("SELECT username, role FROM users WHERE id = :user_id"), {"user_id": user_id}).fetchone()

            username, role = user_data

            # Générer un nouvel access token
            access_token_payload = {
                "user_id": user_id,
                "username": username,
                "role": role,
                "exp": datetime.utcnow() + timedelta(minutes=15)
            }
            access_token = jwt.encode(access_token_payload, SECRET_KEY, algorithm="HS256")

            return jsonify({"access_token": access_token}), 200

        except Exception as e:
            print(f"Refresh token error: {e}")
            return jsonify({"error": "Refresh failed"}), 500

    @app.post("/logout")
    @limiter.limit("10 per minute")
    def logout():
        # Lire le refresh token depuis le cookie pour le révoquer
        refresh_token = request.cookies.get("refresh_token")

        if not refresh_token:
            return jsonify({"message": "No active session to log out from"}), 200

        try:
            with engine.connect() as conn:
                conn.execute(
                    text("UPDATE refresh_tokens SET is_revoked = TRUE WHERE token = :token"),
                    {"token": refresh_token}
                )
                conn.commit()
            response = jsonify({"message": "Successfully logged out"})
            # Demander au navigateur de supprimer le cookie
            response.delete_cookie('refresh_token', path='/', samesite='Lax')
            return response, 200
        except Exception as e:
            print(f"Logout error: {e}")
            return jsonify({"error": "Logout failed"}), 500