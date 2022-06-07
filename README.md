
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

### Optional
To make an alias, append the following line to your .bashrc (linux) or .zshrc (mac):

```bash
viterm() { python <path-to-repo/scripts/run.py> "$@" ;}
```

If you want it to run in a specific conda environment, add the following instead:

```bash
viterm() { conda run -n <your environment name> python <path-to-repo/scripts/run.py> "$@" ;}
```

Run ```source ~/.bashrc``` (linux) or ```source ~/.zshrc``` (mac). You can now call viterm in your terminal with ```viterm```

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

### CLI
Without alias:
```bash
python scripts/run.py <media> -r <Height Width> -c <display character> 
```
With alias:
```bash
viterm <media> -r <Height Width> -c <display character> 
```
* media: Accepts video, images, webcam-index, rtsp-streams and anything else which is supported by cv2.VideoCapture
* --resolution: Two values. Int to set pixel width/height, float to scale image dimension. The image is scaled down to a width of 40 by default (keeping aspect ratio)
* --character: String of what character to use as a display-pixel. Default is ██. 
