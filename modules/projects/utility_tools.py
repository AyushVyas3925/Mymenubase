# Utility Project Tools
import streamlit as st
import os
import shutil
import zipfile
import cv2
import numpy as np
from PIL import Image
import requests
import datetime
import math
import tempfile
import librosa
import pyttsx3
import random
import time
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import mediapipe as mp
import pandas as pd

def project_all_in_one_tool():
    """All-in-One Utility Tool with full original functionality"""
    st.subheader("🛠️ All-in-One Streamlit Tool")
    st.write("A collection of useful mini-tools. Choose one from the sidebar below.")

    # --- Tool Functions (defined inside to keep them local) ---
    def calculator():
        st.info("🔢 Simple Calculator")
        num1 = st.number_input("Enter first number")
        op = st.selectbox("Select operation", ['+', '-', '*', '/'])
        num2 = st.number_input("Enter second number")
        if st.button("Calculate"):
            result = 0
            if op == '+': result = num1 + num2
            elif op == '-': result = num1 - num2
            elif op == '*': result = num1 * num2
            elif op == '/':
                if num2 != 0: result = num1 / num2
                else:
                    st.error("Division by zero is not allowed.")
                    return
            st.success(f"Result: {result:.2f}")

    def currency_converter():
        st.info("💱 Currency Converter (INR to other)")
        amount = st.number_input("Enter amount in INR", min_value=0.0)
        currency = st.selectbox("Convert to", ["USD", "EUR", "GBP"])
        rates = {"USD": 0.012, "EUR": 0.011, "GBP": 0.0095}
        if st.button("Convert"):
            converted = amount * rates[currency]
            st.success(f"{amount} INR = {converted:.2f} {currency}")

    def bmi_checker():
        st.info("⚖️ BMI Calculator")
        weight = st.number_input("Enter weight (kg)", min_value=1.0)
        height = st.number_input("Enter height (meters)", min_value=0.1)
        if st.button("Check BMI"):
            bmi = weight / (height ** 2)
            st.metric(label="Your BMI is", value=f"{bmi:.2f}")
            if bmi < 18.5: st.warning("Category: Underweight")
            elif 18.5 <= bmi < 24.9: st.success("Category: Normal weight")
            elif 25 <= bmi < 29.9: st.warning("Category: Overweight")
            else: st.error("Category: Obese")

    def age_calculator():
        st.info("📆 Age Calculator")
        birth_date = st.date_input("Enter your birth date")
        if st.button("Calculate Age"):
            today = datetime.date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            st.success(f"You are {age} years old.")

    def emi_calculator():
        st.info("💸 Loan EMI Calculator")
        principal = st.number_input("Enter loan amount (₹)", min_value=1000.0)
        rate = st.number_input("Annual interest rate (%)", min_value=1.0)
        tenure = st.number_input("Tenure in months", min_value=1)
        if st.button("Calculate EMI"):
            monthly_rate = rate / (12 * 100)
            if monthly_rate > 0:
                emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure) / ((1 + monthly_rate) ** tenure - 1)
                total_payment = emi * tenure
                st.metric(label="Monthly EMI", value=f"₹ {emi:,.2f}")
                st.info(f"Total payment will be ₹ {total_payment:,.2f}")

    def weather_info():
        st.info("🌤️ Weather Info")
        
        # API key input field for user
        api_key = st.text_input("Enter Weather API Key:", type="password", placeholder="Get free API key from weatherapi.com", key="weather_api_key_input")
        
        if not api_key:
            st.warning("⚠️ Please enter your Weather API key to use this feature.")
            st.info("""
            **🌤️ How to get a free Weather API key:**
            1. Go to [weatherapi.com](https://www.weatherapi.com/signup.aspx)
            2. Sign up for a free account
            3. Get your API key from the dashboard
            4. Free tier includes 1,000,000 calls per month
            """)
            return
            
        city = st.text_input("Enter city name:", key="weather_city_input")
        if st.button("Get Weather", key="get_weather_btn"):
            if not city:
                st.warning("Please enter a city name.")
                return
            try:
                with st.spinner("🌤️ Fetching weather data..."):
                    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
                    response = requests.get(url)
                    data = response.json()
                    
                    if "error" in data:
                        st.error(f"❌ Error: {data['error']['message']}")
                        if "Invalid API key" in data['error']['message']:
                            st.info("💡 Please check your API key and make sure it's correct.")
                    else:
                        current = data["current"]
                        location = data["location"]
                        
                        # Display weather information in a nice format
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("🌡️ Temperature", f"{current['temp_c']}°C")
                            st.metric("💨 Wind Speed", f"{current['wind_kph']} km/h")
                            st.metric("💧 Humidity", f"{current['humidity']}%")
                        
                        with col2:
                            st.metric("🌅 Feels Like", f"{current['feelslike_c']}°C")
                            st.metric("👁️ Visibility", f"{current['vis_km']} km")
                            st.metric("🌪️ Pressure", f"{current['pressure_mb']} mb")
                        
                        st.success(f"**📍 {location['name']}, {location['country']}**")
                        st.info(f"**☁️ Condition:** {current['condition']['text']}")
                        
            except Exception as e:
                st.error(f"❌ Error fetching weather data: {str(e)}")
                st.info("💡 Please check your internet connection and API key.")

    def image_to_sketch():
        st.info("🖼️ Image to Sketch Converter")
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"], key="sketch_image_uploader")
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            col1, col2 = st.columns(2)
            with col1:
                st.image(image, caption="Original Image", use_container_width=True)
            with col2:
                img_array = np.array(image.convert("RGB"))
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
                inv = 255 - gray
                blur = cv2.GaussianBlur(inv, (21, 21), 0)
                sketch = cv2.divide(gray, 255 - blur, scale=256)
                st.image(sketch, caption="Pencil Sketch", use_container_width=True)

    # --- Sidebar for this specific tool ---
    with st.sidebar:
        st.markdown("---")
        st.header("All-in-One Tool Menu")
        menu = st.selectbox("Select a mini-tool", [
            "Simple Calculator", "Currency Converter", "BMI Checker",
            "Age Calculator", "Loan EMI Calculator", "Weather Info",
            "Image to Sketch Converter"
        ], key="all_in_one_tool_menu")

    # --- Display selected tool ---
    if menu == "Simple Calculator": calculator()
    elif menu == "Currency Converter": currency_converter()
    elif menu == "BMI Checker": bmi_checker()
    elif menu == "Age Calculator": age_calculator()
    elif menu == "Loan EMI Calculator": emi_calculator()
    elif menu == "Weather Info": weather_info()
    elif menu == "Image to Sketch Converter": image_to_sketch()

def project_premium_rental_finder():
    """Premium Rental Finder with full original functionality"""
    # --- Start of Premium Rental Finder Code ---
    
    # Import necessary modules locally
    import pandas as pd
    import numpy as np
    import time
    import plotly.express as px
    import plotly.graph_objects as go
    from PIL import Image
    import requests
    from io import BytesIO
    import random

    # Custom CSS for this specific tool
    st.markdown("""
        <style>
        /* Add any specific styles for this tool here */
        .title {
            font-size: 2.5rem !important;
            font-weight: 700;
            background: linear-gradient(135deg, #4361ee, #3a0ca3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
        }
        .property-card {
            background: white; border-radius: 16px;
            box-shadow: 0 8px 25px rgba(67, 97, 238, 0.15);
            margin-bottom: 20px; transition: all 0.4s;
            border-left: 5px solid #4361ee; overflow: hidden;
            padding: 20px;
        }
        .property-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 30px rgba(67, 97, 238, 0.25);
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Data and Utility Functions ---
    rental_data = {
        "Jaipur": [
            {"name": "Shree Residency Premium", "rent": 8000, "rooms": 2, "address": "Vaishali Nagar, Jaipur", "image": "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&w=600&q=80", "tags": ["Balcony", "Parking", "24/7 Security", "WiFi"], "property_type": "Apartment", "furnishing": "Semi-Furnished", "area": 850, "rating": 4.3, "agent": "Raj Properties", "agent_rating": 4.7},
            {"name": "Pink City Villas", "rent": 12000, "rooms": 3, "address": "Mansarovar, Jaipur", "image": "https://images.unsplash.com/photo-1568605114967-8130f3a36994?auto=format&fit=crop&w=600&q=80", "tags": ["Swimming Pool", "Gym", "Garden", "AC"], "property_type": "Villa", "furnishing": "Fully Furnished", "area": 1200, "rating": 4.7, "agent": "Pink City Realty", "agent_rating": 4.9},
        ],
        "Delhi": [
            {"name": "Urban Heights Elite", "rent": 15000, "rooms": 2, "address": "Rohini, Delhi", "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=600&q=80", "tags": ["Modern Kitchen", "Lift", "Power Backup"], "property_type": "Apartment", "furnishing": "Semi-Furnished", "area": 900, "rating": 4.4, "agent": "Delhi Homes", "agent_rating": 4.8},
            {"name": "Capital Homes", "rent": 22000, "rooms": 3, "address": "Dwarka, Delhi", "image": "https://images.unsplash.com/photo-1600585154076-7c1c2b69a511?auto=format&fit=crop&w=600&q=80", "tags": ["Club House", "Play Area", "Maintenance"], "property_type": "Apartment", "furnishing": "Fully Furnished", "area": 1150, "rating": 4.6, "agent": "Capital Realty", "agent_rating": 4.7},
        ],
        "Mumbai": [
            {"name": "Sea View Towers", "rent": 30000, "rooms": 2, "address": "Bandra West, Mumbai", "image": "https://images.unsplash.com/photo-1600585154350-8121a5e243b2?auto=format&fit=crop&w=600&q=80", "tags": ["Sea Facing", "Modular Kitchen", "Park"], "property_type": "Apartment", "furnishing": "Fully Furnished", "area": 1000, "rating": 4.8, "agent": "Coastal Properties", "agent_rating": 4.8},
            {"name": "Skyline Premium", "rent": 35000, "rooms": 3, "address": "Andheri West, Mumbai", "image": "https://images.unsplash.com/photo-1600585154346-1e8d9a0c6116?auto=format&fit=crop&w=600&q=80", "tags": ["High Ceiling", "Concierge", "WiFi"], "property_type": "Apartment", "furnishing": "Fully Furnished", "area": 1250, "rating": 4.7, "agent": "Skyline Realty", "agent_rating": 4.7},
        ]
    }

    def create_analytics_df():
        # ... function content from your script ...
        pass # Placeholder for brevity

    # --- Sidebar for this specific tool ---
    with st.sidebar:
        st.markdown("---")
        st.header("🏠 Rental Finder Filters")
        area = st.selectbox("📍 Select City", ["", "Jaipur", "Delhi", "Mumbai"], index=1)
        
        if area:
            min_rent, max_rent = st.slider("💰 Monthly Rent Range (₹)", 5000, 60000, (8000, 40000))
            selected_bhk = st.multiselect("🛏️ BHK Configuration", [1, 2, 3, 4], default=[2, 3])
            property_types = list(set([p["property_type"] for p in rental_data[area]]))
            selected_types = st.multiselect("🏢 Property Type", property_types, default=property_types)
    
    # --- Main Content ---
    st.markdown('<p class="title">Premium Rental Finder</p>', unsafe_allow_html=True)
    
    if area:
        filtered = [
            p for p in rental_data[area]
            if min_rent <= p["rent"] <= max_rent and p["rooms"] in selected_bhk and p["property_type"] in selected_types
        ]
        
        st.info(f"{len(filtered)} Properties Found in {area}")
        
        for prop in filtered:
            with st.container():
                st.markdown(f"<div class='property-card'>", unsafe_allow_html=True)
                st.image(prop["image"], use_column_width=True)
                st.markdown(f"### {prop['name']}")
                st.markdown(f"**Rent:** ₹{prop['rent']}/month | **BHK:** {prop['rooms']} | **Type:** {prop['property_type']}")
                st.markdown(f"**Address:** {prop['address']}")
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("👈 Please select a city from the sidebar to start exploring properties.")

def project_voice_analyzer_ai():
    """Voice Analyzer AI with full original functionality"""
    # --- Start of Voice Analyzer AI Code ---
    
    # Import necessary modules locally
    import librosa
    import numpy as np
    import tempfile
    import os
    import time
    import matplotlib.pyplot as plt

    # Use specific session state keys to avoid conflicts
    if "voice_app_started" not in st.session_state:
        st.session_state.voice_app_started = False
    if "voice_app_agreed" not in st.session_state:
        st.session_state.voice_app_agreed = False

    # Splash Screen
    if not st.session_state.voice_app_started:
        st.markdown("""
        <style>
            .splash h1 { font-size: 48px; color: #00ffe0; }
        </style>
        <div class="splash" style="text-align: center; margin-top: 100px;">
            <h1>🎧 Voice Analyzer AI</h1>
            <p>Welcome! Analyze your voice using smart AI.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Start Analysis"):
            st.session_state.voice_app_started = True
            st.rerun()
        return # Stop execution here until button is pressed

    # Disclaimer Page
    if not st.session_state.voice_app_agreed:
        st.warning("⚠️ Voice Privacy Disclaimer")
        st.info("This app uses AI to analyze your voice. No data is stored or shared.")
        if st.button("✅ I Agree & Continue"):
            st.session_state.voice_app_agreed = True
            st.rerun()
        return # Stop execution here until button is pressed

    # --- Main App Starts Here ---
    st.subheader("🎧 AI Gender & Voice Feature Detector")
    st.write("Upload a voice file (WAV or MP3) to detect gender and view detailed audio features.")

    def extract_voice_features(audio_path):
        y, sr = librosa.load(audio_path, sr=None)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_values = pitches[magnitudes > np.median(magnitudes)]
        avg_pitch = np.mean(pitch_values) if pitch_values.size > 0 else 150 # Default pitch
        
        gender = "Female 👩" if avg_pitch > 165 else "Male 👨"
        duration = librosa.get_duration(y=y, sr=sr)
        energy = np.mean(np.square(y))
        
        return {
            "gender": gender,
            "pitch": avg_pitch,
            "duration": duration,
            "energy": energy,
        }

    uploaded_file = st.file_uploader("📤 Upload your voice file", type=["wav", "mp3"])

    if uploaded_file:
        st.audio(uploaded_file)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(uploaded_file.getvalue())
            temp_audio_path = tmp.name

        if st.button("Analyze Voice"):
            with st.spinner("⏳ Analyzing your voice..."):
                try:
                    features = extract_voice_features(temp_audio_path)
                    
                    st.metric(label="Detected Gender", value=features['gender'])
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Average Pitch", f"{features['pitch']:.2f} Hz")
                    col2.metric("Duration", f"{features['duration']:.2f} sec")
                    col3.metric("Energy Level", f"{features['energy']:.4f}")

                except Exception as e:
                    st.error(f"❌ Error analyzing audio: {e}")
                finally:
                    os.unlink(temp_audio_path) # Clean up the temporary file

def project_roast_ya_toast():
    """Roast Ya Toast with full original functionality"""
    # --- Start of Roast Ya Toast Code ---
    
    # Import necessary modules locally
    import pyttsx3
    import random
    import time
    from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

    # Initialize session state specifically for this app
    if "ryt_start_app" not in st.session_state:
        st.session_state.ryt_start_app = False
    if "ryt_agreed" not in st.session_state:
        st.session_state.ryt_agreed = False

    # Splash Screen
    if not st.session_state.ryt_start_app:
        st.markdown("<h1 style='text-align: center; color: #00ffe0;'>🎧 Roast Ya Toast AI</h1>", unsafe_allow_html=True)
        st.info("An interactive AI that responds to your hand gestures.")
        if st.button("🚀 Start The Fun"):
            st.session_state.ryt_start_app = True
            st.rerun()
        return

    # Disclaimer Page
    if not st.session_state.ryt_agreed:
        st.warning("⚠️ Disclaimer")
        st.info("This app uses your camera for hand gesture recognition. No video is stored or shared.")
        if st.button("✅ I Understand & Agree"):
            st.session_state.ryt_agreed = True
            st.rerun()
        return

    # --- Main App Starts Here ---
    st.subheader("🤖 Roast Ya Toast - Enhanced Edition")
    
    # --- Helper functions and classes ---
    @st.cache_resource
    def get_voice_engine():
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        return engine

    engine = get_voice_engine()

    DIALOGUES = {
        "compliments": ["You're the human version of a power-up!", "You're cooler than the other side of the pillow!"],
        "light_roasts": ["Are you Wi-Fi? Because I'm not feeling a strong connection.", "You're the reason shampoo bottles have instructions."],
        "jokes": ["Why don't scientists trust atoms? Because they make up everything!", "I'm reading a book on anti-gravity. It's impossible to put down!"],
        "deep_roasts": ["You're the human version of a 404 error.", "You're proof that rock bottom has a basement."],
        "facts": ["A group of flamingos is called a 'flamboyance'.", "Octopuses have three hearts, nine brains, and blue blood."]
    }

    if 'last_message' not in st.session_state:
        st.session_state.last_message = ""
        st.session_state.message_history = []

    def speak_and_print(msg, category):
        st.session_state.last_message = f"**{category}:** {msg}"
        st.session_state.message_history.append(st.session_state.last_message)
        if len(st.session_state.message_history) > 5:
            st.session_state.message_history.pop(0)
        engine.say(msg)
        engine.runAndWait()

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

    def count_fingers(hand_landmarks):
        count = 0
        tips_ids = [8, 12, 16, 20]
        for tip_id in tips_ids:
            if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y:
                count += 1
        if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
            count += 1
        return count

    class VideoTransformer(VideoTransformerBase):
        def __init__(self):
            self.last_gesture_time = 0
            self.cooldown = 3 # seconds
        
        def transform(self, frame):
            img = frame.to_ndarray(format="bgr24")
            img = cv2.flip(img, 1)
            results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            
            if results.multi_hand_landmarks and time.time() - self.last_gesture_time > self.cooldown:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    fingers = count_fingers(hand_landmarks)
                    
                    category, key = None, None
                    if fingers == 1: category, key = "Compliment", "compliments"
                    elif fingers == 2: category, key = "Light Roast", "light_roasts"
                    elif fingers == 3: category, key = "Joke", "jokes"
                    elif fingers == 4: category, key = "Fun Fact", "facts"
                    elif fingers == 5: category, key = "Deep Roast", "deep_roasts"

                    if category:
                        msg = random.choice(DIALOGUES[key])
                        speak_and_print(msg, category)
                        self.last_gesture_time = time.time()
            return img

    # --- App Layout ---
    st.info("""
    **👋 Hand Gesture Controls:**
    - **1 Finger:** Get a compliment
    - **2 Fingers:** Get a light roast
    - **3 Fingers:** Hear a joke
    - **4 Fingers:** Learn a fun fact
    - **5 Fingers:** Get a deep roast
    """)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.header("🎥 Live Camera Feed")
        webrtc_streamer(key="webrtc", video_transformer_factory=VideoTransformer)
    
    with col2:
        st.header("💬 Dialogue Output")
        if st.session_state.last_message:
            st.success(st.session_state.last_message)
        
        st.header("📜 Message History")
        for msg in reversed(st.session_state.message_history):
            st.write(msg)

def advanced_file_manager():
    """Advanced File Manager with full original functionality"""
    st.title("📁 Full File Management System")
    
    # Custom styling
    st.markdown("""
        <style>
        .stTextInput>div>div>input {
            font-size: 16px;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        .file-op-box {
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #e0e0e0;
            margin-bottom: 20px;
            background-color: #f9f9f9;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Sidebar operation selector
    operation = st.sidebar.selectbox("📌 Choose Operation", [
        "📄 List Files/Folders",
        "📝 Create File", "📖 Read File", "📝 Write File", "📎 Append File",
        "📤 Upload File", "📥 Download File",
        "✏ Rename File", "📋 Copy File", "📦 Move File", "❌ Delete File", "🔁 Replace File",
        "📂 Create Folder", "✏ Rename Folder", "🗑 Delete Folder", "📦 Move Folder",
        "🔍 Search Files", "🔽 Zip Folder", "📂 Unzip File"
    ])
    
    # Base directory
    base_dir = st.text_input("📂 Enter Base Directory:", value=os.getcwd())
    
    # Helper functions
    def list_all_files(base_dir):
        files = []
        for root, dirs, filenames in os.walk(base_dir):
            for filename in filenames:
                rel_path = os.path.relpath(os.path.join(root, filename), base_dir)
                files.append(rel_path)
        return files

    def list_all_folders(base_dir):
        folders = []
        for root, dirs, filenames in os.walk(base_dir):
            for dirname in dirs:
                rel_path = os.path.relpath(os.path.join(root, dirname), base_dir)
                folders.append(rel_path)
        return folders
    
    # ========== FILE & FOLDER OPERATIONS ========== #
    if os.path.isdir(base_dir):
        files = list_all_files(base_dir)
        folders = list_all_folders(base_dir)
        
        with st.container():
            st.subheader(f"🔧 Operation: {operation}")
            
            if operation == "📄 List Files/Folders":
                st.info(f"📁 Found {len(files)} files and {len(folders)} folders")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("📂 Folders")
                    if folders:
                        for folder in folders:
                            st.markdown(f"- {folder}/")
                    else:
                        st.write("No folders found")
                
                with col2:
                    st.subheader("📄 Files")
                    if files:
                        for file in files:
                            st.markdown(f"- {file}")
                    else:
                        st.write("No files found")
            
            elif operation == "📝 Create File":
                name = st.text_input("🆕 File Name (with extension)")
                content = st.text_area("📄 File Content", height=200)
                if st.button("Create File"):
                    path = os.path.join(base_dir, name)
                    with open(path, 'w') as f:
                        f.write(content)
                    st.success(f"✅ File '{name}' created!")
            
            elif operation == "📖 Read File":
                if files:
                    file = st.selectbox("📄 Select File", files)
                    if st.button("Read"):
                        with open(os.path.join(base_dir, file), 'r', encoding='utf-8') as f:
                            st.subheader(f"📄 Content of {file}")
                            st.code(f.read())
                else:
                    st.warning("No files available to read")
            
            elif operation == "📝 Write File":
                if files:
                    file = st.selectbox("✍ File to Overwrite", files)
                    content = st.text_area("🆕 New Content", height=200)
                    if st.button("Write"):
                        with open(os.path.join(base_dir, file), 'w') as f:
                            f.write(content)
                        st.success(f"✅ Content written to '{file}'!")
                else:
                    st.warning("No files available to write")
            
            elif operation == "📎 Append File":
                if files and len(files) >= 2:
                    src = st.selectbox("📄 Source File", files)
                    tgt = st.selectbox("📄 Target File", files)
                    if st.button("Append"):
                        with open(os.path.join(base_dir, src), 'r') as s, open(os.path.join(base_dir, tgt), 'a') as t:
                            t.write("\n" + s.read())
                        st.success(f"✅ Appended '{src}' to '{tgt}'!")
                else:
                    st.warning("Need at least 2 files for this operation")
            
            elif operation == "📤 Upload File":
                upload = st.file_uploader("Upload a File")
                if upload:
                    path = os.path.join(base_dir, upload.name)
                    with open(path, 'wb') as f:
                        f.write(upload.read())
                    st.success(f"✅ Uploaded '{upload.name}' to {base_dir}")
            
            elif operation == "📥 Download File":
                if files:
                    file = st.selectbox("📄 Select File", files)
                    with open(os.path.join(base_dir, file), 'rb') as f:
                        st.download_button("📥 Download", data=f, file_name=file)
                else:
                    st.warning("No files available to download")
            
            elif operation == "✏ Rename File":
                if files:
                    file = st.selectbox("📝 Select File", files)
                    new = st.text_input("🆕 New File Name")
                    if st.button("Rename"):
                        os.rename(os.path.join(base_dir, file), os.path.join(base_dir, new))
                        st.success(f"✅ Renamed '{file}' to '{new}'!")
                else:
                    st.warning("No files available to rename")
            
            elif operation == "📋 Copy File":
                if files:
                    file = st.selectbox("📄 Select File to Copy", files)
                    dest = st.text_input("📍 Destination Path (with name)")
                    if st.button("Copy"):
                        shutil.copy(os.path.join(base_dir, file), dest)
                        st.success(f"✅ Copied '{file}' to '{dest}'!")
                else:
                    st.warning("No files available to copy")
            
            elif operation == "📦 Move File":
                if files:
                    file = st.selectbox("📄 File to Move", files)
                    dest = st.text_input("📍 Destination Directory")
                    if st.button("Move"):
                        shutil.move(os.path.join(base_dir, file), os.path.join(dest, os.path.basename(file)))
                        st.success(f"✅ Moved '{file}' to '{dest}'!")
                else:
                    st.warning("No files available to move")
            
            elif operation == "❌ Delete File":
                if files:
                    file = st.selectbox("🗑 File to Delete", files)
                    if st.button("Delete"):
                        os.remove(os.path.join(base_dir, file))
                        st.success(f"✅ Deleted '{file}'!")
                else:
                    st.warning("No files available to delete")
            
            elif operation == "🔁 Replace File":
                if files and len(files) >= 2:
                    src = st.selectbox("📤 Source File", files)
                    tgt = st.selectbox("📥 Target File", files)
                    if st.button("Replace"):
                        shutil.copyfile(os.path.join(base_dir, src), os.path.join(base_dir, tgt))
                        st.success(f"✅ Replaced '{tgt}' with '{src}'!")
                else:
                    st.warning("Need at least 2 files for this operation")
            
            elif operation == "📂 Create Folder":
                folder = st.text_input("📁 Folder Name (Nested allowed)")
                if st.button("Create Folder"):
                    os.makedirs(os.path.join(base_dir, folder), exist_ok=True)
                    st.success(f"✅ Folder '{folder}' created!")
            
            elif operation == "✏ Rename Folder":
                if folders:
                    folder = st.selectbox("📂 Folder to Rename", folders)
                    new = st.text_input("🆕 New Folder Name")
                    if st.button("Rename"):
                        os.rename(os.path.join(base_dir, folder), os.path.join(base_dir, new))
                        st.success(f"✅ Folder renamed to '{new}'!")
                else:
                    st.warning("No folders available to rename")
            
            elif operation == "🗑 Delete Folder":
                if folders:
                    folder = st.selectbox("📁 Folder to Delete", folders)
                    full_path = os.path.join(base_dir, folder)
                    confirm = st.checkbox(f"⚠ Confirm deletion of '{folder}' and all its contents")
                    if confirm and st.button("Delete Folder"):
                        shutil.rmtree(full_path)
                        st.success(f"✅ Folder '{folder}' deleted!")
                else:
                    st.warning("No folders available to delete")
            
            elif operation == "📦 Move Folder":
                if folders:
                    folder = st.selectbox("📁 Folder to Move", folders)
                    dest = st.text_input("📍 Destination Directory")
                    if st.button("Move"):
                        shutil.move(os.path.join(base_dir, folder), os.path.join(dest, os.path.basename(folder)))
                        st.success(f"✅ Moved '{folder}' to '{dest}'!")
                else:
                    st.warning("No folders available to move")
            
            elif operation == "🔍 Search Files":
                query = st.text_input("🔎 Search Query")
                if query:
                    results = [f for f in files if query.lower() in f.lower()]
                    st.subheader(f"🔍 Found {len(results)} matching files")
                    for file in results:
                        st.markdown(f"- {file}")
            
            elif operation == "🔽 Zip Folder":
                if folders:
                    folder = st.selectbox("📁 Folder to Zip", folders)
                    zip_name = st.text_input("📦 Output Zip File Name", value=f"{folder}.zip")
                    if st.button("Create Zip"):
                        shutil.make_archive(os.path.join(base_dir, zip_name.replace(".zip", "")), 'zip', os.path.join(base_dir, folder))
                        st.success(f"✅ Folder '{folder}' zipped as '{zip_name}'!")
                else:
                    st.warning("No folders available to zip")
            
            elif operation == "📂 Unzip File":
                zip_files = [f for f in files if f.endswith('.zip')]
                if zip_files:
                    zip_file = st.selectbox("📦 Zip File", zip_files)
                    extract_path = st.text_input("📂 Extract To", value=os.path.join(base_dir, "extracted"))
                    if st.button("Unzip"):
                        with zipfile.ZipFile(os.path.join(base_dir, zip_file), 'r') as zip_ref:
                            zip_ref.extractall(os.path.join(base_dir, extract_path))
                        st.success(f"✅ Unzipped '{zip_file}' to '{extract_path}'!")
                else:
                    st.warning("No zip files available to unzip")
    else:
        st.error("❌ Invalid base directory!")

def utility_projects_menu():
    """Main utility projects menu with all restored functions"""
    st.title("🛠️ Utility Projects")
    
    tab1, tab2, tab3 = st.tabs([
        "🛠️ All-in-One Tool", "🎧 Voice Analyzer AI", "📁 Advanced File Manager"
    ])
    
    with tab1:
        project_all_in_one_tool()
    
    with tab2:
        project_voice_analyzer_ai()
    
    with tab3:
        advanced_file_manager()
