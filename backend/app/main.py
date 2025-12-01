from flask import Flask, jsonify
from app.routes.questions import questions_endpoint

def create_app():
    app = Flask(__name__)

    @app.get("/")
    def index():
     return jsonify({"message": "Tp-usb15"})
   
    questions_endpoint(app)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
