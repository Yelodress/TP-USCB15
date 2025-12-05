# ...existing code...
from flask import request, jsonify, abort
from sqlalchemy import text
from ..connect import engine
from app.auth import require_api_key
from app.agents.log_agent import send_log

def questions_endpoint(app):
    
    @app.get("/questions") # Afficher la liste des questions
    @require_api_key
    def list_questions():
        with engine.begin() as conn:
            send_log("INFO", "Liste des questions demandée")
            result = conn.execute(text("SELECT id, content, answer FROM question"))
            rows = [dict(r) for r in result.mappings()]
        return jsonify(rows), 200

    @app.get("/question/<int:id>") # Affiche une question en fonction de son ID
    @require_api_key
    def get_question(id):
        with engine.begin() as conn:
            send_log("INFO", f"Détails de la question {id} demandés")
            result = conn.execute(text("SELECT id, content, answer FROM question WHERE id = :id"), {"id": id})
            row = result.mappings().first()

            if row is None:
                send_log("WARNING", f"Tentative d'accès à une question inexistante : {id}")
                abort(404, description="Question not found")

        return jsonify(dict(row)), 200