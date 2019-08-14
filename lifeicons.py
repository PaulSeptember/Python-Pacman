from constants import *

class Lives(object):
    def __init__(self, spritesheet):
        self.width, self.height = 32, 32
        self.image = spritesheet.get_image(0, 1, self.width, self.height)
        self.gap = 10

    def render(self, screen, num):
        for i in range(num):
            x = self.gap*7 + (self.width + self.gap) * i
            y = TILE_HEIGHT * N_ROWS - self.height
            screen.blit(self.image, (x, y))
