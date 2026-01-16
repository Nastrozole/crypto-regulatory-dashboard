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
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    .stProgress > div > div > div > div {
        background-image: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
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
            },
            'ADA': {
                'name': 'Cardano', 'symbol': 'ADA', 'type': 'Utility Token',
                'market_cap': 18000000000, 'price': 0.52,
                'jurisdictions': ['Global'], 'mica_status': 'Exempt',
                'sec_status': 'Not a Security', 'risk_score': 28.7,
                'regulatory_status': 'Compliant',
                'last_audit': '2023-11-30', 'compliance_score': 88
            },
            'SOL': {
                'name': 'Solana', 'symbol': 'SOL', 'type': 'Utility Token',
                'market_cap': 42000000000, 'price': 95.50,
                'jurisdictions': ['Global'], 'mica_status': 'Pending',
                'sec_status': 'Under Review', 'risk_score': 38.9,
                'regulatory_status': 'Medium Risk',
                'last_audit': '2024-01-08', 'compliance_score': 79
            },
            'XRP': {
                'name': 'Ripple', 'symbol': 'XRP', 'type': 'Payment Token',
                'market_cap': 32000000000, 'price': 0.58,
                'jurisdictions': ['Global'], 'mica_status': 'Pending',
                'sec_status': 'Lawsuit', 'risk_score': 65.3,
                'regulatory_status': 'High Risk',
                'last_audit': '2023-12-15', 'compliance_score': 52
            }
        }
        
        # Regulatory frameworks data
        self.frameworks = {
            'MiCA': {
                'name': 'Markets in Crypto-Assets (MiCA)',
                'jurisdiction': 'European Union',
                'effective_date': '2024-12-30',
                'status': 'Active',
                'risk_level': 'High',
                'description': 'Comprehensive EU regulation for crypto-assets, exchanges, and stablecoins',
                'applicable_to': ['Stablecoins', 'Exchanges', 'Asset Tokens']
            },
            'SEC Framework': {
                'name': 'SEC Digital Asset Framework',
                'jurisdiction': 'United States',
                'effective_date': 'Ongoing',
                'status': 'Enforcement',
                'risk_level': 'Critical',
                'description': 'Application of securities laws to digital assets',
                'applicable_to': ['Security Tokens', 'ICOs', 'DeFi']
            },
            'FATF Travel Rule': {
                'name': 'FATF Travel Rule',
                'jurisdiction': 'Global',
                'effective_date': '2020-06',
                'status': 'Active',
                'risk_level': 'Medium',
                'description': 'AML/CFT requirements for Virtual Asset Service Providers',
                'applicable_to': ['All VASPs', 'Exchanges']
            },
            'DFSA Crypto Rules': {
                'name': 'DFSA Crypto Rules',
                'jurisdiction': 'Dubai',
                'effective_date': '2022-11',
                'status': 'Active',
                'risk_level': 'Medium',
                'description': 'Comprehensive regulatory framework for crypto in DIFC',
                'applicable_to': ['All Crypto Businesses']
            }
        }
        
        # Compliance deadlines
        self.deadlines = [
            {'name': 'MiCA Stablecoin Requirements', 'date': '2024-06-30', 'days_left': 120},
            {'name': 'MiCA Full Implementation', 'date': '2024-12-30', 'days_left': 304},
            {'name': 'SEC Crypto Reporting', 'date': '2024-03-31', 'days_left': 30},
            {'name': 'UK Crypto Advertising Rules', 'date': '2024-01-08', 'days_left': -5},
            {'name': 'Singapore MAS Guidelines', 'date': '2024-09-30', 'days_left': 213}
        ]
        
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
            st.markdown('<p class="sub-header">Real-time monitoring, risk assessment, and compliance tracking across global jurisdictions</p>', unsafe_allow_html=True)
        
        with col2:
            current_date = datetime.now().strftime("%B %d, %Y")
            st.markdown(f"**Last Updated:** {current_date}")
        
        with col3:
            st.markdown("**Data Version:** v2.4.1")
        
        st.markdown("---")
    
    def create_metrics_row(self):
        """Create top metrics row"""
        col1, col2, col3, col4, col5 = st.columns(5)
        
        # Calculate metrics
        total_assets = len(self.assets_data)
        total_market_cap = sum(asset['market_cap'] for asset in self.assets_data.values()) / 1e9
        avg_risk = np.mean([asset['risk_score'] for asset in self.assets_data.values()])
        critical_count = sum(1 for asset in self.assets_data.values() if asset['risk_score'] >= 80)
        compliant_count = sum(1 for asset in self.assets_data.values() if asset['compliance_score'] >= 80)
        
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
        
        with col5:
            st.metric(
                label="Compliant Assets",
                value=compliant_count,
                delta="+3"
            )
    
    def create_risk_distribution_chart(self):
        """Create risk distribution chart"""
        st.subheader("📊 Risk Distribution Across Portfolio")
        
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
            textinfo='percent+label',
            hovertemplate="<b>%{label}</b><br>%{value} assets<br>%{percent}"
        )
        
        fig.update_layout(
            height=400,
            showlegend=False,
            margin=dict(t=0, b=0, l=0, r=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def create_compliance_timeline(self):
        """Create regulatory compliance timeline"""
        st.subheader("📅 Regulatory Compliance Timeline")
        
        # Prepare timeline data
        timeline_data = []
        for deadline in self.deadlines:
            timeline_data.append({
                'Task': deadline['name'],
                'Start': (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'),
                'Finish': deadline['date'],
                'Status': 'Overdue' if deadline['days_left'] < 0 else 'Upcoming',
                'Days Left': abs(deadline['days_left'])
            })
        
        df_timeline = pd.DataFrame(timeline_data)
        
        # Create Gantt chart
        fig = px.timeline(
            df_timeline,
            x_start="Start",
            x_end="Finish",
            y="Task",
            color="Status",
            color_discrete_map={"Overdue": "#dc3545", "Upcoming": "#28a745"},
            hover_data=["Days Left"]
        )
        
        fig.update_layout(
            height=300,
            xaxis_title="",
            yaxis_title="",
            showlegend=True,
            margin=dict(t=30, b=0, l=0, r=0)
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
                'Compliance Score': f"{asset['compliance_score']}%",
                'Last Audit': asset['last_audit']
            })
        
        df = pd.DataFrame(table_data)
        
        # Add color coding for risk level
        def color_risk(val):
            if val == 'Critical':
                return 'background-color: #dc3545; color: white'
            elif val == 'High':
                return 'background-color: #fd7e14; color: white'
            elif val == 'Medium':
                return 'background-color: #ffc107; color: black'
            elif val == 'Low':
                return 'background-color: #28a745; color: white'
            else:
                return 'background-color: #17a2b8; color: white'
        
        styled_df = df.style.applymap(color_risk, subset=['Risk Level'])
        
        # Display table
        st.dataframe(
            styled_df,
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
    
    def create_jurisdiction_analysis(self):
        """Create jurisdiction risk analysis"""
        st.subheader("🌍 Jurisdiction Risk Analysis")
        
        # Jurisdiction data
        jurisdiction_data = {
            'United States': {'risk': 85, 'assets': 15, 'frameworks': 3},
            'European Union': {'risk': 75, 'assets': 12, 'frameworks': 2},
            'United Kingdom': {'risk': 65, 'assets': 8, 'frameworks': 2},
            'Singapore': {'risk': 40, 'assets': 6, 'frameworks': 1},
            'Switzerland': {'risk': 35, 'assets': 4, 'frameworks': 1},
            'Dubai': {'risk': 45, 'assets': 5, 'frameworks': 1},
            'Japan': {'risk': 50, 'assets': 7, 'frameworks': 2},
            'Australia': {'risk': 55, 'assets': 6, 'frameworks': 1}
        }
        
        # Create choropleth-like visualization
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=list(jurisdiction_data.keys()),
            y=[data['risk'] for data in jurisdiction_data.values()],
            name='Regulatory Risk',
            marker_color=['#dc3545' if risk > 70 else '#fd7e14' if risk > 50 else '#ffc107' if risk > 30 else '#28a745' for risk in [data['risk'] for data in jurisdiction_data.values()]],
            text=[f"{data['assets']} assets<br>{data['frameworks']} frameworks" for data in jurisdiction_data.values()],
            textposition='auto',
        ))
        
        fig.update_layout(
            height=400,
            xaxis_title="Jurisdiction",
            yaxis_title="Risk Score",
            showlegend=False,
            margin=dict(t=30, b=0, l=0, r=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def create_asset_detail_view(self, symbol):
        """Create detailed view for a specific asset"""
        asset = self.assets_data[symbol]
        category, color, label = self.get_risk_category(asset['risk_score'])
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader(f"{asset['name']} ({symbol}) - Regulatory Analysis")
            
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
            
            # Risk breakdown
            st.subheader("Risk Factors")
            risk_factors = [
                {'factor': 'Token Classification', 'score': 25, 'weight': 0.3},
                {'factor': 'Jurisdiction Exposure', 'score': 40, 'weight': 0.25},
                {'factor': 'Regulatory Compliance', 'score': 60, 'weight': 0.25},
                {'factor': 'Legal History', 'score': 30, 'weight': 0.2}
            ]
            
            for factor in risk_factors:
                st.write(f"**{factor['factor']}**")
                st.progress(factor['score']/100, text=f"Score: {factor['score']}/100")
        
        with col2:
            st.subheader("Quick Actions")
            
            if st.button("📋 Generate Compliance Report", use_container_width=True):
                st.session_state.show_report = True
            
            if st.button("🔔 Set Alert Threshold", use_container_width=True):
                st.session_state.show_alert = True
            
            if st.button("📤 Export Analysis", use_container_width=True):
                st.session_state.export_data = True
            
            # Regulatory status badges
            st.markdown("### Regulatory Status")
            st.markdown(f"**MiCA:** `{asset['mica_status']}`")
            st.markdown(f"**SEC:** `{asset['sec_status']}`")
            
            # Jurisdiction badges
            st.markdown("### Jurisdictions")
            for jurisdiction in asset['jurisdictions']:
                st.markdown(f"- {jurisdiction}")
        
        # Compliance timeline
        st.subheader("Compliance Timeline")
        timeline_data = pd.DataFrame({
            'Milestone': ['Initial Audit', 'MiCA Assessment', 'SEC Review', 'Next Audit'],
            'Date': ['2023-06-15', '2023-11-30', '2024-01-15', '2024-06-30'],
            'Status': ['Completed', 'In Progress', 'Pending', 'Scheduled']
        })
        
        st.dataframe(timeline_data, use_container_width=True)
    
    def create_regulatory_frameworks_view(self):
        """Create regulatory frameworks overview"""
        st.subheader("📚 Regulatory Frameworks Overview")
        
        # Create framework cards
        cols = st.columns(2)
        
        for idx, (framework_id, framework) in enumerate(self.frameworks.items()):
            with cols[idx % 2]:
                with st.container():
                    st.markdown(f"""
                    <div style="padding: 1rem; border-radius: 10px; border: 1px solid #e0e0e0; margin-bottom: 1rem;">
                        <h4>{framework['name']}</h4>
                        <p><strong>Jurisdiction:</strong> {framework['jurisdiction']}</p>
                        <p><strong>Effective Date:</strong> {framework['effective_date']}</p>
                        <p><strong>Status:</strong> <span class="risk-{framework['risk_level'].lower()}">{framework['status']}</span></p>
                        <p><strong>Applicable to:</strong> {', '.join(framework['applicable_to'])}</p>
                        <p>{framework['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"View Details - {framework['name']}", key=f"btn_{framework_id}"):
                        st.session_state.selected_framework = framework_id
    
    def create_sidebar(self):
        """Create sidebar navigation"""
        with st.sidebar:
            st.markdown("""
            <div style="text-align: center; padding: 1rem;">
                <h2 style="color: white;">🏛️ CryptoReg</h2>
                <p style="color: #e0e0e0;">Regulatory Intelligence Platform</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Navigation
            st.markdown("### 📊 Navigation")
            
            view_options = {
                "dashboard": "📈 Dashboard Overview",
                "assets": "💰 Asset Analysis",
                "jurisdictions": "🌍 Jurisdiction Map",
                "frameworks": "📚 Regulatory Frameworks",
                "alerts": "🔔 Risk Alerts",
                "reports": "📋 Compliance Reports"
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
                format_func=lambda x: f"{self.assets_data[x]['name']} ({x})",
                index=list(self.assets_data.keys()).index(st.session_state.selected_asset)
            )
            
            if selected_asset != st.session_state.selected_asset:
                st.session_state.selected_asset = selected_asset
            
            st.markdown("---")
            
            # Filters
            st.markdown("### 🔧 Filters")
            
            risk_filter = st.multiselect(
                "Risk Level",
                options=['Critical', 'High', 'Medium', 'Low', 'Minimal'],
                default=['Critical', 'High']
            )
            
            jurisdiction_filter = st.multiselect(
                "Jurisdiction",
                options=['EU', 'US', 'UK', 'Singapore', 'Global'],
                default=['EU', 'US']
            )
            
            st.markdown("---")
            
            # Data freshness
            st.markdown("### 📅 Data Freshness")
            last_update = datetime.now().strftime("%Y-%m-%d %H:%M")
            st.markdown(f"**Last Update:** {last_update}")
            st.progress(95, text="95% data complete")
            
            # Quick actions
            if st.button("🔄 Refresh Data", use_container_width=True):
                st.rerun()
            
            if st.button("📤 Export Dashboard", use_container_width=True):
                st.success("Export initiated!")
    
    def create_risk_alerts_view(self):
        """Create risk alerts view"""
        st.subheader("🔔 Active Risk Alerts")
        
        # Alert data
        alerts = [
            {
                'asset': 'USDT',
                'type': 'Regulatory',
                'severity': 'Critical',
                'description': 'MiCA stablecoin restrictions apply from June 2024',
                'date': '2024-01-15',
                'status': 'Active'
            },
            {
                'asset': 'XRP',
                'type': 'Legal',
                'severity': 'High',
                'description': 'SEC lawsuit ongoing - final judgment pending',
                'date': '2024-01-10',
                'status': 'Active'
            },
            {
                'asset': 'All Stablecoins',
                'type': 'Compliance',
                'severity': 'Medium',
                'description': 'New reserve reporting requirements effective March 2024',
                'date': '2024-01-05',
                'status': 'Active'
            },
            {
                'asset': 'ETH',
                'type': 'Classification',
                'severity': 'Medium',
                'description': 'SEC security classification review in progress',
                'date': '2023-12-20',
                'status': 'Monitoring'
            }
        ]
        
        # Display alerts
        for alert in alerts:
            severity_color = {
                'Critical': '#dc3545',
                'High': '#fd7e14',
                'Medium': '#ffc107'
            }.get(alert['severity'], '#6c757d')
            
            with st.container():
                col1, col2, col3 = st.columns([1, 3, 1])
                
                with col1:
                    st.markdown(f"**{alert['asset']}**")
                    st.markdown(f"<span style='color: {severity_color}; font-weight: bold;'>{alert['severity']}</span>", unsafe_allow_html=True)
                
                with col2:
                    st.write(alert['description'])
                    st.caption(f"Raised: {alert['date']}")
                
                with col3:
                    if st.button("Acknowledge", key=f"ack_{alert['asset']}"):
                        st.success(f"Acknowledged alert for {alert['asset']}")
                
                st.markdown("---")
    
    def create_reports_view(self):
        """Create compliance reports view"""
        st.subheader("📋 Compliance Reports")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Available reports
            reports = [
                {'name': 'MiCA Readiness Assessment', 'date': '2024-01-15', 'status': 'Ready'},
                {'name': 'SEC Compliance Review', 'date': '2024-01-10', 'status': 'In Progress'},
                {'name': 'Quarterly Risk Report Q4 2023', 'date': '2023-12-31', 'status': 'Ready'},
                {'name': 'Stablecoin Regulatory Analysis', 'date': '2023-12-15', 'status': 'Ready'},
                {'name': 'Global Jurisdiction Report', 'date': '2023-12-01', 'status': 'Archived'}
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
                        'In Progress': 'warning',
                        'Archived': 'secondary'
                    }.get(report['status'], 'secondary')
                    st.write(f":{status_color}[{report['status']}]")
                
                st.markdown("---")
        
        with col2:
            st.markdown("### Generate New Report")
            
            report_type = st.selectbox(
                "Report Type",
                options=['MiCA Compliance', 'Risk Assessment', 'Regulatory Review', 'Custom']
            )
            
            assets = st.multiselect(
                "Select Assets",
                options=[f"{data['name']} ({sym})" for sym, data in self.assets_data.items()],
                default=[f"{self.assets_data['BTC']['name']} (BTC)", f"{self.assets_data['ETH']['name']} (ETH)"]
            )
            
            timeframe = st.selectbox(
                "Timeframe",
                options=['Last 30 days', 'Last quarter', 'Year to date', 'Custom range']
            )
            
            if st.button("📊 Generate Report", use_container_width=True):
                with st.spinner("Generating report..."):
                    st.success("Report generation initiated!")
                    st.info("You will be notified when the report is ready for download.")
    
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
                self.create_compliance_timeline()
            
            # Bottom row
            col3, col4 = st.columns(2)
            
            with col3:
                self.create_jurisdiction_analysis()
            
            with col4:
                self.create_regulatory_frameworks_view()
        
        elif st.session_state.view_mode == 'assets':
            self.create_asset_detail_view(st.session_state.selected_asset)
        
        elif st.session_state.view_mode == 'jurisdictions':
            self.create_jurisdiction_analysis()
            st.subheader("🌐 Global Regulatory Heatmap")
            
            # Mock heatmap data
            heatmap_data = pd.DataFrame({
                'Country': ['USA', 'Germany', 'UK', 'Singapore', 'Japan', 'Australia', 'Switzerland', 'UAE'],
                'Regulatory Score': [85, 75, 65, 40, 50, 55, 35, 45],
                'Number of Assets': [15, 8, 8, 6, 7, 6, 4, 5]
            })
            
            fig = px.choropleth(
                heatmap_data,
                locations='Country',
                locationmode='country names',
                color='Regulatory Score',
                hover_name='Country',
                hover_data=['Number of Assets'],
                color_continuous_scale='RdYlGn_r',
                title='Global Regulatory Risk Heatmap'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        elif st.session_state.view_mode == 'frameworks':
            self.create_regulatory_frameworks_view()
            
            # Framework comparison
            st.subheader("Framework Comparison")
            
            framework_df = pd.DataFrame([
                {
                    'Framework': 'MiCA',
                    'Scope': 'Comprehensive',
                    'Complexity': 'High',
                    'Enforcement': 'Strict',
                    'Implementation': 'Phased'
                },
                {
                    'Framework': 'SEC',
                    'Scope': 'Securities Focus',
                    'Complexity': 'High',
                    'Enforcement': 'Aggressive',
                    'Implementation': 'Case-by-case'
                },
                {
                    'Framework': 'FATF',
                    'Scope': 'AML/CFT',
                    'Complexity': 'Medium',
                    'Enforcement': 'Global',
                    'Implementation': 'Country-specific'
                }
            ])
            
            st.dataframe(framework_df, use_container_width=True)
        
        elif st.session_state.view_mode == 'alerts':
            self.create_risk_alerts_view()
            
            # Alert statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Active Alerts", 4, delta="+1 this week")
            with col2:
                st.metric("Critical Alerts", 1, delta="0", delta_color="off")
            with col3:
                st.metric("Avg. Response Time", "2.5 days", delta="-0.5 days")
        
        elif st.session_state.view_mode == 'reports':
            self.create_reports_view()
            
            # Report statistics
            st.subheader("📈 Reporting Analytics")
            
            report_stats = pd.DataFrame({
                'Month': ['Oct', 'Nov', 'Dec', 'Jan'],
                'Reports Generated': [12, 15, 18, 8],
                'Avg. Completion Time (days)': [2.1, 1.8, 1.5, 1.2]
            })
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(
                go.Bar(x=report_stats['Month'], y=report_stats['Reports Generated'], name="Reports Generated"),
                secondary_y=False,
            )
            
            fig.add_trace(
                go.Scatter(x=report_stats['Month'], y=report_stats['Avg. Completion Time (days)'], name="Avg. Completion Time", mode='lines+markers'),
                secondary_y=True,
            )
            
            fig.update_layout(
                title="Reporting Volume & Efficiency",
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #6c757d;">
            <p>Crypto Regulatory Intelligence Platform v2.4.1 | Data Sources: MiCA, SEC, FCA, MAS, FINMA | Last Full Refresh: 2024-01-16</p>
            <p>For compliance inquiries: compliance@cryptoreg.ai | Emergency Contact: +1 (555) 123-4567</p>
        </div>
        """, unsafe_allow_html=True)

# Create requirements.txt for deployment
requirements_content = """
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.17.0
python-dateutil>=2.8.2
"""

# Save requirements to file
with open("requirements.txt", "w") as f:
    f.write(requirements_content)

# Create a deployment guide
deployment_guide = """
# Deployment Instructions

## 1. Local Development
```bash
pip install -r requirements.txt
streamlit run crypto_regulatory_dashboard.py

