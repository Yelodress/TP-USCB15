from flask import jsonify, request
import requests
import os
from app.utils import gate_is_admin
# These URLs are for communication within the Docker network.
BACKEND_SERVICE_URL = os.environ.get("BACKEND_SERVICE_URL", "http://api:8000")  # 'api' is the service name in docker-compose.yml

def call_endpoint(app):
    @app.post("/call-questions")
    @gate_is_admin
    def call_questions_service():
        """
        An endpoint that acts as a proxy to the backend service.
        It expects a JWT in the Authorization header and forwards the request
        to the backend /questions endpoint.
        """
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify({"error": "HELOOOOOOAuthorization header is required"}), 401

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

    @app.post("/call-answers")
    def call_answers_service():
        """
        Acts as a proxy to the backend service for posting an answer with an optional image.
        It expects a JWT in the Authorization header and multipart/form-data,
        forwarding the request to the backend /answers endpoint.
        """
        # For multipart/form-data, we check for form data or files.
        if not request.form and not request.files:
            return jsonify({"error": "Request body with form data or files is required"}), 400

        # We must not forward the Content-Type header from the original request.
        # `requests` will generate its own with the correct boundary for multipart.
        headers = {"Authorization": request.headers.get('Authorization')}

        # The `requests` library can take Werkzeug's FileStorage objects directly.
        forwarded_files = {
            field: (file.filename, file.stream, file.content_type)
            for field, file in request.files.items()
        }

        try:
            # When sending files, `requests` automatically sets the Content-Type to multipart/form-data.
            response = requests.post(
                f"{BACKEND_SERVICE_URL}/answers",
                headers=headers,
                data=request.form,
                files=forwarded_files,
                timeout=15  # Increased timeout for potential file uploads
            )
            # We forward the response content, status code, and relevant headers directly.
            return response.content, response.status_code, {'Content-Type': response.headers.get('Content-Type')}
        except requests.exceptions.RequestException as e:
            print(f"Error calling backend service: {e}")
            return jsonify({"error": "Failed to communicate with the backend service"}), 502
        
    @app.post("/questions/<ref>")
    def call_questions_service_by_ref(ref):
        """
        An endpoint that acts as a proxy to the backend service.
        It expects a JWT in the Authorization header and forwards the request
        to the backend /questions endpoint with a ref parameter.
        """
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify({"error": "Authorization header is required"}), 401

        headers = {"Authorization": auth_header}
        try:
            response = requests.get(
                f"{BACKEND_SERVICE_URL}/questions/{ref}", headers=headers, timeout=5
            )
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException as e:
            print(f"Error calling backend service: {e}")
            return jsonify({"error": "Failed to communicate with the backend service"}), 502