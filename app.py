import streamlit as st
import os
from datetime import datetime
import time
from streamlit_autorefresh import st_autorefresh
import pytz

st.set_page_config(page_title="Bozi's Bowman Gray Monitor", layout="wide")
ET = pytz.timezone('US/Eastern')
IMAGE_DIR = "images"

# IMPORTANT: No capture logic here anymore. 
# GitHub Actions handles the saving to the repository.

st_autorefresh(interval=480000, key="bozi_refresh")

st.title("📸 Bozi's Bowman Gray Monitor")
current_time = datetime.now(ET).strftime('%I:%M:%S %p')
st.write(f"**Winston-Salem Local Time:** {current_time}")

if os.path.exists(IMAGE_DIR):
    files = sorted([f for f in os.listdir(IMAGE_DIR) if f.endswith(".jpg")])
    
    if files:
        # --- CONTINUOUS TIMELAPSE ---
        st.header("🎞️ Continuous Timelapse Progression")
        video_placeholder = st.empty()
        label_placeholder = st.empty()
        
        gallery_container = st.container()
        
        with gallery_container:
            st.divider()
            st.header("🖼️ Captured Frames")
            cols = st.columns(4)
            for idx, file in enumerate(reversed(files)):
                img_path = f"{IMAGE_DIR}/{file}"
                # Extract time for label
                raw_time = file.replace('.jpg', '').split('_')[1]
                hour, minute = raw_time.split('-')
                formatted_time = datetime.strptime(f"{hour}:{minute}", "%H:%M").strftime("%I:%M %p")
                
                with cols[idx % 4]:
                    st.image(img_path, use_container_width=True)
                    with st.popover(f"🔎 Enlarge {formatted_time}", use_container_width=True):
                        st.image(img_path, use_container_width=True)
                        with open(img_path, "rb") as f:
                            st.download_button("💾 Save", f, file_name=file, key=f"dl_{file}")

        # Continuous Loop
        while True:
            for file in files:
                video_placeholder.image(f"{IMAGE_DIR}/{file}", use_container_width=True)
                label_placeholder.markdown(f"**Looping Frame (ET):** {file.replace('.jpg', '').replace('_', ' ')}")
                time.sleep(0.1)
    else:
        st.info("Archive is empty. GitHub Actions will save the first image soon.")
