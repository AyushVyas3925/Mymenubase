# AWS Tools
import streamlit as st
import boto3
import pandas as pd
from datetime import datetime
import json
import os

def launch_ec2_instance(aws_access_key, aws_secret_key, region, instance_type, image_id, min_count=1, max_count=1):
    """Launch an EC2 instance and return details."""
    try:
        ec2_resource = boto3.resource(
            'ec2',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )
        instances = ec2_resource.create_instances(
            InstanceType=instance_type,
            ImageId=image_id,
            MinCount=min_count,
            MaxCount=max_count
        )
        instance = instances[0]
        instance.wait_until_running()
        instance.load()
        return {
            "id": instance.id,
            "public_ip": instance.public_ip_address,
            "state": instance.state["Name"],
            "region": ec2_resource.meta.client.meta.region_name
        }
    except Exception as e:
        return {"error": str(e)}

def terminate_ec2_instances(aws_access_key, aws_secret_key, region, instance_ids):
    """Terminate EC2 instances by IDs and return their final states."""
    ec2_resource = boto3.resource(
        'ec2',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region
    )
    results = []
    for instance_id in instance_ids:
        try:
            instance = ec2_resource.Instance(instance_id)
            instance.terminate()
            instance.wait_until_terminated()
            instance.load()
            results.append({
                "id": instance.id,
                "state": instance.state["Name"]
            })
        except Exception as e:
            results.append({"id": instance_id, "error": str(e)})
    return results

def docker_aws_ec2_manager():
    """AWS EC2 Manager Tool"""
    st.subheader("☁️ AWS EC2 Manager")

    # AWS credentials input
    st.write("**AWS Credentials:**")
    col1, col2 = st.columns(2)

    with col1:
        aws_access_key = st.text_input("AWS Access Key ID", type="password")
        aws_secret_key = st.text_input("AWS Secret Access Key", type="password")

    with col2:
        region = st.selectbox("AWS Region", [
            "ap-south-1", "us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"
        ])

    if not aws_access_key or not aws_secret_key:
        st.warning("Please enter your AWS credentials to continue.")
        return

    try:
        # Initialize AWS client and resource
        ec2_client = boto3.client(
            'ec2',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )
        ec2_resource = boto3.resource(
            'ec2',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )

        st.success("✅ AWS connection established!")

        # EC2 Manager class (existing)
        class EC2Manager:
            def __init__(self, region_name='ap-south-1'):
                self.ec2_client = boto3.client(
                    'ec2',
                    aws_access_key_id=aws_access_key,
                    aws_secret_access_key=aws_secret_key,
                    region_name=region_name
                )
            def describe_all_instances(self):
                try:
                    response = self.ec2_client.describe_instances()
                    instances = []
                    for reservation in response['Reservations']:
                        for instance in reservation['Instances']:
                            instances.append({
                                'Instance ID': instance['InstanceId'],
                                'Type': instance['InstanceType'],
                                'State': instance['State']['Name'],
                                'Launch Time': instance['LaunchTime'].strftime('%Y-%m-%d %H:%M:%S'),
                                'Public IP': instance.get('PublicIpAddress', 'N/A'),
                                'Private IP': instance.get('PrivateIpAddress', 'N/A'),
                                'Platform': instance.get('Platform', 'linux'),
                                'Tags': ', '.join([f"{tag['Key']}={tag['Value']}" for tag in instance.get('Tags', [])])
                            })
                    return instances
                except Exception as e:
                    st.error(f"Error describing instances: {e}")
                    return []
            def start_instances(self, instance_ids):
                try:
                    response = self.ec2_client.start_instances(InstanceIds=instance_ids)
                    st.success(f"Starting instances: {', '.join(instance_ids)}")
                    return True
                except Exception as e:
                    st.error(f"Error starting instances: {e}")
                    return False
            def stop_instances(self, instance_ids):
                try:
                    response = self.ec2_client.stop_instances(InstanceIds=instance_ids)
                    st.success(f"Stopping instances: {', '.join(instance_ids)}")
                    return True
                except Exception as e:
                    st.error(f"Error stopping instances: {e}")
                    return False
            def terminate_instances(self, instance_ids):
                try:
                    response = self.ec2_client.terminate_instances(InstanceIds=instance_ids)
                    st.success(f"Terminating instances: {', '.join(instance_ids)}")
                    return True
                except Exception as e:
                    st.error(f"Error terminating instances: {e}")
                    return False

        # Initialize EC2 Manager
        ec2_manager = EC2Manager(region)

        # Main interface
        st.write("---")

        # Instance management
        st.subheader("📊 Instance Management")

        if st.button("🔄 Refresh Instances"):
            instances = ec2_manager.describe_all_instances()
            if instances:
                df = pd.DataFrame(instances)
                st.dataframe(df, use_container_width=True)

                # Instance actions
                st.write("---")
                st.subheader("⚡ Instance Actions")

                # Select instances for actions
                instance_ids = st.multiselect(
                    "Select instances for action:",
                    [inst['Instance ID'] for inst in instances]
                )

                if instance_ids:
                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        if st.button("🚀 Start Selected", type="primary"):
                            ec2_manager.start_instances(instance_ids)

                    with col2:
                        if st.button("⏸️ Stop Selected", type="secondary"):
                            ec2_manager.stop_instances(instance_ids)

                    with col3:
                        if st.button("💀 Terminate Selected", type="secondary"):
                            if st.checkbox("I understand this will permanently delete the instances"):
                                ec2_manager.terminate_instances(instance_ids)

                    with col4:
                        if st.button("🗑 Terminate (Notebook Style)", type="secondary"):
                            results = terminate_ec2_instances(
                                aws_access_key,
                                aws_secret_key,
                                region,
                                instance_ids
                            )
                            for r in results:
                                if 'error' in r:
                                    st.error(f"ID: {r['id']} - {r['error']}")
                                else:
                                    st.success(f"Terminated ID: {r['id']} | State: {r['state']}")
            else:
                st.info("No instances found in this region.")

        # Instance creation
        st.write("---")
        st.subheader("➕ Create New Instance")

        with st.expander("Instance Configuration"):
            col1, col2 = st.columns(2)

            with col1:
                instance_type = st.selectbox("Instance Type", [
                    "t2.micro", "t2.small", "t2.medium", "t3.micro", "t3.small"
                ])
                key_name = st.text_input("Key Pair Name")

            with col2:
                security_group = st.text_input("Security Group ID")
                subnet_id = st.text_input("Subnet ID")

            if st.button("🚀 Launch Instance (Notebook Style)"):
                # Use the notebook-style launch logic with credentials
                result = launch_ec2_instance(
                    aws_access_key,
                    aws_secret_key,
                    region,
                    instance_type=instance_type,
                    image_id="ami-0a3ece531caa5d49d",  # Singapore default, can be parameterized
                    min_count=1,
                    max_count=1
                )
                if 'error' in result:
                    st.error(f"Failed to launch: {result['error']}")
                else:
                    st.success(f"✅ Instance Launched!\n🆔 ID: {result['id']}\n🌐 Public IP: {result['public_ip']}\n🔁 State: {result['state']}\n📍 Region: {result['region']}")

            # Existing placeholder button
            if st.button("🚀 Launch Instance"):
                st.info("Instance creation feature coming soon!")

    except Exception as e:
        st.error(f"Failed to connect to AWS: {e}")
        st.info("Please check your credentials and try again.")

def aws_advanced_infra_manager():
    """Advanced AWS Infrastructure Manager"""
    st.subheader("🚀 Advanced AWS Infrastructure Manager")
    
    # AWS credentials input
    st.write("**AWS Credentials:**")
    col1, col2 = st.columns(2)
    
    with col1:
        aws_access_key = st.text_input("AWS Access Key ID", type="password", key="aws_key_2")
        aws_secret_key = st.text_input("AWS Secret Access Key", type="password", key="aws_secret_2")
    
    with col2:
        region = st.selectbox("AWS Region", [
            "ap-south-1", "us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"
        ], key="region_2")
        project_name = st.text_input("Project Name", value="my-app")
    
    if not aws_access_key or not aws_secret_key:
        st.warning("Please enter your AWS credentials to continue.")
        return
    
    try:
        # Initialize AWS clients
        ec2_client = boto3.client(
            'ec2',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )
        
        rds_client = boto3.client(
            'rds',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )
        
        elbv2_client = boto3.client(
            'elbv2',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )
        
        st.success("✅ AWS services connected!")
        
        # AWS Infrastructure Manager class
        class AWSInfraManager:
            def __init__(self, region_name='ap-south-1', project_name='my-app'):
                self.ec2_client = boto3.client(
                    'ec2',
                    aws_access_key_id=aws_access_key,
                    aws_secret_access_key=aws_secret_key,
                    region_name=region_name
                )
                self.rds_client = boto3.client(
                    'rds',
                    aws_access_key_id=aws_access_key,
                    aws_secret_access_key=aws_secret_key,
                    region_name=region_name
                )
                self.elbv2_client = boto3.client(
                    'elbv2',
                    aws_access_key_id=aws_access_key,
                    aws_secret_access_key=aws_secret_key,
                    region_name=region_name
                )
                self.project_name = project_name
            
            def get_project_resources(self):
                """Get all resources for the project"""
                resources = {
                    'ec2_instances': [],
                    'rds_instances': [],
                    'load_balancers': [],
                    'security_groups': [],
                    'volumes': []
                }
                
                try:
                    # EC2 instances
                    ec2_response = self.ec2_client.describe_instances()
                    for reservation in ec2_response['Reservations']:
                        for instance in reservation['Instances']:
                            if any(tag['Key'] == 'Project' and tag['Value'] == self.project_name 
                                   for tag in instance.get('Tags', [])):
                                resources['ec2_instances'].append({
                                    'id': instance['InstanceId'],
                                    'type': instance['InstanceType'],
                                    'state': instance['State']['Name'],
                                    'public_ip': instance.get('PublicIpAddress', 'N/A'),
                                    'launch_time': instance['LaunchTime'].strftime('%Y-%m-%d %H:%M:%S')
                                })
                    
                    # RDS instances
                    rds_response = self.rds_client.describe_db_instances()
                    for db_instance in rds_response['DBInstances']:
                        if db_instance.get('DBInstanceIdentifier', '').startswith(self.project_name):
                            resources['rds_instances'].append({
                                'id': db_instance['DBInstanceIdentifier'],
                                'engine': db_instance['Engine'],
                                'status': db_instance['DBInstanceStatus'],
                                'endpoint': db_instance.get('Endpoint', {}).get('Address', 'N/A')
                            })
                    
                    # Load balancers
                    lb_response = self.elbv2_client.describe_load_balancers()
                    for lb in lb_response['LoadBalancers']:
                        if lb['LoadBalancerName'].startswith(self.project_name):
                            resources['load_balancers'].append({
                                'name': lb['LoadBalancerName'],
                                'type': lb['Type'],
                                'state': lb['State']['Code'],
                                'dns_name': lb['DNSName']
                            })
                    
                    # Security groups
                    sg_response = self.ec2_client.describe_security_groups()
                    for sg in sg_response['SecurityGroups']:
                        if sg['GroupName'].startswith(self.project_name):
                            resources['security_groups'].append({
                                'id': sg['GroupId'],
                                'name': sg['GroupName'],
                                'description': sg['Description'],
                                'vpc_id': sg['VpcId']
                            })
                    
                    # EBS volumes
                    vol_response = self.ec2_client.describe_volumes()
                    for volume in vol_response['Volumes']:
                        if any(tag['Key'] == 'Project' and tag['Value'] == self.project_name 
                               for tag in volume.get('Tags', [])):
                            resources['volumes'].append({
                                'id': volume['VolumeId'],
                                'size': f"{volume['Size']} GB",
                                'type': volume['VolumeType'],
                                'state': volume['State'],
                                'attached_to': volume.get('Attachments', [{}])[0].get('InstanceId', 'N/A')
                            })
                    
                except Exception as e:
                    st.error(f"Error fetching resources: {e}")
                
                return resources
        
        # Initialize Infrastructure Manager
        infra_manager = AWSInfraManager(region, project_name)
        
        # Main interface
        st.write("---")
        
        # Resource overview
        st.subheader("📊 Project Resources Overview")
        
        if st.button("🔄 Refresh Resources"):
            resources = infra_manager.get_project_resources()
            
            # Display resources in tabs
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "🖥️ EC2 Instances", "🗄️ RDS Databases", "⚖️ Load Balancers", 
                "🔒 Security Groups", "💾 EBS Volumes"
            ])
            
            with tab1:
                if resources['ec2_instances']:
                    df = pd.DataFrame(resources['ec2_instances'])
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No EC2 instances found for this project.")
            
            with tab2:
                if resources['rds_instances']:
                    df = pd.DataFrame(resources['rds_instances'])
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No RDS instances found for this project.")
            
            with tab3:
                if resources['load_balancers']:
                    df = pd.DataFrame(resources['load_balancers'])
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No load balancers found for this project.")
            
            with tab4:
                if resources['security_groups']:
                    df = pd.DataFrame(resources['security_groups'])
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No security groups found for this project.")
            
            with tab5:
                if resources['volumes']:
                    df = pd.DataFrame(resources['volumes'])
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No EBS volumes found for this project.")
        
        # Infrastructure management
        st.write("---")
        st.subheader("⚙️ Infrastructure Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Scaling")
            if st.button("🔄 Auto-scaling (Coming Soon)"):
                st.info("Auto-scaling feature will be available soon!")
            
            if st.button("📊 Cost Optimization"):
                st.info("Cost optimization analysis coming soon!")
        
        with col2:
            st.subheader("🔧 Maintenance")
            if st.button("🛠️ Health Check"):
                st.info("Health check feature coming soon!")
            
            if st.button("📋 Backup Management"):
                st.info("Backup management coming soon!")
        
    except Exception as e:
        st.error(f"Failed to connect to AWS services: {e}")
        st.info("Please check your credentials and try again.")

def aws_tools_menu():
    """Main AWS tools menu"""
    st.title("☁️ AWS Tools")
    
    tab1, tab2 = st.tabs([
        "🖥️ EC2 Manager", "🚀 Infrastructure Manager"
    ])
    
    with tab1:
        docker_aws_ec2_manager()
    
    with tab2:
        aws_advanced_infra_manager()
