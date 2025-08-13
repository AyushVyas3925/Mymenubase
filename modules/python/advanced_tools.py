# Advanced Python tools module
import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import pygame
import pyttsx3
import librosa
import os
import subprocess
from PIL import Image
import qrcode
import PyPDF2
import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import google.generativeai as genai
import io
import time
import pandas as pd
import psutil
from datetime import datetime
import csv
import tempfile
import matplotlib.pyplot as plt
from instagrapi import Client

def python_face_swap():
    """Face swap application"""
    st.subheader("😊 Face Swap Application")
    st.write("Swap faces between two images")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📸 Source Image")
        source_image = st.file_uploader("Upload source image", type=['jpg', 'jpeg', 'png'], key="face_swap_source")
        
        if source_image:
            st.image(source_image, caption="Source Image", use_column_width=True)
    
    with col2:
        st.subheader("🎭 Target Image")
        target_image = st.file_uploader("Upload target image", type=['jpg', 'jpeg', 'png'], key="face_swap_target")
        
        if target_image:
            st.image(target_image, caption="Target Image", use_column_width=True)
    
    if source_image and target_image:
        if st.button("🔄 Perform Face Swap", key="face_swap_btn"):
            try:
                with st.spinner("Processing face swap..."):
                    # Initialize MediaPipe
                    mp_face_detection = mp.solutions.face_detection
                    mp_drawing = mp.solutions.drawing_utils
                    
                    # Load images
                    source_img = cv2.imdecode(np.frombuffer(source_image.read(), np.uint8), cv2.IMREAD_COLOR)
                    target_img = cv2.imdecode(np.frombuffer(target_image.read(), np.uint8), cv2.IMREAD_COLOR)
                    
                    # Detect faces
                    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
                        source_results = face_detection.process(cv2.cvtColor(source_img, cv2.COLOR_BGR2RGB))
                        target_results = face_detection.process(cv2.cvtColor(target_img, cv2.COLOR_BGR2RGB))
                    
                    if source_results.detections and target_results.detections:
                        st.success("✅ Faces detected! Face swap simulation completed.")
                        st.info("This is a demonstration. In a real implementation, you would use advanced computer vision techniques for actual face swapping.")
                    else:
                        st.warning("⚠️ No faces detected in one or both images")
                        
            except Exception as e:
                st.error(f"❌ Error during face swap: {str(e)}")

def python_hello_world():
    """Hello World application"""
    st.subheader("🌍 Hello World Application")
    st.write("Simple greeting application")
    
    name = st.text_input("Enter your name:", placeholder="World", key="hello_name_input")
    greeting_type = st.selectbox("Select greeting type:", ["Hello", "Hi", "Good morning", "Good evening", "Welcome"])
    
    if name:
        if st.button("👋 Generate Greeting", key="hello_world_btn"):
            st.success(f"{greeting_type}, {name}!")
            
            # Display greeting in different languages
            greetings = {
                "Spanish": f"¡Hola, {name}!",
                "French": f"Bonjour, {name}!",
                "German": f"Hallo, {name}!",
                "Italian": f"Ciao, {name}!",
                "Japanese": f"こんにちは、{name}さん！"
            }
            
            st.subheader("🌍 Greetings in Different Languages")
            for language, greeting in greetings.items():
                st.write(f"**{language}:** {greeting}")

def python_name_input():
    """Name input and processing application"""
    st.subheader("📝 Name Input Application")
    st.write("Process and analyze names")
    
    first_name = st.text_input("Enter first name:", placeholder="John", key="name_first_input")
    last_name = st.text_input("Enter last name:", placeholder="Doe", key="name_last_input")
    
    if first_name and last_name:
        full_name = f"{first_name} {last_name}"
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Name Analysis")
            st.write(f"**Full Name:** {full_name}")
            st.write(f"**Name Length:** {len(full_name)} characters")
            st.write(f"**First Name Length:** {len(first_name)} characters")
            st.write(f"**Last Name Length:** {len(last_name)} characters")
            
            # Count vowels and consonants
            vowels = sum(1 for char in full_name.lower() if char in 'aeiou')
            consonants = sum(1 for char in full_name.lower() if char.isalpha() and char not in 'aeiou')
            
            st.write(f"**Vowels:** {vowels}")
            st.write(f"**Consonants:** {consonants}")
        
        with col2:
            st.subheader("🔄 Name Transformations")
            st.write(f"**Uppercase:** {full_name.upper()}")
            st.write(f"**Lowercase:** {full_name.lower()}")
            st.write(f"**Title Case:** {full_name.title()}")
            st.write(f"**Reversed:** {full_name[::-1]}")
            
            # Generate initials
            initials = '. '.join([name[0].upper() for name in [first_name, last_name]])
            st.write(f"**Initials:** {initials}")

def python_digital_image():
    """Digital image processing application"""
    st.subheader("🖼️ Digital Image Processing")
    st.write("Basic image manipulation and analysis")
    
    uploaded_image = st.file_uploader("Upload an image", type=['jpg', 'jpeg', 'png'], key="digital_image_upload")
    
    if uploaded_image:
        image = Image.open(uploaded_image)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📸 Original Image")
            st.image(image, caption="Original Image", use_column_width=True)
            
            # Image information
            st.write(f"**Size:** {image.size[0]} x {image.size[1]} pixels")
            st.write(f"**Mode:** {image.mode}")
            st.write(f"**Format:** {image.format}")
        
        with col2:
            st.subheader("🔧 Image Operations")
            
            # Resize
            new_width = st.number_input("New width:", min_value=100, max_value=2000, value=image.size[0])
            new_height = st.number_input("New height:", min_value=100, max_value=2000, value=image.size[1])
            
            if st.button("📏 Resize Image", key="resize_img_btn"):
                if uploaded_image is not None:
                    try:
                        resized_image = image.resize((new_width, new_height))
                        st.image(resized_image, caption="Resized Image", use_column_width=True)
                    except Exception as e:
                        st.error(f"Error resizing image: {str(e)}")
            
            # Rotate
            rotation_angle = st.slider("Rotation angle:", -180, 180, 0)
            if st.button("🔄 Rotate Image", key="rotate_img_btn"):
                if uploaded_image is not None:
                    try:
                        rotated_image = image.rotate(rotation_angle)
                        st.image(rotated_image, caption="Rotated Image", use_column_width=True)
                    except Exception as e:
                        st.error(f"Error rotating image: {str(e)}")
            
            # Convert to grayscale
            if st.button("⚫ Convert to Grayscale", key="grayscale_btn"):
                if uploaded_image is not None:
                    try:
                        gray_image = image.convert('L')
                        st.image(gray_image, caption="Grayscale Image", use_column_width=True)
                    except Exception as e:
                        st.error(f"Error converting to grayscale: {str(e)}")

def batch_image_resize():
    """Batch image resizing tool"""
    st.subheader("📏 Batch Image Resizer")
    st.write("Resize multiple images at once")
    
    uploaded_files = st.file_uploader("Upload images", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True, key="batch_resize_upload")
    
    if uploaded_files:
        st.write(f"📁 {len(uploaded_files)} images uploaded")
        
        col1, col2 = st.columns(2)
        
        with col1:
            target_width = st.number_input("Target width:", min_value=100, max_value=2000, value=800)
            target_height = st.number_input("Target height:", min_value=100, max_value=2000, value=600)
            maintain_aspect = st.checkbox("Maintain aspect ratio", value=True)
        
        with col2:
            quality = st.slider("JPEG quality:", 1, 100, 85)
            output_format = st.selectbox("Output format:", ["JPEG", "PNG"])
        
        if st.button("�� Process All Images", key="process_all_btn"):
            if uploaded_files:
                processed_images = []
                
                with st.spinner("Processing images..."):
                    for i, uploaded_file in enumerate(uploaded_files):
                        try:
                            image = Image.open(uploaded_file)
                            
                            if maintain_aspect:
                                # Calculate aspect ratio
                                aspect_ratio = image.size[0] / image.size[1]
                                if target_width / target_height > aspect_ratio:
                                    new_height = target_height
                                    new_width = int(target_height * aspect_ratio)
                                else:
                                    new_width = target_width
                                    new_height = int(target_width / aspect_ratio)
                            else:
                                new_width, new_height = target_width, target_height
                            
                            # Resize image
                            resized_image = image.resize((new_width, new_height))
                            
                            # Save to bytes
                            import io
                            img_byte_arr = io.BytesIO()
                            
                            if output_format == "JPEG":
                                resized_image.save(img_byte_arr, format='JPEG', quality=quality)
                                file_ext = "jpg"
                            else:
                                resized_image.save(img_byte_arr, format='PNG')
                                file_ext = "png"
                            
                            img_byte_arr.seek(0)
                            processed_images.append((img_byte_arr, f"resized_{i+1}.{file_ext}"))
                            
                        except Exception as e:
                            st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                
                if processed_images:
                    st.success(f"✅ {len(processed_images)} images processed successfully!")
                    
                    # Download all images
                    for img_bytes, filename in processed_images:
                        st.download_button(
                            label=f"📥 Download {filename}",
                            data=img_bytes.getvalue(),
                            file_name=filename,
                            mime=f"image/{file_ext}"
                        )

def python_send_sms():
    """SMS sending application"""
    st.subheader("📱 SMS Sending Application")
    st.write("Send SMS messages using Twilio")
    
    # Note: In real implementation, you'd need Twilio credentials
    st.info("ℹ️ This is a demonstration. In production, you need Twilio account credentials.")
    
    phone_number = st.text_input("Recipient phone number:", placeholder="+1234567890", key="sms_phone_input")
    message = st.text_area("Message content:", placeholder="Hello from Python!", key="sms_message_input")
    
    if st.button("📤 Send SMS", key="send_sms_btn_unique"):
        if phone_number and message:
            try:
                # Simulate SMS sending
                st.success("✅ SMS sent successfully!")
                st.info(f"To: {phone_number}")
                st.info(f"Message: {message}")
                
                # Show Twilio integration code
                st.code("""
# Real Twilio integration code:
from twilio.rest import Client

account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
client = Client(account_sid, auth_token)

message = client.messages.create(
    body=message,
    from_='your_twilio_number',
    to=phone_number
)
                """, language='python')
                
            except Exception as e:
                st.error(f"❌ Error sending SMS: {str(e)}")
        else:
            st.warning("Please fill all fields")

def python_Google_Search():
    """Google Search application"""
    st.subheader("🔍 Google Search Application")
    st.write("Search Google programmatically")
    
    search_query = st.text_input("Enter search query:", placeholder="Python programming", key="google_search_input")
    
    if st.button("🔍 Search Google", key="google_search_btn"):
        if search_query:
            try:
                # Create search URL
                search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
                
                st.success("✅ Search completed!")
                st.info(f"Search query: {search_query}")
                
                # Display search results link
                st.markdown(f"[🔍 View Google Search Results]({search_url})")
                
                # Show web scraping code
                st.code("""
# For actual web scraping, you'd use:
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(search_url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract search results
results = soup.find_all('div', class_='g')
                """, language='python')
                
            except Exception as e:
                st.error(f"❌ Error during search: {str(e)}")
        else:
            st.warning("Please enter a search query")

def python_send_email():
    """Email sending application"""
    st.subheader("📧 Email Sending Application")
    st.write("Send emails using SMTP")
    
    st.info("ℹ️ This is a demonstration. In production, you need SMTP server credentials.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sender_email = st.text_input("Sender email:", placeholder="your@email.com", key="email_sender_input")
        sender_password = st.text_input("Sender password:", type="password", placeholder="your_password", key="email_password_input")
        smtp_server = st.text_input("SMTP server:", placeholder="smtp.gmail.com", key="email_smtp_input")
        smtp_port = st.number_input("SMTP port:", min_value=1, max_value=65535, value=587, key="email_port_input")
    
    with col2:
        recipient_email = st.text_input("Recipient email:", placeholder="recipient@email.com", key="email_recipient_input")
        subject = st.text_input("Email subject:", placeholder="Hello from Python!", key="email_subject_input")
        message_body = st.text_area("Message body:", placeholder="This is a test email sent from Python.", key="email_body_input")
    
    if st.button("📤 Send Email", key="send_email_btn"):
        if all([sender_email, sender_password, smtp_server, recipient_email, subject, message_body]):
            try:
                # Simulate email sending
                st.success("✅ Email sent successfully!")
                st.info(f"From: {sender_email}")
                st.info(f"To: {recipient_email}")
                st.info(f"Subject: {subject}")
                
                # Show SMTP integration code
                st.code("""
# Real SMTP integration code:
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = recipient_email
msg['Subject'] = subject

msg.attach(MIMEText(message_body, 'plain'))

server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(sender_email, sender_password)
server.send_message(msg)
server.quit()
                """, language='python')
                
            except Exception as e:
                st.error(f"❌ Error sending email: {str(e)}")
        else:
            st.warning("Please fill all fields")

def python_pdf_to_text():
    """PDF to text converter"""
    st.subheader("📄 PDF to Text Converter")
    st.write("Extract text from PDF files")
    
    uploaded_pdf = st.file_uploader("Upload PDF file", type=['pdf'], key="pdf_to_text_upload")
    
    if uploaded_pdf:
        try:
            # Read PDF
            pdf_reader = PyPDF2.PdfReader(uploaded_pdf)
            
            st.success(f"✅ PDF loaded successfully! Pages: {len(pdf_reader.pages)}")
            
            # Page selection
            page_number = st.selectbox("Select page to extract:", range(len(pdf_reader.pages)))
            
            if st.button("📖 Extract Text", key="extract_text_btn"):
                if uploaded_pdf is not None:
                    try:
                        page = pdf_reader.pages[page_number]
                        text = page.extract_text()
                        
                        st.subheader(f"📄 Page {page_number + 1} Text")
                        st.text_area("Extracted text:", value=text, height=300)
                        
                        # Download extracted text
                        st.download_button(
                            label="📥 Download Text",
                            data=text,
                            file_name=f"extracted_text_page_{page_number + 1}.txt",
                            mime="text/plain"
                        )
                        
                    except Exception as e:
                        st.error(f"❌ Error extracting text: {str(e)}")
            
            # Extract all pages
            if st.button("📚 Extract All Pages", key="extract_all_btn"):
                if uploaded_pdf is not None:
                    try:
                        all_text = ""
                        for i, page in enumerate(pdf_reader.pages):
                            all_text += f"\n--- Page {i + 1} ---\n"
                            all_text += page.extract_text()
                            all_text += "\n"
                        
                        st.subheader("📚 All Pages Text")
                        st.text_area("Extracted text from all pages:", value=all_text, height=400)
                        
                        # Download all text
                        st.download_button(
                            label="📥 Download All Text",
                            data=all_text,
                            file_name="extracted_text_all_pages.txt",
                            mime="text/plain"
                        )
                        
                    except Exception as e:
                        st.error(f"❌ Error extracting all pages: {str(e)}")
                        
        except Exception as e:
            st.error(f"❌ Error reading PDF: {str(e)}")

def python_qr_generator():
    """QR code generator"""
    st.subheader("📱 QR Code Generator")
    st.write("Generate QR codes for various content")
    
    qr_content = st.text_input("Enter content for QR code:", placeholder="https://example.com", key="qr_content_input")
    qr_type = st.selectbox("QR code type:", ["URL", "Text", "Email", "Phone", "WiFi", "Custom"], key="qr_type_select")
    
    if qr_type == "Email":
        email = st.text_input("Email address:", placeholder="user@example.com", key="qr_email_input")
        subject = st.text_input("Email subject:", placeholder="Hello", key="qr_subject_input")
        body = st.text_area("Email body:", placeholder="This is a test email", key="qr_body_input")
        if email and subject and body:
            qr_content = f"mailto:{email}?subject={subject}&body={body}"
    
    elif qr_type == "Phone":
        phone = st.text_input("Phone number:", placeholder="+1234567890", key="qr_phone_input")
        if phone:
            qr_content = f"tel:{phone}"
    
    elif qr_type == "WiFi":
        ssid = st.text_input("WiFi SSID:", placeholder="MyWiFi", key="qr_ssid_input")
        password = st.text_input("WiFi password:", placeholder="mypassword123", key="qr_password_input")
        encryption = st.selectbox("Encryption:", ["WPA", "WEP", "nopass"], key="qr_encryption_select")
        if ssid and password:
            qr_content = f"WIFI:S:{ssid};T:{encryption};P:{password};;"
    
    if qr_content:
        col1, col2 = st.columns(2)
        
        with col1:
            # QR code customization
            qr_size = st.slider("QR code size:", 100, 400, 200)
            qr_color = st.color_picker("QR code color:", "#000000")
            bg_color = st.color_picker("Background color:", "#FFFFFF")
        
        with col2:
            if st.button("🔲 Generate QR Code", key="qr_generate_btn"):
                try:
                    # Create QR code
                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4,
                    )
                    qr.add_data(qr_content)
                    qr.make(fit=True)
                    
                    # Create QR code image
                    qr_image = qr.make_image(fill_color=qr_color, back_color=bg_color)
                    qr_image = qr_image.resize((qr_size, qr_size))
                    
                    # Convert to PIL Image for display
                    qr_pil = Image.fromarray(np.array(qr_image))
                    
                    st.image(qr_pil, caption="Generated QR Code", use_column_width=True)
                    
                    # Download QR code
                    import io
                    img_byte_arr = io.BytesIO()
                    qr_pil.save(img_byte_arr, format='PNG')
                    img_byte_arr.seek(0)
                    
                    st.download_button(
                        label="📥 Download QR Code",
                        data=img_byte_arr.getvalue(),
                        file_name="qr_code.png",
                        mime="image/png"
                    )
                    
                except Exception as e:
                    st.error(f"❌ Error generating QR code: {str(e)}")

def python_make_call():
    """Voice call application"""
    st.subheader("📞 Voice Call Application")
    st.write("Make voice calls using Twilio")
    
    st.info("ℹ️ This is a demonstration. In production, you need Twilio account credentials.")
    
    phone_number = st.text_input("Recipient phone number:", placeholder="+1234567890", key="call_phone_input")
    message = st.text_area("Message to speak:", placeholder="Hello, this is a test call from Python!", key="call_message_input")
    
    if st.button("📞 Make Call", key="make_call_btn"):
        if phone_number and message:
            try:
                # Simulate call
                st.success("✅ Call initiated successfully!")
                st.info(f"To: {phone_number}")
                st.info(f"Message: {message}")
                
                # Show Twilio integration code
                st.code("""
# Real Twilio voice call integration:
from twilio.rest import Client

account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
client = Client(account_sid, auth_token)

call = client.calls.create(
    twiml=f'<Response><Say>{message}</Say></Response>',
    from_='your_twilio_number',
    to=phone_number
)
                """, language='python')
                
            except Exception as e:
                st.error(f"❌ Error making call: {str(e)}")
        else:
            st.warning("Please fill all fields")

def python_gemini_api():
    """Gemini API integration"""
    st.subheader("🤖 Gemini API Integration")
    st.write("Interact with Google's Gemini AI model")
    
    st.info("ℹ️ This is a demonstration. In production, you need a Gemini API key.")
    
    api_key = st.text_input("Gemini API Key:", type="password", placeholder="your_api_key_here", key="gemini_api_key_input")
    prompt = st.text_area("Enter your prompt:", placeholder="Explain quantum computing in simple terms", key="gemini_prompt_input")
    
    if st.button("🚀 Generate Response", key="gemini_generate_btn"):
        if prompt and api_key:
            try:
                # Simulate Gemini API call
                st.success("✅ Response generated successfully!")
                
                # Show sample response
                sample_response = f"""
Here's a response to your prompt: "{prompt}"

This is a demonstration response. In a real implementation, you would:

1. Configure the Gemini API with your key
2. Send the prompt to the API
3. Receive and display the AI-generated response

The actual response would depend on your specific prompt and the Gemini model's capabilities.
                """
                
                st.text_area("AI Response:", value=sample_response, height=300)
                
                # Show Gemini integration code
                st.code("""
# Real Gemini API integration:
import google.generativeai as genai

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

response = model.generate_content(prompt)
print(response.text)
                """, language='python')
                
            except Exception as e:
                st.error(f"❌ Error generating response: {str(e)}")
        else:
            st.warning("Please provide API key and prompt")

def python_instagram_post_creator():
    """Instagram post creator using instagrapi"""
    st.subheader("📱 Instagram Post Creator")
    st.write("Post to Instagram using your credentials")
    
    # Instagram credentials
    st.subheader("🔐 Instagram Credentials")
    col1, col2 = st.columns(2)
    
    with col1:
        username = st.text_input("Instagram Username:", placeholder="your_username", key="ig_username_input")
        password = st.text_input("Instagram Password:", type="password", placeholder="your_password", key="ig_password_input")
    
    with col2:
        st.info("""
        **📋 Instructions:**
        1. Use your Instagram username and password
        2. Make sure 2FA is disabled or use app password
        3. Be careful with your credentials
        """)
    
    st.markdown("---")
    
    # Post content
    st.subheader("📝 Post Content")
    caption = st.text_area("Caption:", placeholder="Write your Instagram caption here...", height=150, key="ig_caption_input")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload Image/Video:", 
        type=["jpg", "jpeg", "png", "mp4", "mov"], 
        key="ig_file_uploader"
    )
    
    if uploaded_file:
        st.image(uploaded_file, caption="Preview", use_column_width=True)
    
    # Post button
    if st.button("📤 Post to Instagram", key="ig_post_btn", use_container_width=True):
        if not all([username, password, caption, uploaded_file]):
            st.warning("⚠️ Please fill all fields including file upload.")
        else:
            try:
                with st.spinner("📤 Posting to Instagram..."):
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_file_path = tmp_file.name
                    
                    # Initialize Instagram client
                    cl = Client()
                    
                    # Login
                    cl.login(username, password)
                    
                    # Upload photo/video
                    if uploaded_file.type.startswith('image'):
                        result = cl.photo_upload(path=tmp_file_path, caption=caption)
                    else:
                        result = cl.video_upload(path=tmp_file_path, caption=caption)
                    
                    # Clean up temp file
                    os.unlink(tmp_file_path)
                    
                    st.success("✅ Instagram post created successfully!")
                    st.info(f"Post ID: {result.id}")
                    
                    # Clear form
                    st.session_state.ig_username_input = ""
                    st.session_state.ig_password_input = ""
                    st.session_state.ig_caption_input = ""
                    st.rerun()
                    
            except Exception as e:
                st.error(f"❌ Error posting to Instagram: {str(e)}")
                st.info("💡 Common issues: Check credentials, internet connection, or Instagram restrictions")

def python_send_email_app():
    """Email sending application"""
    st.subheader("📧 Email Bhejne Wala App")
    st.write("Send emails directly from your application")

    # Import necessary modules locally
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    # Email configuration inputs
    st.subheader("🔐 Email Configuration")
    col1, col2 = st.columns(2)
    
    with col1:
        sender_email = st.text_input("Sender Email (Gmail):", placeholder="your.email@gmail.com", key="email_app_sender_input")
        app_password = st.text_input("App Password:", type="password", placeholder="Enter Gmail App Password", key="email_app_password_input")
    
    with col2:
        st.info("""
        **📋 Instructions:**
        1. Use your Gmail address
        2. Generate App Password from Google Account settings
        3. Enable 2-factor authentication first
        4. Use App Password, not your regular password
        """)
    
    st.markdown("---")
    
    # Email content inputs
    st.subheader("📝 Email Content")
    receiver_email = st.text_input("Receiver Email:", placeholder="recipient@example.com", key="email_app_receiver_input")
    subject = st.text_input("Subject:", key="email_app_subject_input")
    message = st.text_area("Message:", key="email_app_message_input", height=150)
    
    if st.button("📤 Send Email", key="send_email_app_btn", use_container_width=True):
        if not all([sender_email, app_password, receiver_email, subject, message]):
            st.warning("⚠️ Please fill out all fields including email configuration.")
        else:
            try:
                # Create the email
                email_msg = MIMEMultipart()
                email_msg["From"] = sender_email
                email_msg["To"] = receiver_email
                email_msg["Subject"] = subject
                email_msg.attach(MIMEText(message, "plain"))

                # Connect to Gmail SMTP server
                with st.spinner("📤 Sending email..."):
                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.starttls()
                    server.login(sender_email, app_password)
                    server.sendmail(sender_email, receiver_email, email_msg.as_string())
                    server.quit()
                st.success("✅ Email sent successfully!")
                
                # Clear form
                st.session_state.email_app_receiver_input = ""
                st.session_state.email_app_subject_input = ""
                st.session_state.email_app_message_input = ""
                st.rerun()
                
            except smtplib.SMTPAuthenticationError:
                st.error("❌ Authentication failed! Please check your email and app password.")
            except smtplib.SMTPRecipientsRefused:
                st.error("❌ Invalid recipient email address.")
            except Exception as e:
                st.error(f"❌ Error sending email: {str(e)}")

def python_advanced_ram_reader():
    """Advanced RAM monitoring tool"""
    st.subheader("🧠 Advanced RAM Monitor")
    st.markdown("This tool displays real-time memory usage using the **psutil** library.")

    # Helper Functions
    def log_ram_to_csv(file_name='ram_log.csv'):
        ram = psutil.virtual_memory()
        # Create header if file doesn't exist
        if not os.path.exists(file_name):
            with open(file_name, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Time", "Total_GB", "Available_GB", "Used_GB", "Usage_%"])
        # Append data
        with open(file_name, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                round(ram.total / (1024 ** 3), 2),
                round(ram.available / (1024 ** 3), 2),
                round(ram.used / (1024 ** 3), 2),
                ram.percent
            ])

    def get_top_memory_processes(n=5):
        processes = []
        for p in psutil.process_iter(['name', 'memory_info']):
            try:
                # memory_info().rss returns memory usage in bytes
                processes.append((p.info['name'], p.info['memory_info'].rss))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        top = sorted(processes, key=lambda x: x[1], reverse=True)[:n]
        return top

    # Main App UI
    if 'ram_info' not in st.session_state:
        st.session_state.ram_info = None

    if st.button("�� Refresh RAM Info", key="refresh_ram_btn", use_container_width=True):
        ram = psutil.virtual_memory()
        swap = psutil.swap_memory()
        top_procs = get_top_memory_processes()
        st.session_state.ram_info = {
            "ram": ram, "swap": swap, "top_procs": top_procs
        }
        log_ram_to_csv() # Log data on each refresh

    if st.session_state.ram_info:
        ram = st.session_state.ram_info["ram"]
        swap = st.session_state.ram_info["swap"]
        top_procs = st.session_state.ram_info["top_procs"]

        st.subheader("📊 Real-time RAM Information")
        col1, col2 = st.columns(2)
        col1.metric("Total RAM", f"{ram.total / (1024 ** 3):.2f} GB")
        col2.metric("Used RAM", f"{ram.used / (1024 ** 3):.2f} GB", delta=f"{ram.percent}% Used")
        
        st.progress(ram.percent / 100)
        if ram.percent >= 80:
            st.error("⚠️ ALERT: High RAM usage detected!")

        st.subheader("🔥 Top 5 Memory Consuming Processes")
        df = pd.DataFrame(
            [(p[0], f"{p[1]/(1024**2):.2f} MB") for p in top_procs],
            columns=["Process Name", "Memory Usage"]
        )
        st.table(df)

    # Display historical logs
    st.subheader("📁 RAM Usage Log (Last 20 Readings)")
    try:
        log_df = pd.read_csv("ram_log.csv")
        st.line_chart(log_df.set_index("Time")[["Used_GB", "Available_GB"]].tail(20))
    except FileNotFoundError:
        st.info("No log file found yet. Click 'Refresh RAM Info' to start logging.")

def advanced_python_tools_menu():
    """Main advanced Python tools menu"""
    st.title("🐍 Advanced Python Tools")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Computer Vision", "Image Processing", "Communication", "AI Integration", "Social Media"
    ])

    with tab1:
        st.subheader("👁️ Computer Vision Tools")
        python_face_swap()

    with tab2:
        st.subheader("🖼️ Image Processing")
        col1, col2 = st.columns(2)
        with col1:
            python_digital_image()
        with col2:
            batch_image_resize()

    with tab3:
        st.subheader("📱 Communication Tools")
        col1, col2 = st.columns(2)
        with col1:
            python_send_sms()
            python_send_email()
        with col2:
            python_make_call()
            python_Google_Search()

    with tab4:
        st.subheader("🤖 AI & Data Tools")
        col1, col2 = st.columns(2)
        with col1:
            python_pdf_to_text()
            python_qr_generator()
        with col2:
            python_gemini_api()
            python_advanced_ram_reader()

    with tab5:
        st.subheader("📱 Social Media Tools")
        col1, col2 = st.columns(2)
        with col1:
            python_instagram_post_creator()
        with col2:
            python_send_email_app()
