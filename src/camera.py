# camera.py:
# Author: Julien Devol

import pygame

class Camera:
    SPEED: float = 200
    
    position = [0, 0]
    screen = None

    def __init__(self, screen) -> None:
        Camera.addScreenRef(screen)
        Camera.position[0] = Camera.getWidth() / 2
        Camera.position[1] = Camera.getHeight() / 2

    # move(): Moves the camera in the passed directions.
    def move(self, dir_x: int = 0, dir_y: int = 0, delta_time: float = 0) -> None:
        Camera.position[0] += (dir_x * Camera.SPEED * delta_time)
        Camera.position[1] += (dir_y * Camera.SPEED * delta_time)

    @staticmethod
    def addScreenRef(screen) -> None:
        Camera.screen = screen

    @staticmethod
    def getScreen():
        return Camera.screen

    @staticmethod
    def getWidth():
        return Camera.screen.get_width()
    
    @staticmethod
    def getHeight():
        return Camera.screen.get_height()
    
    @staticmethod
    def getX():
        return Camera.position[0]
    
    @staticmethod
    def getY():
        return Camera.position[1]
    



