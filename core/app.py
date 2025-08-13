# Main Streamlit app configuration
import streamlit as st
from config.settings import PAGE_CONFIG

def setup_page():
    """Configure Streamlit page settings"""
    st.set_page_config(**PAGE_CONFIG)

def inject_custom_css():
    """Inject custom CSS styling with new saffron, blue, green, sky blue theme"""
    st.markdown("""
    <style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main Background */
    .main .block-container {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #334155 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #FF6B35 0%, #FF8E53 50%, #FFA726 100%);
        border-right: 3px solid #3B82F6;
    }
    
    .css-1d391kg .sidebar-content {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem;
    }
    
    /* Headers */
    h1 {
        background: linear-gradient(90deg, #FF6B35, #3B82F6, #10B981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    h2 {
        color: #60A5FA !important;
        font-weight: 600;
        border-left: 4px solid #FF6B35;
        padding-left: 1rem;
        margin: 1.5rem 0 1rem 0;
    }
    
    h3 {
        color: #34D399 !important;
        font-weight: 500;
        margin: 1rem 0;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        margin: 0.5rem 0;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        border-radius: 10px;
        border: 2px solid #34D399;
    }
    
    .stSelectbox > div > div:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        transform: scale(1.02);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #60A5FA 0%, #3B82F6 100%);
        border-radius: 10px;
        color: white;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #FF6B35 0%, #FF8E53 100%);
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(255, 107, 53, 0.4);
    }
    
    /* Metrics */
    .stMetric {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%);
        border-radius: 15px;
        padding: 1.5rem;
        border: 2px solid rgba(59, 130, 246, 0.3);
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.2);
    }
    
    .stMetric > div > div > div {
        color: #60A5FA !important;
        font-weight: 600;
        font-size: 1.2rem;
    }
    
    .stMetric > div > div > div:last-child {
        color: #34D399 !important;
        font-weight: 700;
        font-size: 1.5rem;
    }
    
    /* Text Input */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid #60A5FA;
        border-radius: 10px;
        color: white;
        padding: 0.75rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #FF6B35;
        box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.2);
    }
    
    /* File Uploader */
    .stFileUploader > div {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%);
        border: 2px dashed #34D399;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div:hover {
        border-color: #FF6B35;
        background: linear-gradient(135deg, rgba(255, 107, 53, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%);
    }
    
    /* Alerts and Notifications */
    .stAlert {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%);
        border: 2px solid #60A5FA;
        border-radius: 12px;
        color: #E0E7FF;
        font-weight: 500;
    }
    
    /* Success Alert */
    .stAlert[data-baseweb="alert"] {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(34, 197, 94, 0.1) 100%);
        border-color: #34D399;
        color: #D1FAE5;
    }
    
    /* Error Alert */
    .stAlert[data-baseweb="alert"][data-severity="error"] {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.1) 100%);
        border-color: #F87171;
        color: #FEE2E2;
    }
    
    /* Code Blocks */
    .stCodeBlock {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        border: 2px solid #60A5FA;
        border-radius: 12px;
        padding: 1rem;
    }
    
    /* Sidebar Navigation */
    .css-1d391kg .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #FF6B35, #3B82F6);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #FF8E53, #60A5FA);
    }
    
    /* Animation for elements */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .main .block-container {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Custom Card Style */
    .custom-card {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%);
        border: 2px solid rgba(59, 130, 246, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(59, 130, 246, 0.2);
        border-color: #FF6B35;
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    
    .status-online {
        background: #10B981;
    }
    
    .status-busy {
        background: #F59E0B;
    }
    
    .status-offline {
        background: #EF4444;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        
        h1 {
            font-size: 2rem;
        }
        
        .stButton > button {
            padding: 0.5rem 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def create_header():
    """Create application header with new design"""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 3rem; padding: 2rem; background: linear-gradient(135deg, rgba(255, 107, 53, 0.1) 0%, rgba(59, 130, 246, 0.1) 50%, rgba(16, 185, 129, 0.1) 100%); border-radius: 20px; border: 2px solid rgba(255, 107, 53, 0.3);">
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
            <span style="font-size: 3rem; margin-right: 1rem;">🚀</span>
            <div>
                <h1 style="margin: 0; background: linear-gradient(90deg, #FF6B35, #3B82F6, #10B981); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 2.8rem; font-weight: 700;">MyMenuBase</h1>
                <p style="margin: 0.5rem 0 0 0; color: #60A5FA; font-size: 1.3rem; font-weight: 500;">Advanced Development & Automation Suite</p>
            </div>
        </div>
        <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1.5rem;">
            <span style="display: flex; align-items: center; color: #34D399; font-weight: 500;">
                <span class="status-indicator status-online"></span>System Online
            </span>
            <span style="display: flex; align-items: center; color: #60A5FA; font-weight: 500;">
                <span class="status-indicator status-online"></span>All Services Active
            </span>
            <span style="display: flex; align-items: center; color: #FF6B35; font-weight: 500;">
                <span class="status-indicator status-online"></span>Ready to Deploy
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_metrics():
    """Create dashboard metrics with new design"""
    st.markdown("""
    <div style="margin: 2rem 0;">
        <h2 style="text-align: center; margin-bottom: 2rem;">📊 System Overview</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="custom-card" style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔧</div>
            <div style="color: #60A5FA; font-weight: 600; font-size: 1.2rem;">Linux Tools</div>
            <div style="color: #34D399; font-weight: 700; font-size: 1.5rem;">50+</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="custom-card" style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🐍</div>
            <div style="color: #60A5FA; font-weight: 600; font-size: 1.2rem;">Python Tools</div>
            <div style="color: #34D399; font-weight: 700; font-size: 1.5rem;">30+</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="custom-card" style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🤖</div>
            <div style="color: #60A5FA; font-weight: 600; font-size: 1.2rem;">ML Tools</div>
            <div style="color: #34D399; font-weight: 700; font-size: 1.5rem;">8+</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="custom-card" style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🐳</div>
            <div style="color: #60A5FA; font-weight: 600; font-size: 1.2rem;">DevOps Tools</div>
            <div style="color: #34D399; font-weight: 700; font-size: 1.5rem;">15+</div>
        </div>
        """, unsafe_allow_html=True)

def create_sidebar():
    """Create sidebar branding and navigation with new design"""
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, rgba(255, 107, 53, 0.2) 0%, rgba(59, 130, 246, 0.2) 100%); border-radius: 15px; margin-bottom: 2rem;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">⚡</div>
        <h3 style="margin: 0; color: #FF6B35; font-weight: 700;">MyMenuBase</h3>
        <p style="margin: 0.5rem 0 0 0; color: #60A5FA; font-size: 0.9rem;">Powerful Development Suite</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("""
    <div style="background: rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 1rem; margin-bottom: 1rem;">
        <h4 style="color: #34D399; margin-bottom: 1rem;">🚀 Quick Access</h4>
        <ul style="color: #E0E7FF; padding-left: 1.5rem;">
            <li>Linux Tools</li>
            <li>Python Utilities</li>
            <li>Machine Learning</li>
            <li>DevOps Tools</li>
            <li>Projects</li>
                            <li>Java Script</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def initialize_app():
    """Initialize the Streamlit application"""
    setup_page()
    inject_custom_css()
    create_header()
    create_metrics()
    create_sidebar()
