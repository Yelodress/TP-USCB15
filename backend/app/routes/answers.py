from app.auth import require_jwt
from app.agents.log_agent import send_log

def answers_endpoint(app):
    
    @app.post("/answer ") # Afficher la liste des questions
    @require_jwt
    def list_questions():
        with engine.begin() as conn:
            send_log("INFO", "Liste des questions demandée")
            result = conn.execute(text("SELECT id, content, answer FROM question"))
            rows = [dict(r) for r in result.mappings()]
        return jsonify(rows), 200