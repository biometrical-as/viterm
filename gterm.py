import sys
from typing import Tuple
from time import time, sleep
from argparse import ArgumentParser

import cv2
import numpy as np


class Display:
    COLORS_STEPS = np.array([0, 95, 135, 175, 215, 255])
    INDICIES = np.arange(len(COLORS_STEPS))
    STORED_CELL_CHAR = "█"
    ANSI_RESET = "\u001b[0m"
    ANSI_CURSOR_UP = "\u001b[A"

    def __init__(
        self,
        output_shape: Tuple[int, int] = None,
        display_char: str = None,
    ):
        self._shape = output_shape
        self._display_char = display_char

    @staticmethod
    def image_to_xterm(image):
        at = np.tile(
            np.reshape(
                Display.COLORS_STEPS, (-1, *list(np.ones(len(image.shape)).astype(int)))
            ),
            (1, *image.shape),
        )
        bt = np.tile(
            image,
            (Display.COLORS_STEPS.size, *list(np.ones(len(image.shape)).astype(int))),
        )

        idx = np.argmin(np.abs(at - bt), axis=0)
        xterm_img = Display.INDICIES[idx]
        return 16 + xterm_img[..., 0] * 36 + xterm_img[..., 1] * 6 + xterm_img[..., 2]

    def color_to_xterm_code(self, col, character: str = None):
        if character is not None:
            c = character
        elif self._display_char is not None:
            c = self._display_char
        else:
            c = Display.STORED_CELL_CHAR

        return f"\u001b[38;5;{col}m{c}\033[0m"

    def display_image(self, image: np.ndarray):
        xterm_col = Display.image_to_xterm(image)

        txt = ""
        for i in range(image.shape[0]):
            row = ""
            for j in range(image.shape[1]):
                row += self.color_to_xterm_code(xterm_col[i, j]) * 2
            txt += row + "\n"

        sys.stdout.write(txt)
        sys.stdout.write(Display.ANSI_RESET)
        sys.stdout.write("\n")
        return len(txt)

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        shape = (100, 100)
        if self._shape is not None:
            try:
                shape = (int(self._shape[1]), int(self._shape[0]))
                image = cv2.resize(image, shape)
            except ValueError:
                image = cv2.resize(
                    image, None, fx=float(self._shape[0]), fy=float(self._shape[0])
                )
        else:
            image = cv2.resize(image, shape)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image

    def show_media(self, video):
        cap = cv2.VideoCapture(video)

        sec_pr_frame = 1 / 30
        first_frame = True

        t = time()
        success, frame = cap.read()
        while success:

            frame = self.preprocess_image(frame)

            if not first_frame:
                sys.stdout.write(Display.ANSI_CURSOR_UP * txt_length)
            else:
                first_frame = False

            txt_length = self.display_image(frame)

            sleep_time = sec_pr_frame - (time() - t)
            if 0 <= sleep_time:
                sleep(sleep_time)

            success, frame = cap.read()



def parse_args():
    parser = ArgumentParser(
        "GTerm: displays low-color-representation of image or video in terminal"
    )
    parser.add_argument("media", type=str, help="Media file to display. Image or video")
    parser.add_argument(
        "--character",
        "-c",
        default=Display.STORED_CELL_CHAR,
        help="Ascii character used",
    )
    parser.add_argument(
        "--resolution",
        "-r",
        nargs=2,
        default=(100, 100),
        help="Outputresolution",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    display = Display(args.resolution, args.character)
    display.show_media(args.media)

    # display.show_video("/home/martin/Downloads/bh_slice.mp4")

    # image = cv2.imread("/home/martin/Downloads/lk.jpeg")
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # image = cv2.resize(image, (100, 100))

    # t = time()
    # display.display_image(image)
    # print(time() - t)
