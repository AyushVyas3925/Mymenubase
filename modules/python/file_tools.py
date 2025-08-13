# Python file processing tools module
import streamlit as st
import PyPDF2
from PIL import Image
import os
import qrcode
import io

def pdf_tools():
    """PDF processing tools"""
    st.subheader("📄 PDF Tools")
    
    pdf_file = st.file_uploader("Upload PDF file", type=['pdf'])
    
    if pdf_file is not None:
        if st.button("📖 Read PDF"):
            try:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                
                st.text_area("PDF Content:", text, height=300)
                st.info(f"Total pages: {len(pdf_reader.pages)}")
            except Exception as e:
                st.error(f"Error reading PDF: {e}")

def image_tools():
    """Image processing tools"""
    st.subheader("🖼️ Image Tools")
    
    image_file = st.file_uploader("Upload image", type=['png', 'jpg', 'jpeg'])
    
    if image_file is not None:
        image = Image.open(image_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Convert to Grayscale"):
                gray_image = image.convert('L')
                st.image(gray_image, caption="Grayscale Image", use_column_width=True)
        
        with col2:
            if st.button("📏 Show Image Info"):
                st.write(f"**Format:** {image.format}")
                st.write(f"**Size:** {image.size}")
                st.write(f"**Mode:** {image.mode}")

def qr_generator():
    """QR code generator"""
    st.subheader("🔲 QR Code Generator")
    
    data = st.text_input("Enter data for QR code:")
    if data:
        if st.button("🔲 Generate QR Code"):
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            st.image(img, caption="Generated QR Code", use_column_width=True)
            
            # Download button
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            st.download_button(
                label="📥 Download QR Code",
                data=buf.getvalue(),
                file_name="qr_code.png",
                mime="image/png"
            )

def file_analyzer():
    """File analysis tools"""
    st.subheader("📊 File Analyzer")
    
    uploaded_file = st.file_uploader("Upload any file for analysis", type=None)
    
    if uploaded_file is not None:
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size} bytes",
            "File type": uploaded_file.type
        }
        
        st.write("**File Details:**")
        for key, value in file_details.items():
            st.write(f"**{key}:** {value}")

def file_tools_menu():
    """Main file tools menu"""
    st.subheader("📁 File Processing Tools")
    
    tool_options = ["PDF Tools", "Image Tools", "QR Generator", "File Analyzer"]
    selected = st.selectbox("Select File Tool:", tool_options)
    
    if selected == "PDF Tools":
        pdf_tools()
    elif selected == "Image Tools":
        image_tools()
    elif selected == "QR Generator":
        qr_generator()
    elif selected == "File Analyzer":
        file_analyzer()
