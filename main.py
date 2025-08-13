# Main application entry point
import streamlit as st
from core.app import initialize_app
from modules.linux.commands import linux_commands_menu, linux_network_tools
from modules.linux.advanced_commands import advanced_linux_commands_menu
from modules.python.communication import communication_menu
from modules.python.file_tools import file_tools_menu
from modules.python.web_tools import web_tools_menu
from modules.python.advanced_tools import advanced_python_tools_menu
from modules.machine_learning.calculators import machine_learning_menu
from modules.projects.utility_tools import utility_projects_menu
from modules.projects.hand_gesture_tools import hand_gesture_projects_menu
from modules.devops.docker_tools import docker_tools_menu
from modules.devops.aws_tools import aws_tools_menu
from modules.javascript.demos import javascript_demos_menu

def main():
    """Main application function"""
    # Initialize the app
    initialize_app()
    
    # Main navigation with enhanced styling
    st.sidebar.markdown("""
    <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%); border-radius: 12px; padding: 1rem; margin-bottom: 1rem;">
        <h4 style="color: #FF6B35; margin-bottom: 1rem; text-align: center;">🧭 Navigation</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Category selection with enhanced styling
    category = st.sidebar.selectbox(
        "Choose Category:",
        ["🏠 Dashboard", "🔧 Linux Tools", "🐍 Python Utilities", "🤖 Machine Learning", "🐳 DevOps Tools", "🚀 Projects", "🟨 Java Script"]
    )
    
    # Main content area
    if category == "🏠 Dashboard":
        show_dashboard()
    elif category == "🔧 Linux Tools":
        show_linux_tools()
    elif category == "🐍 Python Utilities":
        show_python_utilities()
    elif category == "🤖 Machine Learning":
        show_machine_learning()
    elif category == "🐳 DevOps Tools":
        show_devops_tools()
    elif category == "🚀 Projects":
        show_projects()
    elif category == "🟨 Java Script":
        show_javascript_demos()

def show_dashboard():
    """Show the main dashboard with enhanced design"""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="background: linear-gradient(90deg, #FF6B35, #3B82F6, #10B981); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 2.5rem; font-weight: 700;">🏠 Welcome to MyMenuBase</h1>
        <p style="color: #60A5FA; font-size: 1.2rem; margin-top: 0.5rem;">Your Ultimate Development & Automation Toolkit</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards with new design
    st.markdown("""
    <div style="margin: 2rem 0;">
        <h2 style="text-align: center; margin-bottom: 2rem; color: #60A5FA;">🎯 What can you do here?</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards in a grid
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #FF6B35; margin-bottom: 1rem;">🔧 Linux Tools</h3>
            <ul style="color: #E0E7FF; padding-left: 1.5rem;">
                <li>Execute Linux commands</li>
                <li>Monitor system resources</li>
                <li>Manage files and directories</li>
                <li>Network configuration</li>
                <li>Advanced disk management</li>
                <li>LVM and NFS tools</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #3B82F6; margin-bottom: 1rem;">🐍 Python Utilities</h3>
            <ul style="color: #E0E7FF; padding-left: 1.5rem;">
                <li>Send emails and SMS</li>
                <li>Process files (PDF, images)</li>
                <li>Generate QR codes</li>
                <li>Web scraping tools</li>
                <li>Social media automation</li>
                <li>Advanced AI tools</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #10B981; margin-bottom: 1rem;">🤖 Machine Learning</h3>
            <ul style="color: #E0E7FF; padding-left: 1.5rem;">
                <li>EMI calculators</li>
                <li>Salary prediction</li>
                <li>Student performance analysis</li>
                <li>Data visualization</li>
                <li>Prompt engineering</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #FF6B35; margin-bottom: 1rem;">🐳 DevOps Tools</h3>
            <ul style="color: #E0E7FF; padding-left: 1.5rem;">
                <li>Docker management</li>
                <li>AWS EC2 operations</li>
                <li>Infrastructure management</li>
                <li>Container orchestration</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #3B82F6; margin-bottom: 1rem;">🚀 Projects</h3>
            <ul style="color: #E0E7FF; padding-left: 1.5rem;">
                <li>Hand gesture recognition</li>
                <li>Voice analysis tools</li>
                <li>All-in-one utilities</li>
                <li>Advanced file manager</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="custom-card">
            <h3 style="color: #10B981; margin-bottom: 1rem;">🟨 Java Script</h3>
            <ul style="color: #E0E7FF; padding-left: 1.5rem;">
                <li>Interactive calculators</li>
                <li>Web demonstrations</li>
                <li>Frontend tools</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick stats with enhanced design
    st.markdown("""
    <div style="margin: 3rem 0;">
        <h2 style="text-align: center; margin-bottom: 2rem; color: #60A5FA;">📊 Quick Statistics</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats in a grid
    stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
    
    with stats_col1:
        st.markdown("""
        <div class="custom-card" style="text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔧</div>
            <div style="color: #60A5FA; font-weight: 600; font-size: 1.1rem;">Linux Commands</div>
            <div style="color: #34D399; font-weight: 700; font-size: 1.8rem;">50+</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stats_col2:
        st.markdown("""
        <div class="custom-card" style="text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🐍</div>
            <div style="color: #60A5FA; font-weight: 600; font-size: 1.1rem;">Python Tools</div>
            <div style="color: #34D399; font-weight: 700; font-size: 1.8rem;">30+</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stats_col3:
        st.markdown("""
        <div class="custom-card" style="text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🤖</div>
            <div style="color: #60A5FA; font-weight: 600; font-size: 1.1rem;">ML Tools</div>
            <div style="color: #34D399; font-weight: 700; font-size: 1.8rem;">8+</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stats_col4:
        st.markdown("""
        <div class="custom-card" style="text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🐳</div>
            <div style="color: #60A5FA; font-weight: 600; font-size: 1.1rem;">DevOps Tools</div>
            <div style="color: #34D399; font-weight: 700; font-size: 1.8rem;">15+</div>
        </div>
        """, unsafe_allow_html=True)
    
    # System status section
    st.markdown("""
    <div style="margin: 3rem 0;">
        <h2 style="text-align: center; margin-bottom: 2rem; color: #60A5FA;">⚡ System Status</h2>
    </div>
    """, unsafe_allow_html=True)
    
    status_col1, status_col2, status_col3 = st.columns(3)
    
    with status_col1:
        st.markdown("""
        <div class="custom-card" style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🟢</div>
            <div style="color: #60A5FA; font-weight: 600; font-size: 1.1rem;">Server Status</div>
            <div style="color: #34D399; font-weight: 700; font-size: 1.3rem;">Online</div>
        </div>
        """, unsafe_allow_html=True)
    
    with status_col2:
        st.markdown("""
        <div class="custom-card" style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">⚡</div>
            <div style="color: #60A5FA; font-weight: 600; font-size: 1.1rem;">Performance</div>
            <div style="color: #34D399; font-weight: 700; font-size: 1.3rem;">Optimal</div>
        </div>
        """, unsafe_allow_html=True)
    
    with status_col3:
        st.markdown("""
        <div class="custom-card" style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔒</div>
            <div style="color: #60A5FA; font-weight: 600; font-size: 1.1rem;">Security</div>
            <div style="color: #34D399; font-weight: 700; font-size: 1.3rem;">Protected</div>
        </div>
        """, unsafe_allow_html=True)

def show_linux_tools():
    """Show Linux tools section with enhanced styling"""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="background: linear-gradient(90deg, #FF6B35, #3B82F6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 2.5rem; font-weight: 700;">🔧 Linux Tools</h1>
        <p style="color: #60A5FA; font-size: 1.2rem; margin-top: 0.5rem;">Advanced Linux Command Suite & System Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # All Linux tools are now integrated into linux_commands_menu()
    linux_commands_menu()

def show_python_utilities():
    """Show Python utilities section with enhanced styling"""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="background: linear-gradient(90deg, #3B82F6, #10B981); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 2.5rem; font-weight: 700;">🐍 Python Utilities</h1>
        <p style="color: #60A5FA; font-size: 1.2rem; margin-top: 0.5rem;">Powerful Python Tools & Automation Suite</p>
    </div>
    """, unsafe_allow_html=True)
    
    python_tab1, python_tab2, python_tab3, python_tab4 = st.tabs(["Communication", "File Processing", "Web Tools", "Advanced Tools"])
    
    with python_tab1:
        communication_menu()
    
    with python_tab2:
        file_tools_menu()
    
    with python_tab3:
        web_tools_menu()
    
    with python_tab4:
        advanced_python_tools_menu()

def show_machine_learning():
    """Show Machine Learning section with enhanced styling"""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="background: linear-gradient(90deg, #10B981, #FF6B35); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 2.5rem; font-weight: 700;">🤖 Machine Learning Tools</h1>
        <p style="color: #60A5FA; font-size: 1.2rem; margin-top: 0.5rem;">Advanced ML Calculators & Predictive Analytics</p>
    </div>
    """, unsafe_allow_html=True)
    machine_learning_menu()

def show_devops_tools():
    """Show DevOps tools section with enhanced styling"""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="background: linear-gradient(90deg, #FF6B35, #3B82F6, #10B981); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 2.5rem; font-weight: 700;">🐳 DevOps Tools</h1>
        <p style="color: #60A5FA; font-size: 1.2rem; margin-top: 0.5rem;">Container Management & Cloud Infrastructure</p>
    </div>
    """, unsafe_allow_html=True)
    
    devops_tab1, devops_tab2 = st.tabs(["🐳 Docker Tools", "☁️ AWS Tools"])
    
    with devops_tab1:
        docker_tools_menu()
    
    with devops_tab2:
        aws_tools_menu()

def show_projects():
    """Show Projects section with enhanced styling"""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="background: linear-gradient(90deg, #3B82F6, #FF6B35); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 2.5rem; font-weight: 700;">🚀 Projects</h1>
        <p style="color: #60A5FA; font-size: 1.2rem; margin-top: 0.5rem;">Innovative Projects & Advanced Applications</p>
    </div>
    """, unsafe_allow_html=True)
    
    project_tab1, project_tab2 = st.tabs(["🛠️ Utility Projects", "✋ Hand Gesture Projects"])
    
    with project_tab1:
        utility_projects_menu()
    
    with project_tab2:
        hand_gesture_projects_menu()

def show_javascript_demos():
    """Show JavaScript demos section with enhanced styling"""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="background: linear-gradient(90deg, #FF6B35, #10B981); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 2.5rem; font-weight: 700;">🟨 Java Script</h1>
        <p style="color: #60A5FA; font-size: 1.2rem; margin-top: 0.5rem;">Interactive Web Demonstrations & Frontend Tools</p>
    </div>
    """, unsafe_allow_html=True)
    
    javascript_demos_menu()

if __name__ == "__main__":
    main()
