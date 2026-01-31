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

# Refresh every 8 minutes (480,000ms)
st_autorefresh(interval=480000, key="bozi_refresh")

# 3. UI Header
st.title("📸 Bozi's Bowman Gray Monitor")
st.write(f"**Last Sync:** {datetime.now().strftime('%H:%M:%S')}")

# 4. Processing Images
if os.path.exists(IMAGE_DIR):
    # Sort files chronologically for the timelapse
    files = sorted([f for f in os.listdir(IMAGE_DIR) if f.endswith(".jpg")])
    
    if files:
        # --- AUTO-PLAY TIMELAPSE SECTION ---
        st.header("🎞️ Live Timelapse Progression")
        
        video_placeholder = st.empty()
        label_placeholder = st.empty()
        
        # This loop runs automatically on page load
        # Using a slice like files[-50:] would play only the last 50 images if the archive gets too big
        for file in files:
            img_path = f"{IMAGE_DIR}/{file}"
            video_placeholder.image(img_path, use_container_width=True)
            label_placeholder.markdown(f"**Timestamp:** {file.replace('.jpg', '').replace('_', ' ')}")
            time.sleep(0.5) # Set to 0.5 seconds per frame

        st.divider()

        # --- GALLERY ---
        st.header("🖼️ Captured Frames")
        st.caption("Expand any frame below to view or download.")
        
        cols = st.columns(4)
        for idx, file in enumerate(reversed(files)):
            img_path = f"{IMAGE_DIR}/{file}"
            time_label = file.replace('.jpg', '').split('_')[1].replace('-', ':')
            
            with cols[idx % 4]:
                st.image(img_path, use_container_width=True)
                with st.popover(f"🔎 Enlarge {time_label}", use_container_width=True):
                    st.image(img_path, use_container_width=True)
                    with open(img_path, "rb") as f:
                        st.download_button("💾 Save Image", f, file_name=file, key=f"dl_{file}")
    else:
        st.info("Archive is empty. Waiting for next capture...")
