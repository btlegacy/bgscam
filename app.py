import streamlit as st
import requests
import os
from datetime import datetime, timedelta
import time
from streamlit_autorefresh import st_autorefresh
import pytz

# 1. Configuration & Setup
st.set_page_config(page_title="Bozi's Bowman Gray Monitor", layout="wide")
ET = pytz.timezone('US/Eastern')
IMAGE_DIR = "images"
URL = "https://eapps.ncdot.gov/services/traffic-prod/v1/cameras/images?filename=MLK_BowmanGray.jpg"

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# 2. Capture Logic (Saves new files correctly in ET)
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
    except:
        pass

capture_latest()
st_autorefresh(interval=480000, key="bozi_refresh")

# 3. Helper Function to fix display labels for old files
def get_display_time(filename):
    # Remove extension and directory
    clean_name = filename.replace('.jpg', '').split('/')[-1]
    try:
        # Try to parse the filename timestamp
        dt = datetime.strptime(clean_name, "%Y-%m-%d_%H-%M")
        
        # LOGIC: If the year/date matches your old UTC captures (before today's fix),
        # subtract 5 hours to shift UTC to Eastern Time.
        # Adjust '2026-01-31 10:30' to the exact moment you switched the code.
        switch_cutoff = datetime(2026, 1, 31, 10, 30) 
        
        if dt < switch_cutoff:
            dt = dt - timedelta(hours=5)
            
        return dt.strftime("%I:%M %p")
    except:
        return clean_name

# 4. UI Header
st.title("📸 Bozi's Bowman Gray Monitor")
st.write(f"**Winston-Salem Local Time:** {datetime.now(ET).strftime('%I:%M:%S %p')}")

# 5. Processing Images
if os.path.exists(IMAGE_DIR):
    files = sorted([f for f in os.listdir(IMAGE_DIR) if f.endswith(".jpg")])
    
    if files:
        # --- AUTO-PLAY TIMELAPSE ---
        st.header("🎞️ Live Timelapse Progression")
        video_placeholder = st.empty()
        label_placeholder = st.empty()
        
        for file in files:
            img_path = f"{IMAGE_DIR}/{file}"
            display_time = get_display_time(file)
            video_placeholder.image(img_path, use_container_width=True)
            label_placeholder.markdown(f"**Frame Time:** {display_time}")
            time.sleep(0.1)

        st.divider()

        # --- GALLERY ---
        st.header("🖼️ Captured Frames")
        cols = st.columns(4)
        for idx, file in enumerate(reversed(files)):
            img_path = f"{IMAGE_DIR}/{file}"
            display_time = get_display_time(file)
            
            with cols[idx % 4]:
                st.image(img_path, use_container_width=True)
                with st.popover(f"🔎 Enlarge {display_time}", use_container_width=True):
                    st.image(img_path, use_container_width=True)
                    st.write(f"Filename Timestamp: {file}")
                    with open(img_path, "rb") as f:
                        st.download_button("💾 Save", f, file_name=file, key=f"dl_{file}")
