import streamlit as st
import requests
import os
from datetime import datetime
import time
from streamlit_autorefresh import st_autorefresh
import pytz

# 1. Configuration & Setup
st.set_page_config(page_title="Bozi's Bowman Gray Monitor", layout="wide")
ET = pytz.timezone('US/Eastern')
URL = "https://eapps.ncdot.gov/services/traffic-prod/v1/cameras/images?filename=MLK_BowmanGray.jpg"
IMAGE_DIR = "images"

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# 2. Capture Logic
def capture_latest():
    now_et = datetime.now(ET)
    timestamp = now_et.strftime("%Y-%m-%d_%H-%M")
    filename = f"{IMAGE_DIR}/{timestamp}.jpg"
    try:
        response = requests.get(URL, timeout=10)
        if response.status_code == 200:
            if not os.path.exists(filename):
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
current_time = datetime.now(ET).strftime('%I:%M:%S %p')
st.write(f"**Winston-Salem Local Time:** {current_time}")

# 4. Processing Images
if os.path.exists(IMAGE_DIR):
    files = sorted([f for f in os.listdir(IMAGE_DIR) if f.endswith(".jpg")])
    
    if files:
        # --- CONTINUOUS TIMELAPSE ---
        st.header("🎞️ Continuous Timelapse Progression")
        
        video_placeholder = st.empty()
        label_placeholder = st.empty()
        
        # --- GALLERY (Rendered before the loop) ---
        # We use a container so the gallery stays on the page while the loop runs above it
        gallery_container = st.container()
        
        with gallery_container:
            st.divider()
            st.header("🖼️ Captured Frames")
            cols = st.columns(4)
            for idx, file in enumerate(reversed(files)):
                img_path = f"{IMAGE_DIR}/{file}"
                raw_time = file.replace('.jpg', '').split('_')[1]
                hour, minute = raw_time.split('-')
                formatted_time = datetime.strptime(f"{hour}:{minute}", "%H:%M").strftime("%I:%M %p")
                
                with cols[idx % 4]:
                    st.image(img_path, use_container_width=True)
                    with st.popover(f"🔎 Enlarge {formatted_time}", use_container_width=True):
                        st.image(img_path, use_container_width=True)
                        st.write(f"Timestamp: {file.replace('.jpg', '')} ET")
                        with open(img_path, "rb") as f:
                            st.download_button("💾 Save", f, file_name=file, key=f"dl_{file}")

        # 5. THE INFINITE LOOP
        # This will keep the timelapse running forever until the page is refreshed or closed
        while True:
            for file in files:
                img_path = f"{IMAGE_DIR}/{file}"
                display_label = file.replace('.jpg', '').replace('_', ' ')
                
                video_placeholder.image(img_path, use_container_width=True)
                label_placeholder.markdown(f"**Looping Frame (ET):** {display_label}")
                time.sleep(0.1)
    else:
        st.info("Archive is empty. Waiting for next capture...")
