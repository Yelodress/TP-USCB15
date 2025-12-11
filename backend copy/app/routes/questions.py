from flask import request, jsonify, abort
from sqlalchemy import text
from ..connect import engine
from app.auth import require_api_key
from app.agents.log_agent import send_log

def KMS_endpoint(app):
    
    @app.get("/questions") # Afficher la liste des questions
    @require_api_key
    def list_questions():
        with engine.begin() as conn:
            send_log("INFO", "Liste des questions demandée")
            result = conn.execute(text("SELECT id, content, answer FROM question"))
            rows = [dict(r) for r in result.mappings()]
        return jsonify(rows), 200

    @app.get("/questions/<ref>") # Afficher un question en particulier
    @require_api_key
    def get_questions(ref):
        with engine.begin() as conn:
            send_log("INFO", f"La question {ref} a ete demandee")
            result = conn.execute(text("SELECT id, content FROM questions Where LOWER(id) = LOWER(:ref)"),{"ref": ref})
            rows = [dict(r) for r in result.mappings()]
        return jsonify(rows), 200
