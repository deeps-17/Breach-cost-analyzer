import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import pickle
import os

def train_and_save_model():
    if os.path.exists('data/model.pkl'):
        print("Model already exists, skipping.")
        return

    print("Training model...")
    df = pd.read_csv('data/processed_data.csv')

    features = ['company_revenue_usd', 'employee_count', 'industry_name',
                'attack_vector_primary', 'data_compromised_records',
                'downtime_hours', 'is_public_company']
    target = 'total_loss_usd'

    model_df = df[features + [target]].dropna(subset=[target])
    model_df['company_revenue_usd'] = model_df['company_revenue_usd'].fillna(model_df['company_revenue_usd'].median())
    model_df['employee_count'] = model_df['employee_count'].fillna(model_df['employee_count'].median())
    model_df['data_compromised_records'] = model_df['data_compromised_records'].fillna(model_df['data_compromised_records'].median())
    model_df['downtime_hours'] = model_df['downtime_hours'].fillna(model_df['downtime_hours'].median())

    le_industry = LabelEncoder()
    le_attack = LabelEncoder()
    model_df['industry_encoded'] = le_industry.fit_transform(model_df['industry_name'].astype(str))
    model_df['attack_encoded'] = le_attack.fit_transform(model_df['attack_vector_primary'].astype(str))
    model_df['is_public_encoded'] = model_df['is_public_company'].map(
        {True: 1, False: 0, 'True': 1, 'False': 0}).fillna(0)

    X = model_df[['company_revenue_usd', 'employee_count', 'industry_encoded',
                   'attack_encoded', 'data_compromised_records', 'downtime_hours', 'is_public_encoded']]
    y = np.log1p(model_df[target])

    X_scaled = X.copy()
    X_scaled['company_revenue_usd'] = np.log1p(X['company_revenue_usd'])
    X_scaled['employee_count'] = np.log1p(X['employee_count'])
    X_scaled['data_compromised_records'] = np.log1p(X['data_compromised_records'])
    X_scaled['downtime_hours'] = np.log1p(X['downtime_hours'])

    model = LinearRegression()
    model.fit(X_scaled, y)

    with open('data/model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('data/encoders.pkl', 'wb') as f:
        pickle.dump({'industry': le_industry, 'attack': le_attack}, f)

    print("Model and encoders saved.")

if __name__ == '__main__':
    train_and_save_model()
