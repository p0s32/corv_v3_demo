\import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# Page config
st.set_page_config(
    page_title="Corv Prosperity Engine",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Premium dark blue & white styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
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
    @media (max-width: 768px) {
        .metric-container { flex-direction: column; }
        .main-title { font-size: 1.5rem; }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_fake_data():
    """Generate realistic fake data for TechRetail Co."""
    np.random.seed(42)
    
    # Core metrics
    financials = {
        'total_revenue': 18_200_000,
        'annual_losses': 2_800_000,
        'revenue_opportunities': 6_400_000,
        'net_roi': 3.2
    }
    
    # Regional performance
    regions = ['North America', 'Europe', 'APAC', 'Latin America']
    revenue_by_region = pd.DataFrame({
        'Region': regions,
        'Revenue': [9.8, 4.2, 2.8, 1.4],
        'Growth': [12.5, 8.3, 19.7, 15.2]
    })
    
    # Churn analysis
    churn_data = pd.DataFrame({
        'Segment': ['Enterprise', 'Mid-Market', 'SMB'],
        'Customers': [145, 890, 3200],
        'Churn_Rate': [4.2, 12.8, 28.6],
        'Impact': [280_000, 1_200_000, 1_320_000]
    })
    
    # Product performance
    products = pd.DataFrame({
        'Product': ['Core Platform', 'Analytics Add-on', 'API Suite', 'Support'],
        'Margin': [68, 82, 75, 45],
        'Revenue': [8.5, 2.1, 1.9, 0.8]
    })
    
    # Monthly trend (last 12 months)
    dates = pd.date_range('2023-07-01', periods=12, freq='M')
    trend_data = pd.DataFrame({
        'Month': [d.strftime('%b %Y') for d in dates],
        'Revenue': [1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3],
        'Churn': [0.045, 0.043, 0.041, 0.040, 0.039, 0.038, 0.037, 0.036, 0.035, 0.034, 0.033, 0.032]
    })
    
    return financials, revenue_by_region, churn_data, products, trend_data

def create_gauge(value, title, min_val=0, max_val=100, color="#1e3a8a"):
    """Create a professional gauge chart."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 14}},
        gauge={
            'axis': {'range': [min_val, max_val]},
            'bar': {'color': color},
            'steps': [
                {'range': [min_val, max_val*0.7], 'color': "f8fafc"},
                {'range': [max_val*0.7, max_val*0.9], 'color': "#fef3c7"},
                {'range': [max_val*0.9, max_val], 'color': "#dcfce7"}
            ],
            'threshold': {
                'line': {'color': "#ef4444", 'width': 3},
                'thickness': 0.75,
                'value': max_val * 0.8
            }
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
    return fig

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">Corv Prosperity Engine</h1>
        <p class="subtitle">TechRetail Co. | Hidden Revenue Analysis | Next Update: 02:15:30</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Live Update Ticker
    next_update = datetime.now() + timedelta(hours=1)
    st.markdown(f"""
    <div class="update-ticker">
    🕐 Live Analysis | Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | Next Update: {next_update.strftime('%H:%M:%S')}
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    financials, revenue_by_region, churn_data, products, trend_data = load_fake_data()
    
    # Key Metrics
    st.markdown('<h3 style="color: #0f172a; margin: 1rem 0;">Financial Impact Overview</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Annual Losses</div>
            <div class="metric-value loss-value">-${financials['annual_losses']:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Revenue Opportunities</div>
            <div class="metric-value gain-value">+${financials['revenue_opportunities']:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Revenue</div>
            <div class="metric-value">${financials['total_revenue']:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Net ROI Potential</div>
            <div class="metric-value">{financials['net_roi']}x</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Two-column layout for charts
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown('<div class="chart-header">Revenue Performance by Region</div>', unsafe_allow_html=True)
        fig_rev = px.bar(
            revenue_by_region,
            x='Region',
            y='Revenue',
            color='Growth',
            color_continuous_scale='Blues',
            labels={'Revenue': 'Revenue ($M)', 'Growth': 'Growth (%)'},
            text=[f'${v:.1f}M' for v in revenue_by_region['Revenue']]
        )
        fig_rev.update_traces(textposition='outside')
        fig_rev.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig_rev, use_container_width=True)
        
        st.markdown('<div class="chart-header">Monthly Trend Analysis</div>', unsafe_allow_html=True)
        fig_trend = px.line(
            trend_data,
            x='Month',
            y=['Revenue', 'Churn'],
            title='Revenue Growth vs Churn Rate (Last 12 Months)'
        )
        fig_trend.update_layout(height=300, yaxis2=dict(overlaying='y', side='right'))
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col_right:
        st.markdown('<div class="chart-header">Churn Risk Analysis</div>', unsafe_allow_html=True)
        fig_churn = px.pie(
            churn_data,
            values='Customers',
            names='Segment',
            hole=0.4,
            color_discrete_sequence=['#1e3a8a', '#3b82f6', '#60a5fa']
        )
        fig_churn.update_traces(textposition='inside', textinfo='percent+label')
        fig_churn.update_layout(height=350)
        st.plotly_chart(fig_churn, use_container_width=True)
        
        st.markdown('<div class="chart-header">Data Quality Score</div>', unsafe_allow_html=True)
        st.plotly_chart(create_gauge(82, "Quality %", 0, 100, "#1e3a8a"), use_container_width=True)
    
    # Product Analysis
    st.markdown('<h3 style="color: #0f172a; margin: 2rem 0 1rem 0;">Product Profitability Analysis</h3>', unsafe_allow_html=True)
    
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        fig_margin = px.bar(
            products,
            x='Product',
            y='Margin',
            title='Profit Margins by Product (%)',
            color='Margin',
            color_continuous_scale='Blues'
        )
        fig_margin.update_layout(height=300, coloraxis_showscale=False)
        st.plotly_chart(fig_margin, use_container_width=True)
    
    with col_p2:
        fig_rev_prod = px.pie(
            products,
            values='Revenue',
            names='Product',
            title='Revenue Distribution by Product',
            color_discrete_sequence=['#1e3a8a', '#3b82f6', '#60a5fa', '#93c5fd']
        )
        fig_rev_prod.update_layout(height=300)
        st.plotly_chart(fig_rev_prod, use_container_width=True)
    
    # Insights
    st.markdown('<h3 style="color: #0f172a; margin: 2rem 0 1rem 0;">Key Insights</h3>', unsafe_allow_html=True)
    
    col_i1, col_i2 = st.columns(2)
    
    with col_i1:
        st.markdown("""
        <div class="insight-box">
            <strong>Revenue Leakage:</strong><br>
            • EU region underperforming by 18% vs potential<br>
            • SMB churn rate at 28.6% costing $1.32M annually<br>
            • Pricing optimization could recover +$1.8M
        </div>
        """, unsafe_allow_html=True)
    
    with col_i2:
        st.markdown("""
        <div class="insight-box">
            <strong>Growth Opportunities:</strong><br>
            • Analytics add-on has 82% margin potential<br>
            • API Suite adoption up 19.7% in APAC<br>
            • Data cleanup could improve accuracy by 24%
        </div>
        """, unsafe_allow_html=True)
    
    # Action Plan Simulator
    st.markdown('<h3 style="color: #0f172a; margin: 2rem 0 1rem 0;">Action Plan Simulator</h3>', unsafe_allow_html=True)
    
    col_s1, col_s2 = st.columns(2)
    
    with col_s1:
        churn_reduction = st.slider(
            "Churn Reduction Target (%)",
            min_value=0.0,
            max_value=15.0,
            value=5.0,
            step=0.5
        )
        churn_uplift = int(churn_reduction * 210_000)
        st.metric(
            "Projected Annual Uplift",
            f"${churn_uplift:,}",
            delta=f"{churn_reduction}% reduction"
        )
    
    with col_s2:
        pricing_increase = st.slider(
            "Pricing Optimization (%)",
            min_value=0.0,
            max_value=12.0,
            value=4.0,
            step=0.5
        )
        price_uplift = int(pricing_increase * 150_000)
        st.metric(
            "Revenue Optimization",
            f"${price_uplift:,}",
            delta=f"{pricing_increase}% adjustment"
        )
    
    # CTA Section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0f172a, #1e3a8a); color: white; padding: 2rem; border-radius: 10px; text-align: center; margin: 2rem 0;">
        <h2 style="margin: 0 0 1rem 0;">Ready to Unlock Your $6.4M Opportunity?</h2>
        <p style="margin: 0 0 1.5rem 0; opacity: 0.9;">
            Full System: $12,000 (50% prototype credit) | Tier 1: $2,000/month<br>
            Hourly updates • AI predictions • Action plans • ROI guarantee
        </p>
        <a href="mailto:hello@corv.ai?subject=Full Build Request" style="text-decoration: none;">
            <button style="background: white; color: #1e3a8a; border: none; padding: 12px 32px; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 1rem;">
                Schedule Implementation
            </button>
        </a>
        <p style="margin: 1.5rem 0 0 0;"><small>Limited to 10 clients per quarter. 3x ROI guarantee.</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
