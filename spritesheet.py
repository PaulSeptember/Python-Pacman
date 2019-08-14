import pygame
from constants import *


class SpriteSheet(object):
    def __init__(self):
        self.sheet = pygame.image.load("Images/spritesheet.png").convert()
        self.sheet.set_colorkey(TRANSPARENT)

    def get_image(self, x, y, width, height):
        x *= width
        y *= height
        self.sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())
