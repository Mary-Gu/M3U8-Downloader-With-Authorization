# M3U8-Downloader-With-Authorization

## Overview
This is a Python-based GUI tool for downloading videos from M3U8 URLs, including those with authentication parameters after `?`. It uses `ffmpeg` to handle the downloading process and ensures that the entire URL, including query parameters, is preserved for proper access.

## Features
- Supports downloading videos from M3U8 links, even when they contain authentication tokens or other parameters.
- Provides a user-friendly GUI using `tkinter`.
- Allows users to specify a custom save location for the downloaded video.
- Uses `ffmpeg` for efficient video downloading and conversion.
- Implements multi-threading to keep the GUI responsive during downloads.
- Displays a real-time loading animation while downloading.
- Allows users to choose different video quality levels (High, Medium, Low) to control file size and download speed.
- Optimized for high DPI screens (Windows compatibility).

## Requirements
- Python 3.x
- `ffmpeg` installed and available in the system PATH

## Installation
1. Install Python 3 if you haven’t already: [Download Python](https://www.python.org/downloads/)
2. Install `ffmpeg`:
   - Windows: Download from [FFmpeg official site](https://ffmpeg.org/download.html) and add it to system PATH.
   - macOS (via Homebrew): `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg` (Ubuntu/Debian) or `sudo dnf install ffmpeg` (Fedora)

## Usage
1. Run the Python script:
   ```sh
   python m3u8_video_downloader.py
   ```
2. Enter the full M3U8 URL, including any parameters after `?`.
3. Select a location to save the downloaded video.
4. Choose the preferred video quality:
   - **High Quality (Original Size)**: Directly copies without re-encoding.
   - **Medium Quality (Smaller File Size)**: Uses H.264 encoding with moderate compression.
   - **Low Quality (Smallest File Size)**: Uses H.264 encoding with higher compression for minimal storage.
5. Click the "Download" button.
6. A dynamic loading animation will indicate the download progress.
7. Once complete, a success message will appear.

## Notes
- Ensure the M3U8 URL contains all necessary authentication tokens if required.
- If the download fails, check that `ffmpeg` is correctly installed and that the URL is accessible.
- The multi-threaded download process ensures that the GUI remains responsive while downloading.

## License
This project is open-source and free to use. Modify it as needed!

