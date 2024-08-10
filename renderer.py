#!venv/bin/python

import cv2, sys, time, os, json, concurrent.futures
import numpy as np
from itertools import repeat
from os import get_terminal_size


clear = lambda: os.system("clear")


def build_image(image):
    img_string = ""

    for row in image:
        for array in row:
            img_string += f"\x1b[48;2;{array[0]};{array[1]};{array[2]}m" + " "
        img_string += "\x1b[0m\n"

    return img_string


def get_image(image_id, config, width, height):
    image = cv2.imread(f"{config['frames_location']}/frame{image_id}.jpg")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (width, height))
    im = np.array(image)

    return im


def render_image(img_string, config):
    _time = time.time()
    sys.stdout.write("\033[H")
    sys.stdout.write("\r" + img_string)
    sys.stdout.flush

    while time.time() - _time < config["delay"]:
        pass


def prep_image(image_id, config, width, height):
    return build_image(get_image(image_id, config, width, height))


def main(name):
    with open("config.json") as f:
        main_config = json.load(f)

    with open(main_config[name]) as f:
        config = json.load(f)

    no_frames = config["frames"]

    width, height = get_terminal_size()

    clear()

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as exe:
        for result in exe.map(
            prep_image,
            [i for i in range(0, no_frames + 1)],
            repeat(config),
            repeat(width),
            repeat(height - 1),
        ):
            render_image(result, config)

    print(f" ----- {config['name']} ----- ")


if __name__ == "__main__":
    name = sys.argv[1]
    main(name)
