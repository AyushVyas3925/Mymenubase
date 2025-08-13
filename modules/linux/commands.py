# Linux commands module
import streamlit as st
import subprocess
import os
import paramiko
from .advanced_commands import advanced_linux_commands_menu

def ssh_configuration():
    """SSH Configuration for remote Linux access"""
    st.subheader("🔐 SSH Configuration")
    st.write("Configure SSH connection to remote Linux server")
    
    # SSH connection parameters
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔗 Connection Settings")
        ssh_host = st.text_input("SSH Host/IP:", placeholder="192.168.1.100", key="ssh_host_input")
        ssh_port = st.number_input("SSH Port:", min_value=1, max_value=65535, value=22, key="ssh_port_input")
        ssh_username = st.text_input("Username:", placeholder="ubuntu", key="ssh_username_input")
        ssh_password = st.text_input("Password:", type="password", key="ssh_password_input")
        
        # Connection test
        if st.button("🔍 Test Connection", key="test_ssh_btn"):
            if ssh_host and ssh_username and ssh_password:
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(ssh_host, port=ssh_port, username=ssh_username, password=ssh_password, timeout=10)
                    st.success("✅ SSH connection successful!")
                    ssh.close()
                except Exception as e:
                    st.error(f"❌ SSH connection failed: {str(e)}")
            else:
                st.warning("Please fill in all connection details")
    
    with col2:
        st.subheader("📊 Connection Status")
        if 'ssh_connection' not in st.session_state:
            st.session_state.ssh_connection = None
            st.session_state.ssh_client = None
        
        if st.session_state.ssh_connection:
            st.success("🟢 Connected to remote server")
            st.write(f"**Host:** {st.session_state.ssh_connection['host']}")
            st.write(f"**User:** {st.session_state.ssh_connection['username']}")
            
            if st.button("❌ Disconnect", key="disconnect_ssh_btn"):
                if st.session_state.ssh_client:
                    st.session_state.ssh_client.close()
                st.session_state.ssh_connection = None
                st.session_state.ssh_client = None
                st.rerun()
        else:
            st.info("🔴 Not connected to remote server")
            if st.button("🔌 Connect", key="connect_ssh_btn"):
                if ssh_host and ssh_username and ssh_password:
                    try:
                        ssh = paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh.connect(ssh_host, port=ssh_port, username=ssh_username, password=ssh_password, timeout=10)
                        
                        st.session_state.ssh_client = ssh
                        st.session_state.ssh_connection = {
                            'host': ssh_host,
                            'port': ssh_port,
                            'username': ssh_username
                        }
                        st.success("✅ Connected to remote server!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Connection failed: {str(e)}")
                else:
                    st.warning("Please fill in all connection details")

def execute_remote_command(command, timeout=30):
    """Execute command on remote server via SSH"""
    if not st.session_state.ssh_client:
        return None, "Not connected to remote server"
    
    try:
        stdin, stdout, stderr = st.session_state.ssh_client.exec_command(command, timeout=timeout)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        return output, error
    except Exception as e:
        return None, str(e)

def linux_basic_commands():
    """Basic Linux commands"""
    st.subheader("🐧 Basic Linux Commands")
    st.write("Essential Linux system commands")
    
    # Check if SSH is connected
    use_remote = st.session_state.ssh_connection is not None
    if use_remote:
        st.info("🖥️ Commands will be executed on remote server via SSH")
    else:
        st.info("💻 Commands will be executed locally")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 System Information")
        
        # System info
        if st.button("💻 System Information", key="sys_info_btn"):
            try:
                if use_remote:
                    output, error = execute_remote_command('uname -a')
                    if output:
                        st.code(output, language='bash')
                    else:
                        st.error(f"Error: {error}")
                else:
                    result = subprocess.run(['uname', '-a'], capture_output=True, text=True)
                    if result.returncode == 0:
                        st.code(result.stdout, language='bash')
                    else:
                        st.error(f"Error: {result.stderr}")
            except Exception as e:
                st.error(f"Error getting system info: {str(e)}")
        
        # Disk usage
        if st.button("💾 Disk Usage", key="disk_usage_btn"):
            try:
                if use_remote:
                    output, error = execute_remote_command('df -h')
                    if output:
                        st.code(output, language='bash')
                    else:
                        st.error(f"Error: {error}")
                else:
                    result = subprocess.run(['df', '-h'], capture_output=True, text=True)
                    if result.returncode == 0:
                        st.code(result.stdout, language='bash')
                    else:
                        st.error(f"Error: {result.stderr}")
            except Exception as e:
                st.error(f"Error getting disk usage: {str(e)}")
        
        # Memory usage
        if st.button("🧠 Memory Usage", key="memory_usage_btn"):
            try:
                if use_remote:
                    output, error = execute_remote_command('free -h')
                    if output:
                        st.code(output, language='bash')
                    else:
                        st.error(f"Error: {error}")
                else:
                    result = subprocess.run(['free', '-h'], capture_output=True, text=True)
                    if result.returncode == 0:
                        st.code(result.stdout, language='bash')
                    else:
                        st.error(f"Error: {result.stderr}")
            except Exception as e:
                st.error(f"Error getting memory usage: {str(e)}")
    
    with col2:
        st.subheader("🔍 File Operations")
        
        # List files
        directory = st.text_input("Directory to list:", placeholder="/home", key="list_dir_input")
        
        if st.button("📁 List Files", key="list_files_btn"):
            if directory:
                try:
                    if use_remote:
                        output, error = execute_remote_command(f'ls -la {directory}')
                        if output:
                            st.code(output, language='bash')
                        else:
                            st.error(f"Error: {error}")
                    else:
                        result = subprocess.run(['ls', '-la', directory], capture_output=True, text=True)
                        if result.returncode == 0:
                            st.code(result.stdout, language='bash')
                        else:
                            st.error(f"Error: {result.stderr}")
                except Exception as e:
                    st.error(f"Error listing files: {str(e)}")
            else:
                st.warning("Please enter directory path")
        
        # Find files
        search_term = st.text_input("Search term:", placeholder="*.txt", key="search_term_input")
        
        if st.button("🔍 Find Files", key="find_files_btn"):
            if search_term:
                try:
                    if use_remote:
                        output, error = execute_remote_command(f'find /home -name "{search_term}"', timeout=60)
                        if output:
                            files = output.strip().split('\n')
                            if files and files[0]:
                                st.write("Files found:")
                                for file in files[:20]:  # Show first 20
                                    st.write(f"• {file}")
                                if len(files) > 20:
                                    st.info(f"... and {len(files) - 20} more files")
                            else:
                                st.info("No files found")
                        else:
                            st.error(f"Error: {error}")
                    else:
                        result = subprocess.run(['find', '/home', '-name', search_term], 
                                             capture_output=True, text=True, timeout=30)
                        if result.returncode == 0:
                            files = result.stdout.strip().split('\n')
                            if files and files[0]:
                                st.write("Files found:")
                                for file in files[:20]:  # Show first 20
                                    st.write(f"• {file}")
                                if len(files) > 20:
                                    st.info(f"... and {len(files) - 20} more files")
                            else:
                                st.info("No files found")
                        else:
                            st.error(f"Error: {result.stderr}")
                except Exception as e:
                    st.error(f"Error finding files: {str(e)}")
            else:
                st.warning("Please enter search term")

def linux_network_tools():
    """Linux networking tools"""
    st.subheader("🌐 Network Tools")
    st.write("Network configuration and troubleshooting")
    
    # Check if SSH is connected
    use_remote = st.session_state.ssh_connection is not None
    if use_remote:
        st.info("🖥️ Network commands will be executed on remote server via SSH")
    else:
        st.info("💻 Network commands will be executed locally")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📡 Network Status")
        
        # Network interfaces
        if st.button("🔌 Network Interfaces", key="network_interfaces_btn"):
            try:
                if use_remote:
                    output, error = execute_remote_command('ip addr')
                    if output:
                        st.code(output, language='bash')
                    else:
                        st.error(f"Error: {error}")
                else:
                    result = subprocess.run(['ip', 'addr'], capture_output=True, text=True)
                    if result.returncode == 0:
                        st.code(result.stdout, language='bash')
                    else:
                        st.error(f"Error: {result.stderr}")
            except Exception as e:
                st.error(f"Error getting network interfaces: {str(e)}")
        
        # Network connections
        if st.button("🔗 Active Connections", key="active_connections_btn"):
            try:
                if use_remote:
                    output, error = execute_remote_command('netstat -tuln')
                    if output:
                        st.code(output, language='bash')
                    else:
                        st.error(f"Error: {error}")
                else:
                    result = subprocess.run(['netstat', '-tuln'], capture_output=True, text=True)
                    if result.returncode == 0:
                        st.code(result.stdout, language='bash')
                    else:
                        st.error(f"Error: {result.stderr}")
            except Exception as e:
                st.error(f"Error getting connections: {str(e)}")
    
    with col2:
        st.subheader("🌍 Network Testing")
        
        # Ping test
        host = st.text_input("Host to ping:", placeholder="8.8.8.8", key="ping_host_input")
        
        if st.button("🏓 Ping Host", key="ping_host_btn"):
            if host:
                try:
                    if use_remote:
                        output, error = execute_remote_command(f'ping -c 4 {host}', timeout=60)
                        if output:
                            st.code(output, language='bash')
                        else:
                            st.error(f"Error: {error}")
                    else:
                        result = subprocess.run(['ping', '-c', '4', host], 
                                             capture_output=True, text=True, timeout=30)
                        if result.returncode == 0:
                            st.code(result.stdout, language='bash')
                        else:
                            st.error(f"Error: {result.stderr}")
                except Exception as e:
                    st.error(f"Error pinging host: {str(e)}")
            else:
                st.warning("Please enter host address")
        
        # Traceroute
        if st.button("🛤️ Traceroute", key="traceroute_btn"):
            if host:
                try:
                    if use_remote:
                        output, error = execute_remote_command(f'traceroute {host}', timeout=90)
                        if output:
                            st.code(output, language='bash')
                        else:
                            st.error(f"Error: {error}")
                    else:
                        result = subprocess.run(['traceroute', host], 
                                             capture_output=True, text=True, timeout=60)
                        if result.returncode == 0:
                            st.code(result.stdout, language='bash')
                        else:
                            st.error(f"Error: {result.stderr}")
                except Exception as e:
                    st.error(f"Error running traceroute: {str(e)}")
            else:
                st.warning("Please enter host address")

def linux_process_management():
    """Linux process management tools"""
    st.subheader("⚙️ Process Management")
    st.write("Process monitoring and control")
    
    # Check if SSH is connected
    use_remote = st.session_state.ssh_connection is not None
    if use_remote:
        st.info("🖥️ Process commands will be executed on remote server via SSH")
    else:
        st.info("💻 Process commands will be executed locally")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Process Information")
        
        # Running processes
        if st.button("🔄 Running Processes", key="running_processes_btn"):
            try:
                if use_remote:
                    output, error = execute_remote_command('ps aux')
                    if output:
                        # Show first 20 lines to avoid overwhelming output
                        lines = output.split('\n')[:20]
                        st.code('\n'.join(lines), language='bash')
                        if len(output.split('\n')) > 20:
                            st.info(f"... and {len(output.split('\n')) - 20} more processes")
                    else:
                        st.error(f"Error: {error}")
                else:
                    result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
                    if result.returncode == 0:
                        # Show first 20 lines to avoid overwhelming output
                        lines = result.stdout.split('\n')[:20]
                        st.code('\n'.join(lines), language='bash')
                        if len(result.stdout.split('\n')) > 20:
                            st.info(f"... and {len(result.stdout.split('\n')) - 20} more processes")
                    else:
                        st.error(f"Error: {result.stderr}")
            except Exception as e:
                st.error(f"Error getting processes: {str(e)}")
        
        # Top processes
        if st.button("📈 Top Processes", key="top_processes_btn"):
            try:
                if use_remote:
                    output, error = execute_remote_command('top -b -n 1', timeout=60)
                    if output:
                        st.code(output, language='bash')
                    else:
                        st.error(f"Error: {error}")
                else:
                    result = subprocess.run(['top', '-b', '-n', '1'], 
                                         capture_output=True, text=True, timeout=30)
                    if result.returncode == 0:
                        st.code(result.stdout, language='bash')
                    else:
                        st.error(f"Error: {result.stderr}")
            except Exception as e:
                st.error(f"Error getting top processes: {str(e)}")
    
    with col2:
        st.subheader("🔧 Process Control")
        
        # Kill process
        process_id = st.text_input("Process ID to kill:", placeholder="1234", key="process_id_input")
        
        if st.button("💀 Kill Process", key="kill_process_btn"):
            if process_id:
                try:
                    st.warning(f"⚠️ This will kill process {process_id}!")
                    if st.checkbox("I understand this will terminate the process", key="kill_confirm_checkbox"):
                        if use_remote:
                            st.info("Kill command would be executed on remote server:")
                            st.code(f"kill {process_id}", language='bash')
                            st.success("✅ Kill command prepared for remote execution")
                        else:
                            st.info("Kill command would be:")
                            st.code(f"kill {process_id}", language='bash')
                            st.success("✅ Kill command prepared")
                except Exception as e:
                    st.error(f"Error preparing kill command: {str(e)}")
            else:
                st.warning("Please enter process ID")
        
        # Process tree
        if st.button("🌳 Process Tree", key="process_tree_btn"):
            try:
                if use_remote:
                    output, error = execute_remote_command('pstree')
                    if output:
                        st.code(output, language='bash')
                    else:
                        st.error(f"Error: {error}")
                else:
                    result = subprocess.run(['pstree'], capture_output=True, text=True)
                    if result.returncode == 0:
                        st.code(result.stdout, language='bash')
                    else:
                        st.error(f"Error: {result.stderr}")
            except Exception as e:
                st.error(f"Error getting process tree: {str(e)}")

def linux_commands_menu():
    """Main Linux commands menu"""
    st.title("🐧 Linux Commands & Tools")
    
    # SSH Configuration at the top
    ssh_configuration()
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Basic Commands", "Network Tools", "Process Management", "Advanced Commands"
    ])
    
    with tab1:
        linux_basic_commands()
    
    with tab2:
        linux_network_tools()
    
    with tab3:
        linux_process_management()
    
    with tab4:
        advanced_linux_commands_menu()
