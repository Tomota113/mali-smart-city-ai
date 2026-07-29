import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime, timedelta

from src.energy_model import generate_energy_dataset, SmartEnergyModel
from src.agri_model import generate_agri_dataset, AgriPriceModel
from src.security_engine import generate_security_logs_data, SmartCitySecurityEngine

# Configuration Streamlit
st.set_page_config(
    page_title="Mali Smart City AI",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #008751;
        margin-bottom: 0.1rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #64748b;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background-color: #0f172a;
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 5px solid #008751;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .kpi-title {
        font-size: 0.9rem;
        color: #94a3b8;
        font-weight: 600;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #f8fafc;
    }
    .agent-box {
        background-color: #1e293b;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #334155;
        margin-bottom: 0.8rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header Principal
st.markdown('<div class="main-title">🏙️ Mali Smart City AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Plateforme Unifiée de Pilotage Intelligent & Prédictif pour la Ville de Bamako et du Mali</div>', unsafe_allow_html=True)

# Navigation par Onglets Principaux
tab_overview, tab_energy, tab_agri, tab_security = st.tabs([
    "🏙️ Vue d'Ensemble Exécutive",
    "⚡ Module 1 : Smart Energy & Grid",
    "🌾 Module 2 : Agri-Market Price Predictor",
    "🛡️ Module 3 : AI Security & System Health"
])

# Chargement des données
energy_path = "/home/ibrahim-tomota/Documents/code/mali-smart-city-ai/data/energy_data.csv"
agri_path = "/home/ibrahim-tomota/Documents/code/mali-smart-city-ai/data/agri_prices.csv"
sec_path = "/home/ibrahim-tomota/Documents/code/mali-smart-city-ai/data/security_logs.json"

if os.path.exists(energy_path):
    df_energy_raw = pd.read_csv(energy_path)
else:
    df_energy_raw = generate_energy_dataset()

if os.path.exists(agri_path):
    df_agri_raw = pd.read_csv(agri_path)
else:
    df_agri_raw = generate_agri_dataset()

if os.path.exists(sec_path):
    with open(sec_path, 'r') as f:
        sec_findings = json.load(f)
else:
    sec_findings = generate_security_logs_data()

# ---------------------------------------------------------
# TAB OVERVIEW : VUE D'ENSEMBLE
# ---------------------------------------------------------
with tab_overview:
    st.subheader("📊 Tableau de Bord Exécutif Smart City - Bamako")
    
    col_ov1, col_ov2, col_ov3, col_ov4 = st.columns(4)
    
    # Prétraitement rapide
    energy_model = SmartEnergyModel(contamination=0.04)
    df_energy_proc = energy_model.fit_predict(df_energy_raw)
    anom_count = len(df_energy_proc[df_energy_proc['is_detected_anomaly']])
    anom_rate = (anom_count / len(df_energy_proc)) * 100
    
    sec_engine = SmartCitySecurityEngine()
    sec_score, sec_status = sec_engine.evaluate_security_risk(sec_findings)
    
    with col_ov1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">ANOMALIES RÉSEAU ÉNERGIE</div>
                <div class="kpi-value" style="color: #ef4444;">{anom_count} ({anom_rate:.1f}%)</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_ov2:
        avg_agri_price = df_agri_raw['price_xof_per_kg'].tail(100).mean()
        st.markdown(f"""
            <div class="kpi-card" style="border-left-color: #f59e0b;">
                <div class="kpi-title">PRIX MOYEN DENRÉES</div>
                <div class="kpi-value" style="color: #f59e0b;">{avg_agri_price:.0f} FCFA/kg</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_ov3:
        st.markdown(f"""
            <div class="kpi-card" style="border-left-color: #10b981;">
                <div class="kpi-title">INDICE CYBERDÉFENSE</div>
                <div class="kpi-value" style="color: #10b981;">{sec_score} / 100</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_ov4:
        st.markdown(f"""
            <div class="kpi-card" style="border-left-color: #3b82f6;">
                <div class="kpi-title">MODULES ACTIFS</div>
                <div class="kpi-value" style="color: #3b82f6;">3 / 3 OK</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    c_left, c_right = st.columns(2)
    with c_left:
        st.subheader("⚡ Aperçu Consommation Énergétique Réseau")
        fig_ov_energy = px.line(
            df_energy_proc.head(300),
            x='timestamp',
            y='consumption_kwh',
            color='meter_id',
            template="plotly_dark"
        )
        fig_ov_energy.update_layout(height=320, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_ov_energy, use_container_width=True)
        
    with c_right:
        st.subheader("🌾 Tendances des Prix Agricoles (Bamako)")
        df_bmk = df_agri_raw[df_agri_raw['region'] == 'Bamako']
        fig_ov_agri = px.line(
            df_bmk,
            x='date',
            y='price_xof_per_kg',
            color='product_name',
            template="plotly_dark"
        )
        fig_ov_agri.update_layout(height=320, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_ov_agri, use_container_width=True)

# ---------------------------------------------------------
# TAB 1 : MODULE ÉNERGIE & DÉTECTION D'ANOMALIES
# ---------------------------------------------------------
with tab_energy:
    st.subheader("⚡ Smart Energy & Grid Anomaly Detector")
    
    st.sidebar.header("⚙️ Paramètres Énergie")
    meters_list = ["Tous les compteurs"] + sorted(df_energy_proc['meter_id'].unique().tolist())
    selected_meter = st.sidebar.selectbox("Filtrer par Compteur (Énergie) :", meters_list)
    
    if selected_meter != "Tous les compteurs":
        df_e_disp = df_energy_proc[df_energy_proc['meter_id'] == selected_meter].copy()
    else:
        df_e_disp = df_energy_proc.copy()
        
    e_anom = df_e_disp[df_e_disp['is_detected_anomaly']]
    
    st.markdown(f"**Relevés analysés :** {len(df_e_disp):,} | **Anomalies détectées :** {len(e_anom)} ({(len(e_anom)/len(df_e_disp)*100):.2f}%)")
    
    fig_e = go.Figure()
    fig_e.add_trace(go.Scatter(x=df_e_disp['timestamp'], y=df_e_disp['consumption_kwh'], mode='lines', name='Consommation (kWh)', line=dict(color='#0284c7', width=1.5)))
    fig_e.add_trace(go.Scatter(x=e_anom['timestamp'], y=e_anom['consumption_kwh'], mode='markers', name='Anomalie / Suspecte', marker=dict(color='#ef4444', size=8, symbol='x-open')))
    fig_e.update_layout(template="plotly_dark", height=400, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig_e, use_container_width=True)
    
    st.subheader("📋 Journal des Anomalies Électriques")
    st.dataframe(e_anom[['timestamp', 'meter_id', 'consumption_kwh', 'voltage_v', 'current_a', 'anomaly_score']].sort_values('anomaly_score', ascending=False), use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# TAB 2 : MODULE PRIX AGRICOLES
# ---------------------------------------------------------
with tab_agri:
    st.subheader("🌾 Agri-Market Price Predictor")
    
    st.sidebar.header("⚙️ Paramètres Agriculture")
    products = sorted(df_agri_raw['product_name'].unique().tolist())
    regions = sorted(df_agri_raw['region'].unique().tolist())
    
    sel_prod = st.sidebar.selectbox("Denrée Agricole :", products)
    sel_reg = st.sidebar.selectbox("Région :", regions)
    
    df_a_sub = df_agri_raw[(df_agri_raw['product_name'] == sel_prod) & (df_agri_raw['region'] == sel_reg)].copy()
    
    agri_model = AgriPriceModel(forecast_days=30)
    future_dates, future_preds = agri_model.forecast_product_region(df_a_sub)
    
    df_a_sub['date'] = pd.to_datetime(df_a_sub['date'])
    df_future = pd.DataFrame({'date': future_dates, 'price_xof_per_kg': future_preds})
    
    fig_a = go.Figure()
    fig_a.add_trace(go.Scatter(x=df_a_sub['date'], y=df_a_sub['price_xof_per_kg'], mode='lines', name='Historique (FCFA/kg)', line=dict(color='#0284c7', width=2)))
    fig_a.add_trace(go.Scatter(x=df_future['date'], y=df_future['price_xof_per_kg'], mode='lines+markers', name='Prédiction IA 30j', line=dict(color='#10b981', width=2.5, dash='dash')))
    fig_a.update_layout(template="plotly_dark", height=400, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig_a, use_container_width=True)
    
    st.subheader(f"🗺️ Comparatif des Prix pour {sel_prod}")
    df_latest_a = df_agri_raw[df_agri_raw['product_name'] == sel_prod].groupby('region')['price_xof_per_kg'].last().reset_index()
    fig_a_bar = px.bar(df_latest_a, x='region', y='price_xof_per_kg', color='region', text_auto='.1f', template="plotly_dark")
    fig_a_bar.update_layout(height=300, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig_a_bar, use_container_width=True)

# ---------------------------------------------------------
# TAB 3 : MODULE SÉCURITÉ & SANTÉ SYSTÈME
# ---------------------------------------------------------
with tab_security:
    st.subheader("🛡️ AI Security & System Health Orchestrator")
    
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.markdown('<div class="agent-box"><b style="color:#38bdf8;">AGT-RECON-01</b><br>Agent Cartographie DNS<br><span style="color:#34d399;">● MicroVM 101 OK</span></div>', unsafe_allow_html=True)
    with col_s2:
        st.markdown('<div class="agent-box"><b style="color:#38bdf8;">AGT-SCAN-02</b><br>Agent Scanner Web & Fuzzing<br><span style="color:#fca5a5;">● MicroVM 102 (Alerte SQLi)</span></div>', unsafe_allow_html=True)
    with col_s3:
        st.markdown('<div class="agent-box"><b style="color:#38bdf8;">AGT-API-03</b><br>Agent Inspecteur API & JWT<br><span style="color:#fef08a;">● MicroVM 103 (Alerte BOLA)</span></div>', unsafe_allow_html=True)
        
    df_sec = pd.DataFrame(sec_findings)
    st.subheader("🚨 Rapport des Fautes de Sécurité Détectées")
    st.dataframe(df_sec[['finding_id', 'target', 'category', 'severity', 'cvss', 'description']], use_container_width=True, hide_index=True)
