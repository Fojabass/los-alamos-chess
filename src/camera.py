# camera.py:
# Author: Julien Devol

import pygame

class Camera:
    SPEED: float = 200
    position = [0, 0]
    screen_width = 0
    screen_height = 0

    def __init__(self, screen) -> None:
        Camera.updateScreenInfo(screen)
        Camera.position[0] = Camera.screen_width / 2
        Camera.position[1] = Camera.screen_height / 2

    # move(): Moves the camera in the passed directions.
    def move(self, dir_x: int = 0, dir_y: int = 0, delta_time: float = 0) -> None:
        Camera.position[0] += (dir_x * Camera.SPEED * delta_time)
        Camera.position[1] += (dir_y * Camera.SPEED * delta_time)

    def updateScreenInfo(screen) -> None:
        Camera.screen_width = screen.get_width()
        Camera.screen_height = screen.get_height()

    @staticmethod
    def getWidth():
        return Camera.screen_width
    
    @staticmethod
    def getHeight():
        return Camera.screen_height
    
    @staticmethod
    def getX():
        return Camera.position[0]
    
    @staticmethod
    def getY():
        return Camera.position[1]
    



