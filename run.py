

import subprocess
import sys
import os

def main():
    """Main launcher function"""
    print("🚀 Starting mymenubase")
    print("📁 Working directory:", os.getcwd())
    
    try:
        # Check if streamlit is installed
        import streamlit
        print("✅ Streamlit is available")
        
        # Run the main application
        print("🌐 Launching application...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "main.py"])
        
    except ImportError:
        print("❌ Streamlit is not installed!")
        print("📦 Installing dependencies...")
        
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dependencies installed successfully!")
            print("🌐 Launching application...")
            subprocess.run([sys.executable, "-m", "streamlit", "run", "main.py"])
        except Exception as e:
            print(f"❌ Error installing dependencies: {e}")
            print("💡 Please run: pip install -r requirements.txt")
            sys.exit(1)

if __name__ == "__main__":
    main()
