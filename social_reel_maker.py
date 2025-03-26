import os
import cv2  # Added this import
import numpy as np
from datetime import datetime
from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip
from moviepy.video.fx.all import resize, crop, fadein, fadeout
from PIL import Image, ImageDraw, ImageFont

class PodcastEnhancer:
    def __init__(self):
        # Initialize paths
        self.input_file = "raw_video.mp4"
        self.output_dir = "enhanced_shorts"
        self.target_resolution = (1080, 1920)  # Shorts format
        
        # Load fonts
        try:
            self.title_font = ImageFont.truetype("arial.ttf", 90)
            self.subtitle_font = ImageFont.truetype("arial.ttf", 60)
        except:
            self.title_font = ImageFont.load_default()
            self.subtitle_font = ImageFont.load_default()
        
        # Create directories
        os.makedirs(self.output_dir, exist_ok=True)

    def _add_professional_overlay(self, clip):
        """Add clean title and subtle gradient overlay"""
        print("🎨 Adding professional overlay...")
        
        # Create a semi-transparent gradient overlay
        overlay = ColorClip(
            size=clip.size,
            color=[0, 0, 0],
            col=lambda t: [0, 0, 0, int(100 * (0.5 + 0.5 * np.sin(t)))]  # Subtle pulsing effect
        ).set_duration(clip.duration)
        
        return CompositeVideoClip([clip, overlay])

    def _enhance_quality(self, clip):
        """Apply subtle quality enhancements"""
        print("✨ Enhancing video quality...")
        
        def enhance_frame(get_frame, t):
            frame = get_frame(t)
            
            # Convert to float for processing
            frame = frame.astype('float32') / 255.0
            
            # Contrast adjustment
            frame = 0.5 + (frame - 0.5) * 1.1
            
            # Convert to HSV for saturation adjustment
            hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
            hsv[:,:,1] = np.clip(hsv[:,:,1] * 1.15, 0, 1)  # Slight saturation boost
            
            # Convert back to RGB
            frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
            
            return np.clip(frame * 255, 0, 255).astype('uint8')
        
        return clip.fl(enhance_frame)

    def _resize_for_shorts(self, clip):
        """Convert to vertical shorts format with smart cropping"""
        print("🖼 Formatting for Shorts...")
        w, h = clip.size
        target_w, target_h = self.target_resolution
        
        if w/h > 0.5625:  # If wider than 9:16
            new_w = int(h * 0.5625)
            x_center = w/2
            cropped = crop(clip, x_center-new_w/2, 0, x_center+new_w/2, h)
            return resize(cropped, (target_w, target_h))
        
        return clip.resize(height=target_h).set_position(('center', 'center'))

    def process_video(self):
        """Main processing pipeline"""
        if not os.path.exists(self.input_file):
            print(f"❌ Error: Input file '{self.input_file}' not found!")
            return False
            
        try:
            print("\n🎬 Loading video...")
            clip = VideoFileClip(self.input_file)
            print(f"📏 Original size: {clip.size[0]}x{clip.size[1]}")
            print(f"⏱ Duration: {clip.duration:.1f}s")
            
            # Enhance video quality
            enhanced_clip = self._enhance_quality(clip)
            
            # Convert to vertical format
            vertical_clip = self._resize_for_shorts(enhanced_clip)
            
            # Add professional overlay
            final_clip = self._add_professional_overlay(vertical_clip)
            
            # Add subtle fade in/out
            final_clip = final_clip.fx(fadein, 0.5).fx(fadeout, 0.5)
            
            # Export with high quality settings
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = os.path.join(self.output_dir, f"podcast_short_{timestamp}.mp4")
            print(f"\n💾 Saving to: {output_path}")
            final_clip.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                threads=4,
                fps=clip.fps,
                preset="slow",  # Better quality encoding
                bitrate="15M",  # Higher bitrate for quality
                audio_bitrate="192k"
            )
            
            clip.close()
            print("\n✅ Enhancement complete!")
            print(f"📁 Saved to: {os.path.abspath(output_path)}")
            return True
            
        except Exception as e:
            print(f"\n❌ Processing failed: {str(e)}")
            return False

if __name__ == "__main__":
    print("\n" + "="*50)
    print("       PODCAST SHORT ENHANCER PRO")
    print("="*50)
    print("Professional quality enhancement for podcast shorts")
    print("Creates perfect 9:16 vertical videos ready for platforms\n")
    
    enhancer = PodcastEnhancer()
    success = enhancer.process_video()
    
    if success:
        print("\n🔥 Ready to post! 🔥")
    else:
        print("\nPlease check the error messages above")
    
    input("\nPress Enter to exit...")