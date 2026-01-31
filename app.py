import streamlit as st
import os
from PIL import Image
import time

st.set_page_config(page_title="NCDOT Webcam Archive", layout="wide")

st.title("📸 MLK @ Bowman Gray Webcam Tracker")

IMAGE_DIR = "images"

# Load and sort images
if not os.path.exists(IMAGE_DIR) or not os.listdir(IMAGE_DIR):
    st.warning("No images captured yet. Run the capture script to begin.")
else:
    # Get all jpg files and sort them chronologically
    files = sorted([f for f in os.listdir(IMAGE_DIR) if f.endswith(".jpg")])
    
    # --- TIMELAPSE SECTION ---
    st.header("🎞️ Timelapse Progression")
    speed = st.slider("Playback Speed (seconds per frame)", 0.05, 1.0, 0.2)
    
    placeholder = st.empty()
    label_placeholder = st.empty()
    
    if st.button("Play Timelapse"):
        for file in files:
            img_path = os.path.join(IMAGE_DIR, file)
            placeholder.image(img_path, use_container_width=True)
            label_placeholder.markdown(f"**Timestamp:** {file.replace('.jpg', '')}")
            time.sleep(speed)

    st.divider()

    # --- GALLERY SECTION ---
    st.header("🖼️ Image Gallery (Newest First)")
    cols = st.columns(3)
    
    # Show newest first
    for idx, file in enumerate(reversed(files)):
        with cols[idx % 3]:
            img_path = os.path.join(IMAGE_DIR, file)
            st.image(img_path, caption=file.replace('.jpg', ''), use_container_width=True)
