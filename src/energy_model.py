import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

def generate_energy_dataset(days=45, meters=5, random_seed=42):
    """
    Génère un jeu de données synthétique de consommation d'énergie réseau IoT.
    """
    np.random.seed(random_seed)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    dates = pd.date_range(start=start_date, end=end_date, freq='h')
    
    records = []
    for m_idx in range(1, meters + 1):
        meter_id = f"GRID-BMK-{100 + m_idx}"
        base_kwh = 3.0 + np.random.uniform(0.5, 1.5)
        
        for dt in dates:
            hour = dt.hour
            is_weekend = dt.weekday() >= 5
            daily_pattern = np.sin((hour - 6) * np.pi / 12) if 6 <= hour <= 23 else -0.4
            kwh = max(0.2, base_kwh + daily_pattern * 1.8 + np.random.normal(0, 0.3)) * (1.2 if is_weekend else 1.0)
            voltage = 230.0 + np.random.normal(0, 3.0)
            power_factor = np.clip(np.random.normal(0.92, 0.03), 0.75, 0.99)
            current = (kwh * 1000) / (voltage * power_factor)
            
            is_anomaly = False
            if np.random.rand() < 0.04:
                is_anomaly = True
                if np.random.rand() < 0.5:
                    kwh = np.random.uniform(0.0, 0.1)
                else:
                    kwh = kwh * np.random.uniform(3.5, 5.5)
                current = (kwh * 1000) / (voltage * power_factor)
                
            records.append({
                'timestamp': dt.strftime("%Y-%m-%d %H:%M:%S"),
                'meter_id': meter_id,
                'consumption_kwh': round(float(kwh), 3),
                'voltage_v': round(float(voltage), 2),
                'current_a': round(float(current), 2),
                'power_factor': round(float(power_factor), 3),
                'is_anomaly_truth': int(is_anomaly)
            })
            
    return pd.DataFrame(records)

class SmartEnergyModel:
    """
    Modèle ML de détection d'anomalies de réseau électrique (Isolation Forest).
    """
    def __init__(self, contamination=0.04, random_state=42):
        self.model = IsolationForest(contamination=contamination, random_state=random_state, n_estimators=100)
        self.scaler = StandardScaler()
        self.feature_cols = ['consumption_kwh', 'voltage_v', 'current_a', 'power_factor', 'rolling_kwh', 'hour_of_day']
        
    def fit_predict(self, df):
        data = df.copy()
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        data['hour_of_day'] = data['timestamp'].dt.hour
        data['rolling_kwh'] = data.groupby('meter_id')['consumption_kwh'].transform(lambda x: x.rolling(6, min_periods=1).mean())
        
        X = data[self.feature_cols]
        X_scaled = self.scaler.fit_transform(X)
        
        preds = self.model.fit_predict(X_scaled)
        scores = self.model.decision_function(X_scaled)
        
        data['is_detected_anomaly'] = (preds == -1)
        data['anomaly_score'] = np.round(1 - (scores - scores.min()) / (scores.max() - scores.min()), 3)
        return data
