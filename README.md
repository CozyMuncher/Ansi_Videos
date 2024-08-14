# Ansi_Videos
Play a video(pixelated) in a terminal with ANSI escape codes

# How to use
## 1 Install the packages
```bash
pip install -r requirements.txt
```

## 2 Run the script
```bash
python3 renderer.py path/to/video.mp4 [vr_split]
```
or 
```bash
python renderer.py path/to/video.mp4 [vr_split]
```
Eg:
```bash
python renderer.py movie.mp4 150
```

[vr_split] is used to specify how many frames each segment should contain. Default value is 100. Increasing this value allows for more stable video, but uses up more resources, and vice versa.