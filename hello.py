import streamlit as st
import cv2
import pytesseract
import time
import numpy as np
import google.generativeai as genai
from PIL import Image
import fitz  # PyMuPDF for PDF processing

# Set up Google Gemini API
genai.configure(api_key="AIzaSyBGyO1zrR0nlVTwXcJVdHRyoUrKsG8w5n4")
model = genai.GenerativeModel("gemini-1.5-pro-latest")  # Change for speed: "gemini-1.5-flash-latest"

# Set Tesseract Path (Change if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load OpenCV Haar cascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

# Streamlit App UI
st.title("📚 AI-Powered Study Assistant")
st.sidebar.header("Upload your Study Material")

# Upload PDF or Image
uploaded_file = st.sidebar.file_uploader("Upload a PDF or Image", type=["pdf", "jpg", "png"])

def extract_text(file):
    """ Extract text from PDF or Image using Tesseract OCR """
    text = ""
    if file.type == "application/pdf":
        # Process PDF using PyMuPDF
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
    st.text_area("Extracted Content", extracted_text, height=200)

# Function to simplify text using Gemini API
def simplify_text(text):
    """ Call Gemini API to simplify the extracted text """
    response = model.generate_content(f"Simplify this text for a beginner:\n{text}")
    return response.text if response.text else "Error generating explanation."

# Confusion Detection Function
def detect_confusion():
    cap = cv2.VideoCapture(0)
    stframe = st.empty()
    stop_camera = st.button("Stop Camera", key="stop_camera_btn")  # Ensure unique key
    confusion_detected = False
    start_time = None
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80))

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            if len(eyes) == 2:
                if start_time is None:
                    start_time = time.time()
                elif time.time() - start_time > 6:  # 4 seconds of confusion detection
                    confusion_detected = True
                    break

        stframe.image(frame, channels="BGR")

        if confusion_detected:
            st.warning("😕 You look confused! Would you like a simpler explanation?")
            cap.release()
            
            return True

        if stop_camera:
            cap.release()
           
            return False

# Run Confusion Detection
if st.button("Start Confusion Detection", key="start_camera_btn"):
    confusion = detect_confusion()
    if confusion and uploaded_file:
        st.subheader("🤖 AI Suggests a Simpler Explanation:")
        simplified_text = simplify_text(extracted_text)
        st.success(simplified_text)

#-------
# import streamlit as st
# import cv2
# import pytesseract
# import time
# import numpy as np
# import google.generativeai as genai
# from PIL import Image
# import fitz  # PyMuPDF for PDF processing

# # Set up Google Gemini API
# genai.configure(api_key="AIzaSyBGyO1zrR0nlVTwXcJVdHRyoUrKsG8w5n4")
# model = genai.GenerativeModel("gemini-1.5-pro-latest")  # Change for speed: "gemini-1.5-flash-latest"

# # Set Tesseract Path (Change if needed)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# # Load OpenCV Haar cascades
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
# eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

# # Streamlit App UI
# st.title("📚 AI-Powered Study Assistant")
# st.sidebar.header("Upload your Study Material")

# # Upload PDF or Image
# uploaded_file = st.sidebar.file_uploader("Upload a PDF or Image", type=["pdf", "jpg", "png"])

# def extract_text(file):
#     """ Extract text from PDF or Image using Tesseract OCR """
#     text = ""
#     if file.type == "application/pdf":
#         # Process PDF using PyMuPDF
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
#     st.text_area("Extracted Content", extracted_text, height=200)

# # Function to simplify text using Gemini API
# def simplify_text(text):
#     """ Call Gemini API to simplify the extracted text """
#     response = model.generate_content(f"Simplify this text for a beginner:\n{text}")
#     return response.text if response.text else "Error generating explanation."

# # Confusion Detection Function (10-second threshold)
# def detect_confusion():
#     cap = cv2.VideoCapture(0)
#     stframe = st.empty()
#     stop_camera = st.button("Stop Camera", key="stop_camera_btn")  # Ensure unique key
#     confusion_detected = False
#     start_time = None
    
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80))

#         for (x, y, w, h) in faces:
#             roi_gray = gray[y:y+h, x:x+w]
#             roi_color = frame[y:y+h, x:x+w]
#             eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

#             if len(eyes) == 2:
#                 if start_time is None:
#                     start_time = time.time()
#                 elif time.time() - start_time > 10:  # Changed from 4 to 10 seconds
#                     confusion_detected = True
#                     break
#             else:
#                 start_time = None  # Reset if eyes are not detected properly

#         stframe.image(frame, channels="BGR")

#         if confusion_detected:
#             st.warning("😕 You look confused! Would you like a simpler explanation?")
#             cap.release()
#             return True

#         if stop_camera:
#             cap.release()
#             return False

# # Run Confusion Detection
# if st.button("Start Confusion Detection", key="start_camera_btn"):
#     confusion = detect_confusion()
#     if confusion and uploaded_file:
#         st.subheader("🤖 AI Suggests a Simpler Explanation:")
#         simplified_text = simplify_text(extracted_text)
#         st.success(simplified_text)

#------

# import streamlit as st
# import cv2
# import pytesseract
# import time
# import numpy as np
# import google.generativeai as genai
# from PIL import Image
# import fitz  # PyMuPDF for PDF processing

# # Set up Google Gemini API
# genai.configure(api_key="AIzaSyBGyO1zrR0nlVTwXcJVdHRyoUrKsG8w5n4")
# model = genai.GenerativeModel("gemini-1.5-pro-latest")  # Change for speed: "gemini-1.5-flash-latest"

# # Set Tesseract Path (Change if needed)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# # Load OpenCV Haar cascades
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
# eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

# # Streamlit App UI
# st.title("📚 AI-Powered Study Assistant")
# st.sidebar.header("Upload your Study Material")

# # Upload PDF or Image
# uploaded_file = st.sidebar.file_uploader("Upload a PDF or Image", type=["pdf", "jpg", "png"])

# def extract_text(file):
#     """ Extract text from PDF or Image using Tesseract OCR """
#     text = ""
#     if file.type == "application/pdf":
#         # Process PDF using PyMuPDF
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
#     st.text_area("Extracted Content", extracted_text, height=300)  # Increased height for better visibility

# # Function to simplify text using Gemini API
# def simplify_text(text):
#     """ Call Gemini API to simplify the extracted text """
#     response = model.generate_content(f"Simplify this text for a beginner:\n{text}")
#     return response.text if response.text else "Error generating explanation."

# # Confusion Detection Function (Skips first 3, triggers on 4th)
# def detect_confusion():
#     cap = cv2.VideoCapture(0)
#     cap.set(3, 480)  # Set width to reduce camera size
#     cap.set(4, 360)  # Set height to reduce camera size

#     stframe = st.empty()
#     stop_camera = st.button("Stop Camera", key="stop_camera_btn")  # Ensure unique key
#     confusion_count = 0
#     start_time = None
    
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80))

#         for (x, y, w, h) in faces:
#             roi_gray = gray[y:y+h, x:x+w]
#             roi_color = frame[y:y+h, x:x+w]
#             eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

#             if len(eyes) == 2:
#                 if start_time is None:
#                     start_time = time.time()
#                 elif time.time() - start_time > 10:  # 10-second confusion threshold
#                     confusion_count += 1  # Track confusion occurrences
#                     start_time = None  # Reset timer for next confusion check

#                 if confusion_count >= 4:  # Trigger only on the 4th detection
#                     stframe.image(frame, channels="BGR", caption="😕 Confusion detected!")
#                     st.warning("😕 You look confused! Would you like a simpler explanation?")
#                     cap.release()
#                     cv2.destroyAllWindows()
#                     return True

#         stframe.image(frame, channels="BGR", use_column_width=False)  # Reduced camera size

#         if stop_camera:
#             cap.release()
#             cv2.destroyAllWindows()
#             return False

# # Run Confusion Detection
# if st.button("Start Confusion Detection", key="start_camera_btn"):
#     confusion = detect_confusion()
#     if confusion and uploaded_file:
#         st.subheader("🤖 AI Suggests a Simpler Explanation:")
#         simplified_text = simplify_text(extracted_text)
#         st.success(simplified_text)
