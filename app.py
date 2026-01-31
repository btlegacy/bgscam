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
        st.error(f"Capture error: {e}")
    return None

capture_latest()
st_autorefresh(interval=480000, key="bozi_refresh")

# 3. UI Header
st.title("📸 Bozi's Bowman Gray Monitor")
st.write(f"**Last Sync:** {datetime.now().strftime('%H:%M:%S')}")

# 4. Processing Images
if os.path.exists(IMAGE_DIR):
    files = sorted([f for f in os.listdir(IMAGE_DIR) if f.endswith(".jpg")])
    
    if files:
        # --- TIMELAPSE PLAYER ---
        with st.expander("🎞️ View Timelapse Progression", expanded=True):
            speed = st.select_slider("Speed (sec/frame)", options=[0.05, 0.1, 0.2, 0.5], value=0.1)
            video_placeholder = st.empty()
            if st.button("▶️ Play Timelapse"):
                for file in files:
                    video_placeholder.image(f"{IMAGE_DIR}/{file}", use_container_width=True)
                    time.sleep(speed)

        st.divider()

        # --- GALLERY ---
        st.header("🖼️ History")
        
        # Display latest image first
        cols = st.columns(4)
        for idx, file in enumerate(reversed(files)):
            img_path = f"{IMAGE_DIR}/{file}"
            # Extract just the time HH-MM from the filename
            time_label = file.replace('.jpg', '').split('_')[1].replace('-', ':')
            
            with cols[idx % 4]:
                st.image(img_path, use_container_width=True)
                
                # The Popover acts as the "Expansion" trigger
                with st.popover(f"🔎 Full View ({time_label})", use_container_width=True):
                    st.image(img_path, use_container_width=True)
                    st.caption(f"Captured: {file.replace('.jpg', '')}")
                    
                    # Add a dedicated download link inside the popover
                    with open(img_path, "rb") as f:
                        st.download_button("💾 Save to Device", f, file_name=file)
    else:
        st.info("Archive is empty. Waiting for next capture...")
