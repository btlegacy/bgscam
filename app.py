import streamlit as st
import os
from datetime import datetime
import time
from streamlit_autorefresh import st_autorefresh
import pytz

# 1. Configuration & Setup
st.set_page_config(page_title="Bozi's Bowman Gray Monitor", layout="wide")
ET = pytz.timezone('US/Eastern')
IMAGE_DIR = "images"

# Ensure directory exists so the app doesn't crash if it's empty
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# 2. Auto-Refresh
# Set to 6 minutes (360,000ms) to match your new capture schedule
st_autorefresh(interval=360000, key="bozi_refresh")

# 3. UI Header
st.title("📸 Bozi's Bowman Gray Monitor")
current_time = datetime.now(ET).strftime('%I:%M:%S %p')
st.write(f"**Winston-Salem Local Time:** {current_time}")
st.caption("Note: This is just a fun tool to follow snow and cleanup progress.")

# 4. Processing Images
if os.path.exists(IMAGE_DIR):
    # Sort files chronologically for the timelapse
    files = sorted([f for f in os.listdir(IMAGE_DIR) if f.endswith(".jpg")])
    
    if files:
        # --- CONTINUOUS TIMELAPSE ---
        st.header("🎞️ Continuous Timelapse Progression")
        
        video_placeholder = st.empty()
        label_placeholder = st.empty()
        
        # --- GALLERY CONTAINER ---
        # We render the gallery first so it's visible while the loop runs
        gallery_container = st.container()
        
        with gallery_container:
            st.divider()
            st.header("🖼️ Captured Frames (Newest First)")
            cols = st.columns(4)
            # Use reversed(files) for the gallery to show newest first
            for idx, file in enumerate(reversed(files)):
                img_path = f"{IMAGE_DIR}/{file}"
                
                # Format time for the popover button (12-hour format)
                try:
                    raw_time = file.replace('.jpg', '').split('_')[1]
                    hour, minute = raw_time.split('-')
                    formatted_time = datetime.strptime(f"{hour}:{minute}", "%H:%M").strftime("%I:%M %p")
                except:
                    formatted_time = "Unknown"
                
                with cols[idx % 4]:
                    st.image(img_path, use_container_width=True)
                    with st.popover(f"🔎 Enlarge {formatted_time}", use_container_width=True):
                        st.image(img_path, use_container_width=True)
                        st.write(f"**Full Timestamp:** {file.replace('.jpg', '')} ET")
                        with open(img_path, "rb") as f:
                            st.download_button("💾 Save to Device", f, file_name=file, key=f"dl_{file}")

        # 5. THE INFINITE LOOP
        # Plays at 0.5 seconds per frame as requested
        while True:
            for file in files:
                img_path = f"{IMAGE_DIR}/{file}"
                display_label = file.replace('.jpg', '').replace('_', ' ')
                
                video_placeholder.image(img_path, use_container_width=True)
                label_placeholder.markdown(f"**Looping Frame (ET):** {display_label}")
                
                time.sleep(0.5) 
    else:
        st.info("Archive is empty. Waiting for GitHub Actions to push the first image...")
else:
    st.warning("Images directory not found. Please ensure the GitHub Action has run at least once.")
