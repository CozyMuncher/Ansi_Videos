import cv2, sys, time, os, threading, math
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


def get_frames(vid_path, vr_split):
    global vr, finish_loading
    vr = VideoReader(vid_path)
    total_instances = math.ceil(vr._num_frame/vr_split)
    del vr
    vr = [VideoReader(vid_path) for i in range(total_instances)]
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
        global finish_loading, vr_split

        finish_loading = threading.Event()

        get_frame_thread = threading.Thread(target=lambda: get_frames(vid_path, vr_split))
        loading_animation_thread = threading.Thread(target=loading_screen)

        get_frame_thread.start()
        loading_animation_thread.start()

        get_frame_thread.join()
        loading_animation_thread.join()

        global vr
        frame_rate = vr[0].get_avg_fps()

        width, height = get_terminal_size()

        for frame in range(vr[0]._num_frame):
            if frame % vr_split == 0 and frame != 0:
                vr.pop(0)
            render_image(
                build_image(resize_image(vr[0][frame].asnumpy(), width, height - 1)),
                frame_rate,
            )

        print(" ----- End ----- ")
    except Exception as e:
        
        print("\x1b[0m\n")
        print(e)


if __name__ == "__main__":
    global vr_split
    vid_path = sys.argv[1]
    try: vr_split = sys.argv[2]
    except: vr_split = 200
    assert os.path.exists(vid_path)
    clear()
    main(vid_path)
