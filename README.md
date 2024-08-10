# Ansi_Videos
Play a video(pixelated) in a terminal with ANSI escape codes

# How to use
First, scrape the frames from the video
```bash
./frame_scrapper.py path/to/video path/to/frame/save/location name_of_video path/to/new/video/config.json
```

Then play the ANSI video
```bash
./renderer.py name_of_video
```