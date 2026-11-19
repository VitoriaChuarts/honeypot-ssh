import os
from datetime import datetime, timezone

import requests

SIEM_URL = os.environ.get("SIEM_URL", "http://localhost:8080/api/alerts")
API_KEY = os.environ.get("SIEM_API_KEY", "")


def enviar_alerta(ip, usuario, senha):
    alerta = {
        "source": "honeypot",
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "srcIp": ip,
        "eventType": "ssh_login_attempt",
        "severity": "high" if usuario == "root" else "medium",
        "details": {"user": usuario, "password": senha},
    }
    try:
        requests.post(SIEM_URL, json=alerta,
                      headers={"X-API-Key": API_KEY}, timeout=2)
    except requests.RequestException:
        # Se o SIEM estiver fora do ar, o honeypot continua funcionando
        pass
