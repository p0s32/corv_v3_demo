import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# Page config: Mobile-first, wide layout
st.set_page_config(
    page_title="Corv Prosperity Engine - Prototype",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS: Clean, responsive, navy/blue theme
st.markdown("""
<style>
    .hero-header { background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; padding: 2rem 1rem; border-radius: 12px; text-align: center; margin-bottom: 2rem; }
    .hero-title { font-size: 2rem; font-weight: 700; margin: 0 0 0.5rem 0; }
    .hero-subtitle { font-size: 1.1rem; margin: 0 0 1rem 0; }
    .metric-card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center; margin: 0.5rem; }
    .loss-card { border-left: 6px solid #ef4444; }
    .gain-card { border-left: 6px solid #10b981; }
    .quality-gauge { font-size: 2.5rem; font-weight: bold; }
    .tab-header { font-size: 1.3rem; font-weight: 600; }
    .cta-button { background: linear-gradient(135deg, #10b981, #059669); color: white; border: none; padding: 1rem 2rem; border-radius: 12px; font-size: 1.1rem; font-weight: 600; width: 100%; }
    @media (max-width: 768px) { .hero-title { font-size: 1.5rem; } .metric-card { margin: 0.25rem 0; padding: 1rem; } }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def generate_fake_data():
    """Generate realistic dirty/clean e-comm sales data for TechRetail Co."""
    np.random.seed(42)
    n_rows = 10000
    dates = pd.date_range('2023-01-01', periods=n_rows, freq='H')
    
    # Dirty data simulation
    dirty_df = pd.DataFrame({
        'customer_id': np.random.choice(['CUST' + str(i).zfill(5) for i in range(1, 5001)], n_rows),
        'revenue': np.random.normal(150, 50, n_rows).clip(10, 500),
        'churn_risk': np.random.choice([0,1], n_rows, p=[0.78, 0.22]),  # 22% churn
        'inventory_level': np.random.normal(100, 30, n_rows).clip(0, 200),
        'price_premium': np.random.normal(-0.05, 0.1, n_rows).clip(-0.2, 0.2),  # Pricing gaps
        'date': dates,
        'region': np.random.choice(['US', 'EU', 'APAC', np.nan], n_rows, p=[0.4, 0.3, 0.2, 0.1]),  # Missings
    })
    # Introduce duplicates
    dirty_df = pd.concat([dirty_df, dirty_df.sample(2000)]).reset_index(drop=True)
    
    # Clean version (simulate ETL)
    clean_df = dirty_df.drop_duplicates().dropna(subset=['region']).fillna({'region': 'US'})
    clean_df['revenue'] = clean_df['revenue'].round(2)
    
    # Aggregates
    total_rev = dirty_df['revenue'].sum()
    losses = {'churn': 2.8e6, 'inventory': 1.2e6, 'pricing': 0.9e6, 'total': 4.9e6}  # Story numbers
    gains = {'churn_fix': 3.2e6, 'pricing_opt': 1.8e6, 'ops': 0.8e6, 'total': 5.8e6}
    
    return dirty_df, clean_df, losses, gains, total_rev

def data_quality_gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Data Quality Score"},
        delta={'reference': 95},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 70], 'color': "lightgray"},
                {'range': [70, 90], "color": "yellow"},
                {'range': [90, 100], "color": "green"}
            ],
            'threshold': {
                'line': {'color": "red", 'width': 4},
                'thickness': 0.75,
                'value': 85
            }
        }
    ))
    fig.update_layout(height=300, font={'size': 16})
    return fig

def main():
    st.markdown('<div class="hero-header"><h1 class="hero-title">Corv Prosperity Engine</h1><p class="hero-subtitle">Unlock $6.4M Hidden Revenue for TechRetail Co.</p><p>Prototype Analysis: $2.8M Losses Detected | Live Tier 1 Dashboard Preview</p></div>', unsafe_allow_html=True)
    
    dirty_df, clean_df, losses, gains, total_rev = generate_fake_data()
    
    # Simulate processing
    with st.spinner("Processing data streams..."):
        time.sleep(2)
    
    # Hero Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card loss-card">
            <h3>Annual Losses</h3>
            <div style="font-size: 2rem; color: #ef4444;">-${losses['total']:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card gain-card">
            <h3>Opportunities</h3>
            <div style="font-size: 2rem; color: #10b981;">+${gains['total']:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.metric("Total Revenue", f"${total_rev:,.0f}")
    with col4:
        st.metric("Net ROI Potential", "+3.2x")
    
    # Data Quality
    st.subheader("Data Quality Assessment")
    col_q1, col_q2 = st.columns([1, 3])
    with col_q1:
        st.plotly_chart(data_quality_gauge(82), use_container_width=True)
    with col_q2:
        st.write("**Issues Fixed:** 2K duplicates removed | 1.2K missings imputed | Formats standardized.")
        before_after_df = pd.DataFrame({
            'Metric': ['Rows', 'Usable %', 'Accuracy Boost'],
            'Dirty': ['12K', '78%', 'Base'],
            'Clean': ['10K', '98%', '+24%']
        })
        st.dataframe(before_after_df, use_container_width=True)
    
    # Engine Tabs (Core Value)
    tab1, tab2, tab3, tab4 = st.tabs(["Revenue Engine", "Churn Engine", "Cost Engine", "Market Engine"])
    
    with tab1:
        st.subheader("Revenue Predictor")
        fig_rev = px.bar(clean_df.groupby('region')['revenue'].sum().reset_index(), x='region', y='revenue', title="Revenue by Region")
        st.plotly_chart(fig_rev, use_container_width=True)
        st.info("Gap: EU underperforms by 18% – optimize for +$800K.")
    
    with tab2:
        st.subheader("Churn Detector")
        churn_df = clean_df.groupby('customer_id')['churn_risk'].sum().reset_index()
        fig_churn = px.histogram(churn_df, x='churn_risk', title="Churn Risk Distribution (22% High-Risk)")
        st.plotly_chart(fig_churn, use_container_width=True)
        st.warning("Target top 15% cohort: Retain for +$3.2M.")
    
    with tab3:
        st.subheader("Cost Optimizer")
        fig_cost = px.scatter(clean_df, x='inventory_level', y='revenue', title="Inventory Waste Heatmap ($1.2M)")
        st.plotly_chart(fig_cost, use_container_width=True)
        st.info("Overstock alert: Reduce 20% → +$900K margins.")
    
    with tab4:
        st.subheader("Market Sentiment")
        fig_market = px.line(clean_df, x='date', y='price_premium', title="Pricing vs. Market (-5% Gap)")
        st.plotly_chart(fig_market, use_container_width=True)
        st.info("Raise premiums 8%: +$1.8M without volume loss.")
    
    # Interactive Insights
    st.subheader("Action Plan Simulator")
    churn_slider = st.slider("Churn Reduction %", 0, 15, 5)
    uplift = (churn_slider / 100) * 3200000
    st.metric("Projected Revenue Uplift", f"+${uplift:,.0f}", delta=f"{churn_slider}% Churn Cut")
    
    st.markdown("""
    **Prioritized Steps:**
    1. Fix churn (Invest $150K, Payback 3mo, +$3.2M)
    2. Optimize pricing (+$1.8M)
    3. Streamline inventory (+$900K)
    4. ETL Clean (Add-On: +24% Accuracy)
    """)
    
    # Scenario Comparison
    st.subheader("Status Quo vs. Corv Optimized (2025 Projection)")
    proj_df = pd.DataFrame({
        'Scenario': ['Status Quo', 'Corv Optimized'],
        'Revenue': [18e6, 25.4e6],
        'Growth': ['+20%', '+69%']
    })
    fig_proj = px.bar(proj_df, x='Scenario', y='Revenue', text='Revenue', title="1-Year Forecast")
    st.plotly_chart(fig_proj, use_container_width=True)
    
    # AI Analyst Teaser (Tier 1)
    st.subheader("AI Insights (Tier 1+ Full Chat)")
    col_ai1, col_ai2 = st.columns(2)
    if col_ai1.button("Key Losses"):
        st.success("Detected: $2.8M total. Churn #1 culprit (22% rate).")
    if col_ai2.button("Top Fix"):
        st.success("Implement churn interventions: 3mo payback, 21x ROI.")
    
    # CTA
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3a8a, #3b82f6); color: white; padding: 2rem; border-radius: 12px; text-align: center;">
        <h2>Ready to Unlock Your $6M+?</h2>
        <p>Full Build: $12K (50% Prototype Credit). Hourly Tier 1: $2K/mo.</p>
        <button class="cta-button" onclick="window.open('mailto:your@email.com?subject=Corv Full Build', '_blank')">Schedule Build (10 Spots Left)</button>
        <p><small>Limited to 10 clients/quarter. 3x ROI Guarantee.</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
