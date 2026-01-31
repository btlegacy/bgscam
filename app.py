import streamlit as st
import requests
import os
from datetime import datetime
import time
from streamlit_autorefresh import st_autorefresh

# 1. Configuration & Setup
st.set_page_config(page_title="Bozi's Bowman Gray Monitor", layout="wide")
URL = "https://eapps.ncdot.gov/services/traffic-prod/v1/cameras/images?filename=MLK_BowmanGray.jpg"
IMAGE_DIR = "images"

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# 2. Capture Logic
def capture_latest():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"{IMAGE_DIR}/{timestamp}.jpg"
    try:
        response = requests.get(URL, timeout=10)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            return filename
    except Exception as e:
        st.error(f"Failed to capture live image: {e}")
    return None

capture_latest()
st_autorefresh(interval=480000, key="bozi_refresh")

# 3. UI Header
st.title("📸 Bozi's Bowman Gray Monitor")

# 4. Processing Images
if os.path.exists(IMAGE_DIR):
    files = sorted([f for f in os.listdir(IMAGE_DIR) if f.endswith(".jpg")])
    
    if files:
        # --- TIMELAPSE PLAYER ---
        with st.expander("🎞️ View Timelapse Progression"):
            speed = st.select_slider("Playback Speed", options=[0.05, 0.1, 0.2, 0.5, 1.0], value=0.1)
            video_placeholder = st.empty()
            if st.button("▶️ Play Timelapse"):
                for file in files:
                    video_placeholder.image(f"{IMAGE_DIR}/{file}", use_container_width=True)
                    time.sleep(speed)

        st.divider()

        # --- CLICKABLE GALLERY ---
        st.header("🖼️ Captured Frames")
        st.caption("Click any image to enlarge it.")
        
        # Use columns for the gallery
        cols = st.columns(4)
        
        for idx, file in enumerate(reversed(files)):
            img_path = f"{IMAGE_DIR}/{file}"
            friendly_time = file.replace('.jpg', '').replace('_', ' ')
            
            with cols[idx % 4]:
                # We use a button with an empty label and set the image inside 
                # This makes the entire image area "active"
                if st.button(f"Enlarge {file}", key=f"btn_{file}", use_container_width=True):
                    st.session_state['selected_img'] = img_path
                    st.session_state['selected_time'] = friendly_time

        # --- MODAL / OVERLAY VIEW ---
        # If an image was clicked, show it at the top or in a focused view
        if 'selected_img' in st.session_state:
            st.divider()
            st.subheader(f"🔍 Viewing: {st.session_state['selected_time']}")
            st.image(st.session_state['selected_img'], use_container_width=True)
            if st.button("Close Enlarged View"):
                del st.session_state['selected_img']
                st.rerun()
    else:
        st.info("Waiting for the first image to be saved...")
