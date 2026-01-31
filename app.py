import streamlit as st
import requests
import os
from datetime import datetime
import time
from streamlit_autorefresh import st_autorefresh

# 1. Setup
st.set_page_config(page_title="Bozi's Bowman Gray Monitor", layout="wide")
URL = "https://eapps.ncdot.gov/services/traffic-prod/v1/cameras/images?filename=MLK_BowmanGray.jpg"
IMAGE_DIR = "images"

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# 2. Capture
def capture_latest():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"{IMAGE_DIR}/{timestamp}.jpg"
    try:
        response = requests.get(URL, timeout=10)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
    except:
        pass

capture_latest()
st_autorefresh(interval=480000, key="bozi_refresh")

# 3. The "Enlarge" Modal
@st.dialog("Full Image View", width="large")
def show_full_image(img_path, timestamp):
    st.image(img_path, use_container_width=True)
    st.write(f"**Captured at:** {timestamp}")
    with open(img_path, "rb") as f:
        st.download_button("💾 Download High-Res", f, file_name=img_path.split("/")[-1])

# 4. App UI
st.title("📸 Bozi's Bowman Gray Monitor")

if os.path.exists(IMAGE_DIR):
    files = sorted([f for f in os.listdir(IMAGE_DIR) if f.endswith(".jpg")])
    
    if files:
        # Timelapse
        with st.expander("🎞️ Play Timelapse"):
            speed = st.slider("Speed", 0.05, 0.5, 0.1)
            video_space = st.empty()
            if st.button("Start Playback"):
                for f in files:
                    video_space.image
