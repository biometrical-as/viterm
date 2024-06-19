from typing import Tuple, List

import typer
from typer import Argument, Option

from viterm import Display, Preprocessor, canny, gray



def get_preprocessor_function(preprocessors: List[Preprocessor]):
    preprocessors = [] if preprocessors is None else preprocessors

    def _func(image):
        for prep in preprocessors:
            if prep == Preprocessor.CANNY:
                image = canny(image)
            if prep == Preprocessor.GRAY:
                image = gray(image)
        return image

    return _func


app = typer.Typer()

@app.command()
def main(
    source: str = Argument(
        ..., show_default=False, help="Media source. [path | rtsp | camera index]"
    ),
    character: str = Option(
        Display.STORED_CELL_CHAR, "--character", "-c", help="Ascii character used"
    ),
    fit: bool = Option(
        True, "--fit_to_terminal", "-f", help="Fit image to terminal size."
    ),
    resolution: Tuple[int, int] = Option(
        (None, None),
        "--resolution",
        "-r",
        show_default=False,
        min=0,
        help="Output resolution",
    ),
    loop: bool = Option(False, "--loop", "-l", help="Loops media if video"),
    fps: int = Option(30, "--fps", "-f", min=0, help="Set FPS of video"),
    preprocessors: List[Preprocessor] = Option(
        None,
        "--preprocess",
        "-p",
        show_default=False,
        case_sensitive=False,
        help="Preprocessing function applied to media",
    ),
):
    """
    Displays low-color-representation of media in terminal as colored ascii characters.
    Media source might be image or video path, rtsp stream or usb camera index,
    or anything else opencv`s VideoCapture might accept.
    """
    try:
        source = int(source)
    except Exception:
        pass

    display = Display(
        resolution,
        character,
        preprocess_func=get_preprocessor_function(preprocessors),
        fit_to_terminal=fit,
    )
    display.show_media(source, fps=fps, loop=loop)


if __name__ == "__main__":
    app()
