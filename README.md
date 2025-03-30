# Aoml-final-proj
This project combines OCR, Machine Learning, Deep Learning, and AI-based NLP to create an interactive, real-time study assistant. It not only detects confusion dynamically but also provides AI-generated explanations, improving user engagement and making self-learning more effective.

📖 Problem Statement
Many students struggle to comprehend complex study materials, often getting confused while reading lengthy or technical content. Traditional learning tools provide text summaries but do not dynamically detect confusion in real time.
This project solves the problem by:
✅ Detecting real-time confusion using eye tracking and facial expressions.
✅ Extracting text from PDFs and images using OCR.
✅ Applying AI-based NLP (via Google Gemini API) to provide simplified explanations.
✅ Using deep learning models to improve confusion detection.
📂 Custom Dataset
We created a custom dataset of labeled confusion and non-confusion facial expressions.
Collected images/videos of users reading different texts.
Manually annotated frames where users showed confusion.
Labeled eye movement and blink rates as additional features.
Dataset is used for training a confusion detection model with OpenCV and deep learning.
🎯 Solution Breakdown
1️⃣ Text Extraction (OCR)
Uses Tesseract OCR to extract text from PDFs and images.
Preprocessing steps:
✅ Grayscale conversion
✅ Noise removal
✅ Adaptive thresholding for better text detection.
2️⃣ Real-Time Confusion Detection
🔹 Tracks eye movements and blink rate.
🔹 Ignores first 3 confusion instances to allow natural reading.
🔹 Uses OpenCV for face & eye tracking.
🔹 Deep learning-based classification for improved accuracy.
3️⃣ AI-Based Simplification (Google Gemini API)
Detects the specific sentence or section causing confusion.
Uses Google Gemini API to generate an easier version.
If still confused, provides an even simpler explanation.
4️⃣ Streamlit UI for Interaction
Webcam-based tracking embedded in the UI.
User uploads PDFs or images for study.
If confused, a pop-up alert asks if they need a simpler explanation.
