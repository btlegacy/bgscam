import streamlit as st
import requests
import os
from datetime import datetime
import time
from streamlit_autorefresh import st_autorefresh

# 1. Configuration & Setup
st.set_page_config(page_title="NCDOT Live Tracker", layout="wide")
URL = "https://eapps.ncdot.gov/services/traffic-prod/v1/cameras/images?filename=MLK_BowmanGray.jpg"
IMAGE_DIR = "images"

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# 2. The Capture Logic (Runs on every load/refresh)
def capture_latest():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"{IMAGE_DIR}/{timestamp}.jpg"
    
    try:
        response = requests.get(URL, timeout=10)
        if response.status_code == 200:
            # Only save if the image data is actually new (optional refinement)
            with open(filename, 'wb') as f:
                f.write(response.content)
            return filename
    except Exception as e:
        st.error(f"Failed to capture live image: {e}")
    return None

# Trigger capture on load
latest_file = capture_latest()

# 3. Auto-Refresh (Triggers a rerun every 8 minutes / 480,000 ms)
st_autorefresh(interval=480000, key="webcam_refresh")

# 4. UI Elements
st.title("📸 MLK @ Bowman Gray Live Archive")
st.write(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")

# Load all images for display
files = sorted([f for f in os.listdir(IMAGE_DIR) if f.endswith(".jpg")])

if files:
    # --- TIMELAPSE PLAYER ---
    st.header("🎞️ Timelapse Progression")
    speed = st.select_slider("Playback Speed", options=[0.1, 0.2, 0.5, 1.0], value=0.2, help="Seconds per frame")
    
    video_placeholder = st.empty()
    label_placeholder = st.empty()
    
    if st.button("▶️ Play Timelapse"):
        for file in files:
            video_placeholder.image(f"{IMAGE_DIR}/{file}", use_container_width=True)
            label_placeholder.markdown(f"**Viewing:** {file.replace('.jpg', '')}")
            time.sleep(speed)

    st.divider()

    # --- GALLERY ---
    st.header("🖼️ History (Newest First)")
    cols = st.columns(4)
    for idx, file in enumerate(reversed(files)):
        with cols[idx % 4]:
            st.image(f"{IMAGE_DIR}/{file}", caption=file.replace('.jpg', ''), use_container_width=True)
