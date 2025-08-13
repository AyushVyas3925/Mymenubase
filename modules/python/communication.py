# Python communication utilities module
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
from config.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

def email_sender():
    """Email sending functionality"""
    st.subheader("📧 Email Sender")
    
    # Email configuration
    sender_email = st.text_input("Your Email:")
    sender_password = st.text_input("Your Password:", type="password")
    receiver_email = st.text_input("Receiver Email:")
    subject = st.text_input("Subject:")
    message = st.text_area("Message:")
    
    if st.button("📤 Send Email"):
        if sender_email and sender_password and receiver_email and subject and message:
            try:
                # Create message
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = receiver_email
                msg['Subject'] = subject
                msg.attach(MIMEText(message, 'plain'))
                
                # Send email
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, sender_password)
                text = msg.as_string()
                server.sendmail(sender_email, receiver_email, text)
                server.quit()
                
                st.success("✅ Email sent successfully!")
            except Exception as e:
                st.error(f"❌ Error sending email: {e}")
        else:
            st.warning("⚠️ Please fill all fields!")

def sms_sender():
    """SMS sending functionality using Twilio"""
    st.subheader("📱 SMS Sender")
    
    # SMS configuration
    receiver_phone = st.text_input("Receiver Phone Number (with country code):")
    message = st.text_area("SMS Message:")
    
    if st.button("📤 Send SMS"):
        if receiver_phone and message:
            try:
                # Initialize Twilio client
                client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                
                # Send SMS
                message_obj = client.messages.create(
                    body=message,
                    from_=TWILIO_PHONE_NUMBER,
                    to=receiver_phone
                )
                
                st.success(f"✅ SMS sent successfully! SID: {message_obj.sid}")
            except Exception as e:
                st.error(f"❌ Error sending SMS: {e}")
        else:
            st.warning("⚠️ Please fill all fields!")

def call_sender():
    """Voice call functionality using Twilio"""
    st.subheader("📞 Voice Call")
    
    # Call configuration
    receiver_phone = st.text_input("Receiver Phone Number (with country code):")
    message = st.text_area("Message to speak:")
    
    if st.button("📞 Make Call"):
        if receiver_phone and message:
            try:
                # Initialize Twilio client
                client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                
                # Make call
                call = client.calls.create(
                    twiml=f'<Response><Say>{message}</Say></Response>',
                    from_=TWILIO_PHONE_NUMBER,
                    to=receiver_phone
                )
                
                st.success(f"✅ Call initiated successfully! Call SID: {call.sid}")
            except Exception as e:
                st.error(f"❌ Error making call: {e}")
        else:
            st.warning("⚠️ Please fill all fields!")

def communication_menu():
    """Main communication menu"""
    st.subheader("📡 Communication Tools")
    
    comm_options = ["Email Sender", "SMS Sender", "Voice Call"]
    selected = st.selectbox("Select Communication Tool:", comm_options)
    
    if selected == "Email Sender":
        email_sender()
    elif selected == "SMS Sender":
        sms_sender()
    elif selected == "Voice Call":
        call_sender()
