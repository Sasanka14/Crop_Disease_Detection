import streamlit as st
import tensorflow as tf
import numpy as np
import time 
from PIL import Image
import base64
import requests
import json

# Set page title, favicon, and page layout
st.set_page_config(
    page_title="AgriNext | AI Crop Disease Detection",
    page_icon="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzIiIGhlaWdodD0iMzIiIHZpZXdCb3g9IjAgMCAzMiAzMiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiBmaWxsPSJub25lIj4KICA8IS0tIENpcmN1bGFyIGJhY2tncm91bmQgLS0+CiAgPGNpcmNsZSBjeD0iMTYiIGN5PSIxNiIgcj0iMTUiIGZpbGw9IiM0Q0FGNTAiIHN0cm9rZT0iIzJFN0QzMiIgc3Ryb2tlLXdpZHRoPSIyIi8+ICA8IS0tIFNwcm91dGluZyBsZWFmIGluc2lkZSB0aGUgY2lyY2xlIC0tPiAgPHBhdGggZD0iTTE2IDIwIFExOCAxNCwgMjIgMTIgUTE4IDE2LCAxNiAyNCIgc3Ryb2tlPSIjRkZDMTA3IiBzdHJva2Utd2lkdGg9IjIiIGZpbGw9Im5vbmUiLz4KICA8cGF0aCBkPSJNMTYgMjQgUTE0IDE2LCAxMCAxNCBRMTQgMTgsIDE2IDI0IiBzdHJva2U9IiNGRkMxMDciIHN0cm9rZS13aWR0aD0iMiIgZmlsbD0ibm9uZSIvPgo8L3N2Zz4=",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Sasanka14',
        'Report a bug': "mailto:sasankasekharkundu24@gmail.com",
        'About': "# AgriNext - Empowering Farmers with AI\nDetect crop diseases instantly and get treatment recommendations."
    }
)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Modern color scheme */
    :root {
        --primary: #2E7D32;
        --secondary: #81C784;
        --accent: #4CAF50;
        --background: #FFFFFF;
        --text: #212121;
        --light-bg: #F5F5F5;
    }
    
    /* Overall page styling */
    .main {
        background-color: var(--background);
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4 {
        color: var(--primary);
        font-family: 'Inter', sans-serif;
        font-weight: 700;
    }
    
    /* Card-like components */
    .css-1r6slb0 {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 1.5rem;
        margin-bottom: 1rem;
        background-color: var(--light-bg);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .css-1r6slb0:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Button styling */
    .stButton>button {
        background-color: var(--primary) !important;
        color: white !important;
        border-radius: 30px !important;
        padding: 0.5rem 2rem !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        background-color: var(--accent) !important;
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--light-bg);
    }
    
    /* Modern sidebar styling */
    .sidebar .sidebar-content {
        background-image: linear-gradient(180deg, rgba(46,125,50,0.05) 0%, rgba(46,125,50,0.01) 100%);
    }
    
    /* Modern nav item styling */
    .nav-item {
        padding: 0.75rem 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        font-weight: 500;
    }
    
    .nav-item:hover {
        background-color: rgba(46,125,50,0.1);
        transform: translateX(5px);
    }
    
    .nav-item.active {
        background-color: rgba(46,125,50,0.2);
        color: var(--primary);
        font-weight: 600;
    }
    
    .nav-icon {
        margin-right: 10px;
        font-size: 1.2rem;
    }
    
    /* Social link styling */
    .social-links {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin: 15px 0;
    }
    
    .social-icon {
        padding: 8px;
        border-radius: 50%;
        background-color: rgba(255,255,255,0.8);
        transition: all 0.3s ease;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .social-icon:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        background-color: white;
    }
    
    /* File uploader styling */
    .css-1v3fvcr label {
        background-color: var(--primary);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background-color: var(--accent) !important;
    }
    
    /* Add animation for content transitions */
    .animate-fade-in {
        animation: fadeIn 0.6s ease-in-out;
    }
    
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main {
            padding: 0.5rem;
        }
        
        h1 {
            font-size: 1.8rem !important;
        }
        
        h2 {
            font-size: 1.5rem !important;
        }
    }
    
    /* Custom image gallery */
    .image-gallery {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: center;
    }
    
    .image-card {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .image-card:hover {
        transform: scale(1.03);
    }
    
    /* Results container */
    .results-container {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        border-left: 5px solid var(--primary);
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        0% { transform: translateX(-20px); opacity: 0; }
        100% { transform: translateX(0); opacity: 1; }
    }
    
    /* Sidebar brand container */
    .sidebar-brand {
        padding: 1.5rem 1rem;
        margin-bottom: 1rem;
        text-align: center;
        border-bottom: 1px solid rgba(46,125,50,0.1);
        background: linear-gradient(180deg, rgba(46,125,50,0.05) 0%, rgba(255,255,255,0) 100%);
    }
    
    /* Sidebar section styling */
    .sidebar-section {
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 10px;
        background-color: rgba(255,255,255,0.7);
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    .sidebar-section h4 {
        margin-top: 0;
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 1.1rem;
    }
    
    .sidebar-footer {
        padding: 1rem;
        margin-top: 2rem;
        text-align: center;
        font-size: 0.8rem;
        color: #666;
        border-top: 1px solid rgba(46,125,50,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Function to add background image
def add_bg_from_url():
            st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://img.freepik.com/free-vector/hand-painted-watercolor-nature-background_23-2148941599.jpg?w=1380&t=st=1686818359~exp=1686818959~hmac=abfc74d04bf8e718f8fa825083c8c729ca70ed39aa63bed37d803c4ca01e9848");
             background-attachment: fixed;
             background-size: cover;
             background-position: center;
             background-repeat: no-repeat;
             background-color: rgba(255, 255, 255, 0.7);
             backdrop-filter: blur(5px);
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

# Add subtle background image
add_bg_from_url()

# Load animation files
# No longer need Lottie animations, using GIF file instead
# Define a function to get a fallback image in case GIF doesn't load
def get_fallback_image():
    return "https://img.icons8.com/color/480/artificial-intelligence.png"

# TensorFlow Model Prediction Function
def model_prediction(test_image):
    model = tf.keras.models.load_model("trained_plant_disease_model_save.keras")
    image = tf.keras.preprocessing.image.load_img(test_image,target_size=(32,32))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr]) #convert single image to batch
    predictions = model.predict(input_arr)
    return np.argmax(predictions) #return index of max element

# Get prediction with confidence score (enhanced version)
def model_prediction_with_confidence(test_image):
    model = tf.keras.models.load_model("trained_plant_disease_model_save.keras")
    image = tf.keras.preprocessing.image.load_img(test_image,target_size=(32,32))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr]) #convert single image to batch
    predictions = model.predict(input_arr)
    class_idx = np.argmax(predictions[0])
    confidence = float(predictions[0][class_idx])
    return class_idx, confidence

# Treatment Suggestions based on Disease Class
def get_treatment(disease_name):
    treatments = {
      'Apple__Apple_scab': "For Apple Scab, apply copper fungicides and remove infected leaves. Avoid overhead irrigation.",
    'Apple_Black_rot': "For Black Rot, remove infected fruits, prune dead wood, and apply fungicides.",
    'Apple_Cedar_apple_rust': "For Cedar Apple Rust, apply fungicides such as myclobutanil and remove infected leaves.",
    'Apple__healthy': "No treatment needed, the plant is healthy.",
    'Blueberry__healthy': "No treatment needed, the plant is healthy.",
    'Blueberry_Mummy_berry': "For Mummy Berry, remove infected berries and apply fungicides before blooming.",
    'Cherry(including_sour)_Powdery_mildew': "For Powdery Mildew, apply fungicides and prune infected parts of the plant.",
    'Grape__Black_rot': "For Black Rot in Grapes, apply fungicides like Mancozeb and remove infected vines and fruit.",
    'Grape__Esca': "For Esca, remove infected grapevines and apply fungicides. Use resistant varieties.",
    'Orange_Haunglongbing(Citrus_greening)': "For Citrus Greening, use disease-resistant varieties and control insect vectors.",
    'Peach__Bacterial_spot': "For Bacterial Spot in Peaches, prune infected branches, and apply copper-based fungicides.",
    'Peach__healthy': "No treatment needed, the plant is healthy.",
    'Pepper_Bacterial_spot': "For Bacterial Spot in Peppers, remove infected plants, and apply copper fungicides.",
    'Potato__Early_blight': "For Early Blight in Potatoes, apply fungicides, remove infected leaves, and rotate crops.",
    'Potato__Late_blight': "For Late Blight in Potatoes, apply fungicides like chlorothalonil and remove infected tubers.",
    'Tomato__Bacterial_spot': "For Bacterial Spot in Tomatoes, remove affected leaves and apply copper-based treatments.",
    'Tomato__Early_blight': "For Early Blight in Tomatoes, apply fungicides and prune infected parts of the plant.",
    'Tomato__Late_blight': "For Late Blight in Tomatoes, use fungicides like chlorothalonil and remove infected leaves.",
    'Tomato__Septoria_leaf_spot': "For Septoria Leaf Spot in Tomatoes, apply fungicides and remove infected leaves.",
    'Tomato__Yellow_leaf_curl_virus': "For Yellow Leaf Curl Virus, remove infected plants and control insect vectors.",
    'Strawberry__Leaf_scorch': "For Leaf Scorch in Strawberries, remove infected leaves and apply fungicides.",
    'Squash__Powdery_mildew': "For Powdery Mildew in Squash, apply fungicides and prune affected leaves.",
    'Soybean__Healthy': "No treatment needed, the plant is healthy.",
    'Soybean__Frogeye_leaf_spot': "For Frogeye Leaf Spot, apply fungicides like strobilurins and remove infected parts.",
    'Wheat__Septoria_leaf_spot': "For Septoria Leaf Spot in Wheat, apply fungicides and remove infected leaves.",
    'Wheat__Stripe_rust': "For Stripe Rust in Wheat, apply fungicides and use resistant wheat varieties.",
    'Wheat__Healthy': "No treatment needed, the plant is healthy.",
    'Corn__Healthy': "No treatment needed, the plant is healthy.",
    'Corn__Common_rust': "For Common Rust in Corn, apply fungicides and remove infected parts.",
    'Corn__Northern_leaf_blade_spot': "For Northern Leaf Blade Spot in Corn, apply fungicides and remove infected leaves.",
    'Corn__Southern_leaf_blade_spot': "For Southern Leaf Blade Spot in Corn, use resistant varieties and apply fungicides.",
    'Corn__Gray_leaf_spot': "For Gray Leaf Spot in Corn, apply fungicides and rotate crops to reduce infection.",
    'Corn__Maize_dwarf_mosaic_virus': "For Maize Dwarf Mosaic Virus, control aphids and remove infected plants.",
    'Cotton__Healthy': "No treatment needed, the plant is healthy.",
    'Cotton__Cotton_leaf_roll': "For Cotton Leaf Roll, use insecticides to control whiteflies and remove infected leaves.",
    'Cotton__Bacterial_blite': "For Bacterial Blight in Cotton, apply copper-based treatments and remove infected parts.",
    'Rice__Healthy': "No treatment needed, the plant is healthy.",
    'Rice__Blast': "For Blast Disease in Rice, apply fungicides such as Tricyclazole and use resistant varieties.",
    'Rice__Brown_spot': "For Brown Spot in Rice, apply fungicides and remove infected plants.",
    'Rice__Leaf_blight': "For Leaf Blight in Rice, apply fungicides and practice crop rotation.",
    'Rice__Stem_rot': "For Stem Rot in Rice, use resistant varieties and apply fungicides like carbendazim."
    }
    
    return treatments.get(disease_name, "No treatment suggestion available for this disease.")


# Sidebar
with st.sidebar:
    # Brand header with SVG logo
    st.markdown("""
    <div class="sidebar-brand">
        <div style="text-align: center;">
        <svg width="100" height="30" viewBox="0 0 200 60" xmlns="http://www.w3.org/2000/svg" fill="none">
          <!-- Leaf integrated with A -->
          <path d="M20 50 L35 10 L50 50" stroke="#4CAF50" stroke-width="5" fill="none"/>
          <path d="M35 10 Q40 20, 35 30 Q30 40, 35 50" stroke="#4CAF50" stroke-width="3" fill="none"/>
          <!-- AgriNext Text -->
          <text x="55" y="45" font-family="Arial, sans-serif" font-size="30" font-weight="bold" fill="#2E7D32">AgriNext</text>
          <!-- Sun above "i" -->
          <circle cx="90" cy="20" r="5" fill="#FFC107" />
        </svg>
        </div>
        <p style="margin: 0.3rem 0 0 0; font-size: 0.9rem; color: #666;">AI-Powered Crop Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Simple navigation header
    st.markdown("### 🧭 Navigation")
    
    # Simple, large, easy-to-understand navigation buttons
    app_mode = st.radio(
        "",
        ["🏠 Home", "ℹ️ About", "🔍 Disease Recognition"],
        label_visibility="collapsed"
    )
    
    # Add space after navigation
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Simple Help Section
    st.markdown("### ❓ Help")
    with st.expander("How to Use"):
        st.write("1. Select a page from above")
        st.write("2. On Disease Recognition page, upload a crop image")
        st.write("3. Click Analyze and get instant results")
        st.write("4. Follow the treatment recommendations")
    
    # Simple Connect Section  
    st.markdown("### 🔗 Connect")
    st.markdown("""
    <div style="display: flex; flex-direction: column; gap: 8px;">
        <a href="https://www.instagram.com/__kuronotsubasa__/profilecard/?igsh=MWdyNHd2NDFzZWl3Yw==" target="_blank" style="display: flex; align-items: center; text-decoration: none; color: inherit;">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#E1306C" viewBox="0 0 16 16" style="margin-right: 8px;">
                <path d="M8 0C5.829 0 5.556.01 4.703.048 3.85.088 3.269.222 2.76.42a3.917 3.917 0 0 0-1.417.923A3.927 3.927 0 0 0 .42 2.76C.222 3.268.087 3.85.048 4.7.01 5.555 0 5.827 0 8.001c0 2.172.01 2.444.048 3.297.04.852.174 1.433.372 1.942.205.526.478.972.923 1.417.444.445.89.719 1.416.923.51.198 1.09.333 1.942.372C5.555 15.99 5.827 16 8 16s2.444-.01 3.298-.048c.851-.04 1.434-.174 1.943-.372a3.916 3.916 0 0 0 1.416-.923c.445-.445.718-.891.923-1.417.198-.509.333-1.09.372-1.942C15.99 10.445 16 10.173 16 8s-.01-2.445-.048-3.299c-.04-.851-.175-1.433-.372-1.941a3.926 3.926 0 0 0-.923-1.417A3.911 3.911 0 0 0 13.24.42c-.51-.198-1.092-.333-1.943-.372C10.443.01 10.172 0 7.998 0h.003zm-.717 1.442h.718c2.136 0 2.389.007 3.232.046.78.035 1.204.166 1.486.275.373.145.64.319.92.599.28.28.453.546.598.92.11.281.24.705.275 1.485.039.843.047 1.096.047 3.231s-.008 2.389-.047 3.232c-.035.78-.166 1.203-.275 1.485a2.47 2.47 0 0 1-.599.919c-.28.28-.546.453-.92.598-.28.11-.704.24-1.485.276-.843.038-1.096.047-3.232.047s-2.39-.009-3.233-.047c-.78-.036-1.203-.166-1.485-.276a2.478 2.478 0 0 1-.92-.598 2.48 2.48 0 0 1-.6-.92c-.109-.281-.24-.705-.275-1.485-.038-.843-.046-1.096-.046-3.233 0-2.136.008-2.388.046-3.231.036-.78.166-1.204.276-1.486.145-.373.319-.64.599-.92.28-.28.546-.453.92-.598.282-.11.705-.24 1.485-.276.738-.034 1.024-.044 2.515-.045v.002zm4.988 1.328a.96.96 0 1 0 0 1.92.96.96 0 0 0 0-1.92zm-4.27 1.122a4.109 4.109 0 1 0 0 8.217 4.109 4.109 0 0 0 0-8.217zm0 1.441a2.667 2.667 0 1 1 0 5.334 2.667 2.667 0 0 1 0-5.334z"/>
            </svg>
            Instagram
        </a>
        <a href="https://github.com/Sasanka14" target="_blank" style="display: flex; align-items: center; text-decoration: none; color: inherit;">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#333" viewBox="0 0 16 16" style="margin-right: 8px;">
                <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
            </svg>
            GitHub
        </a>
        <a href="https://www.linkedin.com/in/sasanka-sekhar-kundu-b746072a7" target="_blank" style="display: flex; align-items: center; text-decoration: none; color: inherit;">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#0077B5" viewBox="0 0 16 16" style="margin-right: 8px;">
                <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248-.822 0-1.359.54-1.359 1.248 0 .694.521 1.248 1.327 1.248h.016zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016a5.54 5.54 0 0 1 .016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225h2.4z"/>
            </svg>
            LinkedIn
        </a>
        <a href="mailto:sasankasekharkundu24@gmail.com" style="display: flex; align-items: center; text-decoration: none; color: inherit;">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#D44638" viewBox="0 0 16 16" style="margin-right: 8px;">
                <path d="M.05 3.555A2 2 0 0 1 2 2h12a2 2 0 0 1 1.95 1.555L8 8.414.05 3.555ZM0 4.697v7.104l5.803-3.558L0 4.697ZM6.761 8.83l-6.57 4.027A2 2 0 0 0 2 14h12a2 2 0 0 0 1.808-1.144l-6.57-4.027L8 9.586l-1.239-.757Zm3.436-.586L16 11.801V4.697l-5.803 3.546Z"/>
            </svg>
            Email
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    # Simple Footer
    st.markdown("---")
    st.caption("Developed by [Sasanka](https://github.com/Sasanka14)")
    st.caption("© 2024 AgriNext | Powered by Plant Disease AI")


# Extract the page selection (remove emoji)
page = app_mode.split(" ", 1)[1] if " " in app_mode else app_mode

# Now all the page content follows

# Home Page
if page == "Home":
    # Title and Subtitle Section (Centered with animation class)
    st.markdown(
        """
        <div style="text-align: center;" class="animate-fade-in">
            <h1 style="font-size: 2.8em; margin-bottom: 0; color: #2E7D32;">Harvest the Future with AI</h1>
            <h3 style="color: #616161; font-weight: 400; margin-top: 0;">Empowering Farmers with Instant Crop Disease Detection</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Main container with animation class
    with st.container():
        # Hero Section with two columns
        col1, col2 = st.columns([2, 1])
        
        with col1:
                    st.markdown("""
            <div class="animate-fade-in">
                <h2>AI-Powered Crop Disease Detection</h2>
                <p style="font-size: 1.1rem; line-height: 1.6;">
                    In today's fast-paced agricultural world, ensuring the health of your crops is crucial 
                    for maximizing yields and minimizing losses. Our advanced AI-powered platform uses 
                    cutting-edge machine learning to provide instant and accurate disease detection.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            
        with col2:
            # Replace Lottie animations with GIF file
            st.markdown("""
            <div style="background-color: #e8f5e9; border-radius: 10px; padding: 15px; text-align: center; margin-bottom: 10px;">
                <h4 style="color: #2E7D32; margin-top: 0;">AI-Powered Analysis</h4>
                <p style="margin-bottom: 10px;">Our advanced algorithms analyze crop images to detect diseases instantly.</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Key Benefits Section
    st.markdown("""
    <div class="animate-fade-in">
        <h2 style="text-align: center; margin-bottom: 20px;">Key Benefits</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Modern card layout for benefits
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown("""
            <div style="padding: 20px; border-radius: 10px; background-color: #e8f5e9; height: 100%;">
                <h3 style="color: #2E7D32;">⚡ Instant Diagnosis</h3>
                <p>Get results in seconds after uploading your crop image. Early detection means faster treatment.</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown("""
            <div style="padding: 20px; border-radius: 10px; background-color: #e8f5e9; height: 100%;">
                <h3 style="color: #2E7D32;">🎯 Accurate Detection</h3>
                <p>Our AI model trained on thousands of images ensures high accuracy in diagnosing diseases.</p>
            </div>
            """, unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        with st.container():
            st.markdown("""
            <div style="padding: 20px; border-radius: 10px; background-color: #e8f5e9; height: 100%; margin-top: 15px;">
                <h3 style="color: #2E7D32;">💊 Treatment Recommendations</h3>
                <p>Receive customized treatment suggestions to effectively manage crop diseases.</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col4:
        with st.container():
            st.markdown("""
            <div style="padding: 20px; border-radius: 10px; background-color: #e8f5e9; height: 100%; margin-top: 15px;">
                <h3 style="color: #2E7D32;">📱 Mobile Friendly</h3>
                <p>Use from any device, including your smartphone, making it perfect for field use.</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Features Section with modern layout
    st.markdown("""
    <div class="animate-fade-in">
        <h2 style="text-align: center;">How It Works</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Step-by-step process with numbering and icons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container():
            st.markdown("""
            <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: #f5f5f5;">
                <div style="background-color: #2E7D32; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin: 0 auto;">1</div>
                <h3>Upload Image</h3>
                <p>Take a clear photo of your crop and upload it to our platform</p>
                <img src="https://img.icons8.com/fluency/96/upload--v1.png" width="60" />
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown("""
            <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: #f5f5f5;">
                <div style="background-color: #2E7D32; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin: 0 auto;">2</div>
                <h3>AI Analysis</h3>
                <p>Our AI processes the image to identify any disease or pest issues</p>
                <img src="https://img.icons8.com/fluency/96/artificial-intelligence.png" width="60" />
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        with st.container():
            st.markdown("""
            <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: #f5f5f5;">
                <div style="background-color: #2E7D32; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin: 0 auto;">3</div>
                <h3>Get Results</h3>
                <p>Receive disease identification and treatment recommendations</p>
                <img src="https://img.icons8.com/color/96/000000/treatment-plan.png" width="60" />
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Video Section with modern container
    st.markdown("""
    <div class="animate-fade-in">
        <h2 style="text-align: center;">See It In Action</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Center the video
    with st.container():
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.video("asset/how_it_works.mp4")
            st.caption("A step-by-step demonstration of how our AI detects crop diseases")
    
    # User testimonials or stats (optional)
    st.markdown("""
    <div class="animate-fade-in" style="margin-top: 30px; text-align: center;">
        <h2>Project Highlights</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats in a modern layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
                st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <h1 style="color: #2E7D32; font-size: 3rem; margin: 0;">38+</h1>
            <p>Crop Diseases Detectable</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <h1 style="color: #2E7D32; font-size: 3rem; margin: 0;">95%+</h1>
            <p>Model Accuracy</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <h1 style="color: #2E7D32; font-size: 3rem; margin: 0;">100%</h1>
            <p>Free & Open Source</p>
        </div>
        """, unsafe_allow_html=True)

elif page == "About":
    # About Page Header
    st.markdown("""
    <div class="animate-fade-in">
        <h1 style="text-align: center;">About the Project</h1>
        <p style="text-align: center; max-width: 800px; margin: 0 auto; font-size: 1.1rem;">
            An AI-powered solution designed to revolutionize modern agriculture by helping farmers 
            detect crop diseases accurately and providing actionable treatment recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # About content in modern two-column layout
    col1, col2 = st.columns([2, 3])
    
    with col1:
        # Profile card
        st.markdown("""
            <div style="background-color: #f5f5f5; border-radius: 10px; padding: 20px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h3>Sasanka Sekhar Kundu</h3>
                <p style="font-style: italic; color: #666;">B.Tech in Computer Science</p>
                <div style="display: flex; justify-content: center; gap: 10px; margin: 15px 0;">
                    <a href="https://github.com/Sasanka14" target="_blank"><img src="https://img.icons8.com/fluency/48/github.png" width="30"/></a>
                    <a href="https://www.linkedin.com/in/sasanka-sekhar-kundu-b746072a7" target="_blank"><img src="https://img.icons8.com/color/48/linkedin.png" width="30"/></a>
                    <a href="mailto:sasankasekharkundu24@gmail.com" target="_blank"><img src="https://img.icons8.com/color/48/gmail--v1.png" width="30"/></a>
                </div>
            </div>
        """, unsafe_allow_html=True)

        
        # Achievement cards
        st.markdown("""
        <div style="background-color: #e8f5e9; border-radius: 10px; padding: 15px; margin-top: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h4 style="margin-top: 0;">🏆 Achievements</h4>
            <ul style="padding-left: 20px;">
                <li>NASA Hackathon 2024 - 5th Place</li>
                <li>1st Semester Internship Experience</li>
                <li>Specializes in Web Development & ML</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="animate-fade-in" style="padding: 10px;">
            <h3>Project Vision</h3>
            <p style="line-height: 1.6;">
                Agriculture is the backbone of India's economy, supporting millions of farmers. However, it faces 
                challenges, especially from crop diseases, which can lead to severe yield losses, financial hardships 
                for farmers, and threats to India's food security.
            </p>
            <p style="line-height: 1.6;">
                Recognizing these issues, this project aims to:
            </p>
            <ul>
                <li>Empower Indian farmers with an affordable tool for early disease detection</li>
                <li>Bridge the gap in access to agricultural expertise, especially in rural areas</li>
                <li>Promote sustainable farming practices by integrating modern technology</li>
            </ul>
        
        </div>
        """, unsafe_allow_html=True)
        
        # Add Technology Stack with native Streamlit components
        st.subheader("Technology Stack")
        tech_col1, tech_col2, tech_col3 = st.columns(3)
        with tech_col1:
            st.markdown("**🧠 Deep Learning**")
            st.markdown("- TensorFlow & Keras")
            st.markdown("- Convolutional Neural Networks")
        
        with tech_col2:
            st.markdown("**🖥️ Frontend**")
            st.markdown("- Streamlit")
            st.markdown("- HTML/CSS")
            
        with tech_col3:
            st.markdown("**🔧 Backend**")
            st.markdown("- Python")
            st.markdown("- Image Processing")
    
    st.markdown("---")
    
    # Dataset information with image
    st.markdown("""
    <div class="animate-fade-in">
        <h2 style="text-align: center;">About the Dataset</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("asset/Dataset-Image.png", caption="New Plant Diseases Dataset")
    
    with col2:
        st.markdown("""
        <div style="padding: 10px;">
            <p style="line-height: 1.6;">
                This project uses a publicly available dataset from Kaggle, which contains thousands of images of 
                healthy and diseased plant leaves. The dataset covers multiple crop species and disease types, 
                allowing our model to learn and recognize a wide variety of plant diseases.
            </p>
            <p style="line-height: 1.6;">
                <strong>Dataset Credit:</strong> <a href="https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset/data" target="_blank">New Plant Diseases Dataset on Kaggle</a>
            </p>
            <p>The dataset includes images for 38 different classes of plant diseases and healthy plants.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Future Roadmap in a modern card layout
    st.markdown("""
    <div class="animate-fade-in">
        <h2 style="text-align: center;">Future Roadmap</h2>
    </div>
    """, unsafe_allow_html=True)

    # Roadmap cards in 2x2 grid
    col1, col2 = st.columns(2)
    
    with col1:
            st.markdown("""
        <div style="background-color: #f5f5f5; border-radius: 10px; padding: 15px; margin: 10px 0; height: 100%;">
            <img src="https://img.icons8.com/fluency/48/mobile-phone.png" width="40"/>
            <h4>Mobile App Development</h4>
            <p>Creating a native mobile application for Android and iOS to improve accessibility for farmers in the field.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #f5f5f5; border-radius: 10px; padding: 15px; margin: 10px 0; height: 100%;">
            <img src="https://img.icons8.com/fluency/48/language.png" width="40"/>
            <h4>Regional Language Support</h4>
            <p>Adding support for Indian regional languages to make the application accessible to more farmers.</p>
        </div>
        """, unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div style="background-color: #f5f5f5; border-radius: 10px; padding: 15px; margin: 10px 0; height: 100%;">
            <img src="https://img.icons8.com/fluency/48/iot-devices.png" width="40"/>
            <h4>IoT Integration</h4>
            <p>Connecting with IoT devices for automated monitoring and detection of crop diseases in real-time.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background-color: #f5f5f5; border-radius: 10px; padding: 15px; margin: 10px 0; height: 100%;">
            <img src="https://img.icons8.com/fluency/48/partly-cloudy-day.png" width="40"/>
            <h4>Weather Data Integration</h4>
            <p>Incorporating local weather data to provide contextual treatment recommendations based on environmental factors.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Final CTA
    st.markdown("""
    <div style="text-align: center; margin-top: 30px;">
        <h3>Ready to try it yourself?</h3>
        <p>Head over to the Disease Recognition page to scan your crop images now!</p>
    </div>
    """, unsafe_allow_html=True)
    

# Disease Recognition Section
elif page == "Disease Recognition":
    # Header with animation
    st.markdown("""
    <div class="animate-fade-in" style="text-align: center; margin-bottom: 20px;">
        <h1>AI Crop Disease Detection</h1>
        <p style="font-size: 1.1rem; max-width: 700px; margin: 0 auto;">
            Upload an image of your crop leaf, and our AI will instantly identify 
            any diseases and provide treatment recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content in two columns
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Modern file uploader
        st.markdown("""
        <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h3 style="margin-top: 0;">Upload Crop Image</h3>
            <p>For best results, ensure the image is clear and well-lit.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Add supported formats
        test_image = st.file_uploader(
            "Supported formats: JPG, PNG, JPEG", 
            type=["jpg", "png", "jpeg"],
            help="Ensure the image clearly shows the affected area of the plant"
        )
        
        # Display uploaded image in a card
        if test_image:
            img = Image.open(test_image)
            st.markdown("""
            <div style="margin-top: 20px;">
                <h4>Uploaded Image:</h4>
            </div>
            """, unsafe_allow_html=True)
            st.image(img, caption="Your crop image", use_column_width=True)
        
        # Modern analyze button
        analyze_button = st.button("🔬 Analyze Image", use_container_width=True)
    
    with col2:
        # Tips for better results and add GIF animation
        st.markdown("""
        <div style="background-color: #e8f5e9; padding: 20px; border-radius: 10px; margin-bottom: 20px; text-align: center;">
            <h3 style="margin-top: 0; color: #2E7D32;">AI Analysis Process</h3>
            <p>Our AI model analyzes leaf patterns to identify diseases and provide treatment recommendations.</p>
        </div>
        """, unsafe_allow_html=True)
        
        
        st.markdown("""
        <div style="background-color: #e8f5e9; padding: 15px; border-radius: 10px; margin-top: 20px;">
            <h4 style="margin-top: 0; color: #2E7D32;">📸 Tips for Better Results</h4>
            <ul style="margin-bottom: 0;">
                <li>Take photos in natural daylight</li>
                <li>Focus on the affected area</li>
                <li>Include both healthy and diseased parts for comparison</li>
                <li>Avoid shadows and glare</li>
                <li>Keep the camera steady for clear images</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Analysis section
    if analyze_button and test_image:
        st.markdown("---")
        
        # Create a modern progress bar
        progress_container = st.container()
        with progress_container:
            st.markdown("""
            <div class="animate-fade-in">
                <h3>Analyzing your crop image...</h3>
            </div>
            """, unsafe_allow_html=True)
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # First few steps with simulation
                initial_steps = [
                    "Preprocessing image...",
                    "Running feature extraction...",
                ]
                
                for i, step in enumerate(initial_steps):
                    # Calculate progress percentage for first part (0-30%)
                    progress_percent = int((i / len(initial_steps)) * 30)
                    status_text.text(f"{step} ({progress_percent}%)")
                    progress_bar.progress(progress_percent)
                    time.sleep(0.3)
                
                # Update status for model loading
                status_text.text("Loading AI model... (40%)")
                progress_bar.progress(40)
                
                # Actually perform the model prediction here
                status_text.text("Applying deep learning model... (50%)")
                progress_bar.progress(50)
                model = tf.keras.models.load_model("trained_plant_disease_model_save.keras")
                
                status_text.text("Processing image... (60%)")
                progress_bar.progress(60)
                image = tf.keras.preprocessing.image.load_img(test_image, target_size=(32,32))
                input_arr = tf.keras.preprocessing.image.img_to_array(image)
                input_arr = np.array([input_arr])
                
                status_text.text("Generating predictions... (70%)")
                progress_bar.progress(70)
                predictions = model.predict(input_arr, verbose=0)  # Set verbose=0 to hide the prediction output
                
                status_text.text("Identifying patterns... (85%)")
                progress_bar.progress(85)
                class_idx = np.argmax(predictions[0])
                confidence = float(predictions[0][class_idx])
                
                status_text.text("Finalizing results... (95%)")
                progress_bar.progress(95)
                time.sleep(0.3)
                
                # Complete the progress bar
                progress_bar.progress(100)
                status_text.text("Analysis complete! (100%)")
                time.sleep(0.5)
                
                # Clear the progress indicators
                progress_container.empty()
                
                class_name = [
                    'Apple__Apple_scab', 'Apple_Black_rot', 'Apple_Cedar_apple_rust', 'Apple__healthy',
                    'Blueberry__healthy', 'Cherry(including_sour)_Powdery_mildew', 
                    'Cherry_(including_sour)healthy', 'Corn(maize)_Cercospora_leaf_spot_Gray_leaf_spot', 
                    'Corn_(maize)Common_rust', 'Corn_(maize)Northern_Leaf_Blight', 'Corn(maize)_healthy', 
                    'Grape__Black_rot', 'Grape_Esca(Black_Measles)', 'Grape__Leaf_blight(Isariopsis_Leaf_Spot)', 
                    'Grape__healthy', 'Orange_Haunglongbing(Citrus_greening)', 'Peach___Bacterial_spot',
                    'Peach__healthy', 'Pepper,_bell_Bacterial_spot', 'Pepper,_bell__healthy', 
                    'Potato__Early_blight', 'Potato_Late_blight', 'Potato__healthy', 
                    'Raspberry__healthy', 'Soybean_healthy', 'Squash__Powdery_mildew', 
                    'Strawberry__Leaf_scorch', 'Strawberry_healthy', 'Tomato__Bacterial_spot', 
                    'Tomato__Early_blight', 'Tomato_Late_blight', 'Tomato__Leaf_Mold', 
                    'Tomato__Septoria_leaf_spot', 'Tomato__Spider_mites_Two-spotted_spider_mite', 
                    'Tomato__Target_Spot', 'Tomato_Tomato_Yellow_Leaf_Curl_Virus', 'Tomato__Tomato_mosaic_virus',
                    'Tomato___healthy'
                ]
                disease_name = class_name[class_idx]
                
                # Display results using Streamlit components instead of raw HTML
                results_container = st.container()
                with results_container:
                    st.markdown(f"<h2 style='color: #2E7D32;'>Analysis Results</h2>", unsafe_allow_html=True)
                    
                    # Create a clean results card
                    st.markdown("""
                    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #2E7D32;">
                    """, unsafe_allow_html=True)
                    
                    # Disease name display
                    st.markdown(f"""
                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                        <div style="background-color: #2E7D32; color: white; padding: 10px; border-radius: 10px; margin-right: 15px;">
                            <img src="https://img.icons8.com/fluency/48/leaf.png" width="24" style="filter: brightness(0) invert(1);">
                        </div>
                        <div>
                            <p style="margin: 0; font-weight: bold;">Detected Condition:</p>
                            <h3 style="margin: 5px 0; color: #2E7D32;">{disease_name.replace('_', ' ').replace('__', ' - ')}</h3>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Treatment recommendations
                treatment = get_treatment(disease_name)
                
                st.markdown(f"""
                <div class="results-container" style="border-left: 5px solid #FFA000;">
                    <h3 style="color: #FFA000; margin-top: 0;">Treatment Recommendations</h3>
                    <div style="display: flex; align-items: flex-start; margin-top: 15px;">
                        <img src="https://img.icons8.com/fluency/48/pill.png" width="30" style="margin-right: 15px; margin-top: 5px;">
                        <p style="margin: 0; line-height: 1.6;">{treatment}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Additional resources section
                st.markdown("""
                <div style="margin-top: 30px;">
                    <h3>Additional Resources</h3>
                    <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                        <a href="https://www.india.gov.in/topics/agriculture/plant-protection" target="_blank" style="text-decoration: none;">
                            <div style="background-color: #f5f5f5; padding: 10px; border-radius: 5px; display: flex; align-items: center;">
                                <img src="https://img.icons8.com/fluency/48/book.png" width="20" style="margin-right: 10px;">
                                <span>Government Plant Protection Resources</span>
                            </div>
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Encourage user to scan more images
                st.markdown("""
                <div style="margin-top: 30px; text-align: center;">
                    <p>Want to scan another crop image?</p>
                </div>
                """, unsafe_allow_html=True)
                
                
                    
            except Exception as e:
                # Clear progress indicators and show error
                progress_container.empty()
                st.error(f"An error occurred during analysis: {e}")
                st.markdown("""
                <div style="background-color: #ffebee; padding: 15px; border-radius: 10px; margin-top: 20px;">
                    <h4 style="margin-top: 0; color: #c62828;">Troubleshooting Tips</h4>
                    <ul>
                        <li>Make sure the image is clear and not corrupted</li>
                        <li>Try with a different image of the crop</li>
                        <li>Check that the image format is supported (JPG, PNG, JPEG)</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
    elif analyze_button:
        # Prompt user to upload an image
        st.warning("Please upload an image to proceed with the analysis.")
    
    # Show sample images if no image uploaded
    if not test_image:
        # Display sample images with a more prominent heading
        st.markdown("""
        <div style="margin-top: 30px; background-color: #f0f8f0; padding: 15px; border-radius: 10px; border-left: 5px solid #2E7D32;">
            <h3 style="color: #2E7D32; margin-top: 0;">Example Images</h3>
            <p>Click on any of these sample images to download and test the system:</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
        
        # Sample image gallery with better error handling
        sample_images = [
            "test/AppleScab1.JPG",
            "test/TomatoEarlyBlight1.JPG",
            "test/PotatoHealthy1.JPG"
        ]
        
        sample_disease_names = [
            "Apple Apple scab",
            "Tomato Late blight", 
            "Apple Black rot"
        ]
        
        # Create three columns for the images
        sample_cols = st.columns(3)
        
        # Display each image in its column with robust error handling
        for i, img_path in enumerate(sample_images):
            try:
                with sample_cols[i]:
                    # Add a styled container for each image
                    st.markdown(f"""
                    <div style="background-color: #f9f9f9; padding: 10px; border-radius: 10px; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                        <h4 style="margin-top: 0; color: #2E7D32;">{sample_disease_names[i]}</h4>
    </div>
                    """, unsafe_allow_html=True)
                    
                    # Try to open and display the image
                    img = Image.open(img_path)
                    st.image(img, use_column_width=True)
                    
                    # Add a download hint
                    st.caption(f"Right-click to save and upload for testing")
            except Exception as e:
                # If there's an error, display an error message in that column
                with sample_cols[i]:
                    st.error(f"Could not load image: {img_path}")
                    st.info(f"{sample_disease_names[i]} (Image not available)")
                    # Log the error to help with debugging
                    print(f"Error loading image {img_path}: {e}")

# Add navigation logic - this should be at the end
if 'navigate_to' in st.session_state:
    if st.session_state.navigate_to == "Disease Recognition":
        st.session_state.app_mode = "🔍 Disease Recognition"
        del st.session_state.navigate_to
        st.experimental_rerun()
