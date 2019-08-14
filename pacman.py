import pygame
from pygame.locals import *
from constants import *
from entity import MazeRunner
from animation import Animation, AnimationGroup


# noinspection PyAttributeOutsideInit
class Pacman(MazeRunner):
    def __init__(self, nodes, spritesheet):
        MazeRunner.__init__(self, nodes, spritesheet)
        self.name = "pacman"
        self.direction = STOP
        self.color = YELLOW
        self.speed = PACMAN_SPEED
        self.radius = 10
        self.collideRadius = 5
        self.nodes = nodes
        self.previousDirection = None
        self.set_start_position()
        # self.set_position()

        self.animate = AnimationGroup()
        self.animateName = "left"
        self.define_animations()
        self.animate.set_animation(self.animateName, 0)
        self.image = self.animate.get_image()

        self.alive = True
        self.deathSequenceFinished = False
        self.previousDirection = self.direction

    def set_position(self):
        self.position = self.node.position.copy()

    def set_position_tuple(self,pos):
        self.position = Vector2D(pos[0],pos[1])

    def get_position(self):
        return self.position.to_tuple()

    def update(self, dt):
        if self.alive:
            self.check_direction_change()
            if self.direction != STOP:
                self.image = self.animate.ping(dt)
            else:
                self.image = self.animate.get_image()

            self.position += self.direction * self.speed * dt
            direction = self.get_valid_key()
            if direction:
                self.move_by_key(direction)
            else:
                self.move_by_self()

        else:
            self.image = self.animate.one_pass(dt)
            if self.animate.animation.finished:
                self.deathSequenceFinished = True

    @staticmethod
    def get_valid_key():
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT

    def move_by_key(self, direction):
        if self.direction is STOP:
            if self.node.neighbors[direction] is not None:
                self.target = self.node.neighbors[direction]
                self.direction = direction
        else:
            if direction == -self.direction:
                self.reverse_direction()

            if self.overshot_target():
                self.node = self.target
                self.portal()
                if self.node.neighbors[direction] is not None:
                    if self.node.is_home_entrance:
                        if self.node.neighbors[self.direction] is not None:
                            self.target = self.node.neighbors[self.direction]
                        else:
                            self.set_position()
                            self.direction = STOP
                    else:
                        self.target = self.node.neighbors[direction]
                        if self.direction != direction:
                            self.set_position()
                            self.direction = direction
                else:
                    if self.node.neighbors[self.direction] is not None:
                        self.target = self.node.neighbors[self.direction]
                    else:
                        self.set_position()
                        self.direction = STOP

    def portal(self):
        if self.node.portal_node:
            self.node = self.node.portal_node
            self.set_position()

    def find_start_node(self):
        for node in self.nodes.nodelist:
            if node.is_pacman_start:
                return node
        return None

    def overshot_target(self):
        vec1 = self.target.position - self.node.position
        vec2 = self.position - self.node.position
        dist_to_target = vec1.magnitude_squared()
        dist_to_self = vec2.magnitude_squared()
        return dist_to_self >= dist_to_target

    def set_start_position(self):
        self.direction = LEFT
        self.node = self.find_start_node()
        self.target = self.node.neighbors[self.direction]
        self.set_position()
        self.position.x -= (self.node.position.x - self.target.position.x) / 2

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

    def eat_pellets(self, pelletlist):
        for pellet in pelletlist:
            d = self.position - pellet.position
            d_squared = d.magnitude_squared()
            r_squared = (pellet.radius+self.collideRadius)**2
            if d_squared <= r_squared:
                return pellet
        return None

    def eat_fruit(self, fruit):
        d = self.position - fruit.position
        d_squared = d.magnitude_squared()
        r_squared = (self.collideRadius + fruit.collideRadius) ** 2
        if d_squared <= r_squared:
            return True
        return False

    def eat_ghost(self, ghostlist):
        for ghost in ghostlist:
            d = self.position - ghost.position
            d_squared = d.magnitude_squared()
            r_squared = (self.collideRadius + ghost.collideRadius) ** 2
            if d_squared <= r_squared:
                return ghost
        return None

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

    def define_animations(self):
        anim = Animation("left")
        anim.speed = 20
        anim.add_frame(self.spritesheet.get_image(4, 0, 32, 32))
        anim.add_frame(self.spritesheet.get_image(0, 0, 32, 32))
        anim.add_frame(self.spritesheet.get_image(0, 1, 32, 32))
        self.animate.add(anim)

        anim = Animation("right")
        anim.speed = 20
        anim.add_frame(self.spritesheet.get_image(4, 0, 32, 32))
        anim.add_frame(self.spritesheet.get_image(1, 0, 32, 32))
        anim.add_frame(self.spritesheet.get_image(1, 1, 32, 32))
        self.animate.add(anim)

        anim = Animation("down")
        anim.speed = 20
        anim.add_frame(self.spritesheet.get_image(4, 0, 32, 32))
        anim.add_frame(self.spritesheet.get_image(2, 0, 32, 32))
        anim.add_frame(self.spritesheet.get_image(2, 1, 32, 32))
        self.animate.add(anim)

        anim = Animation("up")
        anim.speed = 20
        anim.add_frame(self.spritesheet.get_image(4, 0, 32, 32))
        anim.add_frame(self.spritesheet.get_image(3, 0, 32, 32))
        anim.add_frame(self.spritesheet.get_image(3, 1, 32, 32))
        self.animate.add(anim)

        anim = Animation("death")
        anim.speed = 10
        anim.add_frame(self.spritesheet.get_image(0, 7, 32, 32))
        anim.add_frame(self.spritesheet.get_image(1, 7, 32, 32))
        anim.add_frame(self.spritesheet.get_image(2, 7, 32, 32))
        anim.add_frame(self.spritesheet.get_image(3, 7, 32, 32))
        anim.add_frame(self.spritesheet.get_image(4, 7, 32, 32))
        anim.add_frame(self.spritesheet.get_image(5, 7, 32, 32))
        anim.add_frame(self.spritesheet.get_image(6, 7, 32, 32))
        anim.add_frame(self.spritesheet.get_image(7, 7, 32, 32))
        anim.add_frame(self.spritesheet.get_image(8, 7, 32, 32))
        anim.add_frame(self.spritesheet.get_image(9, 7, 32, 32))
        anim.add_frame(self.spritesheet.get_image(10, 7, 32, 32))
        self.animate.add(anim)

    def check_direction_change(self):
        if self.direction != self.previousDirection:
            self.previousDirection = self.direction
        if self.direction == LEFT:
            self.animateName = "left"
        elif self.direction == RIGHT:
            self.animateName = "right"
        elif self.direction == DOWN:
            self.animateName = "down"
        elif self.direction == UP:
            self.animateName = "up"
        self.animate.set_animation(self.animateName, self.animate.animation.col)
