import streamlit as st
import pandas as pd
import sys
sys.path.append('.')
from src.visualizations import (
    plot_incidents_by_industry, plot_cost_by_industry,
    plot_attack_vector_comparison, plot_yearly_trends,
    plot_cost_distribution, plot_stock_price_timeline,
    plot_cost_by_company_size
)

st.set_page_config(page_title="Dashboard", page_icon="📈", layout="wide")
st.title("📈 Breach Analytics Dashboard")
st.markdown("---")

@st.cache_data
def load_data():
    return pd.read_csv('data/processed_data.csv')

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
years = sorted(df['incident_year'].dropna().unique().astype(int).tolist())
selected_years = st.sidebar.multiselect("Year", years, default=years)

industries = sorted(df['industry_name'].dropna().unique().tolist())
selected_industries = st.sidebar.multiselect("Industry", industries, default=industries)

attack_vectors = sorted(df['attack_vector_primary'].dropna().unique().tolist())
selected_attacks = st.sidebar.multiselect("Attack Vector", attack_vectors, default=attack_vectors)

# Apply filters
filtered = df[
    (df['incident_year'].isin(selected_years)) &
    (df['industry_name'].isin(selected_industries)) &
    (df['attack_vector_primary'].isin(selected_attacks))
]

st.caption(f"Showing {len(filtered)} of {len(df)} incidents based on filters")
st.markdown("---")

# Charts
st.subheader("Incidents by Industry")
st.plotly_chart(plot_incidents_by_industry(filtered), use_container_width=True)

st.markdown("---")

st.subheader("Average Breach Cost by Industry")
st.plotly_chart(plot_cost_by_industry(filtered), use_container_width=True)

st.markdown("---")

st.subheader("Attack Vectors: Frequency vs Cost")
st.plotly_chart(plot_attack_vector_comparison(filtered), use_container_width=True)

st.markdown("---")

st.subheader("Breach Trends Over Time")
st.plotly_chart(plot_yearly_trends(filtered), use_container_width=True)

st.markdown("---")

st.subheader("Breach Cost Distribution")
st.plotly_chart(plot_cost_distribution(filtered), use_container_width=True)

st.markdown("---")

st.subheader("Stock Price Around Breach Disclosure")
st.plotly_chart(plot_stock_price_timeline(filtered), use_container_width=True)

st.markdown("---")

st.subheader("Company Size vs Breach Cost")
st.plotly_chart(plot_cost_by_company_size(filtered), use_container_width=True)