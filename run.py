import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import Ghosts
from fruits import Fruit
from lifeicons import Lives
from spritesheet import SpriteSheet
from maze import Maze
from mongodriver import MongoDriver

# noinspection PyAttributeOutsideInit
class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.set_background()
        self.clock = pygame.time.Clock()
        self.score = 0
        self.font = pygame.font.SysFont("arial", 20)
        self.lives = 5
        self.fruit = None
        self.pelletsEaten = 0
        self.sheet = SpriteSheet()
        self.cur_song = 2
        self.data_driver = MongoDriver("1")
        self.level = 1

    def switch_song(self, delta):
        self.cur_song += delta
        if self.cur_song == 5:
            self.cur_song = 1
        if self.cur_song == 0:
            self.cur_song = 4

        if self.cur_song == 1:
            pygame.mixer.music.load("Music/song1.mp3")
        elif self.cur_song == 2:
            pygame.mixer.music.load("Music/song2.mp3")
        elif self.cur_song == 3:
            pygame.mixer.music.load("Music/song3.mp3")
        elif self.cur_song == 4:
            pygame.mixer.music.load("Music/song4.mp3")
        pygame.mixer.music.play(999)
        pygame.event.wait()

    def set_background(self):
        self.background = pygame.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def start_game(self):
        self.nodes = NodeGroup("Mazes/maze1.txt")
        self.pellets = PelletGroup("Mazes/maze1.txt")
        self.pacman = Pacman(self.nodes, self.sheet)
        self.ghosts = Ghosts(self.nodes, self.sheet)
        self.paused = True
        self.lifeIcons = Lives(self.sheet)
        self.maze = Maze(self.sheet)
        self.maze.get_maze("Mazes/maze1")
        self.maze.stitch_maze(self.background)
        self.pelletsEaten = 0
        self.switch_song(1)

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        if not self.paused:
            self.pacman.update(dt)
            self.ghosts.update(dt, self.pacman)
            if self.fruit is not None:
                self.fruit.update(dt)

        else:
            if not self.pacman.alive:
                self.pacman.update(dt)
                if self.pacman.deathSequenceFinished:
                    if self.lives == 0:
                        self.start_game()
                    else:
                        self.restart_level()

        self.check_events()
        self.render()

    def save_game(self):
        self.data_driver.clean()
        self.data_driver.save(self.pellets.get_snapshot(), self.score, self.lives, self.level)

    def load_game(self):
        self.start_game()
        self.pellets.create_pellet_list_snap(self.data_driver.get_pellets())
        self.score = self.data_driver.get_score()

        self.lives = self.data_driver.get_lives()
        self.level = self.data_driver.get_level()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.save_game()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.paused = not self.paused
                if event.key == K_PERIOD:
                    self.switch_song(1)
                if event.key == K_COMMA:
                    self.switch_song(-1)
                if event.key == K_F8:
                    self.save_game()
                if event.key == K_F7:
                    self.load_game()

        if not self.paused:
            self.check_pellet_events()
            self.check_ghost_events()
            self.check_fruit_events()

    def check_pellet_events(self):
        pellet = self.pacman.eat_pellets(self.pellets.pelletList)
        if pellet:
            self.pelletsEaten += 1
            self.score += pellet.points
            if self.pelletsEaten == 70 or self.pelletsEaten == 140:
                if self.fruit is None:
                    self.fruit = Fruit(self.nodes, self.sheet)

            self.pellets.pelletList.remove(pellet)
            if pellet.name == "powerpellet":
                self.ghosts.freight_mode()
            if self.pellets.is_empty():
                self.level += 1
                self.start_game()

    def restart_level(self):
        self.pacman = Pacman(self.nodes, self.sheet)
        self.ghosts = Ghosts(self.nodes, self.sheet)
        self.fruit = None
        self.paused = True

    def check_ghost_events(self):
        self.ghosts.release(self.pelletsEaten)
        ghost = self.pacman.eat_ghost(self.ghosts)
        # if self.pacman.eatGhost(self.ghost):
        if ghost is not None:
            if ghost.mode.name == "FREIGHT":
                self.score += ghost.points
                ghost.spawn_mode()
            elif ghost.mode.name != "SPAWN":
                self.lives -= 1
                self.paused = True
                self.pacman.alive = False
                self.pacman.animate.set_animation("death", 0)
                if (self.lives < 1):
                    self.level = 1
                    self.lives = 5
                    self.score = 0
                    self.start_game()

    def check_fruit_events(self):
        if self.fruit is not None:
            if self.pacman.eat_fruit(self.fruit) or self.fruit.its_time_to_die:
                if not self.fruit.its_time_to_die:
                    self.score += self.fruit.points
                self.fruit = None

    # TODO: original font score
    def render_score(self):
        text = self.font.render("Score: " + str(self.score), False, WHITE)
        self.screen.blit(text, (10, 10, 100, 100))

    def render_level(self):
        text = self.font.render("Level: " + str(self.level), False, WHITE)
        self.screen.blit(text, (200, 10, 300, 100))



    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        self.render_score()
        self.render_level()
        if self.fruit is not None:
            self.fruit.render(self.screen)

        y = TILE_HEIGHT * N_ROWS
        text = self.font.render("Lives: ", False, WHITE)
        self.screen.blit(text, (10,60,100,100))

        self.lifeIcons.render(self.screen, self.lives - 1)
        pygame.display.update()

if __name__ == "__main__":
    game = GameController()
    game.load_game()
    while True:
        game.update()
