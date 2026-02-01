import os
import uuid
from flask import request, jsonify, g
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from ..connect import engine
from app.auth import require_jwt
from app.agents.log_agent import send_log

# Define the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def answers_endpoint(app):
    # Ensure the upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    @app.post("/answers")
    @require_jwt
    def submit_answer():
        # The user_id is extracted from the JWT by the require_jwt decorator
        user_id = g.user.get('user_id')
        if not user_id:
            return jsonify({"error": "User ID not found in token"}), 401

        # Since we are handling file uploads, we expect multipart/form-data
        if 'question_id' not in request.form or 'response' not in request.form:
            return jsonify({"error": "question_id and response are required fields"}), 400

        question_id = request.form.get('question_id')
        response_str = request.form.get('response', '').lower()
        
        # Convert reponse to boolean
        if response_str not in ['true', 'false', '1', '0']:
             return jsonify({"error": "Invalid value for response. Must be true/false or 1/0."}), 400
        response = response_str in ['true', '1']

        image_path = None
        # Check if an image file was posted
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                # Secure the filename and make it unique
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex}-{filename}"
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                
                try:
                    file.save(save_path)
                    image_path = save_path # Store the path to be saved in the DB
                except Exception as e:
                    send_log("ERROR", f"Failed to save image: {e}")
                    return jsonify({"error": "Failed to save image"}), 500
            elif file and file.filename != '':
                return jsonify({"error": "File type not allowed"}), 400

        try:
            with engine.begin() as conn:
                conn.execute(
                    text("""
                        INSERT INTO user_answers (user_id, question_id, response, image_path)
                        VALUES (:user_id, :question_id, :response, :image_path)
                    """),
                    {
                        "user_id": user_id,
                        "question_id": question_id,
                        "response": response,
                        "image_path": image_path
                    }
                )
                send_log("INFO", f"User {user_id} answered question {question_id}")
                return jsonify({"message": "Answer submitted successfully"}), 201
        except IntegrityError:
            # This happens if the (user_id, question_id) unique constraint is violated
            send_log("WARN", f"User {user_id} attempted to answer question {question_id} again.")
            return jsonify({"error": "You have already answered this question."}), 409
        except Exception as e:
            send_log("ERROR", f"Database error on answer submission: {e}")
            return jsonify({"error": "An internal error occurred"}), 500