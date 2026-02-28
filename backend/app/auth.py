from flask import request, abort, g
from functools import wraps
import jwt
from app.connect import SECRET_KEY

def require_jwt(func):
    """
    A decorator to protect endpoints with JWT authentication.

    It expects an 'Authorization: Bearer <token>' header.
    It decodes the JWT and if successful, stores the payload in `flask.g.user`.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            abort(401, description="Authorization header is missing")

        parts = auth_header.split()

        if parts[0].lower() != 'bearer' or len(parts) != 2:
            abort(401, description="Authorization header must be in the format 'Bearer <token>'")

        token = parts[1]
        try:
            # Decode the token. PyJWT automatically handles expiration checks.
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            # Store the payload in Flask's request context for use in the endpoint
            g.user = payload
        except jwt.ExpiredSignatureError:
            abort(401, description="Token has expired")
        except jwt.InvalidTokenError:
            abort(403, description="Invalid token")

        return func(*args, **kwargs)
    return wrapper