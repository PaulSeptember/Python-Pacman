import pygame
from constants import *


# noinspection PyAttributeOutsideInit
class MazeRunner(object):
    def __init__(self, nodes, spritesheet):
        self.name = ""
        self.direction = STOP
        self.speed = 100
        self.radius = 10
        self.collideRadius = 5
        self.color = WHITE
        self.nodes = nodes
        self.node = nodes.nodelist[0]
        self.target = self.node
        self.image = None
        self.spritesheet = spritesheet
        self.set_position()

    def set_position(self):
        self.position = self.node.position.copy()

    def update(self, dt):
        self.position += self.direction * self.speed * dt
        self.move_by_self()

    def move_by_self(self):
        if self.direction is not STOP:
            if self.overshot_target():
                self.node = self.target
                self.portal()
                if self.node.neighbors[self.direction] is not None:
                    self.target = self.node.neighbors[self.direction]
                else:
                    self.set_position()
                    self.direction = STOP

    def overshot_target(self):
        vec1 = self.target.position - self.node.position
        vec2 = self.position - self.node.position
        node_to_target = vec1.magnitude_squared()
        node_to_self = vec2.magnitude_squared()
        return node_to_self >= node_to_target

    def reverse_direction(self):
        if self.direction is UP:
            self.direction = DOWN
        elif self.direction is DOWN:
            self.direction = UP
        elif self.direction is LEFT:
            self.direction = RIGHT
        elif self.direction is RIGHT:
            self.direction = LEFT
        temp = self.node
        self.node = self.target
        self.target = temp

    def portal(self):
        if self.node.portal_node:
            self.node = self.node.portal_node
            self.set_position()

    def render(self, screen):
        px = int(self.position.x - 8)
        py = int(self.position.y - 8)
        if self.image is not None:
            screen.blit(self.image, (px, py))
        else:
            pygame.draw.circle(screen, self.color, (px, py), self.radius)
