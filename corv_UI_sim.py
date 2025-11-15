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
    
    # Monthly trends - FIXED: Ensure exact 12 months
    dates = pd.date_range('2023-07-01', periods=12, freq='M')
    
    # Revenue trend (12 values)
    revenue_trend = [
        1.10,  # Jul 2023
        1.18,  # Aug 2023
        1.15,  # Sep 2023 (quarter-end dip)
        1.25,  # Oct 2023
        1.32,  # Nov 2023
        1.28,  # Dec 2023 (holiday dip)
        1.35,  # Jan 2024
        1.42,  # Feb 2024
        1.48,  # Mar 2024
        1.45,  # Apr 2024 (slight dip)
        1.52,  # May 2024
        1.58   # Jun 2024
    ]
    
    # Churn trend (12 values) - with realistic spikes
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
    
    # Create DataFrame - NOW ALL LISTS ARE EXACTLY 12 ELEMENTS
    trend_data = pd.DataFrame({
        'Month': [d.strftime('%b %Y') for d in dates],
        'Revenue': revenue_trend,
        'Churn': churn_trend
    })
    
    return financials, states_data, churn_segments, products, trend_data

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">Corv Prosperity Engine</h1>
        <p class="subtitle">BrewTech Coffee Co. | Hidden Revenue Analysis | Enterprise Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Live Update Ticker
    st.markdown(f"""
    <div class="update-ticker">
    🕐 Live Analysis | Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | Next Update: {datetime.now() + timedelta(hours=1):%H:%M}
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    financials, states_data, churn_segments, products, trend_data = load_coffee_data()
    
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
    
    # Charts
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown('<div class="chart-header">Revenue Performance by State</div>', unsafe_allow_html=True)
        fig_rev = px.bar(
            states_data,
            x='State',
            y='Revenue',
            color='Growth',
            color_continuous_scale=['red', 'yellow', 'green'],  # Red=negative, Green=positive
            labels={'Revenue': 'Revenue ($M)', 'Growth': 'Growth (%)'},
            text=[f'${v:.1f}M' for v in states_data['Revenue']]
        )
        fig_rev.update_traces(textposition='outside')
        fig_rev.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig_rev, use_container_width=True)
        
        st.markdown('<div class="chart-header">Revenue vs Churn Trends</div>', unsafe_allow_html=True)
        
        fig_trend = px.line(
            trend_data,
            x='Month',
            y=['Revenue', 'Churn'],
            title='Monthly Performance: Revenue Growth vs Customer Churn'
        )
        
        # Add realistic annotations
        fig_trend.add_annotation(x="Aug 2023", y=0.058, text="Summer churn crisis", 
                            showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, 
                            font=dict(color="#dc2626"))
        fig_trend.add_annotation(x="Dec 2023", y=0.051, text="Holiday impact", 
                            showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2,
                            font=dict(color="#ef4444"))
        fig_trend.add_annotation(x="Apr 2024", y=0.036, text="Best retention month", 
                            showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2,
                            font=dict(color="#059669"))
        
        fig_trend.update_layout(height=300)
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col_right:
        st.markdown('<div class="chart-header">Churn Risk Analysis</div>', unsafe_allow_html=True)
        
        # Explain segments first
        st.markdown('<div class="segment-help">', unsafe_allow_html=True)
        st.write("**Customer Segments Explained:**")
        for _, row in churn_segments.iterrows():
            with st.expander(f"{row['Segment']}"):
                st.write(f"**Customers:** {row['Customers']:,}")
                st.write(f"**Churn Rate:** {row['Churn_Rate']}%")
                st.write(f"**Annual Impact:** ${row['Impact']:,}")
                st.write(f"**Profile:** {row['Description']}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Churn pie chart
        fig_churn = px.pie(
            churn_segments,
            values='Customers',
            names='Segment',
            hole=0.4,
            color_discrete_sequence=['#1e3a8a', '#3b82f6', '#60a5fa']
        )
        fig_churn.update_traces(textposition='inside', textinfo='percent+label')
        fig_churn.update_layout(height=350)
        st.plotly_chart(fig_churn, use_container_width=True)
        
        st.markdown('<div class="chart-header">Data Quality Score</div>', unsafe_allow_html=True)
        quality_score = 79
        st.metric("Quality Score", f"{quality_score}%")
        st.progress(quality_score / 100)
        st.caption("21% improvement potential after data cleanup")
    
    # Product Analysis
    st.markdown('<h3 style="color: #0f172a; margin: 2rem 0 1rem 0;">Product Line Profitability</h3>', unsafe_allow_html=True)
    
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        st.markdown('<div class="chart-header">Profit Margins by Product</div>', unsafe_allow_html=True)
        fig_margin = px.bar(
            products,
            x='Product',
            y='Margin',
            title='Gross Margins Across Product Lines',
            color='Margin',
            color_continuous_scale=['red', 'orange', 'green'],
            text=[f'{v}%' for v in products['Margin']]
        )
        fig_margin.update_traces(textposition='outside')
        fig_margin.update_layout(height=350, coloraxis_showscale=False, xaxis_tickangle=-45)
        st.plotly_chart(fig_margin, use_container_width=True)
        
        # Product explanations
        st.markdown("**Product Context:**")
        for _, row in products.iterrows():
            st.write(f"**{row['Product']}:** {row['Description']}")
    
    with col_p2:
        st.markdown('<div class="chart-header">Revenue Distribution</div>', unsafe_allow_html=True)
        fig_rev_prod = px.pie(
            products,
            values='Revenue',
            names='Product',
            title='Revenue Share by Product Line',
            color_discrete_sequence=['#1e3a8a', '#3b82f6', '#60a5fa', '#93c5fd']
        )
        fig_rev_prod.update_layout(height=350)
        st.plotly_chart(fig_rev_prod, use_container_width=True)
    
    # Insights
    st.markdown('<h3 style="color: #0f172a; margin: 2rem 0 1rem 0;">Key Insights</h3>', unsafe_allow_html=True)
    
    col_i1, col_i2 = st.columns(2)
    
    with col_i1:
        st.markdown("""
        <div class="insight-box">
            <strong>Revenue Leakage:</strong><br>
            • Texas showing -3.2% growth (underperforming market)<br>
            • SMB churn at 24.7% costing $1.27M annually<br>
            • Pod subscription renewal process needs automation
        </div>
        """, unsafe_allow_html=True)
    
    with col_i2:
        st.markdown("""
        <div class="insight-box">
            <strong>Growth Opportunities:</strong><br>
            • Pod subscriptions have 68% margin (scale this!)<br>
            • West Coast expansion potential (+15% in WA, CA)<br>
            • Enterprise machine sales pipeline needs investment
        </div>
        """, unsafe_allow_html=True)
    
    # Action Plan Simulator
    st.markdown('<h3 style="color: #0f172a; margin: 2rem 0 1rem 0;">Action Plan Simulator</h3>', unsafe_allow_html=True)
    
    col_s1, col_s2 = st.columns(2)
    
    with col_s1:
        churn_reduction = st.slider(
            "Reduce SMB Churn Rate (%)",
            min_value=0.0,
            max_value=12.0,
            value=4.0,
            step=0.5,
            help="Target high-churn segment with automated renewals"
        )
        churn_uplift = int(churn_reduction * 105_000)  # Coffee-specific multiplier
        st.metric(
            "Projected Annual Uplift",
            f"${churn_uplift:,}",
            delta=f"{churn_reduction}% churn reduction"
        )
    
    with col_s2:
        subscription_increase = st.slider(
            "Increase Pod Subscription Rate (%)",
            min_value=0.0,
            max_value=15.0,
            value=6.0,
            step=0.5,
            help="Upsell existing customers to higher-tier subscriptions"
        )
        sub_uplift = int(subscription_increase * 32_000)
        st.metric(
            "Subscription Revenue Boost",
            f"${sub_uplift:,}",
            delta=f"{subscription_increase}% expansion"
        )
    
    # CTA Section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0f172a, #1e3a8a); color: white; padding: 2rem; border-radius: 10px; text-align: center; margin: 2rem 0;">
        <h2 style="margin: 0 0 1rem 0;">Ready to Unlock Your $5.2M Coffee Opportunity?</h2>
        <p style="margin: 0 0 1.5rem 0; opacity: 0.9;">
            Full System: $12,000 (50% prototype credit) | Tier 1: $2,000/month<br>
            Hourly updates • AI predictions • Action plans • ROI guarantee
        </p>
        <a href="mailto:hello@corv.ai?subject=BrewTech%20Build%20Request" style="text-decoration: none;">
            <button style="background: white; color: #1e3a8a; border: none; padding: 12px 32px; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 1rem;">
                Schedule Implementation
            </button>
        </a>
        <p style="margin: 1.5rem 0 0 0;"><small>Limited to 10 clients per quarter. 3x ROI guarantee.</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

