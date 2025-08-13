import streamlit as st

def javascript_nodejs_demo():
    st.subheader("🟨 JavaScript Task: Custom HTML + JS Integration")

    # Paste your full HTML content as a triple-quote string here
    html_code = r"""
        <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>All Task Manager | All-in-One Utility App</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
        <style>
            :root {
                --primary: #FF6B35;
                --secondary: #3B82F6;
                --accent: #10B981;
                --success: #34D399;
                --light: #f8f9fa;
                --dark: #212529;
                --danger: #EF4444;
                --warning: #F59E0B;
                --info: #60A5FA;
                --gray: #6c757d;
                --radius: 12px;
                --shadow: 0 8px 20px rgba(0,0,0,0.1);
                --transition: all 0.3s ease;
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            
            body {
                background: linear-gradient(135deg, #FF6B35 0%, #3B82F6 50%, #10B981 100%);
                color: var(--light);
                min-height: 100vh;
                padding: 20px;
                overflow-x: hidden;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            
            header {
                text-align: center;
                padding: 30px 0;
                animation: fadeIn 1s ease;
            }
            
            header h1 {
                font-size: 3rem;
                margin-bottom: 10px;
                text-shadow: 0 2px 10px rgba(0,0,0,0.2);
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 15px;
            }
            
            header p {
                font-size: 1.2rem;
                max-width: 700px;
                margin: 0 auto;
                opacity: 0.9;
            }
            
            .app-container {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: 25px;
                margin-top: 30px;
            }
            
            .task-card {
                background: rgba(255, 255, 255, 0.12);
                backdrop-filter: blur(12px);
                border-radius: var(--radius);
                padding: 25px;
                box-shadow: var(--shadow);
                border: 1px solid rgba(255, 255, 255, 0.1);
                transition: var(--transition);
                display: flex;
                flex-direction: column;
                height: 100%;
            }
            
            .task-card:hover {
                transform: translateY(-10px);
                box-shadow: 0 15px 30px rgba(0,0,0,0.2);
                background: rgba(255, 255, 255, 0.18);
            }
            
            .task-header {
                display: flex;
                align-items: center;
                margin-bottom: 20px;
                gap: 15px;
            }
            
            .task-icon {
                width: 50px;
                height: 50px;
                background: var(--primary);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.5rem;
                box-shadow: 0 4px 10px rgba(67, 97, 238, 0.3);
                flex-shrink: 0;
            }
            
            .task-title {
                font-size: 1.5rem;
                font-weight: 600;
            }
            
            .task-description {
                margin-bottom: 20px;
                line-height: 1.6;
                flex-grow: 1;
            }
            
            .task-content {
                margin: 15px 0;
                flex-grow: 1;
            }
            
            .task-actions {
                display: flex;
                gap: 10px;
                margin-top: auto;
                flex-wrap: wrap;
            }
            
            .btn {
                padding: 12px 24px;
                border: none;
                border-radius: 50px;
                font-weight: 600;
                cursor: pointer;
                transition: var(--transition);
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
                font-size: 0.95rem;
                flex-grow: 1;
            }
            .btn:disabled {
                background: var(--gray);
                cursor: not-allowed;
                opacity: 0.6;
            }
            
            .btn-primary { background: var(--primary); color: white; }
            .btn-secondary { background: var(--secondary); color: white; }
            .btn-success { background: var(--success); color: var(--dark); }
            .btn-danger { background: var(--danger); color: white; }
            .btn-warning { background: var(--warning); color: white; }
            .btn-info { background: var(--info); color: white; }
            
            .btn:not(:disabled):hover {
                opacity: 0.9;
                transform: translateY(-2px);
            }
            
            .camera-container {
                position: relative;
                width: 100%;
                background: rgba(0,0,0,0.2);
                border-radius: var(--radius);
                overflow: hidden;
                margin-bottom: 15px;
                aspect-ratio: 16/9;
            }
            
            #cameraPreview, #videoPreview {
                width: 100%;
                height: 100%;
                display: block;
                object-fit: cover;
            }
            
            .captured-media {
                width: 100%;
                border-radius: var(--radius);
                margin: 15px 0;
                display: none;
                max-height: 300px;
                object-fit: contain;
                background: rgba(0,0,0,0.2);
            }
            
            .map-container {
                height: 200px;
                background: var(--dark);
                border-radius: var(--radius);
                margin: 15px 0;
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: hidden;
                position: relative;
            }
            
            #map {
                width: 100%;
                height: 100%;
            }
            
            .map-placeholder { text-align: center; padding: 20px; z-index: 1; }
            
            .store-list {
                list-style: none;
                margin-top: 15px;
                max-height: 200px;
                overflow-y: auto;
            }
            
            .store-list li {
                padding: 10px 15px;
                background: rgba(255,255,255,0.1);
                margin-bottom: 8px;
                border-radius: 8px;
                display: flex;
                align-items: center;
                gap: 10px;
                transition: var(--transition);
            }
            .store-list li:hover { background: rgba(255,255,255,0.2); }
            
            .email-list {
                list-style: none;
                margin-top: 15px;
                max-height: 200px;
                overflow-y: auto;
            }
            
            .email-list li {
                padding: 12px 15px;
                background: rgba(255,255,255,0.1);
                margin-bottom: 8px;
                cursor: pointer;
                transition: var(--transition);
            }
            .email-list li:hover { background: rgba(255,255,255,0.2); }
            .email-list li.unread { border-left: 4px solid var(--accent); }
            .email-subject { font-weight: 600; margin-bottom: 5px; }
            .email-sender { font-size: 0.9rem; opacity: 0.8; }
            
            .social-buttons {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
                margin-top: 15px;
            }
            
            .social-btn { flex: 1; min-width: 120px; }
            
            .input-group { margin: 15px 0; }
            .input-group label { display: block; margin-bottom: 8px; font-weight: 500; }
            .input-group input, .input-group textarea, .input-group select {
                width: 100%;
                padding: 12px 15px;
                border-radius: var(--radius);
                border: 1px solid rgba(255,255,255,0.2);
                background: rgba(0,0,0,0.2);
                color: white;
                font-size: 1rem;
                transition: var(--transition);
            }
            
            .input-group input:focus, .input-group textarea:focus, .input-group select:focus {
                outline: none;
                border-color: var(--accent);
                box-shadow: 0 0 0 3px rgba(72, 149, 239, 0.3);
            }
            
            .input-group input::placeholder, .input-group textarea::placeholder { color: rgba(255,255,255,0.5); }
            
            .status-message {
                padding: 10px 15px;
                border-radius: var(--radius);
                margin: 15px 0;
                text-align: center;
                display: none;
            }
            
            .status-success { background: rgba(76, 201, 240, 0.2); border: 1px solid var(--success); }
            .status-error { background: rgba(247, 37, 133, 0.2); border: 1px solid var(--danger); }
            
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 15px 25px;
                border-radius: var(--radius);
                background: var(--dark);
                color: var(--light);
                box-shadow: var(--shadow);
                display: flex;
                align-items: center;
                gap: 15px;
                z-index: 1000;
                transform: translateX(120%);
                transition: transform 0.4s ease-in-out;
            }
            
            .notification.show { transform: translateX(0); }
            .notification i { font-size: 1.5rem; }
            .notification-success { border-left: 5px solid var(--success); }
            .notification-error { border-left: 5px solid var(--danger); }
            .notification-warning { border-left: 5px solid var(--warning); }
            
            footer {
                text-align: center;
                padding: 30px 0;
                margin-top: 50px;
                font-size: 0.9rem;
                opacity: 0.8;
            }
            
            /* New styles for enhanced features */
            .scanner-container {
                position: relative;
                width: 100%;
                height: 250px;
                background: rgba(0,0,0,0.2);
                border-radius: var(--radius);
                margin: 15px 0;
                overflow: hidden;
            }
            
            #qr-reader, #barcode-reader {
                width: 100%;
                height: 100%;
            }

            .scanner-result {
                margin-top: 15px;
                padding: 10px;
                background: rgba(255,255,255,0.1);
                border-radius: var(--radius);
                word-break: break-all;
                display: none;
            }
            
            .document-preview {
                width: 100%;
                height: 200px;
                background: rgba(0,0,0,0.2);
                border-radius: var(--radius);
                margin: 15px 0;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-direction: column;
                cursor: pointer;
                transition: var(--transition);
                border: 2px dashed rgba(255,255,255,0.3);
            }
            
            .document-preview:hover { background: rgba(0,0,0,0.3); border-color: var(--accent); }
            .document-preview i { font-size: 3rem; margin-bottom: 10px; }
            #documentPreview { width: 100%; height: 100%; object-fit: contain; display: none; background: white; border-radius: var(--radius); }
            
            .weather-display { display: flex; align-items: center; gap: 15px; margin: 15px 0; }
            .weather-icon { font-size: 3rem; }
            .weather-info { flex: 1; }
            .weather-temp { font-size: 2rem; font-weight: bold; }
            .weather-desc { opacity: 0.9; }
            .weather-details { display: flex; gap: 15px; margin-top: 10px; flex-wrap: wrap; }
            .weather-detail { display: flex; align-items: center; gap: 5px; font-size: 0.9rem; }
            
            .notes-container { height: 200px; overflow-y: auto; margin: 15px 0; padding-right: 5px; }
            .note-item { background: rgba(255,255,255,0.1); padding: 12px; border-radius: var(--radius); margin-bottom: 10px; transition: var(--transition); }
            .note-item:hover { background: rgba(255,255,255,0.2); }
            .note-title { font-weight: bold; margin-bottom: 5px; }
            .note-content { font-size: 0.9rem; line-height: 1.4; }
            .note-date { font-size: 0.8rem; opacity: 0.7; margin-top: 5px; text-align: right; }
            
            .tab-container { display: flex; border-bottom: 1px solid rgba(255,255,255,0.2); margin-bottom: 15px; }
            .tab { padding: 8px 16px; cursor: pointer; border-bottom: 2px solid transparent; transition: var(--transition); }
            .tab.active { border-bottom: 2px solid var(--accent); color: var(--accent); font-weight: bold; }
            .tab-content { display: none; }
            .tab-content.active { display: block; animation: fadeIn 0.5s; }
            
            .currency-converter { display: flex; flex-direction: column; gap: 10px; margin: 15px 0; }
            .currency-row { display: flex; align-items: center; gap: 10px; }
            .currency-row input { flex: 1; }
            .currency-row select { width: 100px; }
            .conversion-rate { text-align: center; margin: 10px 0; font-size: 0.9rem; opacity: 0.8; }
            
            .expense-list { list-style: none; margin-top: 15px; max-height: 200px; overflow-y: auto; }
            .expense-item { display: flex; justify-content: space-between; padding: 10px 15px; background: rgba(255,255,255,0.1); margin-bottom: 8px; border-radius: 8px; }
            .expense-category { display: flex; align-items: center; gap: 8px; }
            .expense-amount { font-weight: bold; }
            .expense-income { color: var(--success); }
            .expense-expense { color: var(--danger); }
            
            .progress-container { margin: 15px 0; }
            .progress-bar { height: 10px; background: rgba(255,255,255,0.1); border-radius: 5px; overflow: hidden; margin-bottom: 5px; }
            .progress-fill { height: 100%; background: var(--accent); border-radius: 5px; transition: width 0.5s ease; }
            .progress-info { display: flex; justify-content: space-between; font-size: 0.9rem; }
            
            /* Nearby stores styles */
            .store-type-buttons {
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
                margin: 10px 0;
            }
            
            .store-type-btn {
                padding: 8px 12px;
                border-radius: 20px;
                background: rgba(255,255,255,0.1);
                border: none;
                color: white;
                font-size: 0.8rem;
                cursor: pointer;
                transition: var(--transition);
            }
            
            .store-type-btn:hover, .store-type-btn.active {
                background: var(--accent);
            }
            
            .store-distance {
                font-size: 0.8rem;
                opacity: 0.8;
                margin-left: auto;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            @media (max-width: 768px) {
                .app-container { grid-template-columns: 1fr; }
                header h1 { font-size: 2.2rem; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1><i class="fas fa-tasks"></i> All Task Manager</h1>
                <p>Your all-in-one solution for daily tasks - from communication to navigation and media management</p>
            </header>
            
            <div class="app-container">
                <div class="task-card">
                    <div class="task-header">
                        <div class="task-icon"><i class="fas fa-camera"></i></div>
                        <h2 class="task-title">Photo Capture</h2>
                    </div>
                    <div class="task-content">
                        <div class="camera-container">
                            <video id="cameraPreview" autoplay playsinline></video>
                            <canvas id="photoCanvas" style="display:none;"></canvas>
                        </div>
                        <img id="capturedPhoto" class="captured-media" alt="Captured Photo">
                        <div class="status-message" id="photoStatus"></div>
                    </div>
                    <div class="task-actions">
                        <button class="btn btn-primary" id="capturePhotoBtn"><i class="fas fa-camera"></i> Capture Photo</button>
                        <button class="btn btn-success" id="sendPhotoBtn" disabled><i class="fas fa-paper-plane"></i> Send via Email</button>
                        <button class="btn btn-secondary" id="downloadPhotoBtn" disabled><i class="fas fa-download"></i> Download</button>
                    </div>
                </div>
                
                <div class="task-card">
                    <div class="task-header">
                        <div class="task-icon"><i class="fas fa-video"></i></div>
                        <h2 class="task-title">Video Capture</h2>
                    </div>
                    <div class="task-content">
                        <div class="camera-container">
                            <video id="videoPreview" autoplay playsinline muted></video>
                            <div id="recordingTimer" style="display:none; position:absolute; top:10px; right:10px; background:var(--danger); padding:5px 10px; border-radius:20px; font-weight:bold;">00:00</div>
                        </div>
                        <video id="capturedVideo" class="captured-media" controls style="display:none;"></video>
                        <div class="status-message" id="videoStatus"></div>
                    </div>
                    <div class="task-actions">
                        <button class="btn btn-primary" id="startRecordingBtn"><i class="fas fa-record-vinyl"></i> Start Recording</button>
                        <button class="btn btn-danger" id="stopRecordingBtn" disabled><i class="fas fa-stop"></i> Stop</button>
                        <button class="btn btn-success" id="sendVideoBtn" disabled><i class="fas fa-paper-plane"></i> Send Video</button>
                    </div>
                </div>
                
                <div class="task-card">
                    <div class="task-header">
                        <div class="task-icon"><i class="fas fa-map-marked-alt"></i></div>
                        <h2 class="task-title">Geolocation & Navigation</h2>
                    </div>
                    <div class="task-content">
                        <div class="map-container">
                            <div id="map"></div>
                        </div>
                        <div class="input-group">
                            <label for="destination">Destination Address:</label>
                            <input type="text" id="destination" placeholder="e.g., Hawa Mahal, Jaipur">
                        </div>
                        <div class="status-message" id="locationStatus"></div>
                    </div>
                    <div class="task-actions">
                        <button class="btn btn-primary" id="getLocationBtn"><i class="fas fa-location-dot"></i> Get Location</button>
                        <button class="btn btn-success" id="getRouteBtn" disabled><i class="fas fa-route"></i> Get Directions</button>
                        <button class="btn btn-secondary" id="shareLocationBtn" disabled><i class="fas fa-share"></i> Share Location</button>
                    </div>
                </div>

                <div class="task-card">
                    <div class="task-header">
                        <div class="task-icon"><i class="fas fa-store"></i></div>
                        <h2 class="task-title">Nearby Stores</h2>
                    </div>
                    <div class="task-content">
                        <p>Find stores and services near your current location.</p>
                        <div class="store-type-buttons">
                            <button class="store-type-btn active" data-type="all">All</button>
                            <button class="store-type-btn" data-type="restaurant"><i class="fas fa-utensils"></i> Restaurants</button>
                            <button class="store-type-btn" data-type="grocery"><i class="fas fa-shopping-basket"></i> Grocery</button>
                            <button class="store-type-btn" data-type="pharmacy"><i class="fas fa-prescription-bottle-alt"></i> Pharmacy</button>
                            <button class="store-type-btn" data-type="atm"><i class="fas fa-money-bill-wave"></i> ATMs</button>
                        </div>
                        <ul class="store-list" id="storeList">
                            <li style="text-align: center; padding: 20px;">Get your location to find nearby stores</li>
                        </ul>
                    </div>
                    <div class="task-actions">
                        <button class="btn btn-primary" id="findStoresBtn"><i class="fas fa-search-location"></i> Find Stores</button>
                        <button class="btn btn-secondary" id="refreshStoresBtn" disabled><i class="fas fa-sync-alt"></i> Refresh</button>
                    </div>
                </div>
                
                <div class="task-card">
                    <div class="task-header">
                        <div class="task-icon"><i class="fas fa-comments"></i></div>
                        <h2 class="task-title">Quick Communication</h2>
                    </div>
                    <div class="task-content">
                        <div class="tab-container" id="comm-tabs">
                            <div class="tab active" data-tab="whatsapp-tab"><i class="fab fa-whatsapp"></i> WhatsApp</div>
                            <div class="tab" data-tab="sms-tab"><i class="fas fa-sms"></i> SMS</div>
                            <div class="tab" data-tab="email-tab"><i class="fas fa-envelope"></i> Email</div>
                        </div>
                        
                        <div class="tab-content active" id="whatsapp-tab">
                            <div class="input-group"><input type="tel" id="phoneNumber" placeholder="Phone number with country code"></div>
                            <div class="input-group"><textarea id="whatsappMessage" rows="2" placeholder="WhatsApp message"></textarea></div>
                            <button class="btn btn-success btn-block" id="sendWhatsAppBtn"><i class="fab fa-whatsapp"></i> Send WhatsApp</button>
                        </div>
                        
                        <div class="tab-content" id="sms-tab">
                            <div class="input-group"><input type="tel" id="smsNumber" placeholder="Phone number"></div>
                            <div class="input-group"><textarea id="smsMessage" rows="2" placeholder="SMS message"></textarea></div>
                            <button class="btn btn-primary btn-block" id="sendSmsBtn"><i class="fas fa-sms"></i> Send SMS</button>
                        </div>
                        
                        <div class="tab-content" id="email-tab">
                            <div class="input-group"><input type="email" id="emailTo" placeholder="Recipient's Email"></div>
                            <div class="input-group"><input type="text" id="emailSubject" placeholder="Subject"></div>
                            <div class="input-group"><textarea id="emailMessage" rows="2" placeholder="Email body"></textarea></div>
                            <button class="btn btn-danger btn-block" id="sendEmailBtn"><i class="fas fa-envelope"></i> Send Email</button>
                        </div>
                    </div>
                </div>
                
                <div class="task-card">
                    <div class="task-header">
                        <div class="task-icon"><i class="fas fa-qrcode"></i></div>
                        <h2 class="task-title">QR Code Scanner</h2>
                    </div>
                    <div class="task-content">
                        <div class="scanner-container">
                            <div id="qr-reader"></div>
                        </div>
                        <div class="scanner-result" id="qr-result"></div>
                    </div>
                    <div class="task-actions">
                        <button class="btn btn-primary" id="startQrScanBtn"><i class="fas fa-play"></i> Start Scan</button>
                        <button class="btn btn-danger" id="stopQrScanBtn" disabled><i class="fas fa-stop"></i> Stop Scan</button>
                    </div>
                </div>
                
                <div class="task-card">
                    <div class="task-header">
                        <div class="task-icon"><i class="fas fa-cloud-sun"></i></div>
                        <h2 class="task-title">Weather Report</h2>
                    </div>
                    <div class="task-content">
                        <div class="weather-display">
                            <div class="weather-icon" id="weatherIcon"><i class="fas fa-spinner fa-spin"></i></div>
                            <div class="weather-info">
                                <div class="weather-temp" id="weatherTemp">--°C</div>
                                <div class="weather-desc" id="weatherDesc">Loading...</div>
                            </div>
                        </div>
                        <div class="weather-details">
                            <div class="weather-detail"><i class="fas fa-wind"></i> <span id="weatherWind">-- km/h</span></div>
                            <div class="weather-detail"><i class="fas fa-tint"></i> <span id="weatherHumidity">--%</span></div>
                        </div>
                        <div class="input-group">
                            <input type="text" id="weatherApiKey" placeholder="OpenWeatherMap API Key (optional)" style="margin-bottom: 10px;">
                            <input type="text" id="weatherCity" placeholder="Enter city name">
                        </div>
                    </div>
                    <div class="task-actions">
                        <button class="btn btn-info" id="fetchWeatherBtn"><i class="fas fa-sync-alt"></i> Get Weather</button>
                    </div>
                </div>
            </div>
        </div>

        <div id="notification" class="notification">
            <i id="notificationIcon" class="fas fa-check-circle"></i>
            <span id="notificationMessage">This is a notification!</span>
        </div>
        
        <footer>
            <p>© 2025 All Task Manager. Enhanced by Gemini.</p>
        </footer>

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
        <script src="https://unpkg.com/html5-qrcode/html5-qrcode.min.js"></script>

        <script>
        document.addEventListener('DOMContentLoaded', () => {
            // --- Global Variables & Elements ---
            let currentStream;
            let photoStream;
            let videoStream;
            let mediaRecorder;
            let recordedChunks = [];
            let map;
            let currentLocationMarker;
            let html5QrCode;
            let userCoords;
            let storeType = 'all';

            const cameraPreview = document.getElementById('cameraPreview');
            const videoPreview = document.getElementById('videoPreview');

            // --- Utility Functions ---
            function showNotification(message, type = 'success') {
                const notification = document.getElementById('notification');
                const icon = document.getElementById('notificationIcon');
                const messageEl = document.getElementById('notificationMessage');

                notification.className = 'notification'; // Reset classes
                icon.className = '';

                if (type === 'success') {
                    notification.classList.add('notification-success');
                    icon.classList.add('fas', 'fa-check-circle');
                } else if (type === 'error') {
                    notification.classList.add('notification-error');
                    icon.classList.add('fas', 'fa-times-circle');
                } else if (type === 'warning') {
                    notification.classList.add('notification-warning');
                    icon.classList.add('fas', 'fa-exclamation-triangle');
                }
                
                messageEl.textContent = message;
                notification.classList.add('show');

                setTimeout(() => {
                    notification.classList.remove('show');
                }, 3000);
            }

            async function getCameraStream(constraints) {
                try {
                    return await navigator.mediaDevices.getUserMedia(constraints);
                } catch (err) {
                    console.error("Camera access error:", err);
                    showNotification('Camera access denied or not available.', 'error');
                    return null;
                }
            }

            // --- Photo Capture ---
            const capturePhotoBtn = document.getElementById('capturePhotoBtn');
            const sendPhotoBtn = document.getElementById('sendPhotoBtn');
            const downloadPhotoBtn = document.getElementById('downloadPhotoBtn');
            const photoCanvas = document.getElementById('photoCanvas');
            const capturedPhoto = document.getElementById('capturedPhoto');

            async function initPhotoCamera() {
                photoStream = await getCameraStream({ video: true, audio: false });
                if (photoStream) {
                    cameraPreview.srcObject = photoStream;
                }
            }
            initPhotoCamera(); // Initialize on load

            capturePhotoBtn.addEventListener('click', () => {
                if (!photoStream) {
                    showNotification('Camera is not active.', 'warning');
                    return;
                }
                const context = photoCanvas.getContext('2d');
                photoCanvas.width = cameraPreview.videoWidth;
                photoCanvas.height = cameraPreview.videoHeight;
                context.drawImage(cameraPreview, 0, 0, photoCanvas.width, photoCanvas.height);
                
                const dataUrl = photoCanvas.toDataURL('image/png');
                capturedPhoto.src = dataUrl;
                capturedPhoto.style.display = 'block';
                cameraPreview.style.display = 'none';

                sendPhotoBtn.disabled = false;
                downloadPhotoBtn.disabled = false;
                showNotification('Photo captured!', 'success');
            });

            downloadPhotoBtn.addEventListener('click', () => {
                const link = document.createElement('a');
                link.href = capturedPhoto.src;
                link.download = `capture-${Date.now()}.png`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                showNotification('Photo downloading...', 'success');
            });

            sendPhotoBtn.addEventListener('click', () => {
                const email = prompt("Enter recipient's email address:");
                if (email) {
                    const subject = "Photo from All Task Manager";
                    const body = "Please see the attached photo.";
                    // Note: Sending actual attachments via mailto is not reliably supported. 
                    // This is a simplified implementation. A backend would be needed for true attachments.
                    const mailtoLink = `mailto:${email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
                    window.location.href = mailtoLink;
                    showNotification('Email client opened.', 'success');
                }
            });

            // --- Video Capture ---
            const startRecordingBtn = document.getElementById('startRecordingBtn');
            const stopRecordingBtn = document.getElementById('stopRecordingBtn');
            const sendVideoBtn = document.getElementById('sendVideoBtn');
            const capturedVideo = document.getElementById('capturedVideo');
            const recordingTimer = document.getElementById('recordingTimer');
            let timerInterval;

            async function initVideoCamera() {
                videoStream = await getCameraStream({ video: true, audio: true });
                if (videoStream) {
                    videoPreview.srcObject = videoStream;
                }
            }
            initVideoCamera();

            startRecordingBtn.addEventListener('click', async () => {
                if (!videoStream) {
                    showNotification('Camera is not active for video.', 'warning');
                    await initVideoCamera();
                    return;
                }
                recordedChunks = [];
                mediaRecorder = new MediaRecorder(videoStream, { mimeType: 'video/webm' });
                
                mediaRecorder.ondataavailable = (event) => {
                    if (event.data.size > 0) {
                        recordedChunks.push(event.data);
                    }
                };

                mediaRecorder.onstart = () => {
                    startRecordingBtn.disabled = true;
                    stopRecordingBtn.disabled = false;
                    sendVideoBtn.disabled = true;
                    recordingTimer.style.display = 'block';
                    let seconds = 0;
                    timerInterval = setInterval(() => {
                        seconds++;
                        const min = String(Math.floor(seconds / 60)).padStart(2, '0');
                        const sec = String(seconds % 60).padStart(2, '0');
                        recordingTimer.textContent = `${min}:${sec}`;
                    }, 1000);
                    showNotification('Recording started!', 'success');
                };

                mediaRecorder.onstop = () => {
                    clearInterval(timerInterval);
                    recordingTimer.style.display = 'none';
                    startRecordingBtn.disabled = false;
                    stopRecordingBtn.disabled = true;
                    sendVideoBtn.disabled = false;

                    const blob = new Blob(recordedChunks, { type: 'video/webm' });
                    const videoUrl = URL.createObjectURL(blob);
                    capturedVideo.src = videoUrl;
                    capturedVideo.style.display = 'block';
                    videoPreview.style.display = 'none';
                    showNotification('Recording stopped. Video is ready.', 'success');
                };
                
                mediaRecorder.start();
            });

            stopRecordingBtn.addEventListener('click', () => {
                if (mediaRecorder && mediaRecorder.state === 'recording') {
                    mediaRecorder.stop();
                }
            });

            sendVideoBtn.addEventListener('click', () => {
                const email = prompt("Enter recipient's email address to send video:");
                if (email) {
                    const subject = "Video from All Task Manager";
                    const body = "A video has been recorded for you. Please note that due to browser limitations, the video is not attached directly. A real app would upload this to a server and share a link.";
                    const mailtoLink = `mailto:${email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
                    window.location.href = mailtoLink;
                    showNotification('Email client opened.', 'success');
                }
            });

                    // --- Geolocation & Maps ---
            const getLocationBtn = document.getElementById('getLocationBtn');
            const getRouteBtn = document.getElementById('getRouteBtn');
            const shareLocationBtn = document.getElementById('shareLocationBtn');
            const destinationInput = document.getElementById('destination');
            const locationStatus = document.getElementById('locationStatus');

            // Initialize map
            map = L.map('map').setView([20.5937, 78.9629], 5); // Default to India view
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);

            getLocationBtn.addEventListener('click', () => {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(
                        (position) => {
                            userCoords = {
                                lat: position.coords.latitude,
                                lng: position.coords.longitude
                            };
                            
                            // Update map view
                            map.setView([userCoords.lat, userCoords.lng], 15);
                            
                            // Clear previous marker if exists
                            if (currentLocationMarker) {
                                map.removeLayer(currentLocationMarker);
                            }
                            
                            // Add new marker
                            currentLocationMarker = L.marker([userCoords.lat, userCoords.lng]).addTo(map)
                                .bindPopup("Your Location").openPopup();
                            
                            // Enable buttons
                            getRouteBtn.disabled = false;
                            shareLocationBtn.disabled = false;
                            
                            // Show success
                            locationStatus.textContent = `Location found! Latitude: ${userCoords.lat.toFixed(4)}, Longitude: ${userCoords.lng.toFixed(4)}`;
                            locationStatus.className = 'status-message status-success';
                            locationStatus.style.display = 'block';
                            
                            showNotification('Location found!', 'success');
                        },
                        (error) => {
                            let errorMessage;
                            switch(error.code) {
                                case error.PERMISSION_DENIED:
                                    errorMessage = "User denied the request for Geolocation.";
                                    break;
                                case error.POSITION_UNAVAILABLE:
                                    errorMessage = "Location information is unavailable.";
                                    break;
                                case error.TIMEOUT:
                                    errorMessage = "The request to get user location timed out.";
                                    break;
                                case error.UNKNOWN_ERROR:
                                    errorMessage = "An unknown error occurred.";
                                    break;
                            }
                            
                            locationStatus.textContent = errorMessage;
                            locationStatus.className = 'status-message status-error';
                            locationStatus.style.display = 'block';
                            
                            showNotification(errorMessage, 'error');
                        }
                    );
                } else {
                    locationStatus.textContent = "Geolocation is not supported by this browser.";
                    locationStatus.className = 'status-message status-error';
                    locationStatus.style.display = 'block';
                    
                    showNotification("Geolocation not supported", 'error');
                }
            });

            getRouteBtn.addEventListener('click', () => {
                const destination = destinationInput.value;
                if (!destination) {
                    showNotification('Please enter a destination.', 'warning');
                    return;
                }

                if (userCoords) {
                    const mapsUrl = `https://www.google.com/maps/dir/?api=1&origin=${userCoords.lat},${userCoords.lng}&destination=${encodeURIComponent(destination)}`;
                    window.open(mapsUrl, '_blank');
                    showNotification('Redirecting to Google Maps for directions.', 'success');
                } else {
                    showNotification('Please get your location first.', 'warning');
                }
            });

            shareLocationBtn.addEventListener('click', () => {
                if (navigator.share) {
                    navigator.share({
                        title: 'My Current Location',
                        text: `I'm at this location: Latitude ${userCoords.lat}, Longitude ${userCoords.lng}`,
                        url: `https://www.google.com/maps?q=${userCoords.lat},${userCoords.lng}`
                    }).then(() => {
                        showNotification('Location shared successfully', 'success');
                    }).catch(err => {
                        showNotification('Error sharing location: ' + err, 'error');
                    });
                } else {
                    // Fallback for browsers that don't support Web Share API
                    const shareText = `My current location: https://www.google.com/maps?q=${userCoords.lat},${userCoords.lng}`;
                    prompt("Copy this link to share your location:", shareText);
                    showNotification('Share link copied to clipboard', 'success');
                }
            });

            // --- Nearby Stores ---
            const findStoresBtn = document.getElementById('findStoresBtn');
            const refreshStoresBtn = document.getElementById('refreshStoresBtn');
            const storeList = document.getElementById('storeList');
            const storeTypeButtons = document.querySelectorAll('.store-type-btn');

            storeTypeButtons.forEach(btn => {
                btn.addEventListener('click', () => {
                    storeTypeButtons.forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    storeType = btn.dataset.type;
                    
                    if (userCoords) {
                        findNearbyStores();
                    }
                });
            });

            findStoresBtn.addEventListener('click', () => {
                if (!userCoords) {
                    showNotification('Please get your location first', 'warning');
                    return;
                }
                findNearbyStores();
            });

            refreshStoresBtn.addEventListener('click', findNearbyStores);

            function findNearbyStores() {
                // In a real app, this would use a Places API like Google Places
                // Here we simulate with mock data
                
                storeList.innerHTML = '<li style="text-align: center; padding: 20px;"><i class="fas fa-spinner fa-spin"></i> Finding nearby stores...</li>';
                
                setTimeout(() => {
                    const mockStores = generateMockStores();
                    displayStores(mockStores);
                    refreshStoresBtn.disabled = false;
                }, 1000);
            }

            function generateMockStores() {
                const storeTypes = {
                    restaurant: { name: 'Restaurant', icon: 'fa-utensils' },
                    grocery: { name: 'Grocery Store', icon: 'fa-shopping-basket' },
                    pharmacy: { name: 'Pharmacy', icon: 'fa-prescription-bottle-alt' },
                    atm: { name: 'ATM', icon: 'fa-money-bill-wave' }
                };
                
                const stores = [];
                const count = Math.floor(Math.random() * 5) + 3; // 3-7 stores
                
                for (let i = 0; i < count; i++) {
                    const types = Object.keys(storeTypes);
                    const randomType = types[Math.floor(Math.random() * types.length)];
                    const distance = (Math.random() * 2 + 0.5).toFixed(1);
                    
                    stores.push({
                        name: `${storeTypes[randomType].name} ${i + 1}`,
                        type: randomType,
                        icon: storeTypes[randomType].icon,
                        distance: distance
                    });
                }
                
                return stores.filter(store => storeType === 'all' || store.type === storeType);
            }

            function displayStores(stores) {
                if (stores.length === 0) {
                    storeList.innerHTML = '<li style="text-align: center; padding: 20px;">No stores found nearby</li>';
                    return;
                }
                
                storeList.innerHTML = stores.map(store => `
                    <li>
                        <i class="fas ${store.icon}"></i>
                        <div>
                            <strong>${store.name}</strong>
                            <div style="font-size: 0.8rem; opacity: 0.8;">${store.type}</div>
                        </div>
                        <span class="store-distance">${store.distance} km</span>
                    </li>
                `).join('');
            }

            // --- Communication Features ---
            const sendWhatsAppBtn = document.getElementById('sendWhatsAppBtn');
            const sendSmsBtn = document.getElementById('sendSmsBtn');
            const sendEmailBtn = document.getElementById('sendEmailBtn');
            const tabs = document.querySelectorAll('.tab');
            const tabContents = document.querySelectorAll('.tab-content');

            // Tab switching
            tabs.forEach(tab => {
                tab.addEventListener('click', () => {
                    const targetTab = tab.dataset.tab;
                    
                    tabs.forEach(t => t.classList.remove('active'));
                    tabContents.forEach(content => content.classList.remove('active'));
                    
                    tab.classList.add('active');
                    document.getElementById(targetTab).classList.add('active');
                });
            });

            sendWhatsAppBtn.addEventListener('click', () => {
                const phone = document.getElementById('phoneNumber').value;
                const message = document.getElementById('whatsappMessage').value;
                
                if (!phone || !message) {
                    showNotification('Please fill in both phone number and message.', 'warning');
                    return;
                }
                
                const whatsappUrl = `https://wa.me/${phone.replace(/\D/g, '')}?text=${encodeURIComponent(message)}`;
                window.open(whatsappUrl, '_blank');
                showNotification('Opening WhatsApp...', 'success');
            });

            sendSmsBtn.addEventListener('click', () => {
                const phone = document.getElementById('smsNumber').value;
                const message = document.getElementById('smsMessage').value;
                
                if (!phone || !message) {
                    showNotification('Please fill in both phone number and message.', 'warning');
                    return;
                }
                
                const smsUrl = `sms:${phone}?body=${encodeURIComponent(message)}`;
                window.location.href = smsUrl;
                showNotification('Opening SMS app...', 'success');
            });

            sendEmailBtn.addEventListener('click', () => {
                const to = document.getElementById('emailTo').value;
                const subject = document.getElementById('emailSubject').value;
                const message = document.getElementById('emailMessage').value;
                
                if (!to || !subject || !message) {
                    showNotification('Please fill in all email fields.', 'warning');
                    return;
                }
                
                const mailtoUrl = `mailto:${to}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(message)}`;
                window.location.href = mailtoUrl;
                showNotification('Opening email client...', 'success');
            });

            // --- QR Code Scanner ---
            const startQrScanBtn = document.getElementById('startQrScanBtn');
            const stopQrScanBtn = document.getElementById('stopQrScanBtn');
            const qrResult = document.getElementById('qr-result');

            startQrScanBtn.addEventListener('click', () => {
                if (!html5QrCode) {
                    html5QrCode = new Html5Qrcode("qr-reader");
                }
                
                html5QrCode.start(
                    { facingMode: "environment" },
                    {
                        fps: 10,
                        qrbox: { width: 250, height: 250 }
                    },
                    (decodedText, decodedResult) => {
                        qrResult.textContent = `Scanned: ${decodedText}`;
                        qrResult.style.display = 'block';
                        showNotification('QR Code scanned successfully!', 'success');
                        stopQrScan();
                    },
                    (errorMessage) => {
                        // Handle scan error, ignore for now
                    }
                ).then(() => {
                    startQrScanBtn.disabled = true;
                    stopQrScanBtn.disabled = false;
                    showNotification('QR Scanner started', 'success');
                }).catch(err => {
                    showNotification('Failed to start QR scanner: ' + err, 'error');
                });
            });

            stopQrScanBtn.addEventListener('click', stopQrScan);

            function stopQrScan() {
                if (html5QrCode && html5QrCode.isScanning) {
                    html5QrCode.stop().then(() => {
                        startQrScanBtn.disabled = false;
                        stopQrScanBtn.disabled = true;
                        showNotification('QR Scanner stopped', 'success');
                    }).catch(err => {
                        showNotification('Error stopping scanner: ' + err, 'error');
                    });
                }
            }

            // --- Weather API ---
            const fetchWeatherBtn = document.getElementById('fetchWeatherBtn');
            const weatherCity = document.getElementById('weatherCity');
            const weatherTemp = document.getElementById('weatherTemp');
            const weatherDesc = document.getElementById('weatherDesc');
            const weatherIcon = document.getElementById('weatherIcon');
            const weatherWind = document.getElementById('weatherWind');
            const weatherHumidity = document.getElementById('weatherHumidity');

            fetchWeatherBtn.addEventListener('click', async () => {
                const city = weatherCity.value || 'Jaipur';
                const userApiKey = weatherApiKey.value.trim();
                
                // Show loading state
                weatherTemp.textContent = 'Loading...';
                weatherDesc.textContent = 'Fetching data...';
                weatherWind.textContent = '...';
                weatherHumidity.textContent = '...';
                weatherIcon.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
                
                // If user provided API key, try OpenWeatherMap first
                if (userApiKey) {
                    try {
                        console.log('Trying OpenWeatherMap API with user key for:', city);
                        
                        const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${userApiKey}&units=metric`);
                        
                        if (!response.ok) {
                            const errorData = await response.json();
                            console.log('OpenWeatherMap API error:', errorData);
                            throw new Error(`OpenWeatherMap API Error: ${errorData.message || response.statusText}`);
                        }
                        
                        const data = await response.json();
                        console.log('OpenWeatherMap API success:', data);
                        
                        weatherTemp.textContent = `${Math.round(data.main.temp)}°C`;
                        weatherDesc.textContent = data.weather[0].description;
                        weatherWind.textContent = `${data.wind.speed} km/h`;
                        weatherHumidity.textContent = `${data.main.humidity}%`;
                        
                        // Set weather icon based on condition
                        const weatherCode = data.weather[0].id;
                        let iconClass = 'fa-cloud';
                        
                        if (weatherCode >= 200 && weatherCode < 300) iconClass = 'fa-bolt';
                        else if (weatherCode >= 300 && weatherCode < 400) iconClass = 'fa-cloud-rain';
                        else if (weatherCode >= 500 && weatherCode < 600) iconClass = 'fa-cloud-showers-heavy';
                        else if (weatherCode >= 600 && weatherCode < 700) iconClass = 'fa-snowflake';
                        else if (weatherCode >= 700 && weatherCode < 800) iconClass = 'fa-smog';
                        else if (weatherCode === 800) iconClass = 'fa-sun';
                        else if (weatherCode >= 801 && weatherCode < 900) iconClass = 'fa-cloud';
                        
                        weatherIcon.innerHTML = `<i class="fas ${iconClass}"></i>`;
                        
                        showNotification(`Weather updated for ${city} (OpenWeatherMap)`, 'success');
                        return; // Success, exit early
                        
                    } catch (error) {
                        console.log('OpenWeatherMap API failed, trying wttr.in:', error);
                        showNotification('OpenWeatherMap failed, trying alternative API...', 'warning');
                    }
                }
                
                // Try wttr.in API (free, no API key needed)
                try {
                    console.log('Trying wttr.in API for:', city);
                    
                    const response = await fetch(`https://wttr.in/${encodeURIComponent(city)}?format=j1`);
                    
                    if (!response.ok) {
                        throw new Error(`wttr.in API failed: ${response.status}`);
                    }
                    
                    const data = await response.json();
                    console.log('wttr.in API success:', data);
                    
                    if (data.current_condition && data.current_condition[0]) {
                        const current = data.current_condition[0];
                        
                        weatherTemp.textContent = `${current.temp_C}°C`;
                        weatherDesc.textContent = current.weatherDesc[0].value;
                        weatherWind.textContent = `${current.windspeedKmph} km/h`;
                        weatherHumidity.textContent = `${current.humidity}%`;
                        
                        // Set weather icon based on condition
                        const weatherDesc = current.weatherDesc[0].value.toLowerCase();
                        let iconClass = 'fa-cloud';
                        
                        if (weatherDesc.includes('rain') || weatherDesc.includes('drizzle')) iconClass = 'fa-cloud-rain';
                        else if (weatherDesc.includes('snow')) iconClass = 'fa-snowflake';
                        else if (weatherDesc.includes('storm') || weatherDesc.includes('thunder')) iconClass = 'fa-bolt';
                        else if (weatherDesc.includes('fog') || weatherDesc.includes('mist')) iconClass = 'fa-smog';
                        else if (weatherDesc.includes('clear') || weatherDesc.includes('sunny')) iconClass = 'fa-sun';
                        else if (weatherDesc.includes('cloud')) iconClass = 'fa-cloud';
                        else if (weatherDesc.includes('partly')) iconClass = 'fa-cloud-sun';
                        
                        weatherIcon.innerHTML = `<i class="fas ${iconClass}"></i>`;
                        
                        showNotification(`Weather updated for ${city} (wttr.in)`, 'success');
                    } else {
                        throw new Error('No weather data from wttr.in');
                    }
                    
                } catch (error) {
                    console.log('wttr.in API failed, using offline data:', error);
                    
                    // Fallback with realistic data for major Indian cities
                    const cityWeather = {
                        'Jaipur': { temp: '32°C', desc: 'Sunny', wind: '8 km/h', humidity: '45%', icon: 'fa-sun' },
                        'Mumbai': { temp: '28°C', desc: 'Partly cloudy', wind: '12 km/h', humidity: '75%', icon: 'fa-cloud-sun' },
                        'Delhi': { temp: '35°C', desc: 'Clear sky', wind: '6 km/h', humidity: '40%', icon: 'fa-sun' },
                        'Bangalore': { temp: '24°C', desc: 'Cloudy', wind: '10 km/h', humidity: '70%', icon: 'fa-cloud' },
                        'Chennai': { temp: '30°C', desc: 'Hot', wind: '15 km/h', humidity: '80%', icon: 'fa-sun' },
                        'Kolkata': { temp: '33°C', desc: 'Humid', wind: '9 km/h', humidity: '70%', icon: 'fa-cloud-sun' },
                        'Hyderabad': { temp: '29°C', desc: 'Warm', wind: '11 km/h', humidity: '65%', icon: 'fa-cloud-sun' },
                        'Pune': { temp: '26°C', desc: 'Pleasant', wind: '9 km/h', humidity: '60%', icon: 'fa-cloud-sun' },
                        'Ahmedabad': { temp: '34°C', desc: 'Hot', wind: '7 km/h', humidity: '50%', icon: 'fa-sun' },
                        'Surat': { temp: '31°C', desc: 'Warm', wind: '10 km/h', humidity: '70%', icon: 'fa-cloud-sun' }
                    };
                    
                    const defaultCity = 'Jaipur';
                    const weather = cityWeather[city] || cityWeather[defaultCity];
                    
                    weatherTemp.textContent = weather.temp;
                    weatherDesc.textContent = weather.desc;
                    weatherWind.textContent = weather.wind;
                    weatherHumidity.textContent = weather.humidity;
                    weatherIcon.innerHTML = `<i class="fas ${weather.icon}"></i>`;
                    
                    showNotification(`Weather data for ${city} (offline mode)`, 'warning');
                }
            });

            // Load initial weather
            fetchWeatherBtn.click();
        });
        </script>
    </body>
    </html>
    """

    # Display the HTML content
    st.components.v1.html(html_code, height=800, scrolling=True)

def javascript_simple_calculator():
    st.subheader("🧮 JavaScript - Simple Calculator (Browser)")
    
    html_code = r"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple Calculator</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
            .calculator { display: inline-block; border: 2px solid #333; border-radius: 10px; padding: 20px; background: #f0f0f0; }
            input[type="text"] { width: 200px; height: 40px; font-size: 20px; text-align: right; margin-bottom: 10px; }
            button { width: 50px; height: 50px; font-size: 18px; margin: 5px; border: 1px solid #999; border-radius: 5px; cursor: pointer; }
            button:hover { background: #ddd; }
            .equals { background: #4CAF50; color: white; }
            .clear { background: #f44336; color: white; }
        </style>
    </head>
    <body>
        <div class="calculator">
            <input type="text" id="display" readonly>
            <br>
            <button onclick="clearDisplay()" class="clear">C</button>
            <button onclick="appendToDisplay('/')">/</button>
            <button onclick="appendToDisplay('*')">×</button>
            <button onclick="backspace()">⌫</button>
            <br>
            <button onclick="appendToDisplay('7')">7</button>
            <button onclick="appendToDisplay('8')">8</button>
            <button onclick="appendToDisplay('9')">9</button>
            <button onclick="appendToDisplay('-')">-</button>
            <br>
            <button onclick="appendToDisplay('4')">4</button>
            <button onclick="appendToDisplay('5')">5</button>
            <button onclick="appendToDisplay('6')">6</button>
            <button onclick="appendToDisplay('+')">+</button>
            <br>
            <button onclick="appendToDisplay('1')">1</button>
            <button onclick="appendToDisplay('2')">2</button>
            <button onclick="appendToDisplay('3')">3</button>
            <button onclick="calculate()" class="equals" style="height: 110px;">=</button>
            <br>
            <button onclick="appendToDisplay('0')" style="width: 110px;">0</button>
            <button onclick="appendToDisplay('.')">.</button>
        </div>
        
        <script>
            function appendToDisplay(value) {
                document.getElementById('display').value += value;
            }
            
            function clearDisplay() {
                document.getElementById('display').value = '';
            }
            
            function backspace() {
                let display = document.getElementById('display');
                display.value = display.value.slice(0, -1);
            }
            
            function calculate() {
                try {
                    let result = eval(document.getElementById('display').value);
                    document.getElementById('display').value = result;
                } catch (error) {
                    document.getElementById('display').value = 'Error';
                }
            }
        </script>
    </body>
    </html>
    """
    
    st.components.v1.html(html_code, height=500)

def javascript_moving_box():
    st.subheader("📦 JavaScript - Moving Color Box")
    
    html_code = r"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Moving Box</title>
        <style>
            body { margin: 0; overflow: hidden; background: #000; }
            #box { 
                position: absolute; 
                width: 50px; 
                height: 50px; 
                background: linear-gradient(45deg, #ff0000, #00ff00, #0000ff);
                border-radius: 10px;
                cursor: pointer;
                transition: all 0.3s ease;
            }
        </style>
    </head>
    <body>
        <div id="box"></div>
        
        <script>
            const box = document.getElementById('box');
            let x = 100, y = 100;
            let dx = 2, dy = 2;
            
            function moveBox() {
                x += dx;
                y += dy;
                
                if (x <= 0 || x >= window.innerWidth - 50) dx = -dx;
                if (y <= 0 || y >= window.innerHeight - 50) dy = -dy;
                
                box.style.left = x + 'px';
                box.style.top = y + 'px';
                
                // Change color randomly
                if (Math.random() < 0.01) {
                    box.style.background = `hsl(${Math.random() * 360}, 70%, 50%)`;
                }
            }
            
            setInterval(moveBox, 50);
            
            box.addEventListener('click', () => {
                dx = (Math.random() - 0.5) * 10;
                dy = (Math.random() - 0.5) * 10;
            });
        </script>
    </body>
    </html>
    """
    
    st.components.v1.html(html_code, height=400)

def javascript_demos_menu():
    st.title("🟨 Java Script")
    
    demo1, demo2, demo3 = st.tabs(["All Task Manager", "Scientific Calculator", "Moving Box"])
    
    with demo1:
        javascript_nodejs_demo()
    
    with demo2:
        javascript_simple_calculator()
    
    with demo3:
        javascript_moving_box()

 