from flask import request, abort
from functools import wraps
from sqlalchemy import text
from app.config import engine

def require_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Protection API KEY activée sur", request.path)
        api_key = request.headers.get('X-API-KEY') or request.args.get('api_key')
        if not api_key:
            abort(401, description="API key required")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 FROM api_keys WHERE api_key = :api_key"), {"api_key": api_key})
            if not result.first():
                abort(403, description="Invalid API key")
        return func(*args, **kwargs)
    return wrapper