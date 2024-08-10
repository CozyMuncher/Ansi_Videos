import cv2, sys, time, os, threading
from os import get_terminal_size
from decord import VideoReader

clear = lambda: os.system("clear")


def build_image(image):
    img_string = ""

    for row in image:
        for array in row:
            img_string += f"\x1b[48;2;{array[0]};{array[1]};{array[2]}m" + " "
        img_string += "\x1b[0m\n"

    return img_string


def render_image(img_string, frame_rate):
    _time = time.time()
    sys.stdout.write("\033[H")
    sys.stdout.write("\r" + img_string)
    sys.stdout.flush()

    if time.time() - _time < (1 / frame_rate):
        time.sleep((1 / frame_rate) - (time.time() - _time))


def resize_image(frame, width, height):
    image = cv2.resize(frame, (width, height))
    return image


def get_frames(vid_path):
    global vr, finish_loading
    vr = VideoReader(vid_path)
    finish_loading.set()


def loading_screen():
    global finish_loading
    while not finish_loading.is_set():
        for character in "\\-/|":
            sys.stdout.write("\r" + character + " Loading...")
            sys.stdout.flush()
            time.sleep(0.1)


def main(vid_path):
    try:
        global finish_loading
        finish_loading = threading.Event()

        get_frame_thread = threading.Thread(target=lambda: get_frames(vid_path))
        loading_animation_thread = threading.Thread(target=loading_screen)

        get_frame_thread.start()
        loading_animation_thread.start()

        get_frame_thread.join()
        loading_animation_thread.join()

        global vr
        frame_rate = vr.get_avg_fps()

        width, height = get_terminal_size()

        for frame in range(vr._num_frame):
            render_image(
                build_image(resize_image(vr[frame].asnumpy(), width, height - 1)),
                frame_rate,
            )

        print(" ----- End ----- ")
    except Exception as e:
        clear()
        print("\x1b[0m\n")
        print(e)


if __name__ == "__main__":
    vid_path = sys.argv[1]
    assert os.path.exists(vid_path)
    clear()
    main(vid_path)
