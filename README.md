# M3U8-Downloader-With-Authorization

## Overview
This is a Python-based GUI tool for downloading videos from M3U8 URLs, including those with authentication parameters after `?`. It uses `ffmpeg` to handle the downloading process and ensures that the entire URL, including query parameters, is preserved for proper access.

## What is M3U8?
M3U8 is a file format used for streaming videos over the internet. It contains a list of media segments (small video files) that are played sequentially to form a complete video. Streaming services use M3U8 to provide adaptive bitrate streaming, where different video qualities are available based on the viewer's internet speed.

However, since M3U8 only provides a playlist of video chunks rather than a single file, directly downloading an M3U8 link will not give you a playable video. This tool uses `ffmpeg` to download and merge these chunks into a single MP4 file.

## Features
- **Supports authentication parameters**: Can download videos even when the M3U8 link contains authentication tokens or query parameters.
- **User-friendly GUI**: Built with `tkinter` for easy interaction.
- **Custom save location**: Choose where to save the downloaded video.
- **Multi-threading support**: Keeps the interface responsive while downloading videos.
- **Real-time download animation**: Shows progress with a dynamic loading indicator.
- **Video quality options**:
  - **High Quality (Original Size)**: No re-encoding, full resolution.
  - **Medium Quality (Smaller File Size)**: Compressed with H.264 for a balance of quality and size.
  - **Low Quality (Smallest File Size)**: Highly compressed for minimal storage.
- **Optimized for high DPI screens**: Especially useful for Windows users with high-resolution displays.

## Requirements
- **Python 3.x**
- **FFmpeg** installed and available in the system PATH

## Installation
1. **Install Python 3**: [Download Python](https://www.python.org/downloads/)
2. **Install FFmpeg**:
   - **Windows**: Download from [FFmpeg official site](https://ffmpeg.org/download.html) and add it to system PATH.
   - **macOS (via Homebrew)**: Run `brew install ffmpeg`
   - **Linux**:
     - Debian/Ubuntu: `sudo apt install ffmpeg`
     - Fedora: `sudo dnf install ffmpeg`

## How It Works
1. **Launch the script**:
   ```sh
   python m3u8_video_downloader.py
   ```
2. **Enter the M3U8 URL**, including any parameters after `?` (e.g., authentication tokens). 
   - The script provides an example URL: `https://example.com/video.m3u8?parse1=1&parse2=2etc`. This illustrates how query parameters (`?parse1=1&parse2=2etc`) must be included in order to access protected streams.
   - Many M3U8 downloaders online fail to support query parameters, making this tool unique in its ability to handle them properly.
3. **Choose where to save the video**.
4. **Select video quality**:
   - **High Quality**: No compression, original size.
   - **Medium Quality**: Compressed using H.264 codec.
   - **Low Quality**: Highly compressed for minimum file size.
5. **Click the "Download" button**.
6. **What happens next?**
   - The script starts a background thread to download the video.
   - A loading animation appears to indicate progress.
   - `ffmpeg` processes the M3U8 file, downloads video segments, and merges them into an MP4 file.
   - Once complete, a success message appears.

## Common Issues and Solutions
- **The download fails immediately**:
  - Check if the M3U8 URL is correct and includes all required authentication parameters.
  - Test the URL in a web browser to see if it plays the video.
  - Ensure `ffmpeg` is installed and correctly added to the system PATH.

- **The downloaded video has no audio**:
  - Some M3U8 files have separate audio tracks. Ensure your URL includes both video and audio.
  - Modify the `ffmpeg` command to manually merge audio if necessary.

- **The video is slow or laggy**:
  - Try selecting "High Quality" to avoid re-encoding.
  - Check your computer’s performance during the download process.

## License
This project is open-source and free to use. Modify it as needed!

## Final Thoughts
This tool is ideal for downloading M3U8 videos quickly and efficiently while keeping the interface responsive. It is particularly useful for beginners who want a simple way to save streaming videos to their local storage without dealing with complex command-line options in `ffmpeg`.
