# Advanced Linux commands module
import streamlit as st
import subprocess
import os

def linux_advanced_format_mount():
    """Advanced disk formatting and mounting"""
    st.subheader("💾 Advanced Disk Format & Mount")
    st.write("Advanced disk management operations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔧 Disk Operations")
        
        # List disks
        if st.button("📋 List Available Disks", key="list_disks_btn"):
            try:
                result = subprocess.run(['lsblk'], capture_output=True, text=True, shell=True)
                if result.returncode == 0:
                    st.code(result.stdout, language='bash')
                else:
                    st.error(f"Error: {result.stderr}")
            except Exception as e:
                st.error(f"Error listing disks: {str(e)}")
        
        # Format disk
        disk_path = st.text_input("Disk path (e.g., /dev/sdb):", placeholder="/dev/sdb")
        fs_type = st.selectbox("Filesystem type:", ["ext4", "xfs", "btrfs", "ntfs"])
        
        if st.button("🔨 Format Disk", key="format_disk_btn"):
            if disk_path:
                st.warning(f"⚠️ This will format {disk_path} with {fs_type} filesystem!")
                if st.checkbox("I understand this will erase all data"):
                    try:
                        # Note: In real environment, you'd need sudo privileges
                        st.info("Format command would be:")
                        st.code(f"sudo mkfs.{fs_type} {disk_path}", language='bash')
                        st.success("✅ Format command prepared (requires sudo)")
                    except Exception as e:
                        st.error(f"Error preparing format command: {str(e)}")
            else:
                st.warning("Please enter disk path")
    
    with col2:
        st.subheader("📁 Mount Operations")
        
        # Mount point
        mount_point = st.text_input("Mount point:", placeholder="/mnt/disk")
        
        if st.button("📌 Mount Disk", key="mount_disk_btn"):
            if disk_path and mount_point:
                try:
                    st.info("Mount command would be:")
                    st.code(f"sudo mount {disk_path} {mount_point}", language='bash')
                    st.success("✅ Mount command prepared (requires sudo)")
                except Exception as e:
                    st.error(f"Error preparing mount command: {str(e)}")
            else:
                st.warning("Please enter both disk path and mount point")
        
        # Unmount
        if st.button("🔓 Unmount Disk", key="unmount_disk_btn"):
            if mount_point:
                try:
                    st.info("Unmount command would be:")
                    st.code(f"sudo umount {mount_point}", language='bash')
                    st.success("✅ Unmount command prepared (requires sudo)")
                except Exception as e:
                    st.error(f"Error preparing unmount command: {str(e)}")
            else:
                st.warning("Please enter mount point")

def linux_disk_usage_analyzer():
    """Advanced disk usage analysis"""
    st.subheader("📊 Disk Usage Analyzer")
    st.write("Comprehensive disk space analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💾 Space Analysis")
        
        # Disk usage
        if st.button("📈 Analyze Disk Usage", key="analyze_disk_usage_btn"):
            try:
                result = subprocess.run(['df', '-h'], capture_output=True, text=True)
                if result.returncode == 0:
                    st.code(result.stdout, language='bash')
                else:
                    st.error(f"Error: {result.stderr}")
            except Exception as e:
                st.error(f"Error analyzing disk usage: {str(e)}")
        
        # Directory usage
        directory = st.text_input("Directory to analyze:", placeholder="/home")
        
        if st.button("📁 Analyze Directory", key="analyze_directory_btn"):
            if directory:
                try:
                    result = subprocess.run(['du', '-sh', directory], capture_output=True, text=True)
                    if result.returncode == 0:
                        st.success(f"Directory size: {result.stdout.strip()}")
                    else:
                        st.error(f"Error: {result.stderr}")
                except Exception as e:
                    st.error(f"Error analyzing directory: {str(e)}")
            else:
                st.warning("Please enter directory path")
    
    with col2:
        st.subheader("🧹 Cleanup Suggestions")
        
        # Find large files
        if st.button("🔍 Find Large Files"):
            try:
                st.info("Finding files larger than 100MB...")
                result = subprocess.run(['find', '/home', '-type', 'f', '-size', '+100M'], 
                                     capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    files = result.stdout.strip().split('\n')
                    if files and files[0]:
                        st.write("Large files found:")
                        for file in files[:10]:  # Show first 10
                            st.write(f"• {file}")
                        if len(files) > 10:
                            st.info(f"... and {len(files) - 10} more files")
                    else:
                        st.info("No large files found")
                else:
                    st.error(f"Error: {result.stderr}")
            except Exception as e:
                st.error(f"Error finding large files: {str(e)}")
        
        # Cleanup commands
        st.subheader("🧹 Cleanup Commands")
        st.code("sudo apt autoremove", language='bash')
        st.code("sudo apt autoclean", language='bash')
        st.code("journalctl --vacuum-time=7d", language='bash')

def linux_nfs_mount_tool():
    """NFS mount management tool"""
    st.subheader("🌐 NFS Mount Tool")
    st.write("Network File System mount management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📡 NFS Server")
        
        nfs_server = st.text_input("NFS Server IP:", placeholder="192.168.1.100")
        nfs_share = st.text_input("NFS Share path:", placeholder="/shared")
        local_mount = st.text_input("Local mount point:", placeholder="/mnt/nfs")
        
        if st.button("📌 Mount NFS Share"):
            if nfs_server and nfs_share and local_mount:
                try:
                    st.info("NFS mount command would be:")
                    st.code(f"sudo mount -t nfs {nfs_server}:{nfs_share} {local_mount}", language='bash')
                    st.success("✅ NFS mount command prepared (requires sudo)")
                except Exception as e:
                    st.error(f"Error preparing NFS mount: {str(e)}")
            else:
                st.warning("Please fill all fields")
    
    with col2:
        st.subheader("🔧 NFS Configuration")
        
        # Check NFS status
        if st.button("📊 Check NFS Status"):
            try:
                result = subprocess.run(['systemctl', 'status', 'nfs-server'], 
                                     capture_output=True, text=True)
                if result.returncode == 0:
                    st.code(result.stdout, language='bash')
                else:
                    st.info("NFS server not running or not installed")
            except Exception as e:
                st.error(f"Error checking NFS status: {str(e)}")
        
        # NFS exports
        if st.button("📋 Show NFS Exports"):
            try:
                result = subprocess.run(['showmount', '-e'], capture_output=True, text=True)
                if result.returncode == 0:
                    st.code(result.stdout, language='bash')
                else:
                    st.info("No NFS exports found or NFS not configured")
            except Exception as e:
                st.error(f"Error showing NFS exports: {str(e)}")

def linux_lvm_manager():
    """Logical Volume Manager tool"""
    st.subheader("💿 LVM Manager")
    st.write("Logical Volume Management operations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 LVM Information")
        
        # Physical volumes
        if st.button("💾 Show Physical Volumes"):
            try:
                result = subprocess.run(['pvs'], capture_output=True, text=True)
                if result.returncode == 0:
                    st.code(result.stdout, language='bash')
                else:
                    st.error(f"Error: {result.stderr}")
            except Exception as e:
                st.error(f"Error showing PVs: {str(e)}")
        
        # Volume groups
        if st.button("📦 Show Volume Groups"):
            try:
                result = subprocess.run(['vgs'], capture_output=True, text=True)
                if result.returncode == 0:
                    st.code(result.stdout, language='bash')
                else:
                    st.error(f"Error: {result.stderr}")
            except Exception as e:
                st.error(f"Error showing VGs: {str(e)}")
        
        # Logical volumes
        if st.button("🔗 Show Logical Volumes"):
            try:
                result = subprocess.run(['lvs'], capture_output=True, text=True)
                if result.returncode == 0:
                    st.code(result.stdout, language='bash')
                else:
                    st.error(f"Error: {result.stderr}")
            except Exception as e:
                st.error(f"Error showing LVs: {str(e)}")
    
    with col2:
        st.subheader("🔧 LVM Operations")
        
        # Create PV
        pv_device = st.text_input("Device for Physical Volume:", placeholder="/dev/sdb")
        
        if st.button("💾 Create Physical Volume"):
            if pv_device:
                try:
                    st.info("Create PV command would be:")
                    st.code(f"sudo pvcreate {pv_device}", language='bash')
                    st.success("✅ PV create command prepared (requires sudo)")
                except Exception as e:
                    st.error(f"Error preparing PV create: {str(e)}")
            else:
                st.warning("Please enter device path")
        
        # Extend LV
        lv_name = st.text_input("Logical Volume name:", placeholder="lv_data")
        extend_size = st.text_input("Size to extend (e.g., +10G):", placeholder="+10G")
        
        if st.button("📈 Extend Logical Volume"):
            if lv_name and extend_size:
                try:
                    st.info("Extend LV command would be:")
                    st.code(f"sudo lvextend -L {extend_size} {lv_name}", language='bash')
                    st.success("✅ LV extend command prepared (requires sudo)")
                except Exception as e:
                    st.error(f"Error preparing LV extend: {str(e)}")
            else:
                st.warning("Please fill all fields")

def linux_advanced_disk_info():
    """Advanced disk information and monitoring"""
    st.subheader("📊 Advanced Disk Information")
    st.write("Comprehensive disk monitoring and analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💾 Disk Health")
        
        # SMART status
        if st.button("🔍 Check Disk Health (SMART)"):
            try:
                st.info("Checking disk health...")
                result = subprocess.run(['smartctl', '-a', '/dev/sda'], 
                                     capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    st.code(result.stdout, language='bash')
                else:
                    st.warning("SMART tools not available or disk not accessible")
            except Exception as e:
                st.error(f"Error checking disk health: {str(e)}")
        
        # I/O statistics
        if st.button("📈 Show I/O Statistics"):
            try:
                result = subprocess.run(['iostat', '-x', '1', '3'], 
                                     capture_output=True, text=True)
                if result.returncode == 0:
                    st.code(result.stdout, language='bash')
                else:
                    st.warning("iostat not available")
            except Exception as e:
                st.error(f"Error showing I/O stats: {str(e)}")
    
    with col2:
        st.subheader("🔧 Performance Monitoring")
        
        # Disk usage patterns
        if st.button("📊 Analyze Disk Usage Patterns"):
            try:
                st.info("Analyzing disk usage patterns...")
                result = subprocess.run(['iotop', '-b', '-n', '1'], 
                                     capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    st.code(result.stdout, language='bash')
                else:
                    st.info("iotop not available")
            except Exception as e:
                st.error(f"Error analyzing disk patterns: {str(e)}")
        
        # File system info
        if st.button("📁 Show File System Info"):
            try:
                result = subprocess.run(['mount'], capture_output=True, text=True)
                if result.returncode == 0:
                    st.code(result.stdout, language='bash')
                else:
                    st.error(f"Error: {result.stderr}")
            except Exception as e:
                st.error(f"Error showing file system info: {str(e)}")

def linux_redhat_yum_setup():
    """Red Hat YUM package manager setup"""
    st.subheader("🔴 Red Hat YUM Setup")
    st.write("YUM package manager configuration and management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📦 Package Management")
        
        # Update system
        if st.button("🔄 Update System"):
            try:
                st.info("System update commands:")
                st.code("sudo yum update -y", language='bash')
                st.code("sudo yum upgrade -y", language='bash')
                st.success("✅ Update commands prepared (requires sudo)")
            except Exception as e:
                st.error(f"Error preparing update commands: {str(e)}")
        
        # Install packages
        package_name = st.text_input("Package to install:", placeholder="httpd")
        
        if st.button("📥 Install Package"):
            if package_name:
                try:
                    st.info("Install command would be:")
                    st.code(f"sudo yum install {package_name} -y", language='bash')
                    st.success("✅ Install command prepared (requires sudo)")
                except Exception as e:
                    st.error(f"Error preparing install command: {str(e)}")
            else:
                st.warning("Please enter package name")
    
    with col2:
        st.subheader("🔧 Repository Management")
        
        # List repositories
        if st.button("📋 List Repositories"):
            try:
                result = subprocess.run(['yum', 'repolist'], capture_output=True, text=True)
                if result.returncode == 0:
                    st.code(result.stdout, language='bash')
                else:
                    st.error(f"Error: {result.stderr}")
            except Exception as e:
                st.error(f"Error listing repositories: {str(e)}")
        
        # Clean cache
        if st.button("🧹 Clean YUM Cache"):
            try:
                st.info("Cache cleanup commands:")
                st.code("sudo yum clean all", language='bash')
                st.code("sudo yum makecache", language='bash')
                st.success("✅ Cache cleanup commands prepared (requires sudo)")
            except Exception as e:
                st.error(f"Error preparing cache cleanup: {str(e)}")

def advanced_linux_commands_menu():
    """Main advanced Linux commands menu"""
    st.title("🔧 Advanced Linux Commands")
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Disk Format & Mount", "Disk Usage Analyzer", "NFS Mount Tool", 
        "LVM Manager", "Advanced Disk Info", "Red Hat YUM Setup"
    ])
    
    with tab1:
        linux_advanced_format_mount()
    
    with tab2:
        linux_disk_usage_analyzer()
    
    with tab3:
        linux_nfs_mount_tool()
    
    with tab4:
        linux_lvm_manager()
    
    with tab5:
        linux_advanced_disk_info()
    
    with tab6:
        linux_redhat_yum_setup()
