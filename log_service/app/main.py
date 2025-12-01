# ...existing code...
from flask import Flask, request, jsonify
from sqlalchemy import text
from .connect import engine
import json

app = Flask(__name__)

@app.post("/log")
def receive_log():
    data = request.get_json(force=True, silent=True) or {}
    raw_details = data.get("details", None)
    if raw_details is None:
        details_json = None
    else:
        # ensure details are stored as JSON text
        try:
            details_json = json.dumps(raw_details)
        except Exception:
            # fallback: store string representation if not JSON-serializable
            details_json = json.dumps(str(raw_details))

    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO log (timestamp, service, level, message, details)
                VALUES (NOW(), :service, :level, :message, :details)
            """),
            {
                "service": data.get("service"),
                "level": data.get("level"),
                "message": data.get("message"),
                "details": details_json,
            },
        )
    return jsonify({"status": "ok"})

@app.get("/log")
def get_logs():
    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT id, timestamp, service, level, message, details FROM log ORDER BY timestamp DESC")
        ).fetchall()

    out = []
    for r in rows:
        ts = r[1].isoformat() if r[1] else None
        details = r[5]
        try:
            details = json.loads(details) if isinstance(details, str) else details
        except Exception:
            pass
        out.append({
            "id": r[0],
            "timestamp": ts,
            "service": r[2],
            "level": r[3],
            "message": r[4],
            "details": details,
        })
    return jsonify(out)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
# ...existing code...