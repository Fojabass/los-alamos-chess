# camera.py: Handles the camera's position which can be used by other scripts to calculate where on the screen to draw objects.
# Author: Julien Devol

import pygame

class Camera:
    SPEED: float = 300
    position_xy = [0, 0]

    # __init__(): Constructor
    def __init__(self, screen) -> None:
        Camera.screen = screen
        Camera.position_xy[0] = Camera.getWidth() / 2
        Camera.position_xy[1] = Camera.getHeight() / 2

    # move(): Moves the camera in the passed directions.
    def move(self, dir_x: int = 0, dir_y: int = 0, delta_time: float = 0) -> None:
        Camera.position_xy[0] -= (dir_x * Camera.SPEED * delta_time)
        Camera.position_xy[1] -= (dir_y * Camera.SPEED * delta_time)

    # getScreen(): Returns the current screen.
    @staticmethod
    def getScreen():
        return Camera.screen

    # getWidth(): Returns the width of the current screen.
    @staticmethod
    def getWidth():
        return Camera.screen.get_width()
    
    # getHeight(): Returns the height of the current screen.
    @staticmethod
    def getHeight():
        return Camera.screen.get_height()
    
    # getX(): Returns the current x-coordinate of the camera.
    @staticmethod
    def getX():
        return Camera.position_xy[0]
    
    # getY(): Returns the current y-coordinate of the camera.
    @staticmethod
    def getY():
        return Camera.position_xy[1]
    



