import cv2, sys, json, os


def main(vid_path, frame_location, name, config_path):
    vidcap = cv2.VideoCapture(vid_path)
    success, image = vidcap.read()
    count = 0

    if not os.path.exists(frame_location):
        os.makedirs(frame_location)

    while success:
        cv2.imwrite(f"{frame_location}/frame%d.jpg" % count, image)
        success, image = vidcap.read()
        count += 1

    with open("config.json", "r") as f:
        _config = json.load(f)
        _config[name] = config_path
        config = json.dumps(_config)

    with open("config.json", "w") as f:
        f.write(config)
        f.close()

    with open(config_path, "w") as f:
        _config = {
            "frames": count,
            "frames_location": frame_location,
            "name": name,
            "delay": 1 / vidcap.get(cv2.CAP_PROP_FPS),
        }
        config = json.dumps(_config)
        f.write(config)
        f.close()

    print("Done")
    print(f"Config File Saved At: {config_path}")
    print(f"Frames Saved At: {frame_location}")


if __name__ == "__main__":
    vid_path = sys.argv[1]
    frame_location = sys.argv[2]
    name = sys.argv[3]
    config_path = sys.argv[4]

    main(vid_path, frame_location, name, config_path)
