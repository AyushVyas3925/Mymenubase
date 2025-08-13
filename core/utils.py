# Utility functions for the application
import os
import subprocess
import streamlit as st

def run_command(command):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else result.stderr.strip()
    except Exception as e:
        return f"Error: {e}"

def list_files(directory="."):
    """List all files in a directory"""
    try:
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    except Exception as e:
        return f"Error: {e}"

def list_directories(directory="."):
    """List all directories in a directory"""
    try:
        return [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    except Exception as e:
        return f"Error: {e}"

def get_file_info(filepath):
    """Get information about a file"""
    try:
        stat = os.stat(filepath)
        return {
            "size": stat.st_size,
            "modified": stat.st_mtime,
            "permissions": oct(stat.st_mode)[-3:]
        }
    except Exception as e:
        return f"Error: {e}"

def safe_execute(func, *args, **kwargs):
    """Safely execute a function with error handling"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        st.error(f"Error executing {func.__name__}: {e}")
        return None

def format_bytes(bytes_value):
    """Format bytes into human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"

def validate_input(value, validation_type="text"):
    """Validate user input based on type"""
    if validation_type == "email":
        return "@" in value and "." in value
    elif validation_type == "phone":
        return value.replace("+", "").replace("-", "").replace(" ", "").isdigit()
    elif validation_type == "url":
        return value.startswith(("http://", "https://"))
    return True
