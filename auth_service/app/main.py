from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.routes.auth import auth_endpoint
from app.routes.call import call_endpoint

# Initialize rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def create_app():
    app = Flask(__name__)
    limiter.init_app(app)

    @app.get("/")
    def index():
        return jsonify({"message": "auth service"})

    auth_endpoint(app, limiter)
    call_endpoint(app)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002)