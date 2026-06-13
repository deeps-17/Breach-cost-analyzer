import os
import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.set_page_config(page_title="Cost Estimator", page_icon="🧮", layout="wide")
st.title("🧮 Breach Cost Estimator")
st.markdown("Input your organization's details to get an estimated breach cost.")
st.markdown("---")

@st.cache_resource
def load_model():
    if not os.path.exists('data/model.pkl'):
        from setup import train_and_save_model
        train_and_save_model()
    with open('data/model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('data/encoders.pkl', 'rb') as f:
        encoders = pickle.load(f)
    return model, encoders

@st.cache_data
def load_data():
    return pd.read_csv('data/processed_data.csv')

model, encoders = load_model()
df = load_data()

# Input form
st.subheader("Organization Details")

col1, col2 = st.columns(2)

with col1:
    industry = st.selectbox("Industry", sorted(df['industry_name'].dropna().unique().tolist()))
    company_revenue = st.number_input("Annual Revenue (USD)", min_value=100000,
                                       max_value=1000000000000, value=50000000, step=1000000)
    employee_count = st.number_input("Employee Count", min_value=1,
                                      max_value=500000, value=500, step=100)
    is_public = st.selectbox("Is the company publicly listed?", ["No", "Yes"])

with col2:
    attack_vector = st.selectbox("Attack Vector", sorted(df['attack_vector_primary'].dropna().unique().tolist()))
    records_compromised = st.number_input("Records Compromised", min_value=0,
                                           max_value=1000000000, value=10000, step=1000)
    downtime_hours = st.number_input("Estimated Downtime (hours)", min_value=0,
                                      max_value=10000, value=48, step=1)

st.markdown("---")

if st.button("Estimate Breach Cost", type="primary"):
    try:
        # Encode inputs
        industry_encoded = encoders['industry'].transform([industry])[0]
        attack_encoded = encoders['attack'].transform([attack_vector])[0]
        is_public_encoded = 1 if is_public == "Yes" else 0

        # Build feature vector with log transforms
        features = np.array([[
            np.log1p(company_revenue),
            np.log1p(employee_count),
            industry_encoded,
            attack_encoded,
            np.log1p(records_compromised),
            np.log1p(downtime_hours),
            is_public_encoded
        ]])

        # Predict and reverse log transform
        log_pred = model.predict(features)[0]
        predicted_cost = np.expm1(log_pred)

        # Show result
        st.success(f"### Estimated Breach Cost: ${predicted_cost:,.0f}")

        col1, col2, col3 = st.columns(3)
        col1.metric("Low Estimate", f"${predicted_cost * 0.5:,.0f}")
        col2.metric("Central Estimate", f"${predicted_cost:,.0f}")
        col3.metric("High Estimate", f"${predicted_cost * 2.0:,.0f}")

        st.markdown("---")
        st.warning("""
        ⚠️ **Important disclaimer:** This estimate is based on historical breach data and 
        organizational characteristics. Actual breach costs vary significantly depending on 
        incident response quality, insurance coverage, legal jurisdiction, and regulatory environment. 
        Use this as a directional estimate for risk planning purposes only.
        """)

        # Show comparable incidents
        st.subheader("Similar Historical Incidents")
        similar = df[
            (df['industry_name'] == industry) &
            (df['attack_vector_primary'] == attack_vector) &
            (df['total_loss_usd'].notna())
        ][['company_name', 'incident_year', 'attack_vector_primary',
           'total_loss_usd', 'downtime_hours']].head(5)

        if len(similar) > 0:
            similar['total_loss_usd'] = similar['total_loss_usd'].apply(lambda x: f"${x:,.0f}")
            st.dataframe(similar, use_container_width=True)
        else:
            st.info("No historical incidents found matching this exact industry and attack vector combination.")

    except Exception as e:
        st.error(f"Prediction error: {e}. Make sure the selected industry and attack vector exist in the training data.")
