# Video Compressor

## Requirement
pyinstaller, pillow

## Mac
pyinstaller -F -w -i "appicon.png" --name "Video Compressor" ffmpeg_compressor.py

## Windows
python3 gen_icon.py
pyinstaller -F -w -i "appicon.ico" --name "Video Compressor" ffmpeg_compressor.py
