import streamlit as st
import tensorflow as tf
import numpy as np
import time 
from PIL import Image

# Set page title and favicon
st.set_page_config(page_title="AgriNext",  page_icon="asset/Logo.png")

# Title and Subtitle Section (Centered)
st.markdown(
    """
    <div style="text-align: center;">
        <h1 style="font-size: 2.5em; margin-bottom: 0;">Harvest the Future with AI</h1>
        <h3 style="color: grey; font-weight: 400; margin-top: 0;">Empowering Farmers with Instant Crop Disease Detection</h3>
    </div>
    """,
    unsafe_allow_html=True,
)

# TensorFlow Model Prediction Function
def model_prediction(test_image):
    model = tf.keras.models.load_model("trained_plant_disease_model_save.keras")
    image = tf.keras.preprocessing.image.load_img(test_image,target_size=(32,32))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr]) #convert single image to batch
    predictions = model.predict(input_arr)
    return np.argmax(predictions) #return index of max element

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
st.sidebar.title("🌿 AgriNext")
st.sidebar.image("asset/Logo.png", use_column_width=True)  # Replace with your logo or image URL
st.sidebar.markdown("Welcome to the AgriNext! 🌱")

# Select the page
app_mode = st.sidebar.selectbox(
    "Select Page",
    ["Home", "About", "Disease Recognition"]
)

# Add some helpful links or info to the sidebar
st.sidebar.markdown("### Useful Links")
st.sidebar.markdown(
    """
    - [Contact Us](mailto:sasankasekharkundu24@gmail.com)
    - [Visit our Blog](https://insightforgedotcom.wordpress.com/)
    - [Learn more about Plant Care](https://www.india.gov.in/topics/agriculture/plant-protection)
    """
)

# Add some tips or description
st.sidebar.markdown("### How to Use:")
st.sidebar.markdown("""
    - Select a page from the dropdown menu.
    - On the **Home** page, you'll find an overview of the app.
    - On the **About** page, you can learn more about plant diseases.
    - On the **Disease Recognition** page, upload a plant image to diagnose the disease.
""")

# Add footer information
st.sidebar.markdown("""
    - Developed by [Sasanka](https://github.com/Sasanka14)
    - Data sourced from kaggle
    - © 2024 Plant Disease Dashboard
""")

# Home Page
if app_mode == "Home":
    # Hero Section
    st.write("""
        In today's fast-paced agricultural world, ensuring the health of your crops is crucial for maximizing yields and minimizing losses. 
        Our advanced AI-powered platform uses cutting-edge machine learning techniques to provide instant and accurate disease detection in crops.
    
        By simply uploading an image of your crop's leaf or plant, our system processes the image and identifies any potential diseases. 
        With the ability to recognize early signs of disease, our system allows farmers to act quickly, preventing the spread of harmful pathogens 
        and protecting crop health.
    
        Key Benefits:
        - **Instant Diagnosis**: Get results in just a few seconds after uploading your crop image.
        - **Accurate Detection**: Our AI model has been trained on thousands of images, ensuring high accuracy in diagnosing diseases.
        - **Preventive Actions**: Early disease detection allows farmers to take preventive measures, reducing crop damage and increasing yield.
        - **Easy to Use**: Simply upload an image, and the system will take care of the rest, making it user-friendly for all farmers, regardless of their tech-savviness.
    """)

    # Call to Action
    if st.button("Start Scanning"):
        st.write("Navigate to the 'Disease Recognition' page from the sidebar.")

    # Features Section
    st.header("Key Features to Revolutionize Crop Health")
    
    # Feature 1: Instant Disease Detection
    st.subheader("Instant Disease Detection")
    st.write("""
        Our AI-powered disease detection system allows you to quickly upload an image of your crop. 
        The model instantly analyzes the image, identifies any disease, and provides detailed results 
        within seconds. This helps farmers and gardeners detect issues early and take timely actions 
        to preserve crop health.
    """)
    
    # Feature 2: AI-Powered
    st.subheader("AI-Powered")
    st.write("""
        The disease detection is powered by a deep learning model trained on lakhs of images from 
        different crops. It has the ability to recognize patterns and predict diseases with high accuracy. 
        By leveraging AI, the system helps make quick decisions, improving efficiency in crop management.
    """)

    # Feature 3: Treatment Recommendations
    st.subheader("Treatment Recommendations")
    st.write("""
        After detecting a disease, the system provides useful treatment recommendations to help you manage 
        the health of your crops. This includes suggested pesticide usage, organic treatment options, 
        or preventive measures to avoid the disease spreading further.
    """)
    
    # Feature 4: Track Crop Health
    st.subheader("Track Crop Health")
    st.write("""
        With our system, you can monitor the health of your crops over time. By scanning your crops regularly, 
        you can track changes, observe improvement or deterioration, and make informed decisions about when 
        to take action. This helps you maintain optimal conditions for crop growth.
    """)
    
     # Bento Grid Layout for Images (Side by Side)
    col1, col2 = st.columns(2)
    
    # Image for Feature 1: Instant Disease Detection (Local image path)
    with col1:
        st.image("asset/Instant Disease Detection.png", caption="Instant Disease Detection", use_column_width=True, width=300)
    
    # Image for Feature 2: AI-Powered (Local image path)
    with col2:
        st.image("asset/AI-Powered.png", caption="AI-Powered Disease Recognition", use_column_width=True, width=300)
    
    # Bento Grid Continued
    
    col3, col4 = st.columns(2)
    
    # Image for Feature 3: Treatment Recommendations (Local image path)
    with col3:
        st.image("asset/Treatment Recommendations.png", caption="Suggested Treatments", use_column_width=True, width=300)
    
    # Image for Feature 4: Track Crop Health (Local image path)
    with col4:
        st.image("asset/Track Crop Health.png", caption="Monitor Crop Health", use_column_width=True, width=300)

    # How It Works Section
    st.header("How It Works")
    st.write("""
    **Step 1: Upload Your Crop Image**
    - Take a clear photo of your crop using your mobile phone or camera. Make sure the image is well-lit and focuses on the affected area of the crop.
    - The image should capture the leaves, stems, and any visible signs of disease or damage.
    - Upload the image to the platform. The clearer the photo, the more accurate the analysis will be.
    
    **Step 2: Disease Detection Using AI Technology**
    - Once the image is uploaded, our advanced AI (Artificial Intelligence) model will process it.
    - The AI has been trained using thousands of images of crops with different diseases, so it can recognize patterns and identify potential problems.
    - It looks for specific symptoms such as spots, discoloration, wilting, or unusual growth that are common in diseased crops.
    - Within a few seconds, the AI will detect any signs of disease or pest infestations.
    
    **Step 3: View the Results and Treatment Recommendations**
    - After the AI analysis, you will receive a detailed report on the disease detected in your crop.
    - The report will describe:
        - What the disease or pest is called.
        - The potential causes of the problem (e.g., weather, pests, or improper care).
        - Clear pictures of the disease so you can better understand the issue.
    - In addition to the disease identification, the report will suggest:
        - Safe and natural treatments to apply.
        - Preventive measures to avoid future issues.
        - Best practices to keep your crops healthy and thriving.
    """)
    
    # Then, display the caption below the video
    st.write("A Step-by-Step Guide on How the AI Detects and Helps Your Crops.")

        # Technology Section
    st.header("Technology Behind the App")
    st.write("""
        Our app utilizes cutting-edge machine learning, deep learning, and Streamlit to deliver an efficient, user-friendly solution 
        for crop disease detection. Below are the key technologies used to build this app and the machine learning model that powers it.
    """)
    
    # Web Development Technologies (Streamlit and Python)
    st.subheader("Web Development Technologies")
    st.write("""
        1. **Streamlit**:
           - Streamlit is a powerful, open-source framework for building interactive web applications in Python. 
           - We used Streamlit for building the front-end of the app, allowing farmers to easily interact with the machine learning model.
           - Streamlit makes it incredibly easy to create beautiful web apps with minimal code, making it an ideal choice for our project.
        
        2. **Python**:
           - Python is the primary programming language used throughout the app. It is widely known for its simplicity and extensive libraries for data science and machine learning.
           - We used Python for integrating the machine learning model, handling data, and building the web interface with Streamlit.
           - Libraries like NumPy, Pandas, and Matplotlib were used for data manipulation and visualization tasks in the backend of the app.
    """)
    
    # Machine Learning and Deep Learning Technologies
    st.subheader("Machine Learning and Deep Learning Technologies")
    st.write("""
        The core of our application is a machine learning model that analyzes images of crops and detects diseases. 
        Here’s a breakdown of the technologies used to build the model:
        
        1. **TensorFlow / Keras**:
           - TensorFlow is an open-source deep learning framework used to build and train the crop disease detection model.
           - We used Keras, a high-level API built on top of TensorFlow, to simplify the model-building process.
           - The model is based on Convolutional Neural Networks (CNNs), which are particularly effective for image classification tasks like crop disease detection.
        
        2. **OpenCV**:
           - OpenCV (Open Source Computer Vision Library) is used for pre-processing the crop images before they are fed into the machine learning model.
           - We use OpenCV for tasks like resizing images, normalizing the pixel values, and other image adjustments to ensure the best performance from the model.
        
        3. **scikit-learn**:
           - scikit-learn is used for machine learning tasks like model evaluation and hyperparameter tuning.
           - It helps us assess the performance of the model, calculate accuracy, precision, recall, and F1-score, and also tune the model to achieve the best results.
    
        4. **Custom Model Development**:
            - Instead of using pre-trained models, we built our own custom deep learning model tailored specifically for crop disease recognition. This model was designed and trained from scratch using our dataset of crop images. By carefully selecting and tuning the architecture, including layers like convolutional layers, pooling layers, and dense layers, we aimed to optimize the model for accurate disease classification. This approach allowed us to have more control over the model's performance and adaptability to our unique crop disease dataset.
        
        5. **Cloud Computing / GPU**:
           - During model training, we used cloud computing platforms like Google Colab or local GPU resources to accelerate the training process.
           - Training a deep learning model requires significant computational power, and utilizing GPUs allows for much faster training compared to using standard CPUs.
    """)
    
    # Continuous Model Improvement
    st.subheader("Continuous Model Improvement")
    st.write("""
        We are committed to continually improving the model and the overall user experience. Our model is regularly updated with:
        
        1. **New Crop Disease Data**: 
           - We continually gather new crop disease images to enhance the model's accuracy and generalization capabilities.
        
        2. **User Feedback**: 
           - We actively collect feedback from farmers and app users to improve the app and model, ensuring it serves their needs better.
        
        3. **Model Tuning**: 
           - We experiment with different models, fine-tune hyperparameters, and adjust the training process to ensure the model's performance keeps improving.
    """)

    # Local Video Section
    st.subheader("To better understand the technology behind it, we encourage you to watch the full video.")
    st.video("asset/how_it_works.mp4")  # Video file location
    
    # Footer Section
    st.markdown("---")
    st.markdown("<h3 style='text-align: center;'>Useful Links</h3>", unsafe_allow_html=True)
    
    # Center the footer links with small icons
    footer_html = """
    <div style='text-align: center;'>
        <a href="https://www.instagram.com/__kuronotsubasa__/profilecard/?igsh=MWdyNHd2NDFzZWl3Yw==" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/32px-Instagram_icon.png" alt="Instagram" style="margin: 5px; width: 32px; height: 32px;">
        </a>
        <a href="https://github.com/Sasanka14" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" alt="GitHub" style="margin: 5px; width: 32px; height: 32px;">
        </a>
        <a href="https://www.linkedin.com/in/sasanka-sekhar-kundu-b746072a7" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" alt="LinkedIn" style="margin: 5px; width: 32px; height: 32px;">
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

elif app_mode == "About":
    st.header("About the Project")
    st.markdown("""
    Welcome to the **Crop Disease Detection System**, an AI-powered solution designed to revolutionize modern agriculture. This application helps farmers detect crop diseases accurately and provides actionable treatment recommendations. The primary aim of this project is to address the challenges faced by farmers due to undiagnosed or late-diagnosed crop diseases, empowering them with technology to achieve better yields and sustainable farming practices.

    ## About the Creator
    **Sasanka Sekhar Kundu** is the mind behind this project. As a B.Tech student in Computer Science and Engineering at Sandip University, Sasanka combines his expertise in technology with a deep understanding of real-world challenges to create innovative solutions. His journey is marked by passion, teamwork, and a drive to use technology for societal impact.

    ### Achievements:
    - Participated in the **NASA Hackathon 2024**, securing 5th place out of 800 participants.
    - Gained internship experience in the **1st semester of B.Tech**, showcasing his early commitment to practical applications of knowledge.
    - Specializes in web development, machine learning, and data analysis, with a proven track record in freelancing and team collaborations.

    Sasanka's vision is to leverage his skills to address pressing issues in sectors like agriculture, combining AI with user-centric designs to empower communities.

    **Why Was This Project Built?**  

    Agriculture is the backbone of India's economy, supporting millions of farmers. However, it faces challenges, especially from crop diseases, which can lead to:  
    
    - Severe yield losses, impacting the food supply chain.  
    - Financial hardships for farmers, many of whom already struggle with limited resources.  
    - Threats to India's food security and rural stability.  
    
    Recognizing these issues, **Sasanka** built this project to:  
    
    - Empower Indian farmers with an affordable tool for early disease detection.  
    - Bridge the gap in access to agricultural expertise, especially in rural and remote areas.  
    - Promote sustainable farming practices by integrating modern technology with traditional Indian agricultural wisdom.  

    **Dataset Credit**: This project uses a publicly available dataset from Kaggle, which can be found at [New Plant Diseases Dataset](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset/data). Special thanks to the contributors for their valuable efforts in creating and sharing this resource.

    """, unsafe_allow_html=True)

    st.image("asset/Dataset-Image.png", caption="New Plant Diseases Dataset", use_column_width=True)
    
    st.markdown("""
    ## How It Works
    1. **Upload an Image**: Farmers can upload a clear image of the crop leaf.
    2. **AI Detection**: The system processes the image using advanced machine learning models to identify potential diseases.
    3. **Detailed Report**: Users receive a diagnosis, along with actionable treatment recommendations.

    ## Technology Behind the App
    - **Machine Learning**: Trained models analyze crop leaf patterns to detect diseases with high accuracy.
    - **Deep Learning**: CNNs (Convolutional Neural Networks) are used for image classification and disease identification.
    - **Streamlit**: A lightweight and efficient framework for building interactive and user-friendly web applications.
    - **Data Augmentation**: Techniques like rotation, flipping, and color adjustments were used to create a robust dataset.

    ## Future Roadmap
    Sasanka envisions several enhancements for this project:
    - **Mobile App Development**: Ensuring accessibility on smartphones for real-time use in the field.
    - **Regional Language Support**: Making the app multilingual to cater to farmers in different regions.
    - **Integration with IoT**: Linking the app with smart farming devices for holistic crop management.
    - **Weather and Soil Data**: Adding features to consider external factors like weather conditions and soil health.

    ## Modern-Day Relevance
    This app is a vital tool for:
    - **Farmers**: Empowering them with immediate disease detection and actionable insights.
    - **Agriculture Experts**: Supporting informed decision-making and efficient resource allocation.
    - **Sustainable Farming**: Encouraging eco-friendly practices by reducing chemical use through targeted treatment.

    ## Acknowledgments
    This project would not have been possible without:
    - **Dataset Support**: A recreated dataset using offline augmentation from publicly available sources.
    - **Open-Source Community**: For tools and frameworks that enabled seamless development.
    - **Agriculture Experts**: For insights into disease classification and crop management.
    Together, let's make agriculture smarter, more sustainable, and future-ready!
    """, unsafe_allow_html=True)
    
    st.image("asset/AI Transforming Indian Agriculture.png", caption="AI Transforming Indian Agriculture", use_column_width=True)

    # Center the footer links with small icons
    footer_html = """
    <div style='text-align: center;'>
        <a href="https://www.instagram.com/__kuronotsubasa__/profilecard/?igsh=MWdyNHd2NDFzZWl3Yw==" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/32px-Instagram_icon.png" alt="Instagram" style="margin: 5px; width: 32px; height: 32px;">
        </a>
        <a href="https://github.com/Sasanka14" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" alt="GitHub" style="margin: 5px; width: 32px; height: 32px;">
        </a>
        <a href="https://www.linkedin.com/in/sasanka-sekhar-kundu-b746072a7" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" alt="LinkedIn" style="margin: 5px; width: 32px; height: 32px;">
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

# Disease Recognition Section
elif app_mode == "Disease Recognition":
    st.header("Disease Recognition")
    st.write("""
    Upload an image of your crop leaf, and our AI-powered model will detect the disease and suggest potential treatments. 
    Ensure the image is clear and focused for accurate results.
    """)

    # File uploader for image
    test_image = st.file_uploader("Upload an Image of the Crop Leaf (Supported formats: JPG, PNG, JPEG)", type=["jpg", "png", "jpeg"])
    
    if test_image:
        img = Image.open(test_image)
        st.image(img, caption="Uploaded Image", use_column_width=True)

    # Predict button functionality
    if st.button("Analyze Image"):
        if test_image:
            # Add progress bar for the prediction process
            progress_bar = st.progress(0)
            status_text = st.empty()  # Empty placeholder to update status

            # Inform the user the process has started
            status_text.text("Analyzing the image... Please wait.")

            # Simulate progress bar increment (this would be linked to actual processing)
            for i in range(100):
                time.sleep(0.05)  # Simulate task
                progress_bar.progress(i + 1)
                status_text.text(f"Analyzing... {i + 1}%")

            # Call the prediction function
            try:
                result_index = model_prediction(test_image)
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
                disease_name = class_name[result_index]
                st.success(f"Prediction Result: **{disease_name}**")
                
                # Provide Treatment Suggestions
                treatment = get_treatment(disease_name)
                st.subheader("Suggested Treatment")
                st.write(f"🩺 **Treatment Recommendation:** {treatment}")

                # Encourage User Engagement
                st.write("""
                🌱 **Tip for Best Results:** Always follow the recommended agricultural practices and consult a local agricultural expert for further advice.
                """)
            except Exception as e:
                st.error(f"An error occurred during prediction: {e}")
        else:
            st.warning("Please upload an image to proceed.")
    else:
        st.info("Waiting for you to upload an image and click the 'Analyze Image' button.")

   # Center the footer links with small icons
    footer_html = """
    <div style='text-align: center;'>
        <a href="https://www.instagram.com/__kuronotsubasa__/profilecard/?igsh=MWdyNHd2NDFzZWl3Yw==" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/32px-Instagram_icon.png" alt="Instagram" style="margin: 5px; width: 32px; height: 32px;">
        </a>
        <a href="https://github.com/Sasanka14" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" alt="GitHub" style="margin: 5px; width: 32px; height: 32px;">
        </a>
        <a href="https://www.linkedin.com/in/sasanka-sekhar-kundu-b746072a7" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" alt="LinkedIn" style="margin: 5px; width: 32px; height: 32px;">
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)
