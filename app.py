import streamlit as st
import requests
import os
from datetime import datetime
import time
from streamlit_autorefresh import st_autorefresh
import pytz

# 1. Configuration & Setup
st.set_page_config(page_title="Bozi's Bowman Gray Monitor", layout="wide")

# Define Eastern Timezone
ET = pytz.timezone('US/Eastern')

URL = "https://eapps.ncdot.gov/services/traffic-prod/v1/cameras/images?filename=MLK_BowmanGray.jpg"
IMAGE_DIR = "images"

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# 2. Capture Logic with ET Timestamp
def capture_latest():
    # Get current time in Eastern Time
    now_et = datetime.now(ET)
    timestamp = now_et.strftime("%Y-%m-%d_%H-%M")
    filename = f"{IMAGE_DIR}/{timestamp}.jpg"
    
    try:
        response = requests.get(URL, timeout=10)
        if response.status_code == 200:
            # We check if the file already exists to avoid redundant saves 
            # if the page is manually refreshed multiple times
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
# Show current local time in Winston-Salem
current_time = datetime.now(ET).strftime('%I:%M:%S %p')
st.write(f"**Winston-Salem Local Time:** {current_time}")

# 4. Processing Images
if os.path.exists(IMAGE_DIR):
    files = sorted([f for f in os.listdir(IMAGE_DIR) if f.endswith(".jpg")])
    
    if files:
        # --- FAST AUTO-PLAY TIMELAPSE ---
        st.header("🎞️ Live Timelapse Progression")
        
        video_placeholder = st.empty()
        label_placeholder = st.empty()
        
        for file in files:
            img_path = f"{IMAGE_DIR}/{file}"
            # Format label for display: YYYY-MM-DD HH:MM
            display_label = file.replace('.jpg', '').replace('_', ' ')
            
            video_placeholder.image(img_path, use_container_width=True)
            label_placeholder.markdown(f"**Frame Time (ET):** {display_label}")
            time.sleep(0.1)

        st.success("Timelapse complete.")
        st.divider()

        # --- GALLERY ---
        st.header("🖼️ Captured Frames")
        
        cols = st.columns(4)
        for idx, file in enumerate(reversed(files)):
            img_path = f"{IMAGE_DIR}/{file}"
            # Extract time and convert to 12-hour format for the button
            raw_time = file.replace('.jpg', '').split('_')[1] # e.g. "14-20"
            hour, minute = raw_time.split('-')
            formatted_time = datetime.strptime(f"{hour}:{minute}", "%H:%M").strftime("%I:%M %p")
            
            with cols[idx % 4]:
                st.image(img_path, use_container_width=True)
                with st.popover(f"🔎 Enlarge {formatted_time}", use_container_width=True):
                    st.image(img_path, use_container_width=True)
                    st.write(f"Timestamp: {file.replace('.jpg', '')} ET")
                    with open(img_path, "rb") as f:
                        st.download_button("💾 Save", f, file_name=file, key=f"dl_{file}")
    else:
        st.info("Archive is empty. Waiting for next capture...")
