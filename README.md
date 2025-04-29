# Video Compressor

## Overview
Video Compressor is a Python-based GUI application that allows users to compress videos using FFmpeg. It provides options to adjust the CRF value, speed multiplier, remove audio, and set start/end times for clipping videos. The program uses FFmpeg to perform the compression, offering a user-friendly interface built with Tkinter.

## Features
- Select input video and output directory.
- Customize output file name.
- Adjust video quality with CRF (Constant Rate Factor).
- Modify playback speed with a speed multiplier.
- Option to remove audio from the video.
- Clip videos by specifying start and end times.
- Progress bar and log output for compression status.

## Requirements
This program requires the following:

### 1. Python
- **Version**: Python 3.8 or higher
- The program uses the `tkinter` library for the GUI, which is included with standard Python installations. If `tkinter` is not available, you may need to install it:
  - On Debian/Ubuntu: `sudo apt-get install python3-tk`
  - On macOS (with Homebrew): `brew install python-tk`

### 2. FFmpeg
- **FFmpeg** is required to perform video compression. This program does **not** include FFmpeg; you must install it separately.
- **Download FFmpeg**:
  - Visit the official FFmpeg website: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
  - Follow the instructions for your operating system to download and install FFmpeg.
  - Ensure FFmpeg is added to your system's PATH so the program can find it.
- **FFmpeg License**: FFmpeg is licensed under the GNU General Public License (GPL) version 2 or later, or the GNU Lesser General Public License (LGPL) depending on its configuration. This program uses FFmpeg with GPL components (e.g., `libx264`), so FFmpeg is GPL-licensed in this context. You must comply with FFmpeg's license terms when using it. You can find FFmpeg's source code and license details at: [https://ffmpeg.org](https://ffmpeg.org).

## Installation
1. **Download the Program**:
   - Clone or download this repository to your local machine.
   - Alternatively, download the `ffmpeg_compressor.py` file directly.

2. **Install Python**:
   - Ensure Python 3.8 or higher is installed on your system.
   - Verify by running: `python3 --version`

3. **Install FFmpeg**:
   - Follow the instructions above to install FFmpeg and ensure it's accessible in your PATH.
   - Verify FFmpeg installation by running: `ffmpeg -version`

## Usage
1. **Run the Program**:
   - Open a terminal or command prompt.
   - Navigate to the directory containing `ffmpeg_compressor.py`.
   - Run the program with: `python3 ffmpeg_compressor.py`

2. **Interface Overview**:
   - **Input Video**: Click "Browse" to select a video file (e.g., MP4, AVI, MKV, MOV).
   - **Output Directory**: Click "Browse" to choose where to save the compressed video.
   - **Output File Name**: Specify the name of the compressed video (default: `<input>_compress.mp4`).
   - **CRF Value**: Set the Constant Rate Factor (0-51, lower values = better quality, default: 23).
   - **Speed Multiplier**: Adjust playback speed (e.g., 2.0 for double speed, default: 1.0).
   - **Remove Audio**: Check this box to remove audio from the output video.
   - **Start/End Time**: Optionally clip the video by specifying start and end times in `HH:MM:SS` format.
   - **Compress Button**: Start the compression process.
   - **Cancel Button**: Stop an ongoing compression.
   - **Progress Bar**: Displays compression progress.
   - **Log Output**: Shows FFmpeg logs and status messages.

3. **Example**:
   - Input Video: `movie.mp4`
   - Output Directory: `/path/to/output/`
   - Output File Name: `movie_compressed.mp4`
   - CRF Value: `28`
   - Speed Multiplier: `1.5`
   - Remove Audio: Unchecked
   - Start Time: `00:01:00`
   - End Time: `00:02:00`
   - Click "Compress" to generate a 1-minute clip of `movie.mp4` at 1.5x speed, saved as `/path/to/output/movie_compressed.mp4`.

## Building the Program with PyInstaller
You can use PyInstaller to package the `ffmpeg_compressor.py` script into a standalone executable file, so users don't need to install Python or dependencies to run the program. Follow the steps below:

### 1. Install PyInstaller
First, ensure you have PyInstaller installed. You can install it using pip:
```bash
pip install pyinstaller
```
Verify the installation by running:
```bash
pyinstaller --version
```

### 2. Package the Program
Navigate to the directory containing `ffmpeg_compressor.py` and run the following command to package the program into a single executable file:

#### For macOS: 
```sh
pyinstaller -F -i "appicon.icns" --name "Video Compressor" ffmpeg_compressor.py
```
#### For Windows: 
```sh
python3 gen_icon.py
pyinstaller -F -w -i "appicon.ico" --name "Video Compressor" ffmpeg_compressor.py
```

## Notes
- **FFmpeg Dependency**: If FFmpeg is not installed or not in your PATH, the program will display an error: "FFmpeg not found." Ensure FFmpeg is properly installed.
- **Time Format**: Start and end times must be in `HH:MM:SS` format (e.g., `00:01:30` for 1 minute 30 seconds).
- **Video Duration**: If FFmpeg's `ffprobe` is available, the program will calculate the video duration for accurate progress tracking. If `ffprobe` is missing, the progress bar may not work.
- **H.264 Patent**: This program uses `libx264` (H.264 encoding), which may be subject to patent licensing in some regions (e.g., the USA). For non-commercial use, this is typically not an issue, but please verify local regulations.

## License
This program is licensed under the **GNU General Public License (GPL) version 3** (or later) due to its dependency on FFmpeg, which is GPL-licensed when using components like `libx264`. For details, see the [LICENSE](LICENSE) file.

If you modify or distribute this program, you must make your source code available under the GPL. FFmpeg's source code and license details are available at: [https://ffmpeg.org](https://ffmpeg.org).

## Dependencies
- **Python 3.8+**: For running the program.
- **Tkinter**: For the GUI (usually included with Python).
- **FFmpeg**: For video compression (must be installed separately).

---

Thank you for using Video Compressor!
