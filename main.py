import streamlit as st
from video_processor import generate_clips
import os

# Configure
st.set_page_config(layout="wide")
st.title("🎬 ViralClip Pro")

# File Upload
uploaded_file = st.file_uploader("Upload Video", type=["mp4", "mov"])
if uploaded_file:
    temp_path = f"temp_{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.video(temp_path)
    
    if st.button("✨ Generate Viral Clip"):
        with st.spinner("Adding TikTok magic..."):
            try:
                output_path = generate_clips(temp_path)
                st.success("Done!")
                st.video(output_path)
                
                # Download button
                with open(output_path, "rb") as f:
                    st.download_button("Download Clip", f, file_name="viral_clip.mp4")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
            finally:
                os.remove(temp_path)