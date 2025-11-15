import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Corv Prosperity Engine",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Clean dark blue & white styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
    }
    .main-title {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
    }
    .subtitle {
        font-size: 1.1rem;
        text-align: center;
        opacity: 0.9;
        margin: 0.5rem 0;
    }
    .metric-container {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
        flex-wrap: wrap;
    }
    .metric-card {
        background: white;
        border-radius: 8px;
        padding: 1.25rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #1e3a8a;
        flex: 1;
        min-width: 200px;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0.25rem 0;
    }
    .loss-value {
        color: #dc2626 !important;
    }
    .gain-value {
        color: #059669 !important;
    }
    .chart-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #0f172a;
        margin: 0.5rem 0;
    }
    .insight-box {
        background: #f8fafc;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
    }
    .update-ticker {
        background: #1e3a8a;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-size: 0.9rem;
        text-align: center;
        margin: 1rem 0;
    }
    .segment-help {
        background: #eff6ff;
        border: 1px solid #dbeafe;
        border-radius: 6px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    @media (max-width: 768px) {
        .metric-container { flex-direction: column; }
        .main-title { font-size: 1.5rem; }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
@st.cache_data
def load_coffee_data():
    """Generate realistic fake data for BrewTech Coffee Co."""
    np.random.seed(42)
    
    financials = {
        'total_revenue': 14_800_000,
        'annual_losses': 2_100_000,
        'revenue_opportunities': 5_200_000,
        'net_roi': 2.8
    }
    
    # US States Performance
    states_data = pd.DataFrame({
        'State': ['California', 'New York', 'Texas', 'Florida', 'Washington', 'Colorado', 'Illinois', 'Massachusetts'],
        'Revenue': [2.1, 1.8, 1.2, 1.1, 0.9, 0.8, 0.7, 0.6],
        'Growth': [8.5, 12.1, -3.2, 6.8, 15.3, 18.7, 2.4, 11.9]
    })
    
    # Customer Segments
    churn_segments = pd.DataFrame({
        'Segment': ['Enterprise (50+ machines)', 'Mid-Market (5-49 machines)', 'SMB (1-4 machines)'],
        'Customers': [89, 342, 1200],
        'Churn_Rate': [3.1, 9.8, 24.7],
        'Impact': [180_000, 650_000, 1_270_000],
        'Description': [
            'Large contracts, low churn, high value',
            'Growing segment, moderate retention risk', 
            'High volume, high churn, subscription dependent'
        ]
    })
    
    # Coffee Product Lines
    products = pd.DataFrame({
        'Product': ['Commercial Espresso Machine', 'Pod Subscription (Monthly)', 'Home Brewer', 'Premium Coffee Pods'],
        'Margin': [45, 68, 35, 52],
        'Revenue': [3.2, 5.1, 1.8, 2.4],
        'Description': [
            'One-time equipment sales ($4K-$12K per unit)',
            'Recurring revenue - 72% of business',
            'Lower-cost home units ($150-$400)',
            'High-margin consumables'
        ]
    })
    
    # Monthly trends - FIXED: Exact 12 months with realistic patterns
    dates = pd.date_range('2023-07-01', periods=12, freq='M')
    
    # Revenue trend (12 values exactly)
    revenue_trend = [
        1.10,  # Jul 2023
        1.18,  # Aug 2023
        1.15,  # Sep 2023
        1.25,  # Oct 2023
        1.32,  # Nov 2023
        1.28,  # Dec 2023
        1.35,  # Jan 2024
        1.42,  # Feb 2024
        1.48,  # Mar 2024
        1.45,  # Apr 2024
        1.52,  # May 2024
        1.58   # Jun 2024
    ]
    
    # Churn trend (12 values exactly) - volatile with clear spike
    churn_trend = [
        0.042,  # Jul 2023 (baseline)
        0.058,  # Aug 2023 (summer spike!)
        0.048,  # Sep 2023 (still elevated)
        0.039,  # Oct 2023 (recovery)
        0.038,  # Nov 2023 (stable)
        0.051,  # Dec 2023 (holiday spike)
        0.042,  # Jan 2024 (recovery)
        0.041,  # Feb 2024 (steady)
        0.044,  # Mar 2024 (small uptick)
        0.036,  # Apr 2024 (best month)
        0.039,  # May 2024 (gradual rise)
        0.043   # Jun 2024 (pre-summer)
    ]
    
    # Create DataFrame - ALL LISTS ARE EXACTLY 12 ELEMENTS
    trend_data = pd.DataFrame({
        'Month': [d.strftime('%b %Y') for d in dates],
        'Revenue': revenue_trend,
        'Churn': churn_trend
    })
    
    return financials, states_data, churn_segments, products, trend_data

