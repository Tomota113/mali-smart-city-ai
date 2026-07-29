# 🏙️ Mali Smart City AI

> **Plateforme Unifiée de Pilotage Intelligent & Prédictif pour la Ville de Bamako et du Mali**  
> *Projet Phare développé pour la Semaine du Numérique au Mali.*

![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Ubuntu Linux](https://img.shields.io/badge/OS-Ubuntu%20Linux-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![License MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Operational%20PoC-008751?style=for-the-badge)

---

## 📌 Présentation & Vision

La transformation numérique des villes africaines passe par une gouvernance basée sur la **donnée en temps réel** et **l'intelligence artificielle prédictive**. 

**Mali Smart City AI** réunit au sein d'une seule architecture applicative haute performance 3 piliers stratégiques de la gestion urbaine et économique au Mali :

1. ⚡ **Smart Energy & Grid Anomaly Detector** : Surveillance IoT du réseau électrique de Bamako, détection par apprentissage non surveillé (*Isolation Forest*) des pertes non-techniques et surcharges.
2. 🌾 **Agri-Market Price Predictor** : Modèle de prévision des prix des denrées alimentaires sur 30 jours (*Random Forest Regressor*) couvrant les régions de Bamako, Sikasso, Mopti et Kayes.
3. 🛡️ **AI Security & System Health Orchestrator** : Console SOC de cyberdéfense simulant l'orchestration d'agents d'audit de sécurité exécutés sous conteneurs isolés (MicroVM Sandboxes).

---

## 🏗️ Architecture Système (Pipeline Global)

```text
  +-----------------------------------------------------------------------+
  |                        SOURCES DE DONNÉES URBAN                      |
  |  [ Capteurs IoT Électricité ]   [ Marchés Agricoles ]   [ Serveurs SOC ]  |
  +-----------------------------------------------------------------------+
                                      |
                                      v
  +-----------------------------------------------------------------------+
  |                     MOTEUR D'INTELLIGENCE ARTIFICIELLE                 |
  |  - Isolation Forest (Détection d'anomalies de consommation)            |
  |  - Random Forest Regressor (Prédiction temporelle des prix)          |
  |  - Scoring de Risque CVSS (Audit de sécurité applicative)             |
  +-----------------------------------------------------------------------+
                                      |
                                      v
  +-----------------------------------------------------------------------+
  |                    CONSOLE COMPOSITE STREAMLIT (UI)                    |
  |  [ Vue Exécutive ]  [ Module Énergie ]  [ Module Agri ]  [ Module SOC ] |
  +-----------------------------------------------------------------------+
                                      |
                                      v
  +-----------------------------------------------------------------------+
  |              DÉCISIONS BUSINESS & POLITIQUES PUBLIQUES                |
  | (Réduction des fraudes, Régulation des prix, Protection des SI)       |
  +-----------------------------------------------------------------------+
```

---

## 📋 Tableau des Fonctionnalités par Module

| Module | Algorithmes ML & Outils | Cas d'Usage Business / Impact Mali |
| :--- | :--- | :--- |
| ⚡ **Smart Energy & Grid** | `Isolation Forest`, `StandardScaler`, `Plotly` | Détection des pertes non-techniques, prévention des surcharges transformateurs et réduction des pertes financières (FCFA). |
| 🌾 **Agri Price Predictor** | `Random Forest Regressor`, `Lagging Features` | Anticiper les périodes de soudure, stabilisation des prix alimentaires et aide à la décision pour les commerçants locaux. |
| 🛡️ **AI Security SOC** | `Score CVSS`, `MicroVM Sandboxes`, `Orchestrator` | Protection continue des infrastructures Web/API gouvernementales et privées contre les cyberattaques. |

---

## 🚀 Guide d'Installation et d'Exécution Rapide (Ubuntu / Linux)

### 1. Cloner le répertoire
```bash
git clone https://github.com/Tomota113/mali-smart-city-ai.git
cd mali-smart-city-ai
```

### 2. Initialiser l'environnement virtuel Python
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Lancer la plateforme Streamlit
```bash
streamlit run app.py
```

L'application s'ouvrira dans votre navigateur à l'adresse : `http://localhost:8501`.

---

## 🇲🇱 Impact pour le Mali & Perspectives

- **Pour les Ministères & Collectivités** : Un outil de pilotage unifié de la ville intelligente pour piloter les infrastructures et la sécurité en un seul coup d'œil.
- **Pour les PME & Startups** : Une démonstration technique concrète prouvant que l'IA peut apporter des réponses opérationnelles aux défis maliens.

---

## 👤 Auteur & Contact

**Ibrahim Tomota**  
*Étudiant en IA & Data Science | Machine Learning & Lead Tech Architect*  
- **GitHub** : [@Tomota113](https://github.com/Tomota113)  
- **LinkedIn** : [Ibrahim Tomota](https://www.linkedin.com/in/ibrahim-tomota-056756330)  
- **Email** : `itomota11@gmail.com`
