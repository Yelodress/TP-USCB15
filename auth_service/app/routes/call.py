from flask import jsonify, request
import requests
import os
# These URLs are for communication within the Docker network.
BACKEND_SERVICE_URL = os.environ.get("BACKEND_SERVICE_URL", "http://api:8000")  # 'api' is the service name in docker-compose.yml

def call_endpoint(app):
    @app.post("/call-questions")
    def call_questions_service():
        """
        An endpoint that acts as a proxy to the backend service.
        It expects a JWT in the Authorization header and forwards the request
        to the backend /questions endpoint.
        """
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify({"error": "Authorization header is required"}), 401

        headers = {"Authorization": auth_header}
        try:
            response = requests.get(
                f"{BACKEND_SERVICE_URL}/questions", headers=headers, timeout=5
            )
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException as e:
            print(f"Error calling backend service: {e}")
            return jsonify({"error": "Failed to communicate with the backend service"}), 502