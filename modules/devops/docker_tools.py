# Docker Tools
import streamlit as st
import subprocess
import os
import json
import tempfile
import paramiko

def ssh_configuration_docker():
    """SSH Configuration for remote Docker access"""
    st.subheader("🔐 SSH Configuration for Docker")
    st.write("Configure SSH connection to remote Linux server with Docker")
    
    # SSH connection parameters
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔗 Connection Settings")
        ssh_host = st.text_input("SSH Host/IP:", placeholder="192.168.1.100", key="docker_ssh_host_input")
        ssh_port = st.number_input("SSH Port:", min_value=1, max_value=65535, value=22, key="docker_ssh_port_input")
        ssh_username = st.text_input("Username:", placeholder="ubuntu", key="docker_ssh_username_input")
        ssh_password = st.text_input("Password:", type="password", key="docker_ssh_password_input")
        
        # Connection test
        if st.button("🔍 Test Connection", key="docker_test_ssh_btn"):
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
        if 'docker_ssh_connection' not in st.session_state:
            st.session_state.docker_ssh_connection = None
            st.session_state.docker_ssh_client = None
        
        if st.session_state.docker_ssh_connection:
            st.success("🟢 Connected to remote Docker server")
            st.write(f"**Host:** {st.session_state.docker_ssh_connection['host']}")
            st.write(f"**User:** {st.session_state.docker_ssh_connection['username']}")
            
            if st.button("❌ Disconnect", key="docker_disconnect_ssh_btn"):
                if st.session_state.docker_ssh_client:
                    st.session_state.docker_ssh_client.close()
                st.session_state.docker_ssh_connection = None
                st.session_state.docker_ssh_client = None
                st.rerun()
        else:
            st.info("🔴 Not connected to remote Docker server")
            if st.button("🔌 Connect", key="docker_connect_ssh_btn"):
                if ssh_host and ssh_username and ssh_password:
                    try:
                        ssh = paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh.connect(ssh_host, port=ssh_port, username=ssh_username, password=ssh_password, timeout=10)
                        
                        st.session_state.docker_ssh_client = ssh
                        st.session_state.docker_ssh_connection = {
                            'host': ssh_host,
                            'port': ssh_port,
                            'username': ssh_username
                        }
                        st.success("✅ Connected to remote Docker server!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Connection failed: {str(e)}")
                else:
                    st.warning("Please fill in all connection details")

def execute_remote_docker_command(command, timeout=30):
    """Execute Docker command on remote server via SSH"""
    if not st.session_state.docker_ssh_client:
        return None, "Not connected to remote server"
    
    try:
        stdin, stdout, stderr = st.session_state.docker_ssh_client.exec_command(command, timeout=timeout)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        return output, error
    except Exception as e:
        return None, str(e)

def docker_project():
    """Docker Project Management Tool"""
    st.subheader("🐳 Docker Project Management")
    st.write("Manage Docker containers, images, and projects")
    
    # SSH Configuration at the top
    ssh_configuration_docker()
    
    st.markdown("---")
    
    # Check if SSH is connected
    use_remote = st.session_state.docker_ssh_connection is not None
    if use_remote:
        st.info("🖥️ Docker commands will be executed on remote server via SSH")
    else:
        st.info("💻 Docker commands will be executed locally")

    def run_cmd(cmd):
        """Run command and return result"""
        if use_remote:
            output, error = execute_remote_docker_command(cmd)
            if output is not None:
                return output, error, 0
            else:
                return "", error, -1
        else:
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                return result.stdout, result.stderr, result.returncode
            except Exception as e:
                return "", str(e), -1

    # Main interface
    tab1, tab2, tab3, tab4 = st.tabs([
        "📦 Images", "🐳 Containers", "🌐 Networks", "💾 Volumes"
    ])

    with tab1:
        st.subheader("📦 Docker Images")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📋 List Images"):
                stdout, stderr, returncode = run_cmd("docker images")
                if returncode == 0:
                    st.code(stdout, language="bash")
                else:
                    st.error(f"Error: {stderr}")
            
            if st.button("🧹 Prune Images"):
                if st.checkbox("Force remove all unused images"):
                    stdout, stderr, returncode = run_cmd("docker image prune -a -f")
                    if returncode == 0:
                        st.success("Images pruned successfully!")
                        st.code(stdout, language="bash")
                    else:
                        st.error(f"Error: {stderr}")
                else:
                    stdout, stderr, returncode = run_cmd("docker image prune")
                    if returncode == 0:
                        st.success("Images pruned successfully!")
                        st.code(stdout, language="bash")
                    else:
                        st.error(f"Error: {stderr}")
        
        with col2:
            # Build image
            st.subheader("🔨 Build Image")
            dockerfile_path = st.text_input("Dockerfile Path:", value="./Dockerfile")
            image_name = st.text_input("Image Name:", value="myapp:latest")
            
            if st.button("🔨 Build"):
                if os.path.exists(dockerfile_path):
                    cmd = f"docker build -t {image_name} -f {dockerfile_path} ."
                    stdout, stderr, returncode = run_cmd(cmd)
                    if returncode == 0:
                        st.success("Image built successfully!")
                        st.code(stdout, language="bash")
                    else:
                        st.error(f"Build failed: {stderr}")
                else:
                    st.error("Dockerfile not found!")

    with tab2:
        st.subheader("🐳 Docker Containers")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📋 List Containers"):
                stdout, stderr, returncode = run_cmd("docker ps -a")
                if returncode == 0:
                    st.code(stdout, language="bash")
                else:
                    st.error(f"Error: {stderr}")
            
            if st.button("📊 Container Stats"):
                stdout, stderr, returncode = run_cmd("docker stats --no-stream")
                if returncode == 0:
                    st.code(stdout, language="bash")
                else:
                    st.error(f"Error: {stderr}")
        
        with col2:
            # Container operations
            st.subheader("⚡ Container Operations")
            
            container_id = st.text_input("Container ID/Name:")
            
            col_op1, col_op2 = st.columns(2)
            
            with col_op1:
                if st.button("▶️ Start"):
                    if container_id:
                        stdout, stderr, returncode = run_cmd(f"docker start {container_id}")
                        if returncode == 0:
                            st.success(f"Container {container_id} started!")
                        else:
                            st.error(f"Error: {stderr}")
                
                if st.button("⏸️ Pause"):
                    if container_id:
                        stdout, stderr, returncode = run_cmd(f"docker pause {container_id}")
                        if returncode == 0:
                            st.success(f"Container {container_id} paused!")
                        else:
                            st.error(f"Error: {stderr}")
            
            with col_op2:
                if st.button("⏹️ Stop"):
                    if container_id:
                        stdout, stderr, returncode = run_cmd(f"docker stop {container_id}")
                        if returncode == 0:
                            st.success(f"Container {container_id} stopped!")
                        else:
                            st.error(f"Error: {stderr}")
                
                if st.button("🗑️ Remove"):
                    if container_id:
                        if st.checkbox("Force remove"):
                            stdout, stderr, returncode = run_cmd(f"docker rm -f {container_id}")
                        else:
                            stdout, stderr, returncode = run_cmd(f"docker rm {container_id}")
                        
                        if returncode == 0:
                            st.success(f"Container {container_id} removed!")
                        else:
                            st.error(f"Error: {stderr}")

    with tab3:
        st.subheader("🌐 Docker Networks")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📋 List Networks"):
                stdout, stderr, returncode = run_cmd("docker network ls")
                if returncode == 0:
                    st.code(stdout, language="bash")
                else:
                    st.error(f"Error: {stderr}")
            
            if st.button("🔍 Inspect Networks"):
                stdout, stderr, returncode = run_cmd("docker network ls --format '{{.Name}}' | head -5")
                if returncode == 0:
                    networks = stdout.strip().split('\n')
                    for network in networks:
                        if network:
                            inspect_cmd = f"docker network inspect {network}"
                            inspect_stdout, inspect_stderr, inspect_returncode = run_cmd(inspect_cmd)
                            if inspect_returncode == 0:
                                st.write(f"**Network: {network}**")
                                st.code(inspect_stdout, language="json")
        
        with col2:
            # Network operations
            st.subheader("🌐 Network Operations")
            
            network_name = st.text_input("Network Name:", value="my-network")
            network_driver = st.selectbox("Driver:", ["bridge", "host", "overlay", "macvlan"])
            
            if st.button("➕ Create Network"):
                cmd = f"docker network create --driver {network_driver} {network_name}"
                stdout, stderr, returncode = run_cmd(cmd)
                if returncode == 0:
                    st.success(f"Network {network_name} created!")
                    st.code(stdout, language="bash")
                else:
                    st.error(f"Error: {stderr}")
            
            if st.button("🗑️ Remove Network"):
                cmd = f"docker network rm {network_name}"
                stdout, stderr, returncode = run_cmd(cmd)
                if returncode == 0:
                    st.success(f"Network {network_name} removed!")
                else:
                    st.error(f"Error: {stderr}")

    with tab4:
        st.subheader("💾 Docker Volumes")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📋 List Volumes"):
                stdout, stderr, returncode = run_cmd("docker volume ls")
                if returncode == 0:
                    st.code(stdout, language="bash")
                else:
                    st.error(f"Error: {stderr}")
            
            if st.button("🔍 Volume Info"):
                stdout, stderr, returncode = run_cmd("docker volume ls --format '{{.Name}}' | head -5")
                if returncode == 0:
                    volumes = stdout.strip().split('\n')
                    for volume in volumes:
                        if volume:
                            inspect_cmd = f"docker volume inspect {volume}"
                            inspect_stdout, inspect_stderr, inspect_returncode = run_cmd(inspect_cmd)
                            if inspect_returncode == 0:
                                st.write(f"**Volume: {volume}**")
                                st.code(inspect_stdout, language="json")
        
        with col2:
            # Volume operations
            st.subheader("💾 Volume Operations")
            
            volume_name = st.text_input("Volume Name:", value="my-volume")
            
            if st.button("➕ Create Volume"):
                cmd = f"docker volume create {volume_name}"
                stdout, stderr, returncode = run_cmd(cmd)
                if returncode == 0:
                    st.success(f"Volume {volume_name} created!")
                    st.code(stdout, language="bash")
                else:
                    st.error(f"Error: {stderr}")
            
            if st.button("🗑️ Remove Volume"):
                if st.checkbox("Force remove"):
                    cmd = f"docker volume rm -f {volume_name}"
                else:
                    cmd = f"docker volume rm {volume_name}"
                
                stdout, stderr, returncode = run_cmd(cmd)
                if returncode == 0:
                    st.success(f"Volume {volume_name} removed!")
                else:
                    st.error(f"Error: {stderr}")

def docker_compose_manager():
    """Docker Compose Manager"""
    st.subheader("🐳 Docker Compose Manager")
    st.write("Manage Docker Compose projects and services")

    def run_compose_command(path, command):
        """Run docker-compose command"""
        try:
            cmd = f"docker-compose -f {path} {command}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=os.path.dirname(path))
            return result.stdout, result.stderr, result.returncode
        except Exception as e:
            return "", str(e), -1

    def get_compose_projects(base_path="."):
        """Get list of docker-compose projects"""
        projects = []
        for root, dirs, files in os.walk(base_path):
            for file in files:
                if file in ['docker-compose.yml', 'docker-compose.yaml']:
                    projects.append(os.path.join(root, file))
        return projects

    # Main interface
    tab1, tab2, tab3 = st.tabs([
        "📁 Projects", "⚡ Services", "🔧 Commands"
    ])

    with tab1:
        st.subheader("📁 Compose Projects")
        
        # Find compose files
        compose_files = get_compose_projects()
        
        if compose_files:
            st.write(f"Found {len(compose_files)} Docker Compose projects:")
            
            for compose_file in compose_files:
                with st.expander(f"📁 {os.path.basename(os.path.dirname(compose_file))}"):
                    st.write(f"**File:** {compose_file}")
                    
                    # Show compose file content
                    try:
                        with open(compose_file, 'r') as f:
                            content = f.read()
                            st.code(content, language="yaml")
                    except:
                        st.error("Could not read compose file")
                    
                    # Project actions
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("▶️ Up", key=f"up_{compose_file}"):
                            stdout, stderr, returncode = run_compose_command(compose_file, "up -d")
                            if returncode == 0:
                                st.success("Project started!")
                                st.code(stdout, language="bash")
                            else:
                                st.error(f"Error: {stderr}")
                    
                    with col2:
                        if st.button("⏹️ Down", key=f"down_{compose_file}"):
                            stdout, stderr, returncode = run_compose_command(compose_file, "down")
                            if returncode == 0:
                                st.success("Project stopped!")
                                st.code(stdout, language="bash")
                            else:
                                st.error(f"Error: {stderr}")
                    
                    with col3:
                        if st.button("🔄 Restart", key=f"restart_{compose_file}"):
                            stdout, stderr, returncode = run_compose_command(compose_file, "restart")
                            if returncode == 0:
                                st.success("Project restarted!")
                                st.code(stdout, language="bash")
                            else:
                                st.error(f"Error: {stderr}")
        else:
            st.info("No Docker Compose projects found in current directory")

    with tab2:
        st.subheader("⚡ Service Management")
        
        # Select compose file
        compose_file = st.selectbox("Select Compose File:", compose_files if 'compose_files' in locals() else [])
        
        if compose_file:
            # Service operations
            st.write(f"**Managing services in:** {os.path.basename(compose_file)}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📋 List Services"):
                    stdout, stderr, returncode = run_compose_command(compose_file, "ps")
                    if returncode == 0:
                        st.code(stdout, language="bash")
                    else:
                        st.error(f"Error: {stderr}")
                
                if st.button("📊 Service Logs"):
                    service_name = st.text_input("Service Name (optional):")
                    if service_name:
                        stdout, stderr, returncode = run_compose_command(compose_file, f"logs {service_name}")
                    else:
                        stdout, stderr, returncode = run_compose_command(compose_file, "logs")
                    
                    if returncode == 0:
                        st.code(stdout, language="bash")
                    else:
                        st.error(f"Error: {stderr}")
            
            with col2:
                if st.button("🔍 Service Status"):
                    stdout, stderr, returncode = run_compose_command(compose_file, "ps --format table")
                    if returncode == 0:
                        st.code(stdout, language="bash")
                    else:
                        st.error(f"Error: {stderr}")
                
                if st.button("📈 Service Stats"):
                    stdout, stderr, returncode = run_compose_command(compose_file, "top")
                    if returncode == 0:
                        st.code(stdout, language="bash")
                    else:
                        st.error(f"Error: {stderr}")

    with tab3:
        st.subheader("🔧 Custom Commands")
        
        compose_file = st.selectbox("Select Compose File:", compose_files if 'compose_files' in locals() else [], key="custom_cmd")
        
        if compose_file:
            st.write(f"**Compose File:** {compose_file}")
            
            # Custom command input
            custom_command = st.text_input("Custom Docker Compose Command:", placeholder="e.g., exec web bash")
            
            if st.button("🚀 Execute"):
                if custom_command:
                    stdout, stderr, returncode = run_compose_command(compose_file, custom_command)
                    if returncode == 0:
                        st.success("Command executed successfully!")
                        st.code(stdout, language="bash")
                    else:
                        st.error(f"Command failed: {stderr}")
                else:
                    st.warning("Please enter a command")

def docker_tools_menu():
    """Main Docker tools menu"""
    st.title("🐳 Docker Tools")
    
    tab1, tab2 = st.tabs([
        "🐳 Docker Management", "📦 Compose Manager"
    ])
    
    with tab1:
        docker_project()
    
    with tab2:
        docker_compose_manager()
