# Hand Gesture Project Tools
import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import time
import os
import pygame
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
import av

def project_hand_gesture_music():
    """Hand Gesture Music Controller"""
    # Custom CSS styling
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # Custom HTML/CSS with colorful decorations
    st.markdown("""
    <style>
        /* Vibrant gradient background */
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        /* Glowing title effect */
        .title-text {
            font-family: 'Arial', sans-serif;
            color: white;
            text-shadow: 0 0 10px #ff00ff, 
                         0 0 20px #ff00ff, 
                         0 0 30px #ff00ff;
            animation: glow 2s ease-in-out infinite alternate;
        }
        
        @keyframes glow {
            from {
                text-shadow: 0 0 10px #ff00ff, 
                             0 0 20px #ff00ff, 
                             0 0 30px #ff00ff;
            }
            to {
                text-shadow: 0 0 15px #ff00ff, 
                             0 0 25px #ff00ff, 
                             0 0 35px #ff00ff;
            }
        }
        
        /* Neon buttons */
        .stButton>button {
            border: 2px solid #00ffff;
            border-radius: 25px;
            padding: 12px 28px;
            background: rgba(0, 0, 0, 0.3);
            color: #00ffff;
            font-weight: bold;
            font-size: 16px;
            transition: all 0.3s;
            box-shadow: 0 0 10px #00ffff;
        }
        
        .stButton>button:hover {
            background: rgba(0, 255, 255, 0.2);
            transform: scale(1.05);
            box-shadow: 0 0 20px #00ffff;
        }
        
        /* Song display with pulse animation */
        .song-title {
            font-size: 1.4em;
            color: #ffcc00;
            text-shadow: 0 0 5px #ff6600;
            font-weight: bold;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        /* Status box with gradient border */
        .status-box {
            background: rgba(0, 0, 0, 0.4);
            border-radius: 15px;
            padding: 15px;
            margin: 15px 0;
            border-left: 5px solid;
            border-image: linear-gradient(to bottom, #ff00ff, #00ffff) 1;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        
        /* Animated volume bar */
        .volume-container {
            margin: 20px 0;
        }
        
        .volume-bar {
            height: 15px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            margin: 10px 0;
            overflow: hidden;
        }
        
        .volume-fill {
            height: 100%;
            background: linear-gradient(90deg, #ff5e62, #ff9966);
            border-radius: 10px;
            transition: width 0.5s;
            box-shadow: 0 0 10px #ff9966;
        }
        
        /* Gesture instructions with floating effect */
        .gesture-instruction {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 15px;
            margin: 15px 0;
            backdrop-filter: blur(5px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s;
        }
        
        .gesture-instruction:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }
        
        /* Camera feed styling */
        .stImage>img {
            border-radius: 15px;
            border: 3px solid #00ffff;
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
            transition: all 0.3s;
        }
        
        .stImage>img:hover {
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.8);
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(#00ffff, #ff00ff);
            border-radius: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Fancy title with HTML and glowing effect
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 class="title-text">🎶 Hand Gesture Music Maestro</h1>
        <p style="color: #e0e0e0; font-size: 18px;">Control your music with magical hand gestures ✨</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize music system
    try:
        pygame.mixer.init()
        volume = 0.5
        pygame.mixer.music.set_volume(volume)
    except pygame.error as e:
        st.error(f"❌ Failed to initialize audio system: {e}")
        st.stop()

    # Load music files
    song_folder = "song"
    if not os.path.exists(song_folder):
        os.makedirs(song_folder)
        st.error(f"❌ Created 'song' folder. Please add some MP3 files to it.")
        st.stop()

    song_list = sorted([file for file in os.listdir(song_folder) if file.endswith(".mp3")])
    if not song_list:
        st.error("No MP3 files found in the 'song' folder. Please add some music files.")
        st.stop()

    # Mediapipe init
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1)
    mp_drawing = mp.solutions.drawing_utils

    # State variables
    if "run_camera" not in st.session_state:
        st.session_state.run_camera = False
    if "volume" not in st.session_state:
        st.session_state.volume = 0.5
    if "song_index" not in st.session_state:
        st.session_state.song_index = 0
    if "status" not in st.session_state:
        st.session_state.status = "Ready"
    if "current_song" not in st.session_state:
        st.session_state.current_song = "No song selected"

    # Music control functions
    def play_song(index):
        try:
            pygame.mixer.music.load(os.path.join(song_folder, song_list[index]))
            pygame.mixer.music.play()
            st.session_state.current_song = song_list[index]
            return f"▶ Playing: {song_list[index]}"
        except (pygame.error, IndexError) as e:
            st.error(f"❌ Error playing song: {e}")
            return "❌ Error"

    def stop_song():
        try:
            pygame.mixer.music.stop()
            st.session_state.current_song = "No song selected"
        except pygame.error:
            pass

    def pause_song():
        try:
            pygame.mixer.music.pause()
        except pygame.error:
            pass

    def unpause_song():
        try:
            pygame.mixer.music.unpause()
        except pygame.error:
            pass

    # Finger counter
    def count_fingers(landmarks):
        count = 0
        if landmarks[8].y < landmarks[6].y: count += 1   # Index
        if landmarks[12].y < landmarks[10].y: count += 1 # Middle
        if landmarks[16].y < landmarks[14].y: count += 1 # Ring
        if landmarks[20].y < landmarks[18].y: count += 1 # Pinky
        return count

    # Gesture instructions with emoji icons
    with st.expander("✨ Gesture Controls Guide", expanded=True):
        st.markdown("""
        <div class="gesture-instruction">
            <p style="font-size: 18px;"><span style="font-size: 24px;">👊</span> <b>Fist (0 fingers)</b> - Mute volume</p>
            <p style="font-size: 18px;"><span style="font-size: 24px;">☝️</span> <b>1 Finger</b> - Play current song</p>
            <p style="font-size: 18px;"><span style="font-size: 24px;">✌️</span> <b>2 Fingers</b> - Volume Down</p>
            <p style="font-size: 18px;"><span style="font-size: 24px;">🤟</span> <b>3 Fingers</b> - Next Song</p>
            <p style="font-size: 18px;"><span style="font-size: 24px;">✋</span> <b>4 Fingers</b> - Volume Up</p>
            <p style="font-size: 18px;"><span style="font-size: 24px;">🖐️</span> <b>5 Fingers</b> - Stop Music</p>
        </div>
        """, unsafe_allow_html=True)

    # Current song and volume display with animations
    st.markdown(f"""
    <div class="volume-container">
        <div class="song-title">🎵 Now Playing: {st.session_state.current_song}</div>
        <div style="margin: 15px 0; font-size: 16px;">🔊 Volume Level</div>
        <div class="volume-bar">
            <div class="volume-fill" style="width: {st.session_state.volume * 100}%;"></div>
        </div>
        <div style="text-align: right; margin-top: 5px; font-size: 16px;">{int(st.session_state.volume * 100)}%</div>
    </div>
    """, unsafe_allow_html=True)

    # Camera control buttons with neon effect
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        if st.button("📷 Start Camera", key="start_cam"):
            st.session_state.run_camera = True
    with col2:
        if st.button("⏸️ Pause Music", key="pause_music"):
            pause_song()
            st.session_state.status = "⏸️ Paused"
    with col3:
        if st.button("🛑 Stop Camera", key="stop_cam"):
            st.session_state.run_camera = False
            stop_song()

    # Status box with gradient border
    status_placeholder = st.empty()

    # Camera feed with glowing border
    FRAME_WINDOW = st.image([], use_column_width=True)

    # Main loop
    cap = None
    try:
        if st.session_state.run_camera:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                st.error("❌ Could not open camera")
                st.session_state.run_camera = False
                st.stop()

            while st.session_state.run_camera:
                ret, frame = cap.read()
                if not ret:
                    st.warning("⚠️ Failed to grab frame")
                    break

                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(rgb)

                if results.multi_hand_landmarks:
                    for lm in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(frame, lm, mp_hands.HAND_CONNECTIONS)
                        fingers = count_fingers(lm.landmark)

                        # Gesture-based music control
                        if fingers == 0:
                            pygame.mixer.music.set_volume(0.0)
                            st.session_state.status = "🔇 Muted"
                        elif fingers == 1:
                            st.session_state.status = play_song(st.session_state.song_index)
                        elif fingers == 2:
                            st.session_state.volume = max(0.0, st.session_state.volume - 0.1)
                            pygame.mixer.music.set_volume(st.session_state.volume)
                            st.session_state.status = f"🔉 Volume Down: {int(st.session_state.volume * 100)}%"
                        elif fingers == 3:
                            st.session_state.song_index = (st.session_state.song_index + 1) % len(song_list)
                            st.session_state.status = play_song(st.session_state.song_index)
                        elif fingers == 4:
                            st.session_state.volume = min(1.0, st.session_state.volume + 0.1)
                            pygame.mixer.music.set_volume(st.session_state.volume)
                            st.session_state.status = f"🔊 Volume Up: {int(st.session_state.volume * 100)}%"
                        elif fingers == 5:
                            stop_song()
                            st.session_state.status = "⏹️ Stopped"

                        # Display text on frame with colorful styling
                        cv2.putText(frame, f"Fingers: {fingers}", (10, 60), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 105, 180), 2)  # Hot pink
                        cv2.putText(frame, f"{st.session_state.status}", (10, 100), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)  # Cyan
                        cv2.putText(frame, f"Volume: {int(st.session_state.volume * 100)}%", (10, 140), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)  # Yellow

                FRAME_WINDOW.image(frame, channels="BGR")
                
                # Update status with HTML styling
                status_placeholder.markdown(f"""
                <div class="status-box">
                    <strong style="font-size: 18px; color: #00ffff;">Status:</strong> 
                    <span style="font-size: 16px;">{st.session_state.status}</span>
                </div>
                """, unsafe_allow_html=True)
                
                time.sleep(0.05)

    finally:
        if cap is not None:
            cap.release()
        hands.close()

    # Footer with colorful gradient
    st.markdown("""
    <div style="text-align: center; margin-top: 30px; padding: 15px; 
                background: linear-gradient(90deg, #ff00ff, #00ffff);
                border-radius: 10px;">
        <p style="color: white; font-size: 14px;">✨ Hand Gesture Music Controller ✨</p>
    </div>
    """, unsafe_allow_html=True)

def project_hand_calculator():
    """Hand Gesture Calculator"""
    st.subheader("🧮 Hand Gesture Calculator")
    st.write("Perform calculations using hand gestures")

    # Initialize session state
    if 'calculator_display' not in st.session_state:
        st.session_state.calculator_display = "0"
    if 'current_operation' not in st.session_state:
        st.session_state.current_operation = None
    if 'first_number' not in st.session_state:
        st.session_state.first_number = None
    if 'waiting_for_second' not in st.session_state:
        st.session_state.waiting_for_second = False
    if 'run_camera_calc' not in st.session_state:
        st.session_state.run_camera_calc = False

    def count_fingers(hand_landmarks):
        """Count raised fingers"""
        finger_tips = [8, 12, 16, 20]  # Index, middle, ring, pinky
        thumb_tip = 4
        
        fingers = []
        
        # Thumb
        if hand_landmarks[thumb_tip].x < hand_landmarks[thumb_tip - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)
        
        # Other fingers
        for tip in finger_tips:
            if hand_landmarks[tip].y < hand_landmarks[tip - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return sum(fingers)

    def get_operation(finger_count):
        """Get operation based on finger count"""
        operations = {
            1: "+",
            2: "-", 
            3: "×",
            4: "÷",
            5: "="
        }
        return operations.get(finger_count, None)

    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📹 Hand Gesture Input")
        st.write("Show your hand to perform calculations:")
        
        # Camera control buttons
        col_cam1, col_cam2 = st.columns(2)
        with col_cam1:
            if st.button("📷 Start Camera", key="start_cam_calc"):
                st.session_state.run_camera_calc = True
        with col_cam2:
            if st.button("🛑 Stop Camera", key="stop_cam_calc"):
                st.session_state.run_camera_calc = False
        
        # Camera feed
        FRAME_WINDOW_CALC = st.image([], use_column_width=True)
        
        # Status display
        status_placeholder_calc = st.empty()

    with col2:
        st.subheader("🧮 Calculator Display")
        
        # Display
        st.markdown(f"""
        <div style="background: #000; color: #0f0; padding: 20px; border-radius: 10px; font-family: monospace; font-size: 24px; text-align: right;">
            {st.session_state.calculator_display}
        </div>
        """, unsafe_allow_html=True)
        
        # Number input
        st.subheader("🔢 Number Input")
        
        # Number pad
        numbers = [
            [7, 8, 9],
            [4, 5, 6], 
            [1, 2, 3],
            [0, ".", "C"]
        ]
        
        for row in numbers:
            cols = st.columns(3)
            for i, num in enumerate(row):
                with cols[i]:
                    if st.button(str(num), key=f"btn_{num}"):
                        if num == "C":
                            st.session_state.calculator_display = "0"
                            st.session_state.first_number = None
                            st.session_state.current_operation = None
                            st.session_state.waiting_for_second = False
                        elif num == ".":
                            if "." not in st.session_state.calculator_display:
                                st.session_state.calculator_display += "."
                        else:
                            if st.session_state.calculator_display == "0":
                                st.session_state.calculator_display = str(num)
                            else:
                                st.session_state.calculator_display += str(num)
        
        # Operation buttons
        st.subheader("⚡ Quick Operations")
        col_op1, col_op2 = st.columns(2)
        
        with col_op1:
            if st.button("➕ Add", key="add_btn"):
                if st.session_state.calculator_display != "0":
                    st.session_state.first_number = float(st.session_state.calculator_display)
                    st.session_state.current_operation = "+"
                    st.session_state.waiting_for_second = True
                    st.session_state.calculator_display = "0"
        
        with col_op2:
            if st.button("➖ Subtract", key="subtract_btn"):
                if st.session_state.calculator_display != "0":
                    st.session_state.first_number = float(st.session_state.calculator_display)
                    st.session_state.current_operation = "-"
                    st.session_state.waiting_for_second = True
                    st.session_state.calculator_display = "0"

    # Camera processing for calculator
    if st.session_state.run_camera_calc:
        # Mediapipe init
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(max_num_hands=1)
        mp_drawing = mp.solutions.drawing_utils
        
        cap = None
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                st.error("❌ Could not open camera")
                st.session_state.run_camera_calc = False
                st.stop()

            while st.session_state.run_camera_calc:
                ret, frame = cap.read()
                if not ret:
                    st.warning("⚠️ Failed to grab frame")
                    break

                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(rgb)

                if results.multi_hand_landmarks:
                    for lm in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(frame, lm, mp_hands.HAND_CONNECTIONS)
                        fingers = count_fingers(lm.landmark)

                        # Display finger count on frame
                        cv2.putText(frame, f"Fingers: {fingers}", (10, 60), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 105, 180), 2)
                        
                        # Process calculator operations based on finger count
                        operation = get_operation(fingers)
                        if operation:
                            if operation == "=":
                                if st.session_state.current_operation and st.session_state.first_number is not None:
                                    # Perform calculation
                                    second_num = float(st.session_state.calculator_display)
                                    first_num = st.session_state.first_number
                                    op = st.session_state.current_operation
                                    
                                    if op == "+":
                                        result = first_num + second_num
                                    elif op == "-":
                                        result = first_num - second_num
                                    elif op == "×":
                                        result = first_num * second_num
                                    elif op == "÷":
                                        result = first_num / second_num if second_num != 0 else "Error"
                                    
                                    if result != "Error":
                                        st.session_state.calculator_display = str(result)
                                        st.session_state.first_number = None
                                        st.session_state.current_operation = None
                                        st.session_state.waiting_for_second = False
                                        status_placeholder_calc.success(f"Result: {result}")
                                    else:
                                        status_placeholder_calc.error("Cannot divide by zero!")
                                else:
                                    status_placeholder_calc.warning("No operation to perform")
                            else:
                                # Set operation
                                if st.session_state.calculator_display != "0":
                                    st.session_state.first_number = float(st.session_state.calculator_display)
                                    st.session_state.current_operation = operation
                                    st.session_state.waiting_for_second = True
                                    st.session_state.calculator_display = "0"
                                    status_placeholder_calc.success(f"Operation set: {operation}")
                                else:
                                    status_placeholder_calc.warning("Enter a number first")

                FRAME_WINDOW_CALC.image(frame, channels="BGR")
                time.sleep(0.05)

        finally:
            if cap is not None:
                cap.release()
            hands.close()

def project_game_controller():
    st.subheader("🎮 Hand Gesture Game Controller")
    st.info("This tool uses your webcam to control a game with hand gestures. It will open a separate camera window.")

    # Make the game window title configurable
    game_window_title = st.text_input("Enter the Exact Game Window Title:", "Hill Climb Racing")

    if st.button("🚀 Start Game Controller"):
        
        # Import necessary libraries here
        import cv2
        import mediapipe as mp
        import pyautogui
        import pygetwindow as gw
        import time

        st.warning(f"Attempting to focus the '{game_window_title}' window in 3 seconds. Please make sure it's open.", icon="⚠️")
        time.sleep(3)

        # --- Functions defined inside the start block ---
        def focus_game_window(title):
            try:
                windows = gw.getWindowsWithTitle(title)
                if windows:
                    windows[0].activate()
                    st.success(f"✅ Focused window: {title}")
                    return True
                else:
                    st.error(f"❌ Game window '{title}' not found.")
                    return False
            except Exception as e:
                st.error(f"❌ Error focusing window: {e}")
                return False

        def is_hand_open(hand_landmarks):
            tips = [4, 8, 12, 16, 20]
            fingers_up = 0
            
            # Thumb (checks x-axis)
            if hand_landmarks.landmark[tips[0]].x < hand_landmarks.landmark[tips[0]-1].x:
                fingers_up += 1
            
            # Other 4 fingers (checks y-axis)
            for i in range(1, 5):
                if hand_landmarks.landmark[tips[i]].y < hand_landmarks.landmark[tips[i]-2].y:
                    fingers_up += 1
            return fingers_up >= 4 # True if 4 or 5 fingers are up

        # --- Main controller logic ---
        if not focus_game_window(game_window_title):
            st.stop() # Stop if the game window isn't found

        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        mp_draw = mp.solutions.drawing_utils

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.error("❌ Could not access webcam.")
            st.stop()
        
        last_action = None
        st.info("🎮 Controller is running! Open hand = Accelerate, Closed hand = Brake. Press 'ESC' in the camera window to stop.")

        while True:
            success, frame = cap.read()
            if not success:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)

            gesture = "No Hand"

            if result.multi_hand_landmarks:
                for handLms in result.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

                    if is_hand_open(handLms):
                        gesture = "Accelerate ->"
                        if last_action != "right":
                            pyautogui.keyDown("right")
                            pyautogui.keyUp("left")
                            last_action = "right"
                    else:
                        gesture = "Brake <-"
                        if last_action != "left":
                            pyautogui.keyDown("left")
                            pyautogui.keyUp("right")
                            last_action = "left"
            else:
                if last_action is not None:
                    pyautogui.keyUp("right")
                    pyautogui.keyUp("left")
                    last_action = None

            # Display the camera feed in a separate window
            cv2.putText(frame, f"Gesture: {gesture}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Game Controller Feed", cv2.resize(frame, (320, 240)))

            # Check if the user pressed ESC to quit
            if cv2.waitKey(1) & 0xFF == 27:
                break
        
        # Cleanup
        st.success("Controller stopped.")
        cap.release()
        cv2.destroyAllWindows()
        pyautogui.keyUp("right")
        pyautogui.keyUp("left")

def hand_gesture_projects_menu():
    """Main hand gesture projects menu"""
    st.title("✋ Hand Gesture Projects")
    
    tab1, tab2 = st.tabs([
        "🎵 Music Controller", "🎮 Game Controller"
    ])
    
    with tab1:
        project_hand_gesture_music()
    
    with tab2:
        project_game_controller()
