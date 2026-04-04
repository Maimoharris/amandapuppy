# Video Optimization Guide

## Overview
This guide explains the video optimization improvements made to the hero section and how to further optimize video loading performance.

## Current Implementation

### 1. **Thumbnail Fallback**
- The hero video now displays a thumbnail image while the video is loading
- The thumbnail is shown via the `poster` attribute on the `<video>` element
- A fallback gradient is displayed if no thumbnail is available
- The `hero-video-loading` div serves as a visual placeholder with a spinning loader

### 2. **Video Loading Optimizations**
- `preload="metadata"` - Only loads video metadata initially, reducing bandwidth usage
- `poster` attribute - Displays thumbnail immediately while video buffers
- Loading spinner shows during initial load and buffering
- JavaScript event handlers manage the loading state

### 3. **Performance Features**
- **Visibility Handling** - Video pauses when the tab is not visible (saves bandwidth)
- **Buffering Management** - Loading spinner reappears if video needs to buffer
- **Error Handling** - Graceful fallback if video fails to load
- **Mobile Optimization** - Respects browser autoplay policies

## JavaScript Optimization Events

The video uses these events for optimal performance:

- `loadedmetadata` - Metadata loaded, initiates playback
- `play` - Video started playing, hides loading spinner
- `waiting` - Video paused to buffer, shows loading spinner
- `canplay` - Video has enough data to play, hides spinner
- `visibilitychange` - Pauses video when tab is not active
- `error` - Handles video load failures

## Video Format Recommendations

### Current Format: MP4
- **Pros**: Wide browser support, good quality
- **Cons**: Larger file size

### Recommended: WebM (VP9/VP8)
- **Pros**: Better compression (30-50% smaller), better quality/size ratio
- **Cons**: Limited support in Safari and older browsers

### Recommended: VP9 (H.265 Alternative)
- **Pros**: Excellent compression, modern format
- **Cons**: Limited support, longer encoding time

## Converting Videos to Multiple Formats

### Prerequisites
```bash
pip install ffmpeg-python
# or install ffmpeg directly
brew install ffmpeg  # macOS
sudo apt-get install ffmpeg  # Ubuntu/Debian
```

### Conversion Script

Create a file `convert_hero_videos.py` in your project root:

```python
#!/usr/bin/env python
import os
import subprocess
from pathlib import Path

def convert_video(input_path, output_format='webm'):
    """
    Convert video to specified format optimized for web
    
    Args:
        input_path: Path to video file
        output_format: 'webm', 'mp4-optimized', or 'all'
    """
    input_file = Path(input_path)
    output_dir = input_file.parent
    base_name = input_file.stem
    
    conversions = {
        'webm': {
            'extension': '.webm',
            'codec': 'libvpx-vp9',
            'crf': 30,  # Quality (0-63, lower is better, 30 is good for web)
            'preset': 'slower',  # slow, slower for better compression
        },
        'mp4-optimized': {
            'extension': '.mp4',
            'codec': 'h264',
            'crf': 23,  # Quality (0-51)
            'preset': 'faster',
        }
    }
    
    formats = [output_format] if output_format != 'all' else conversions.keys()
    
    for fmt in formats:
        if fmt not in conversions:
            continue
            
        config = conversions[fmt]
        output_file = output_dir / f"{base_name}{config['extension']}"
        
        cmd = [
            'ffmpeg',
            '-i', str(input_file),
            '-c:v', config['codec'],
            '-crf', str(config['crf']),
            '-preset', config['preset'],
            '-c:a', 'aac',
            '-b:a', '128k',
            '-y',  # Overwrite output
            str(output_file)
        ]
        
        print(f"Converting {input_file.name} to {fmt}...")
        print(f"Command: {' '.join(cmd)}")
        
        try:
            subprocess.run(cmd, check=True)
            file_size_mb = output_file.stat().st_size / (1024 * 1024)
            print(f"✓ Created: {output_file.name} ({file_size_mb:.2f} MB)")
        except subprocess.CalledProcessError as e:
            print(f"✗ Conversion failed: {e}")

if __name__ == '__main__':
    # Convert your hero video
    hero_video_path = 'media/hero_videos/Dog_Hero_Final_mn4S7zC.mp4'
    
    if os.path.exists(hero_video_path):
        # Create WebM version (best compression)
        convert_video(hero_video_path, 'webm')
        # Optionally keep MP4 as fallback
        # convert_video(hero_video_path, 'all')
    else:
        print(f"Video not found at: {hero_video_path}")
```

Run the conversion:
```bash
python convert_hero_videos.py
```

### Manual FFmpeg Commands

**Convert to WebM (VP9) - Best Compression:**
```bash
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 30 -preset slower -c:a libopus -b:a 128k output.webm
```

**Convert to Optimized MP4:**
```bash
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset fast -c:a aac -b:a 128k output.mp4
```

**Generate Thumbnail:**
```bash
ffmpeg -i input.mp4 -ss 00:00:02 -vf "scale=1920:1080" -vframes 1 thumbnail.jpg
ffmpeg -i input.mp4 -ss 00:00:02 -vf "scale=1920:1080" -vframes 1 thumbnail.webp
```

## Updating Video in Admin

1. Go to Django Admin (`/admin/`)
2. Navigate to **Hero Videos**
3. Upload or select your video:
   - Keep `Dog_Hero_Final_mn4S7zC.mp4` as primary (for fallback)
   - Add converted `webm` version if available
4. Upload the **Thumbnail** image
5. Save

## HTML Implementation

The hero video now includes:

```html
<video 
    id="heroVideo"
    class="hero-video" 
    autoplay 
    muted 
    loop 
    playsinline 
    preload="metadata"
    poster="{{ hero_videos.0.thumbnail.url }}"
>
    <source src="{{ hero_videos.0.video_file.url }}" type="video/mp4">
    <!-- Optional: Add WebM for better compression -->
    <!-- <source src="{{ hero_videos.0.video_file.url|add:'.webm' }}" type="video/webm"> -->
</video>
```

## Performance Metrics

Expected improvements with these optimizations:

| Metric | Before | After |
|--------|--------|-------|
| Initial Load | Show blank | Show thumbnail immediately |
| Buffering UX | Blank screen | Thumbnail + spinner |
| Mobile Experience | Poor (autoplay may fail) | Good (respects policies) |
| Tab Inactive | Keeps loading | Paused (saves bandwidth) |

### File Size Comparison
- Original MP4: ~15-20 MB
- WebM (VP9): ~6-8 MB (50-60% reduction)
- Optimized MP4: ~10-12 MB (35-40% reduction)

## Browser Support

| Format | Chrome | Firefox | Safari | Edge |
|--------|--------|---------|--------|------|
| MP4    | ✓      | ✓       | ✓      | ✓    |
| WebM   | ✓      | ✓       | ✗      | ✓    |

**Recommendation**: Use WebM as primary with MP4 fallback for full compatibility.

## Recommended Multi-Source Setup

```html
<video id="heroVideo" ... poster="thumbnail.jpg">
    <source src="hero.webm" type="video/webm">
    <source src="hero.mp4" type="video/mp4">
</video>
```

This ensures:
- Modern browsers load smallest WebM format
- Safari and older browsers fallback to MP4
- All browsers get good performance

## Testing Performance

Use these tools to verify improvements:

1. **Network Tab in DevTools**
   - Check which video format downloads
   - Monitor bandwidth usage
   - Verify preload="metadata" behavior

2. **Lighthouse Audit**
   - Run Lighthouse in Chrome DevTools
   - Check First Contentful Paint (FCP)
   - Monitor Largest Contentful Paint (LCP)

3. **Chrome Speed Insights**
   - https://pagespeed.web.dev/
   - Check real-world Core Web Vitals

## Troubleshooting

### Thumbnail not showing
- Ensure `Hero Video` has a thumbnail image uploaded
- Check the thumbnail URL is accessible
- Verify CSS z-index values are correct

### Video not autoplaying
- Check browser autoplay policies (requires `muted` attribute)
- Check browser console for errors
- Test in incognito mode (no extensions interfering)

### Video buffering frequently
- Consider converting to WebM format (smaller file)
- Check video quality/bitrate in encoding
- Monitor network conditions

### Spinner not disappearing
- Check browser console for JS errors
- Verify video loads successfully
- Test with different video formats

## Next Steps

1. **Generate thumbnail** from the hero video (if not already done)
2. **Convert to WebM** for better compression (optional but recommended)
3. **Update media** in Django Admin
4. **Test** on mobile devices and slow networks
5. **Monitor** performance metrics

---

For more info on video format optimization:
- [MDN Video Element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/video)
- [WebM Format](https://www.webmproject.org/)
- [VP9 Codec](https://en.wikipedia.org/wiki/VP9)
