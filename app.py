import streamlit as st

st.set_page_config(
    page_title="Data Breach Cost Analyzer",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 Data Breach Cost Analyzer")
st.markdown("---")

st.markdown("""
### About this project
This tool analyzes **850 real cybersecurity breach incidents** from 2021–2025 across 
20 industries and 38 countries.

Use the sidebar to navigate between pages:

| Page | What it does |
|------|-------------|
| 📊 EDA Report | Automated data overview — distributions, missing values, correlations |
| 📈 Dashboard | Interactive charts — breach trends, costs by industry and attack vector |
| 🧮 Cost Estimator | Input your organization's details and get a predicted breach cost |

---
### Key findings at a glance
""")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Incidents", "850")
col2.metric("Avg Breach Cost", "$71M")
col3.metric("Max Breach Cost", "$3.4B")
col4.metric("Years Covered", "2021–2025")

st.markdown("---")
st.caption("Dataset: Kaggle Cyber Security Dataset | Built with Python, Pandas, Scikit-learn, Plotly, Streamlit")