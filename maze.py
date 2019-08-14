import pygame
from numpy import loadtxt
from constants import *
import random

class Maze(object):
    def __init__(self, spritesheet):
        self.spritesheet = spritesheet
        self.maze_info = None
        self.rotate_info = None
        self.images = []
        self.sprite_number = random.randint(0, 10)
        self.image_row = 16 #16 + self.sprite_number % 5
        self.image_column = 11

        self.get_maze_images()

    def get_maze_images(self):
        for i in range(11):
            self.images.append(self.spritesheet.get_image(i, self.image_row, 16, 16))

    @staticmethod
    def rotate(image, value):
        return pygame.transform.rotate(image, value * 90)

    def get_maze(self, txtfile):
        self.maze_info = loadtxt(txtfile + ".txt", dtype=str)
        try:
            self.rotate_info = loadtxt(txtfile + "_rot.txt", dtype=str)
        except IOError:
            pass

    def stitch_maze(self, background):
        rows, cols = self.maze_info.shape
        for row in range(rows):
            for col in range(cols):
                x = col * TILE_WIDTH
                y = row * TILE_HEIGHT
                try:
                    if self.maze_info[row][col] == 'x':
                        val = 10
                    else:
                        val = int(self.maze_info[row][col])
                except ValueError:
                    pass
                else:
                    if self.rotate_info is not None:
                        rotation_value = self.rotate_info[row][col]
                        image = self.rotate(self.images[val], int(rotation_value))
                        background.blit(image, (x, y))
                    else:
                        background.blit(self.images[val], (x, y))
