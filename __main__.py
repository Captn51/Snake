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
FRAMERATE = 10
WINDOWS_SIZE = (800, 600)


class Snake:
    """Classe modélisant le serpent.
    """

    DIRECTIONS = {
        K_UP: (0, -1),
        K_LEFT: (-1, 0),
        K_DOWN: (0, 1),
        K_RIGHT: (1, 0)
    }

    _PIECE_SIZE = 10
    _INITIAL_LEN = 20

    def __init__(self, area):
        """Initialisation du serpent.

        Le serpent apparait à un endroit aléatoire de la zone, mais en entier. Il
        a également une direction aléatoire et une longueur de _INITIAL_LEN bouts.
        """
        pos_i = [
            randrange(self._INITIAL_LEN*self._PIECE_SIZE, i-self._INITIAL_LEN*self._PIECE_SIZE, self._PIECE_SIZE)
            for i in area
        ]
        self.area = area
        self.digestion = False
        self.direction = choice(list(self.DIRECTIONS.values()))
        self.body = [
            [p_i - i*self._PIECE_SIZE*d for p_i, d in zip(pos_i, self.direction)]
            for i in range(self._INITIAL_LEN)
        ]

    def set_direcion(self, key_direction):
        """Change la direction du serpent.
        """
        # Pas possible de faire demi-tour
        new_plus_old = [new + old for new, old in zip(self.DIRECTIONS[key_direction], self.direction)]
        if not new_plus_old == [0, 0]:
            self.direction = self.DIRECTIONS[key_direction]

    def move(self):
        """Déplace le serpent.

        Le serpent retourne de l'autre côté de la zone s'il en sort.
        """
        if self.digestion:
            self.body[1:] = self.body
            self.digestion = False
        else:
            self.body[1:] = self.body[:len(self.body)-1]

        self.body[0] = [b + self._PIECE_SIZE*d for b, d in zip(self.body[0], self.direction)]

        # Gestion aux bords de la zone
        for i in range(2):
            if self.body[0][i] < 0:
                self.body[0][i] = self.area[i] - self._PIECE_SIZE
            elif self.body[0][i] > self.area[i]-self._PIECE_SIZE:
                self.body[0][i] = 0

    def move_on_itself(self):
        """Indique si le serpent se déplace sur lui-même ou non.
        """
        return self.body[0] in self.body[1:]

    def draw(self, screen, rgb_color):
        """Dessine un serpent dans une fenêtre avec une couleur donnée.
        """
        for piece in self.body:
            pygame.draw.rect(screen, DARK_GRAY, Rect(piece[0], piece[1], self._PIECE_SIZE, self._PIECE_SIZE))


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

