import streamlit as st
from video_processor import generate_clips
import os
import time
import tempfile

# Configure
st.set_page_config(layout="wide")
st.title("🎬 ViralClip Pro")

def safe_remove(filepath, max_retries=3, delay=1):
    """Safely remove files with retries"""
    for _ in range(max_retries):
        try:
            if filepath and os.path.exists(filepath):
                os.remove(filepath)
                return True
        except (PermissionError, OSError):
            time.sleep(delay)
    return False

# File Upload
uploaded_file = st.file_uploader("Upload Video", type=["mp4", "mov"])
output_path = None

if uploaded_file:
    # Use temp directory for all files
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, f"upload_{uploaded_file.name}")
    
    try:
        # Save uploaded file
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.video(temp_path)
        
        if st.button("✨ Generate Viral Clip"):
            with st.spinner("Adding TikTok magic..."):
                try:
                    output_path = generate_clips(temp_path)
                    st.success("Processing complete!")
                    st.video(output_path)
                    
                    # Download button
                    with open(output_path, "rb") as f:
                        st.download_button(
                            "Download Clip", 
                            f, 
                            file_name="viral_clip.mp4",
                            key="download_button"
                        )
                    
                except Exception as e:
                    st.error(f"Processing error: {str(e)}")
                    st.exception(e)  # Shows full traceback in debug mode
                    
    finally:
        # Clean up all files
        safe_remove(temp_path)
        if output_path and os.path.exists(output_path):
            safe_remove(output_path)