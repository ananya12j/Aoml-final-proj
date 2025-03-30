# import streamlit as st
# import cv2
# import pytesseract
# import time
# import numpy as np
# import google.generativeai as genai
# from PIL import Image
# import fitz  # PyMuPDF for PDF processing
# import joblib
# import tensorflow as tf
# from tensorflow.keras.applications import VGG16
# from tensorflow.keras.preprocessing import image
# from tensorflow.keras.applications.vgg16 import preprocess_input

# # -----------------------------
# # ✅ Load Pretrained Models
# # -----------------------------
# # Load Google Gemini API
# genai.configure(api_key="AIzaSyBGyO1zrR0nlVTwXcJVdHRyoUrKsG8w5n4")
# model = genai.GenerativeModel("gemini-1.5-pro-latest")

# # Load Trained Confusion Detection Model
# confusion_model = joblib.load("confusion_detector.pkl")

# # Load VGG16 for Feature Extraction
# vgg16 = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# # -----------------------------
# # ✅ Streamlit UI
# # -----------------------------
# st.title("📚 AI-Powered Study Assistant")
# st.sidebar.header("Upload your Study Material")

# # Upload PDF or Image
# uploaded_file = st.sidebar.file_uploader("Upload a PDF or Image", type=["pdf", "jpg", "png"])

# # -----------------------------
# # ✅ Extract Text from PDF/Image
# # -----------------------------
# def extract_text(file):
#     text = ""
#     if file.type == "application/pdf":
#         doc = fitz.open(stream=file.read(), filetype="pdf")
#         for page in doc:
#             text += page.get_text("text") + "\n"
#     else:
#         image = Image.open(file)
#         text = pytesseract.image_to_string(image)
#     return text.strip()

# # Display Extracted Text
# if uploaded_file:
#     extracted_text = extract_text(uploaded_file)
#     st.subheader("📜 Extracted Text:")
#     st.markdown(f"<h3 style='color:blue'>{extracted_text}</h3>", unsafe_allow_html=True)

# # -----------------------------
# # ✅ Simplify Text Using Gemini API
# # -----------------------------
# def simplify_text(text):
#     """ Call Gemini API to simplify the extracted text """
#     response = model.generate_content(f"Simplify this text for a beginner:\n{text}")
#     return response.text if response.text else "Error generating explanation."

# # -----------------------------
# # ✅ Extract Features for Confusion Detection
# # -----------------------------
# def extract_features_from_frame(frame):
#     img = cv2.resize(frame, (224, 224))
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     img = image.img_to_array(img)
#     img = np.expand_dims(img, axis=0)
#     img = preprocess_input(img)
#     features = vgg16.predict(img)

#     # Flatten and reduce to 5120 features (to match trained SVM)
#     features = features.flatten()[:5120]
#     return features.reshape(1, -1)

# # -----------------------------
# # ✅ Live Confusion Detection
# # -----------------------------
# def detect_confusion():
#     cap = cv2.VideoCapture(0)
#     cap.set(3, 640)  # Reduce camera width
#     cap.set(4, 480)  # Reduce camera height

#     stframe = st.empty()
#     stop_camera = st.button("Stop Camera")

#     confusion_count = 0  # Track number of confusions detected
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         features = extract_features_from_frame(frame)
#         prediction = confusion_model.predict(features)[0]

#         # Count confusion instances
#         if prediction == 1:
#             confusion_count += 1

#         # Only trigger response after 4 confusion detections (skip first 3)
#         if confusion_count >= 4:
#             cv2.putText(frame, "😕 You look confused!", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
#             stframe.image(frame, channels="BGR")
#             time.sleep(1.5)  # Pause before response

#             # Show warning as pop-up
#             st.warning("😕 You look confused! Would you like a simpler explanation?")
#             cap.release()
#             return True

#         # Show normal frame with Confusion Status
#         label = "😕 Confused" if prediction == 1 else "😊 Not Confused"
#         color = (0, 0, 255) if prediction == 1 else (0, 255, 0)
#         cv2.putText(frame, label, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

#         stframe.image(frame, channels="BGR")

#         # Stop camera if button is pressed
#         if stop_camera:
#             cap.release()
#             return False

#     cap.release()
#     return False

# # -----------------------------
# # ✅ Run Confusion Detection & Provide Explanation
# # -----------------------------
# if st.button("Start Confusion Detection"):
#     confusion = detect_confusion()
    
#     if confusion and uploaded_file:
#         st.subheader("🤖 AI Suggests a Simpler Explanation:")
#         simplified_text = simplify_text(extracted_text)
#         st.success(simplified_text)

#------

import streamlit as st
import cv2
import pytesseract
import time
import numpy as np
import google.generativeai as genai
from PIL import Image
import fitz  # PyMuPDF for PDF processing
import joblib
import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input

# -----------------------------
# ✅ Load Pretrained Models
# -----------------------------
# Load Google Gemini API
genai.configure(api_key="AIzaSyBGyO1zrR0nlVTwXcJVdHRyoUrKsG8w5n4")
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Load Confusion Detection Model (SVM trained on VGG16 embeddings)
confusion_model = joblib.load("confusion_detector.pkl")

# Load VGG16 for Feature Extraction (no fully connected layers)
vgg16 = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# -----------------------------
# ✅ Streamlit UI
# -----------------------------
st.title("📚 AI-Powered Study Assistant")
st.sidebar.header("Upload your Study Material")

# Upload PDF or Image
uploaded_file = st.sidebar.file_uploader("Upload a PDF or Image", type=["pdf", "jpg", "png"])

# -----------------------------
# ✅ Extract Text from PDF/Image
# -----------------------------
def extract_text(file):
    text = ""
    if file.type == "application/pdf":
        doc = fitz.open(stream=file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text("text") + "\n"
    else:
        image = Image.open(file)
        text = pytesseract.image_to_string(image)
    return text.strip()

# Display Extracted Text
if uploaded_file:
    extracted_text = extract_text(uploaded_file)
    st.subheader("📜 Extracted Text:")
    st.markdown(f"<h3 style='color:blue'>{extracted_text}</h3>", unsafe_allow_html=True)

# -----------------------------
# ✅ Simplify Text Using Gemini API
# -----------------------------
def simplify_text(text):
    """ Call Gemini API to simplify the extracted text """
    response = model.generate_content(f"Simplify this text for a beginner:\n{text}")
    return response.text if response.text else "Error generating explanation."

# -----------------------------
# ✅ Extract Features for Confusion Detection (Using VGG16)
# -----------------------------
def extract_features_from_frame(frame):
    """ Extract deep features from an image frame using VGG16 """
    img = cv2.resize(frame, (224, 224))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    
    # Extract features and flatten
    features = vgg16.predict(img)
    features = features.flatten()[:5120]  # Match trained model's feature size
    return features.reshape(1, -1)

# -----------------------------
# ✅ Live Confusion Detection (Skip Every 3rd Frame)
# -----------------------------
def detect_confusion():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  # Camera width
    cap.set(4, 480)  # Camera height

    stframe = st.empty()
    stop_camera = st.button("Stop Camera")

    frame_count = 0  # Track frames
    confusion_count = 0  # Track confusion instances
    no_confusion_count = 0  # Track non-confused instances

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Skip every 3 frames
        if frame_count % 3 == 0:
            features = extract_features_from_frame(frame)
            prediction = confusion_model.predict(features)[0]

            # Implement confidence-based tracking
            if prediction == 1:
                confusion_count += 1
                no_confusion_count = 0  # Reset no confusion counter
            else:
                no_confusion_count += 1
                confusion_count = max(0, confusion_count - 1)  # Gradual decrease

        frame_count += 1  # Increment frame count

        # Display prediction label
        label = "😕 Confused" if confusion_count >= 3 else "😊 Not Confused"
        color = (0, 0, 255) if confusion_count >= 3 else (0, 255, 0)
        cv2.putText(frame, label, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        stframe.image(frame, channels="BGR")

        # Stop camera if button is pressed
        if stop_camera:
            cap.release()
            return False

        # Trigger AI explanation if confusion count reaches threshold
        if confusion_count >= 3:
            st.warning("😕 You look confused! Would you like a simpler explanation?")
            cap.release()
            return True

    cap.release()
    return False

# -----------------------------
# ✅ Run Confusion Detection & Provide Explanation
# -----------------------------
if st.button("Start Confusion Detection"):
    confusion = detect_confusion()
    
    if confusion and uploaded_file:
        st.subheader("🤖 AI Suggests a Simpler Explanation:")
        simplified_text = simplify_text(extracted_text)
        st.success(simplified_text)
