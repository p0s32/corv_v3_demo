import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="Corv Prosperity Engine", layout="wide", initial_sidebar_state="collapsed")

# Dark blue & white styling
st.markdown("""
<style>
    .hero { background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%); color: white; padding: 2rem; border-radius: 12px; text-align: center; margin-bottom: 2rem; }
    .metric-card { background: white; border-radius: 8px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    .loss { color: #dc2626; font-size: 1.5rem; font-weight: bold; }
    .gain { color: #059669; font-size: 1.5rem; font-weight: bold; }
    .cta-box { background: linear-gradient(135deg, #1e3a8a, #3b82f6); color: white; padding: 2rem; border-radius: 12px; text-align: center; margin-top: 2rem; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def get_fake_data():
    np.random.seed(42)
    
    # Simulated metrics
    losses = 2_800_000
    opportunities = 6_400_000
    
    # Fake regional revenue
    revenue_data = pd.DataFrame({
        'Region': ['US', 'EU', 'APAC'],
        'Revenue': [8.2, 4.5, 2.1]
    })
    
    # Churn data
    churn_data = pd.DataFrame({
        'Risk Level': ['Low', 'Medium', 'High'],
        'Customers': [3800, 1800, 1400]
    })
    
    return losses, opportunities, revenue_data, churn_data

def main():
    # Header
    st.markdown('<div class="hero"><h1>Corv Prosperity Engine</h1><p>Unlock $6.4M Hidden Revenue for TechRetail Co.</p></div>', unsafe_allow_html=True)
    
    losses, opportunities, revenue_data, churn_data = get_fake_data()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card"><h4>Annual Losses</h4><div class="loss">-$2.8M</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h4>Revenue Opportunities</h4><div class="gain">+$6.4M</div></div>', unsafe_allow_html=True)
    with col3:
        st.metric("Total Revenue", "$14.8M")
    with col4:
        st.metric("Net ROI", "+3.2x")
    
    # Charts
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Revenue by Region")
        fig_rev = px.bar(revenue_data, x='Region', y='Revenue', color='Revenue', color_continuous_scale='Blues')
        fig_rev.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_rev, use_container_width=True)
    
    with col_b:
        st.subheader("Churn Risk Distribution")
        fig_churn = px.pie(churn_data, values='Customers', names='Risk Level', hole=0.4)
        st.plotly_chart(fig_churn, use_container_width=True)
    
    # Simulator
    st.subheader("Impact Simulator")
    slider_val = st.slider("Reduce churn by (%)", 0, 15, 5)
    uplift = int(slider_val * 210_000)  # Fake calc
    st.metric("Projected Uplift", f"${uplift:,}")
    
    # CTA
    st.markdown(f'''
    <div class="cta-box">
        <h2>Ready to Unlock Your $6M+?</h2>
        <p>Full Build: $12K (50% Prototype Credit) | Tier 1: $2K/mo</p>
        <a href="mailto:hello@corv.ai?subject=Build%20Request" target="_blank">
            <button style="background:white;color:#1e3a8a;border:none;padding:12px24px;border-radius:8px;font-weight:bold;cursor:pointer;">
                Schedule Build (10 Spots Left)
            </button>
        </a>
        <p><small>Limited to 10 clients/quarter. 3x ROI Guarantee.</small></p>
    </div>
    ''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
