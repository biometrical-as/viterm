from argparse import ArgumentParser

import cv2
import numpy as np

from viterm import Display


def parse_args():
    parser = ArgumentParser(
        "GTerm: displays low-color-representation of image or video in terminal"
    )
    parser.add_argument(
        "media",
        type=str,
        help="Media file to display. Image or video. Index for usb camera",
    )
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
        default=None,
        help="Outputresolution",
    )
    parser.add_argument(
        "--preprocess",
        "-p",
        type=str,
        help="Preprocess function. Only canny edgedetection supported atm",
    )
    return parser.parse_args()


def canny(image: np.ndarray):
    image = cv2.Canny(image, 100, 200)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    return image


if __name__ == "__main__":
    args = parse_args()
    resolution = args.resolution
    character = args.character
    media = args.media
    try:
        media = int(media)
    except Exception:
        pass

    if args.preprocess == "canny":
        preprocess = canny
    elif args.preprocess is None:
        preprocess = None
    else:
        raise NotImplementedError("Only Canny edge detection supported ATM")

    display = Display(resolution, character, preprocess_func=preprocess)

    display.show_media(media)
