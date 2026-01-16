"""
Crypto Regulatory Intelligence Dashboard
Professional regulatory monitoring system with real-time insights
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Crypto Regulatory Intelligence Platform",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        color: #6c757d;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
    }
    .risk-critical { background-color: #dc3545; color: white; padding: 4px 12px; border-radius: 20px; }
    .risk-high { background-color: #fd7e14; color: white; padding: 4px 12px; border-radius: 20px; }
    .risk-medium { background-color: #ffc107; color: #212529; padding: 4px 12px; border-radius: 20px; }
    .risk-low { background-color: #28a745; color: white; padding: 4px 12px; border-radius: 20px; }
    .risk-minimal { background-color: #17a2b8; color: white; padding: 4px 12px; border-radius: 20px; }
</style>
""", unsafe_allow_html=True)

class CryptoRegulatoryDashboard:
    def __init__(self):
        self.load_data()
        self.initialize_session_state()
    
    def load_data(self):
        """Load sample data with realistic regulatory information"""
        self.assets_data = {
            'BTC': {
                'name': 'Bitcoin', 'symbol': 'BTC', 'type': 'Payment Token',
                'market_cap': 850000000000, 'price': 43000,
                'jurisdictions': ['Global'], 'mica_status': 'Exempt',
                'sec_status': 'Not a Security', 'risk_score': 18.5,
                'regulatory_status': 'Compliant',
                'last_audit': '2024-01-15', 'compliance_score': 92
            },
            'ETH': {
                'name': 'Ethereum', 'symbol': 'ETH', 'type': 'Utility Token',
                'market_cap': 350000000000, 'price': 2900,
                'jurisdictions': ['Global'], 'mica_status': 'Pending',
                'sec_status': 'Under Review', 'risk_score': 35.2,
                'regulatory_status': 'Compliant',
                'last_audit': '2024-01-10', 'compliance_score': 85
            },
            'USDT': {
                'name': 'Tether', 'symbol': 'USDT', 'type': 'Stablecoin',
                'market_cap': 95000000000, 'price': 1.00,
                'jurisdictions': ['EU', 'US'], 'mica_status': 'Restricted',
                'sec_status': 'Investigation', 'risk_score': 78.4,
                'regulatory_status': 'High Risk',
                'last_audit': '2023-12-20', 'compliance_score': 45
            },
            'BNB': {
                'name': 'BNB', 'symbol': 'BNB', 'type': 'Exchange Token',
                'market_cap': 65000000000, 'price': 420,
                'jurisdictions': ['Singapore', 'EU'], 'mica_status': 'Pending',
                'sec_status': 'Not Listed', 'risk_score': 42.8,
                'regulatory_status': 'Medium Risk',
                'last_audit': '2024-01-05', 'compliance_score': 72
            },
            'USDC': {
                'name': 'USD Coin', 'symbol': 'USDC', 'type': 'Stablecoin',
                'market_cap': 32000000000, 'price': 1.00,
                'jurisdictions': ['US', 'EU'], 'mica_status': 'Compliant',
                'sec_status': 'Registered', 'risk_score': 25.1,
                'regulatory_status': 'Compliant',
                'last_audit': '2024-01-12', 'compliance_score': 94
            }
        }
        
        # Risk categories
        self.risk_categories = {
            'CRITICAL': {'min': 80, 'color': '#dc3545', 'label': 'Critical'},
            'HIGH': {'min': 60, 'color': '#fd7e14', 'label': 'High'},
            'MEDIUM': {'min': 40, 'color': '#ffc107', 'label': 'Medium'},
            'LOW': {'min': 20, 'color': '#28a745', 'label': 'Low'},
            'MINIMAL': {'min': 0, 'color': '#17a2b8', 'label': 'Minimal'}
        }
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'selected_asset' not in st.session_state:
            st.session_state.selected_asset = 'BTC'
        if 'view_mode' not in st.session_state:
            st.session_state.view_mode = 'dashboard'
    
    def get_risk_category(self, score):
        """Get risk category from score"""
        for category, info in self.risk_categories.items():
            if score >= info['min']:
                return category, info['color'], info['label']
        return 'MINIMAL', '#17a2b8', 'Minimal'
    
    def create_header(self):
        """Create dashboard header"""
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown('<h1 class="main-header">🏛️ Crypto Regulatory Intelligence Platform</h1>', unsafe_allow_html=True)
            st.markdown('<p class="sub-header">Real-time monitoring, risk assessment, and compliance tracking</p>', unsafe_allow_html=True)
        
        with col2:
            current_date = datetime.now().strftime("%B %d, %Y")
            st.markdown(f"**Last Updated:** {current_date}")
        
        with col3:
            st.markdown("**Version:** v2.0")
        
        st.markdown("---")
    
    def create_metrics_row(self):
        """Create top metrics row"""
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate metrics
        total_assets = len(self.assets_data)
        total_market_cap = sum(asset['market_cap'] for asset in self.assets_data.values()) / 1e9
        avg_risk = np.mean([asset['risk_score'] for asset in self.assets_data.values()])
        critical_count = sum(1 for asset in self.assets_data.values() if asset['risk_score'] >= 80)
        
        with col1:
            st.metric(
                label="Total Assets",
                value=total_assets,
                delta="+2 this month"
            )
        
        with col2:
            st.metric(
                label="Total Market Cap",
                value=f"${total_market_cap:,.0f}B",
                delta="+12.5%"
            )
        
        with col3:
            st.metric(
                label="Avg. Risk Score",
                value=f"{avg_risk:.1f}",
                delta="-3.2",
                delta_color="inverse"
            )
        
        with col4:
            st.metric(
                label="Critical Risks",
                value=critical_count,
                delta="-1",
                delta_color="inverse"
            )
    
    def create_risk_distribution_chart(self):
        """Create risk distribution chart"""
        st.subheader("📊 Risk Distribution")
        
        # Prepare data
        risk_bins = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0, 'Minimal': 0}
        for asset in self.assets_data.values():
            category, _, label = self.get_risk_category(asset['risk_score'])
            risk_bins[label] += 1
        
        # Create chart
        fig = px.pie(
            values=list(risk_bins.values()),
            names=list(risk_bins.keys()),
            color=list(risk_bins.keys()),
            color_discrete_map={
                'Critical': '#dc3545',
                'High': '#fd7e14',
                'Medium': '#ffc107',
                'Low': '#28a745',
                'Minimal': '#17a2b8'
            },
            hole=0.4
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label'
        )
        
        fig.update_layout(
            height=300,
            showlegend=False,
            margin=dict(t=0, b=0, l=0, r=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def create_assets_table(self):
        """Create interactive assets table"""
        st.subheader("📋 Asset Regulatory Overview")
        
        # Prepare table data
        table_data = []
        for symbol, asset in self.assets_data.items():
            category, color, label = self.get_risk_category(asset['risk_score'])
            
            table_data.append({
                'Symbol': symbol,
                'Name': asset['name'],
                'Type': asset['type'],
                'Market Cap ($B)': f"${asset['market_cap']/1e9:,.1f}",
                'MiCA Status': asset['mica_status'],
                'SEC Status': asset['sec_status'],
                'Risk Score': asset['risk_score'],
                'Risk Level': label,
                'Compliance Score': f"{asset['compliance_score']}%"
            })
        
        df = pd.DataFrame(table_data)
        
        # Display table
        st.dataframe(
            df,
            use_container_width=True,
            column_config={
                "Risk Score": st.column_config.ProgressColumn(
                    "Risk Score",
                    format="%.1f",
                    min_value=0,
                    max_value=100,
                ),
                "Compliance Score": st.column_config.ProgressColumn(
                    "Compliance",
                    format="%s",
                    min_value=0,
                    max_value=100,
                )
            }
        )
    
    def create_sidebar(self):
        """Create sidebar navigation"""
        with st.sidebar:
            st.markdown("""
            <div style="text-align: center; padding: 1rem;">
                <h2 style="color: white;">🏛️ CryptoReg</h2>
                <p style="color: #e0e0e0;">Regulatory Intelligence</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Navigation
            st.markdown("### 📊 Navigation")
            
            view_options = {
                "dashboard": "📈 Dashboard",
                "assets": "💰 Assets",
                "reports": "📋 Reports"
            }
            
            for view_id, view_label in view_options.items():
                if st.button(view_label, key=f"nav_{view_id}", use_container_width=True):
                    st.session_state.view_mode = view_id
            
            st.markdown("---")
            
            # Asset selector
            st.markdown("### 🔍 Quick Select")
            selected_asset = st.selectbox(
                "Select Asset",
                options=list(self.assets_data.keys()),
                format_func=lambda x: f"{self.assets_data[x]['name']} ({x})"
            )
            
            if selected_asset != st.session_state.selected_asset:
                st.session_state.selected_asset = selected_asset
            
            st.markdown("---")
            
            # Quick actions
            if st.button("🔄 Refresh Data", use_container_width=True):
                st.rerun()
    
    def create_asset_detail_view(self, symbol):
        """Create detailed view for a specific asset"""
        asset = self.assets_data[symbol]
        category, color, label = self.get_risk_category(asset['risk_score'])
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader(f"{asset['name']} ({symbol})")
            
            # Key metrics
            cols = st.columns(4)
            with cols[0]:
                st.metric("Risk Score", f"{asset['risk_score']:.1f}", delta_color="inverse")
            
            with cols[1]:
                st.metric("Compliance Score", f"{asset['compliance_score']}%")
            
            with cols[2]:
                st.metric("Market Cap", f"${asset['market_cap']/1e9:,.1f}B")
            
            with cols[3]:
                st.metric("Regulatory Status", asset['regulatory_status'])
        
        with col2:
            st.subheader("Regulatory Status")
            st.markdown(f"**MiCA:** `{asset['mica_status']}`")
            st.markdown(f"**SEC:** `{asset['sec_status']}`")
            
            st.markdown("### Jurisdictions")
            for jurisdiction in asset['jurisdictions']:
                st.markdown(f"- {jurisdiction}")
    
    def create_reports_view(self):
        """Create compliance reports view"""
        st.subheader("📋 Compliance Reports")
        
        # Available reports
        reports = [
            {'name': 'MiCA Readiness Assessment', 'date': '2024-01-15', 'status': 'Ready'},
            {'name': 'SEC Compliance Review', 'date': '2024-01-10', 'status': 'In Progress'},
            {'name': 'Quarterly Risk Report Q4 2023', 'date': '2023-12-31', 'status': 'Ready'},
        ]
        
        for report in reports:
            col_a, col_b, col_c = st.columns([3, 1, 1])
            with col_a:
                st.write(f"**{report['name']}**")
            with col_b:
                st.write(report['date'])
            with col_c:
                status_color = {
                    'Ready': 'success',
                    'In Progress': 'warning'
                }.get(report['status'], 'secondary')
                st.write(f":{status_color}[{report['status']}]")
            
            st.markdown("---")
        
        # Generate new report
        st.markdown("### Generate New Report")
        
        if st.button("📊 Generate MiCA Compliance Report", use_container_width=True):
            st.success("Report generation started!")
    
    def run(self):
        """Run the dashboard"""
        self.create_header()
        
        # Create sidebar
        self.create_sidebar()
        
        # Main content based on view mode
        if st.session_state.view_mode == 'dashboard':
            self.create_metrics_row()
            
            # Create layout with columns
            col1, col2 = st.columns([2, 1])
            
            with col1:
                self.create_assets_table()
            
            with col2:
                self.create_risk_distribution_chart()
            
        elif st.session_state.view_mode == 'assets':
            self.create_asset_detail_view(st.session_state.selected_asset)
        
        elif st.session_state.view_mode == 'reports':
            self.create_reports_view()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #6c757d;">
            <p>Crypto Regulatory Intelligence Platform v2.0 | Last Refresh: 2024-01-16</p>
        </div>
        """, unsafe_allow_html=True)

# Run the dashboard
if __name__ == "__main__":
    dashboard = CryptoRegulatoryDashboard()
    dashboard.run()
