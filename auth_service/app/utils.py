from functools import wraps
from flask import request, jsonify
import jwt
from app.connect import SECRET_KEY

def gate_is_admin(f):
    """
    Decorator to ensure the user is an admin.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Authorization header is required"}), 401

        try:
            token_parts = auth_header.split()
            if len(token_parts) != 2 or token_parts[0].lower() != 'bearer':
                return jsonify({"error": "Invalid Authorization header format"}), 401
            
            token = token_parts[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            
            if payload.get("role") != "ADMIN":
                return jsonify({"error": "Admin access required"}), 403
        except Exception:
            return jsonify({"error": "Invalid or expired token"}), 401
            
        return f(*args, **kwargs)
    return decorated_function