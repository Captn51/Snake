# -*- coding: utf-8 -*-

from sys import exit
from random import choice, randrange
import pygame
from pygame.locals import *


# ================================
# Variables, classes et fonctions
# ================================


BLACK = (0, 0, 0)
DARK_GRAY = (100, 100, 100)
FRAMERATE = 2
WINDOWS_SIZE = (800, 600)


class Snake:
    """Classe modélisant le serpent.
    """

    PIECE_SIZE = 10
    DIRECTIONS = {
        K_UP: (0, -1),
        K_LEFT: (-1, 0),
        K_DOWN: (0, 1),
        K_RIGHT: (1, 0)
    }

    _INITIAL_LEN = 20

    def __init__(self, area):
        """Initialisation du serpent.

        Le serpent apparait à un endroit aléatoire de la zone, mais en entier. Il
        a également une direction aléatoire et une longueur de _INITIAL_LEN bouts.
        """
        pos_i = [
            randrange(self._INITIAL_LEN*self.PIECE_SIZE, i - self._INITIAL_LEN*self.PIECE_SIZE, self.PIECE_SIZE)
            for i in area
        ]
        self.area = area
        self.len = self._INITIAL_LEN
        self.direction = choice(list(self.DIRECTIONS.values()))
        self.body = [
            [pos_i[0] - i*self.direction[0]*self.PIECE_SIZE, pos_i[1] - i*self.direction[1]*self.PIECE_SIZE]
            for i in range(self.len)
        ]

    def set_direcion(self, key_direction):
        """Change la direction du serpent.
        """
        self.direction = self.DIRECTIONS[key_direction]

        # TODO: empêcher de prendre la direction opposée

    def move(self):
        """Déplace le serpent.

        Le serpent retourne de l'autre côté de la zone s'il en sort.
        """
        for i in range(self.len - 1, 0, -1):
            self.body[i] = self.body[i-1]

        self.body[0] = [
            self.body[0][0] + self.direction[0]*self.PIECE_SIZE,
            self.body[0][1] + self.direction[1]*self.PIECE_SIZE
        ]

        if self.body[0][0] < 0:
            self.body[0][0] = self.area[0] - self.PIECE_SIZE
        elif self.body[0][0] > self.area[0]-self.PIECE_SIZE:
            self.body[0][0] = 0

        if self.body[0][1] < 0:
            self.body[0][1] = self.area[1] - self.PIECE_SIZE
        elif self.body[0][1] > self.area[1]-self.PIECE_SIZE:
            self.body[0][1] = 0

    def move_on_itself(self):
        """Indique si le serpent se déplace sur lui-même ou non.
        """
        return self.body[0] in self.body[1:]

    def draw(self, screen, rgb_color):
        """Dessine un serpent dans une fenêtre avec une couleur donnée.
        """
        for piece in self.body:
            pygame.draw.rect(screen, DARK_GRAY, Rect(piece[0], piece[1], self.PIECE_SIZE, self.PIECE_SIZE))


# ====
# Jeu
# ====


pygame.init()

snake = Snake(WINDOWS_SIZE)
my_clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOWS_SIZE)

pygame.display.set_caption("Snake")
snake.draw(screen, DARK_GRAY)

while True:
    my_clock.tick(FRAMERATE)
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

        if event.type == KEYDOWN and event.key in snake.DIRECTIONS.keys():
            snake.set_direcion(event.key)

    snake.move()
    if snake.move_on_itself():
        break

    screen.fill(BLACK)
    snake.draw(screen, DARK_GRAY)
    pygame.display.flip()

pygame.quit()

