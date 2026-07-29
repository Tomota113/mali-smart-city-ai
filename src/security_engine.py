import pandas as pd
import json
from datetime import datetime, timedelta

def generate_security_logs_data(target_domain="smartcity.bamako.ml"):
    """
    Génère un jeu de données synthétique de logs de sécurité et trouvailles SOC.
    """
    findings = [
        {
            "finding_id": "SEC-BMK-001",
            "timestamp": (datetime.now() - timedelta(minutes=18)).strftime("%Y-%m-%d %H:%M:%S"),
            "agent_id": "AGT-RECON-01",
            "target": f"admin.{target_domain}:8443",
            "category": "Port / Service Sensible Exposé",
            "severity": "MOYEN",
            "cvss": 5.4,
            "description": "Port d'administration serveur exposé sans restriction d'IP.",
            "microvm": "microvm-node-101"
        },
        {
            "finding_id": "SEC-BMK-002",
            "timestamp": (datetime.now() - timedelta(minutes=14)).strftime("%Y-%m-%d %H:%M:%S"),
            "agent_id": "AGT-SCAN-02",
            "target": f"https://{target_domain}/api/v1/auth",
            "category": "Injection SQL / Bypass Auth",
            "severity": "CRITIQUE",
            "cvss": 9.8,
            "description": "Paramètre d'authentification vulnérable à l'injection SQL.",
            "microvm": "microvm-node-102"
        },
        {
            "finding_id": "SEC-BMK-003",
            "timestamp": (datetime.now() - timedelta(minutes=9)).strftime("%Y-%m-%d %H:%M:%S"),
            "agent_id": "AGT-API-03",
            "target": f"https://{target_domain}/api/v1/grid/data",
            "category": "BOLA / IDOR Authorization",
            "severity": "ÉLEVÉ",
            "cvss": 8.2,
            "description": "Absence de vérification des droits sur les données IoT du réseau.",
            "microvm": "microvm-node-103"
        },
        {
            "finding_id": "SEC-BMK-004",
            "timestamp": (datetime.now() - timedelta(minutes=4)).strftime("%Y-%m-%d %H:%M:%S"),
            "agent_id": "AGT-SCAN-02",
            "target": f"https://{target_domain}/portal",
            "category": "En-têtes HTTP Sécurité Manquants",
            "severity": "FAIBLE",
            "cvss": 3.2,
            "description": "HSTS et Content-Security-Policy absents de la réponse HTTP.",
            "microvm": "microvm-node-102"
        }
    ]
    return findings

class SmartCitySecurityEngine:
    """
    Moteur de sécurité et d'audit d'orchestration pour Mali Smart City AI.
    """
    def __init__(self):
        pass

    def evaluate_security_risk(self, findings):
        if len(findings) == 0:
            return 100.0, "SÉCURISÉ"
            
        penalties = {"CRITIQUE": 30, "ÉLEVÉ": 15, "MOYEN": 5, "FAIBLE": 2}
        total_pen = sum(penalties.get(f['severity'], 2) for f in findings)
        score = max(0.0, round(100.0 - total_pen, 1))
        
        status = "EXCELLENT" if score >= 85 else "MODÉRÉ" if score >= 60 else "CRITIQUE"
        return score, status
