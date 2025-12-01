import requests
import os

LOG_SERVICE_URL = os.getenv("LOG_SERVICE_URL", "http://log_service:8001/log")

def send_log(level, message, service="backend", details=None):
    payload = {
        "level": level,
        "message": message,
        "service": service,
        "details": details
    }
    try:
        requests.post(LOG_SERVICE_URL, json=payload, timeout=2)
    except Exception as e:
        pass