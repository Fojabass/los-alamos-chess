# camera.py:
# Author: Julien Devol

from typing import List, Tuple, Optional

class Camera:
    camera_size: Tuple[float, float] = (0, 0) # Potentially for zooming in/out
    camera_pos: Tuple[float, float] = (0, 0)
    margin_xy: Tuple[float, float] = (0, 0)

