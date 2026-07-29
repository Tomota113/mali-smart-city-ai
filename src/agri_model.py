import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor

def generate_agri_dataset(days=365, random_seed=42):
    """
    Génère un jeu de données synthétique des cours des denrées agricoles sur les marchés régionaux.
    """
    np.random.seed(random_seed)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    regions = ["Bamako", "Sikasso", "Mopti", "Kayes"]
    products = [
        {"name": "Riz Local (1kg)", "base_price": 520, "mults": {"Bamako": 1.05, "Sikasso": 0.90, "Mopti": 1.00, "Kayes": 1.15}},
        {"name": "Millet (1kg)", "base_price": 360, "mults": {"Bamako": 1.08, "Sikasso": 0.92, "Mopti": 0.95, "Kayes": 1.12}},
        {"name": "Maïs Jaune (1kg)", "base_price": 310, "mults": {"Bamako": 1.04, "Sikasso": 0.85, "Mopti": 1.00, "Kayes": 1.10}},
        {"name": "Oignon Violet (1kg)", "base_price": 620, "mults": {"Bamako": 1.00, "Sikasso": 1.05, "Mopti": 0.90, "Kayes": 1.20}}
    ]
    
    records = []
    for prod in products:
        for reg in regions:
            base_p = prod["base_price"] * prod["mults"].get(reg, 1.0)
            for dt in dates:
                doy = dt.dayofyear
                seasonality = 1.0 + 0.16 * np.sin((doy - 150) * 2 * np.pi / 365)
                noise = np.random.normal(0, 0.03 * base_p)
                price = max(100, round(base_p * seasonality + noise, 1))
                records.append({
                    "date": dt.strftime("%Y-%m-%d"),
                    "product_name": prod["name"],
                    "region": reg,
                    "price_xof_per_kg": price
                })
    return pd.DataFrame(records)

class AgriPriceModel:
    """
    Modèle ML de prévision temporelle des prix des denrées alimentaires.
    """
    def __init__(self, forecast_days=30):
        self.forecast_days = forecast_days
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        
    def forecast_product_region(self, df_subset):
        df_subset['date'] = pd.to_datetime(df_subset['date'])
        df_subset = df_subset.sort_values('date')
        
        df_subset['day_of_year'] = df_subset['date'].dt.dayofyear
        df_subset['month'] = df_subset['date'].dt.month
        df_subset['price_lag_1'] = df_subset['price_xof_per_kg'].shift(1)
        df_subset['price_lag_7'] = df_subset['price_xof_per_kg'].shift(7)
        df_subset['rolling_avg_7'] = df_subset['price_xof_per_kg'].shift(1).rolling(7).mean()
        
        df_feat = df_subset.dropna()
        feature_cols = ['day_of_year', 'month', 'price_lag_1', 'price_lag_7', 'rolling_avg_7']
        
        X = df_feat[feature_cols]
        y = df_feat['price_xof_per_kg']
        self.model.fit(X, y)
        
        last_date = df_subset['date'].max()
        future_dates = [last_date + timedelta(days=i) for i in range(1, self.forecast_days + 1)]
        recent_prices = list(df_subset['price_xof_per_kg'].values)
        future_preds = []
        
        for f_date in future_dates:
            feat_dict = {
                'day_of_year': f_date.dayofyear,
                'month': f_date.month,
                'price_lag_1': recent_prices[-1],
                'price_lag_7': recent_prices[-7] if len(recent_prices) >= 7 else recent_prices[-1],
                'rolling_avg_7': np.mean(recent_prices[-7:])
            }
            X_future = pd.DataFrame([feat_dict])[feature_cols]
            pred = round(float(self.model.predict(X_future)[0]), 1)
            future_preds.append(pred)
            recent_prices.append(pred)
            
        return future_dates, future_preds
