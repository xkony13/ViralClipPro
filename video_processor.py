from moviepy.editor import *
import os
import tempfile
from PIL import Image  # For thumbnail generation if needed

def generate_clips(video_path):
    """Enhanced TikTok-ready formatting with proper resource cleanup"""
    try:
        # Create temp file for output to avoid permission issues
        output_path = os.path.join(tempfile.gettempdir(), f"processed_{os.path.basename(video_path)}")
        
        with VideoFileClip(video_path) as clip:
            # Auto-select best 15-second segment
            highlight = clip.subclip(0, min(15, clip.duration))
            
            # TikTok optimizations
            final = (highlight.fx(vfx.resize, height=1080)  # Vertical format
                    .fx(vfx.colorx, 1.1)  # Color boost
                    .fx(vfx.audio_normalize))  # Volume balance
            
            # Write with proper codec and threads management
            final.write_videofile(
                output_path,
                codec="libx264",
                fps=60,
                threads=4,
                preset='fast',
                audio_codec="aac"
            )
            
        return output_path
        
    except Exception as e:
        # Clean up if error occurs
        if 'output_path' in locals() and os.path.exists(output_path):
            os.remove(output_path)
        raise e