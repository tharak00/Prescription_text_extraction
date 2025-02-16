import streamlit as st
import google.generativeai as genai
from PIL import Image
import requests
from io import BytesIO
import time

# Set Gemini API Key (Replace with your actual key)
GEMINI_API_KEY = "AIzaSyCLz0_Vlm9uhurPJmiOMHQnEHD-rHrucrE"
genai.configure(api_key=GEMINI_API_KEY)

# Banner Image URL
BANNER_IMAGE_URL = "https://pharmacyconnection.ca/wp-content/uploads/2023/08/banner_detecting_fraudulent_prescriptions.jpg"

# Supported image formats
SUPPORTED_FORMATS = ["jpg", "jpeg", "png", "bmp", "webp", "tiff"]

# Function to extract text & detect medicine names using Gemini 1.5 Flash
def get_medicine_info(image):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        "Extract text from this prescription image. Identify medicine names and provide "
        "clear, concise details for each detected medicine including usage, side effects, and dosage."
    )

    try:
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"❌ Error fetching data: {e}"

# Streamlit UI Configuration
st.set_page_config(page_title="Prescription Analyzer", page_icon="💊", layout="wide")

# Custom CSS for Animations and UI Improvements
st.markdown(
    """
    <style>
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .banner-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
            animation: fadeIn 1.5s ease-in-out;
        }

        .title-container h1 {
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #2E8B57;
            animation: fadeIn 2s ease-in-out;
        }

        .upload-button label {
            background-color: #2E8B57;
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 18px;
            cursor: pointer;
            transition: background 0.3s ease;
        }

        .upload-button label:hover {
            background-color: #246C4F;
        }

        .loading-animation {
            font-size: 18px;
            font-weight: bold;
            color: #2E8B57;
            animation: fadeIn 1.5s ease-in-out infinite alternate;
        }

        .output-container {
            background: #f4f4f4;
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
            font-size: 16px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Banner Layout
st.markdown(
    f"""
    <div class="banner-container">
        <div class="title-container">
            <h1>💊 Prescription Text extractor </h1>
            <h4>Upload a prescription image to extract medicine names and details.</h4>
        </div>
        <img src="{BANNER_IMAGE_URL}" width="500" style="border-radius: 10px;">
    </div>
    """,
    unsafe_allow_html=True
)

# File uploader with styling
st.markdown('<div class="upload-button">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload Prescription Image", type=SUPPORTED_FORMATS)
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    st.markdown("---")
    st.subheader("📸 Uploaded Image")
    image = Image.open(uploaded_file)
    st.image(image, caption="Prescription Image", use_container_width=True)

    # Animated Loading Effect
    with st.spinner("⏳ Extracting medicine details... Please wait!"):
        time.sleep(2)  # Simulating processing time
        result = get_medicine_info(image)

    # Display Extracted Text
    st.markdown('<div class="output-container">', unsafe_allow_html=True)
    st.markdown("### ✅ Extracted Information:")
    st.write(result)
    st.markdown('</div>', unsafe_allow_html=True)
