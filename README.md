# M3U8 Downloader with Authorization Support

A powerful Python-based GUI tool for downloading videos from M3U8 playlists — including authenticated streams with query parameters. Built with tkinter and powered by ffmpeg, this tool supports parallel downloading, automatic merging, and quality control.

## 🔍 What is M3U8?

M3U8 is a playlist format used for HTTP Live Streaming (HLS). It contains links to video segments (usually .ts files) that are streamed in sequence. Simply downloading the M3U8 file won't give you a complete video — you must fetch, order, and combine all segments.

This tool automates that process and outputs a playable .mp4 file.

## ✨ Features

- ✅ Supports Authenticated M3U8 URLs: Fully preserves query parameters (after ?) for token-based access.
- 🎛️ User-Friendly GUI: Simple and clean interface built with tkinter.
- 💾 Custom Save Path and Filename: Auto-fills name from URL, with .mp4 extension appended.
- ⚡ Multi-threaded Segment Download: Downloads segments in parallel for higher speed.
- 🧠 Parallel Merge with Divide-and-Conquer: Fast and efficient merging of .ts segments.
- 🔁 Retry on Failure: Segments will retry download up to 5 times automatically.
- 🎚️ Video Quality Selection:
  - High – Original resolution, no re-encoding.
  - Medium – Compressed using libx264 at crf=23.
  - Low – Highly compressed, smaller file size.
- 🖥️ HiDPI Display Support: Looks great on high-resolution displays (Windows-compatible).

## 🧰 Requirements

- Python 3.x
- ffmpeg installed and available in system PATH

## 🚀 Installation

1. Install Python 3.x: https://www.python.org/downloads/
2. Install FFmpeg:
   - Windows: Download from https://ffmpeg.org/download.html and add to PATH
   - macOS: brew install ffmpeg
   - Ubuntu/Debian: sudo apt install ffmpeg
   - Fedora: sudo dnf install ffmpeg

## ▶️ How to Use

Step 1: Launch the program
```bash
    python m3u8_video_downloader.py
```
Step 2: Paste the full M3U8 URL (including authentication parameters if any), for example:

    https://example.com/video.m3u8?token=abc123&expires=1680000000

Step 3: Choose the save location and filename

Step 4: Select the video quality:
- High Quality (Original size)
- Medium Quality (Balanced compression)
- Low Quality (Highly compressed)

Step 5: Adjust download thread count (optional)

Step 6: Click the "Download" button

The tool will:
- Fetch and parse the M3U8 playlist
- Download all .ts video segments using multithreading
- Retry failed segments automatically (up to 5 times)
- Merge all segments using ffmpeg with multi-stage parallelism
- Transcode the video depending on quality selection
- Save the result as an MP4 file

## 🛠 Troubleshooting

### ❌ Download fails immediately
- Ensure the M3U8 URL is complete and includes all required parameters.
- Try opening the URL in a browser to confirm it's valid.
- Make sure ffmpeg is installed and included in the system PATH.

### 🔇 No audio in the output
- Some streams provide video and audio as separate playlists.
- Use the full master playlist instead, or manually merge audio using ffmpeg.

### 🐢 Video playback is laggy
- Use "High Quality" to skip transcoding.
- Make sure your system has enough CPU resources during merging.

## 🪪 License

This project is open-source and free to use under the MIT License. Modify and redistribute freely.

## ❤️ Final Thoughts

This tool is ideal for anyone who needs to download authenticated M3U8 videos with full control, especially when query parameters are involved. It simplifies complex ffmpeg operations into a GUI-based workflow for faster, friendlier access.

---

✨ Built with threads, tkinter, and ffmpeg.
