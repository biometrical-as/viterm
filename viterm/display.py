from asyncore import loop
import sys
import shutil
from time import time, sleep
from typing import Tuple, Callable, Union

import cv2
import numpy as np


class Display:
    COLORS_STEPS = np.array([0, 95, 135, 175, 215, 255])
    INDICIES = np.arange(len(COLORS_STEPS))
    STORED_CELL_CHAR = "██"
    ANSI_RESET = "\u001b[0m"
    ANSI_CURSOR_UP = "\u001b[A"

    def __init__(
        self,
        output_shape: Tuple[int, int] = None,
        display_char: str = None,
        preprocess_func: Callable = None, 
        fit_to_terminal: bool = False
    ):
        self._shape = output_shape
        self._fit_to_terminal = fit_to_terminal

        if display_char is not None and len(display_char) == 1: 
            display_char *= 2 
        self._display_char = display_char
        self._ext_preprocess_func = lambda x: x 

        if preprocess_func is not None: 
            self._ext_preprocess_func = preprocess_func

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
                row += self.color_to_xterm_code(xterm_col[i, j])
            txt += row + "\n"

        sys.stdout.write(txt)
        sys.stdout.write(Display.ANSI_RESET)
        sys.stdout.write("\n")
        return len(txt)

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        if self._fit_to_terminal:
            h, w = self.get_terminal_size() 
            scale = min(h/image.shape[0], w/image.shape[1])
            image = cv2.resize(image, None, fx=scale, fy=scale)
        elif self._shape is not None:
            try:
                shape = (int(self._shape[1]), int(self._shape[0]))
                image = cv2.resize(image, shape)
            except ValueError:
                image = cv2.resize(
                    image, None, fx=float(self._shape[0]), fy=float(self._shape[0])
                )
        else:
            s = 40 / image.shape[1]
            image = cv2.resize(image, None, fx=s, fy=s)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = self._ext_preprocess_func(image)
        return image

    def get_terminal_size(self):         
        size = shutil.get_terminal_size() 
        return size.lines, size.columns//len(self._display_char) 

    def show_media(self, media: str, fps: Union[int, float] = 30, loop: bool = False):
        

        first_frame = True
        sec_pr_frame = 1 / fps
        try:
            while True:
                cap = cv2.VideoCapture(media)
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
                    t = time()
                    success, frame = cap.read()
                
                if not loop: 
                    break 
        except KeyboardInterrupt:
            sys.stdout.write(Display.ANSI_CURSOR_UP * txt_length)
            sys.stdout.write(txt_length * " ")
            sys.stdout.write(Display.ANSI_CURSOR_UP * txt_length)
            raise KeyboardInterrupt()

