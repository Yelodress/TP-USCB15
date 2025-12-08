from flask import Flask, jsonify
from app.routes.auth import auth_endpoint

def create_app():
    app = Flask(__name__)

    @app.get("/")
    def index():
        return jsonify({"message": "auth service"})

    auth_endpoint(app)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002)