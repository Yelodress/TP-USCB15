from flask import jsonify
from sqlalchemy import text
from ..connect import engine
from app.auth import require_jwt

from app.agents.log_agent import send_log

def answers_endpoint(app):
    
    @app.post("/answers")
    @require_jwt

    def submit_answer():
        with engine.begin() as conn:
            send_log("INFO", "Traitement de la réponse")
            result = conn.execute(text("SELECT id, content FROM question"))
            rows = [dict(r) for r in result.mappings()]
        return jsonify(rows), 200