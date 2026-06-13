# Data Breach Cost Analyzer

A full-stack data analytics pipeline analyzing cybersecurity breach incidents to identify cost drivers, 
trends, and market impact across industries.

---

## Overview

This project ingests, cleans, and analyzes 850 real-world cybersecurity breach incidents from 2021 to 2025. 
It covers 20 industries and 38 countries, with financial impact and stock market data joined at the incident level. 
The output is a three-page interactive web application built with Streamlit.

---

## Stack

Python, Pandas, NumPy, Scikit-learn, XGBoost, Plotly, Streamlit

---

## Dataset

Source: [Kaggle — Cyber Security Dataset](https://www.kaggle.com/datasets/algozee/cyber-security)

Three tables joined on `incident_id`:

- `incidents_master` — company profile, attack vector, downtime, records compromised
- `financial_impact` — direct loss, ransom, recovery cost, legal fees, regulatory fines, total loss
- `market_impact` — stock prices before and after disclosure, abnormal returns, cumulative abnormal returns (CAR), days to price recovery

---

## Application Pages

**EDA Report**
Automated dataset overview including distributions, missing value analysis, descriptive statistics,
and per-column histograms and box plots.

**Dashboard**
Seven interactive Plotly charts with sidebar filters by year, industry, and attack vector:
- Breach incidents by industry
- Average breach cost by industry
- Attack vector frequency vs average cost
- Breach trends 2021 to 2025
- Breach cost distribution (raw and log-transformed)
- Stock price timeline around breach disclosure
- Company size vs breach cost scatter

**Cost Estimator**
Regression-based scenario simulator. User inputs organizational characteristics 
(industry, revenue, employee count, attack vector, records compromised, downtime) and 
receives a predicted breach cost with confidence range and comparable historical incidents.

---

## Key Findings

- Average breach cost: $71M. Maximum: $3.4B. Median: $16.5M — distribution is heavily right-skewed (skewness 9.18).
- Breach frequency increased 67% from 2021 to 2025.
- Frequency does not equal severity: Finance and Insurance has the most incidents;
- Public Administration as the highest average cost per incident.
- Ransomware is the most common attack vector.
- Backdoor and supply chain attacks cost the most per incident on average.
- Stock prices begin declining before the official disclosure date and bottom out one day after disclosure — consistent with event study methodology in academic finance literature.
- Pre-breach organizational characteristics explain limited variance in breach cost (R² 0.04).
- Breach costs are highly stochastic; response quality, insurance, and jurisdiction are more determinative than company size or attack type.

---

## Project Structure

```
breach-cost-analyzer/
├── data/
│   ├── incidents_master.csv
│   ├── financial_impact.csv
│   ├── market_impact.csv
│   └── processed_data.csv
├── notebooks/
│   ├── 01_data_preparation.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_visualization.ipynb
│   └── 04_model.ipynb
├── pages/
│   ├── 1_EDA_Report.py
│   ├── 2_Dashboard.py
│   └── 3_Cost_Estimator.py
├── src/
│   └── visualizations.py
├── app.py
├── setup.py
└── requirements.txt
```

---

## Running Locally

```bash
git clone https://github.com/deeps-17/Breach-cost-analyzer.git
cd Breach-cost-analyzer
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

---

## Limitations

The regression model uses only pre-breach organizational characteristics as features to avoid data leakage. 
Post-breach costs such as legal fees and recovery costs are excluded from model inputs. 
As a result, predictive accuracy is limited —
this is an honest reflection of the inherent unpredictability of breach costs rather than a modeling deficiency.
