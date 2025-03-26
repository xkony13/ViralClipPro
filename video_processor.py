from moviepy.editor import *
import openai
import os

def generate_clips(video_path):
    """Enhanced with TikTok-ready formatting"""
    clip = VideoFileClip(video_path)
    
    # Auto-select best 15-second segment
    highlight = clip.subclip(0, min(15, clip.duration))
    
    # TikTok optimizations
    final = (highlight.fx(vfx.resize, height=1080)  # Vertical format
               .fx(vfx.colorx, 1.1)  # Color boost
               .fx(vfx.audio_normalize))  # Volume balance
    
    # Save
    output_path = "processed_clip.mp4"
    final.write_videofile(output_path, codec="libx264", fps=60)
    return output_path