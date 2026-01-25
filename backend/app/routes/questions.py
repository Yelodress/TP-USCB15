from flask import request, jsonify, abort
from sqlalchemy import text
from ..connect import engine
from app.auth import require_jwt
from app.agents.log_agent import send_log
from app.utils import require_admin

def questions_endpoint(app):
    
    @app.get("/questions")
    @require_jwt
    @require_admin
    def list_all_questions():
        with engine.begin() as conn:
            send_log("INFO", "Liste des questions demandée")
            result = conn.execute(text("SELECT id, content, answer FROM question"))
            rows = [dict(r) for r in result.mappings()]
        return jsonify(rows), 200

    @app.get("/questions/<ref>")
    @require_jwt
    @require_admin
    def get_one_question(ref):
        with engine.begin() as conn:
            send_log("INFO", f"La question {ref} a ete demandee")
            result = conn.execute(text("SELECT id, content FROM question Where id = :ref"),{"ref": ref})
            rows = [dict(r) for r in result.mappings()]
        return jsonify(rows), 200
