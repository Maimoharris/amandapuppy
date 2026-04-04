#!/usr/bin/env python
"""
Video Format Converter for Hero Videos
Converts videos to WebM (VP9) and MP4 formats optimized for web delivery
"""

import os
import subprocess
import sys
from pathlib import Path


class VideoConverter:
    """Convert videos to optimized web formats"""
    
    FORMATS = {
        'webm': {
            'extension': '.webm',
            'codec': 'libvpx-vp9',
            'crf': 30,  # 0-63, lower is better, 30 is good balance
            'preset': 'slower',  # slow, slower for better compression
            'audio_codec': 'libopus',
            'audio_bitrate': '128k',
        },
        'mp4-optimized': {
            'extension': '.mp4',
            'codec': 'libx264',
            'crf': 23,  # 0-51, lower is better, 23 is default
            'preset': 'fast',
            'audio_codec': 'aac',
            'audio_bitrate': '128k',
        }
    }
    
    @staticmethod
    def check_ffmpeg():
        """Check if ffmpeg is installed"""
        try:
            subprocess.run(['ffmpeg', '-version'], 
                         capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    @staticmethod
    def get_video_info(video_path):
        """Get video information using ffprobe"""
        try:
            cmd = [
                'ffprobe', '-v', 'error',
                '-show_entries', 'format=duration,size',
                '-of', 'default=noprint_wrappers=1:nokey=1:noprint_names=1',
                str(video_path)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            lines = result.stdout.strip().split('\n')
            duration = float(lines[0]) if len(lines) > 0 else 0
            size = int(lines[1]) if len(lines) > 1 else 0
            
            return {
                'duration': duration,
                'size_mb': size / (1024 * 1024),
                'path': video_path
            }
        except Exception as e:
            print(f"Could not get video info: {e}")
            return None
    
    @classmethod
    def convert(cls, input_path, output_format='webm'):
        """
        Convert video to specified format
        
        Args:
            input_path: Path to input video
            output_format: 'webm', 'mp4-optimized', or 'all'
        
        Returns:
            dict with conversion results
        """
        if not cls.check_ffmpeg():
            return {
                'success': False,
                'error': 'ffmpeg not found. Install it with: brew install ffmpeg'
            }
        
        input_file = Path(input_path)
        if not input_file.exists():
            return {
                'success': False,
                'error': f'Input file not found: {input_path}'
            }
        
        output_dir = input_file.parent
        base_name = input_file.stem
        
        # Get original video info
        video_info = cls.get_video_info(input_file)
        if video_info:
            print(f"\nOriginal Video: {input_file.name}")
            print(f"  Duration: {video_info['duration']:.1f}s")
            print(f"  Size: {video_info['size_mb']:.2f} MB")
        
        formats = [output_format] if output_format != 'all' else cls.FORMATS.keys()
        results = {'success': True, 'conversions': {}}
        
        for fmt in formats:
            if fmt not in cls.FORMATS:
                continue
            
            config = cls.FORMATS[fmt]
            output_file = output_dir / f"{base_name}{config['extension']}"
            
            # Build ffmpeg command
            cmd = [
                'ffmpeg',
                '-i', str(input_file),
                '-c:v', config['codec'],
                '-crf', str(config['crf']),
                '-preset', config['preset'],
                '-c:a', config['audio_codec'],
                '-b:a', config['audio_bitrate'],
                '-movflags', '+faststart',  # Enable streaming in MP4
                '-y',  # Overwrite output
                str(output_file)
            ]
            
            print(f"\n{'='*60}")
            print(f"Converting to {fmt.upper()}...")
            print(f"Output: {output_file.name}")
            print(f"{'='*60}")
            
            try:
                subprocess.run(cmd, check=True)
                output_size = output_file.stat().st_size / (1024 * 1024)
                
                if video_info:
                    compression = ((video_info['size_mb'] - output_size) / 
                                 video_info['size_mb'] * 100)
                    print(f"✓ Success!")
                    print(f"  Output Size: {output_size:.2f} MB")
                    print(f"  Compression: {compression:.1f}% reduction")
                else:
                    print(f"✓ Success! Created: {output_file.name}")
                
                results['conversions'][fmt] = {
                    'success': True,
                    'output': str(output_file),
                    'size_mb': output_size
                }
                
            except subprocess.CalledProcessError as e:
                print(f"✗ Conversion failed")
                results['success'] = False
                results['conversions'][fmt] = {'success': False, 'error': str(e)}
        
        return results
    
    @staticmethod
    def generate_thumbnail(video_path, timestamp='00:00:02', 
                          width=1920, height=1080):
        """
        Generate thumbnail from video
        
        Args:
            video_path: Path to video
            timestamp: Time in video to extract (HH:MM:SS)
            width: Thumbnail width
            height: Thumbnail height
        """
        input_file = Path(video_path)
        output_file = input_file.parent / f"{input_file.stem}_thumbnail.jpg"
        
        cmd = [
            'ffmpeg',
            '-i', str(input_file),
            '-ss', timestamp,
            '-vf', f'scale={width}:{height}',
            '-vframes', '1',
            '-y',
            str(output_file)
        ]
        
        print(f"\nGenerating thumbnail from {input_file.name}...")
        print(f"Timestamp: {timestamp}")
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✓ Thumbnail created: {output_file.name}")
            return str(output_file)
        except subprocess.CalledProcessError as e:
            print(f"✗ Thumbnail generation failed: {e}")
            return None


def main():
    """Main entry point"""
    
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║            Video Format Converter for Web                  ║
    ║    Optimize hero videos for faster loading on your site    ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # Check if ffmpeg is installed
    if not VideoConverter.check_ffmpeg():
        print("❌ ffmpeg is not installed!")
        print("\nInstall it with:")
        print("  - macOS: brew install ffmpeg")
        print("  - Ubuntu: sudo apt-get install ffmpeg")
        print("  - Windows: Download from https://ffmpeg.org/download.html")
        sys.exit(1)
    
    print("✓ ffmpeg is installed\n")
    
    # Get hero video path
    default_video = 'media/hero_videos/Dog_Hero_Final_mn4S7zC.mp4'
    
    print(f"Default video path: {default_video}")
    video_path = input(f"Enter video path (or press Enter for default): ").strip()
    video_path = video_path or default_video
    
    # Check if file exists
    if not Path(video_path).exists():
        print(f"❌ File not found: {video_path}")
        sys.exit(1)
    
    print("\nConversion options:")
    print("  1. WebM (VP9) - Best compression, ~50% smaller")
    print("  2. MP4 (H.264) - High compatibility, ~35% smaller")
    print("  3. Both WebM and MP4")
    print("  4. Just generate thumbnail")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == '1':
        result = VideoConverter.convert(video_path, 'webm')
    elif choice == '2':
        result = VideoConverter.convert(video_path, 'mp4-optimized')
    elif choice == '3':
        result = VideoConverter.convert(video_path, 'all')
    elif choice == '4':
        timestamp = input("Enter thumbnail timestamp (HH:MM:SS) [default: 00:00:02]: ").strip()
        timestamp = timestamp or '00:00:02'
        VideoConverter.generate_thumbnail(video_path, timestamp)
        return
    else:
        print("Invalid option")
        sys.exit(1)
    
    if result.get('success'):
        print(f"\n{'='*60}")
        print("✓ Conversion complete!")
        print(f"{'='*60}")
        
        # Also generate thumbnail
        generate_thumb = input("\nGenerate thumbnail too? (y/n): ").strip().lower()
        if generate_thumb == 'y':
            VideoConverter.generate_thumbnail(video_path)
    else:
        print(f"\n❌ Conversion failed: {result.get('error')}")
        sys.exit(1)
    
    print("""
    
Next steps:
1. Upload the new video files to Django Admin
2. Update the HeroVideo model with the new files
3. Test on mobile devices with slow networks
4. Monitor performance metrics

For more info, see VIDEO_OPTIMIZATION_GUIDE.md
    """)


if __name__ == '__main__':
    main()
