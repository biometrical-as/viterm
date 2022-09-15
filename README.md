
# ViTerm 
<p align="center">
  <img src="/figures/viterm_logo.png" alt="Viterm logo"/>
</p>

Displays video, images, webcam or rtsp stream in terminal. 

## Requirements
viterm is developed for python >=3.8.

## Setup
```
pip install -r requirements.txt
pip install .
```
## Use
```
from viterm import Display

resolution = (50, 50)
character = '#'

display = Display(resolution, character)

# Show image
display.display_image(image)
# Video or webcam
display.show_media(<file_path or cam index>)
```

When displaying video, viterm will do its best to keep 30fps. 

## CLI
```bash
viterm <media> -r <Height Width> -c <display character> 
```
* media: Accepts video, images, webcam-index, rtsp-streams and anything else which is supported by cv2.VideoCapture
* --resolution: Two values. Int to set pixel width/height, float to scale image dimension. The image is scaled down to a width of 40 by default (keeping aspect ratio)
* --character: String of what character to use as a display-pixel. Default is ██. 
* --fps: Set fps of video 
* --fit_to_terminal: Resize image/video to fit terminal size
* --loop: loops media
* --preprocess: Runs a aditional preprocessor on media. Only Canny edge detections is supported ATM
