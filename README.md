# Task Machine Pro - All-in-One Utility Toolkit

A comprehensive Streamlit application providing Linux tools, Python utilities, Machine Learning capabilities, and DevOps tools in a single interface.

## 🏗️ Project Structure

```
jaisyh_manu/
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── main.py                  # Main application entry point
├── config/
│   ├── __init__.py
│   ├── settings.py          # Configuration settings
│   └── constants.py         # Application constants
├── core/
│   ├── __init__.py
│   ├── app.py               # Main Streamlit app configuration
│   └── utils.py             # Utility functions
├── modules/
│   ├── __init__.py
│   ├── linux/               # Linux tools module
│   │   ├── __init__.py
│   │   ├── commands.py      # Basic Linux commands
│   │   ├── disk_tools.py    # Disk management tools
│   │   ├── network_tools.py # Networking tools
│   │   └── system_tools.py  # System monitoring tools
│   ├── python/              # Python utilities module
│   │   ├── __init__.py
│   │   ├── communication.py # Email, SMS, calls
│   │   ├── file_tools.py    # File processing tools
│   │   ├── web_tools.py     # Web scraping, search
│   │   └── media_tools.py   # Image, video processing
│   ├── machine_learning/    # ML tools module
│   │   ├── __init__.py
│   │   ├── calculators.py   # EMI, salary predictors
│   │   ├── data_analysis.py # Data analysis tools
│   │   └── models.py        # ML model implementations
│   ├── devops/              # DevOps tools module
│   │   ├── __init__.py
│   │   ├── docker_tools.py  # Docker management
│   │   ├── aws_tools.py     # AWS management
│   │   └── jenkins_tools.py # Jenkins tools
│   ├── projects/            # Project implementations
│   │   ├── __init__.py
│   │   ├── hand_gestures.py # Hand gesture recognition
│   │   ├── social_media.py  # Social media tools
│   │   └── utilities.py     # General utilities
│   └── javascript/          # JavaScript demos
│       ├── __init__.py
│       ├── demos.py         # JavaScript demonstrations
│       └── calculators.py   # JS calculator implementations
├── static/                  # Static assets
│   ├── css/
│   │   └── styles.css       # Custom CSS styles
│   └── js/
│       └── scripts.js       # Custom JavaScript
└── data/                    # Data files and cache
    └── .gitkeep
```

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   streamlit run main.py
   ```

3. **Open your browser** and navigate to `http://localhost:8501`

## 🔧 Features

### Linux Tools
- Basic command execution
- Disk usage analysis
- Network configuration
- System monitoring
- LVM management
- NFS mounting

### Python Utilities
- Email and SMS sending
- File processing (PDF, images)
- Web scraping
- QR code generation
- API integrations

### Machine Learning
- EMI calculators
- Salary prediction
- Student performance analysis
- Data visualization

### DevOps Tools
- Docker container management
- AWS EC2 management
- Jenkins automation
- Infrastructure management

### Projects
- Hand gesture recognition
- Social media automation
- Voice analysis
- All-in-one utilities

## 📁 Module Organization

Each module is self-contained with its own `__init__.py` file and specific functionality:

- **`core/`**: Core application logic and configuration
- **`modules/`**: Feature-specific modules organized by domain
- **`static/`**: CSS and JavaScript assets
- **`data/`**: Data storage and cache files

## 🎯 Benefits of This Structure

1. **Maintainability**: Code is organized by functionality
2. **Scalability**: Easy to add new modules and features
3. **Reusability**: Functions can be imported across modules
4. **Testing**: Each module can be tested independently
5. **Documentation**: Clear separation makes code easier to understand

## 🔄 Migration Notes

The original `menu2.py` file has been restructured into:
- **Main application logic** → `main.py`
- **Linux tools** → `modules/linux/`
- **Python utilities** → `modules/python/`
- **ML tools** → `modules/machine_learning/`
- **DevOps tools** → `modules/devops/`
- **Project implementations** → `modules/projects/`
- **JavaScript demos** → `modules/javascript/`

## 📝 Usage Examples

### Adding a New Linux Tool
```python
# In modules/linux/commands.py
def new_linux_tool():
    st.subheader("New Linux Tool")
    # Your tool implementation here
```

### Adding a New Python Utility
```python
# In modules/python/file_tools.py
def new_python_utility():
    st.subheader("New Python Utility")
    # Your utility implementation here
```

## 🤝 Contributing

1. Follow the existing module structure
2. Add your functions to the appropriate module
3. Update the main navigation if needed
4. Test your changes before submitting

## 📄 License

This project is open source and available under the MIT License.
