import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="EDA Report", page_icon="📊", layout="wide")

st.title("📊 EDA Report")
st.markdown("Automated overview of the breach dataset.")
st.markdown("---")

@st.cache_data
def load_data():
    return pd.read_csv('data/processed_data.csv')

df = load_data()

# Dataset summary
st.subheader("Dataset Summary")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Incidents", len(df))
col2.metric("Industries", df['industry_name'].nunique())
col3.metric("Countries", df['country_hq'].nunique())
col4.metric("Attack Vectors", df['attack_vector_primary'].nunique())

st.markdown("---")

# Data preview
st.subheader("Data Preview")
st.dataframe(df.head(20), use_container_width=True)

st.markdown("---")

# Missing values
st.subheader("Missing Values")
missing = df.isnull().sum()
missing = missing[missing > 0].sort_values(ascending=False).reset_index()
missing.columns = ['Column', 'Missing Count']
missing['Missing %'] = (missing['Missing Count'] / len(df) * 100).round(1)
st.dataframe(missing, use_container_width=True)

st.markdown("---")

# Numeric distributions
st.subheader("Numeric Column Distributions")
numeric_cols = ['total_loss_usd', 'company_revenue_usd', 'employee_count',
                'data_compromised_records', 'downtime_hours']

selected_col = st.selectbox("Select column to explore", numeric_cols)
col_data = df[selected_col].dropna()

col1, col2 = st.columns(2)
with col1:
    fig = px.histogram(col_data, nbins=50, title=f'Distribution: {selected_col}')
    st.plotly_chart(fig, use_container_width=True)
with col2:
    fig2 = px.box(df, y=selected_col, title=f'Box Plot: {selected_col}')
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Descriptive stats
st.subheader("Descriptive Statistics")
st.dataframe(df[numeric_cols].describe().round(2), use_container_width=True)