from argparse import ArgumentParser

from viterm.viterm import Display


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
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    resolution = args.resolution
    character = args.character
    media = args.media
    try:
        media = int(media)
    except Exception:
        pass

    display = Display(resolution, character)

    display.show_media(media)
