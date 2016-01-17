# -*- coding: utf-8 -*-

from sys import exit
from time import sleep
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
        self._area = area
        self._digestion = False
        self._direction = choice(list(self.DIRECTIONS.values()))
        self._body = [
            [p_i - i*self._PIECE_SIZE*d for p_i, d in zip(pos_i, self._direction)]
            for i in range(self._INITIAL_LEN)
        ]

    def set_direction(self, key_direction):
        """Change la direction du serpent.
        """
        # Pas possible de faire demi-tour
        new_plus_old = [new + old for new, old in zip(self.DIRECTIONS[key_direction], self._direction)]
        if new_plus_old != [0, 0]:
            self._direction = self.DIRECTIONS[key_direction]

    def move(self):
        """Déplace le serpent.

        Le serpent retourne de l'autre côté de la zone s'il en sort.
        """
        if self._digestion:
            self._body[1:] = self._body
            self._digestion = False
        else:
            self._body[1:] = self._body[:len(self._body)-1]

        self._body[0] = [b + self._PIECE_SIZE*d for b, d in zip(self._body[0], self._direction)]

        # Gestion aux bords de la zone
        for i in range(2):
            if self._body[0][i] < 0:
                self._body[0][i] = self._area[i] - self._PIECE_SIZE
            elif self._body[0][i] > self._area[i]-self._PIECE_SIZE:
                self._body[0][i] = 0

    def move_on_itself(self):
        """Indique si le serpent se déplace sur lui-même ou non.
        """
        return self._body[0] in self._body[1:]

    def eat(self, cube):
        """Indique si le serpent a mangé un cube ou non.

        Si le serpent a mangé un cube, il entre en phase de digestion.
        """
        if cube.pos == self._body[0]:
            self._digestion = True
            return True
        else:
            return False

    def __len__(self):
        """Renvoie la longueur du serpent.
        """
        return len(self._body)

    def draw(self, screen, rgb_color):
        """Dessine un serpent dans une fenêtre avec une couleur donnée.
        """
        for piece in self._body:
            pygame.draw.rect(screen, DARK_GRAY, Rect(piece[0], piece[1], self._PIECE_SIZE, self._PIECE_SIZE))


class Cube:
    """Classe modélisant le cube. Le cube est unique tout au long de la partie. Il
    se déplace lorsqu'il a été attrapé par le serpent, tout en lui donnant un petit
    bout de lui-même pour qu'il grossisse.
    """

    _PIECE_SIZE = 10

    def __init__(self, area):
        """Initialisation du cube.

        Le cube apparait à un endroit aléatoire de la zone.
        """
        # TODO: property ?
        self.pos = [randrange(0, i, self._PIECE_SIZE) for i in area]

    def move(self, area):
        """Déplace le cube.
        """
        self.pos = [randrange(0, i, self._PIECE_SIZE) for i in area]

    def draw(self, screen, rgb_color):
        """Dessine un cube dans une fenêtre avec une couleur donnée.
        """
        pygame.draw.rect(screen, DARK_GRAY, Rect(self.pos[0], self.pos[1], self._PIECE_SIZE, self._PIECE_SIZE))


# ====
# Jeu
# ====


print("Bienvenue dans le jeu du SNAKE !!")
print("Attention !! Départ dans 2s !!")
sleep(2)

pygame.init()

snake = Snake(WINDOWS_SIZE)
cube = Cube(WINDOWS_SIZE)
my_clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOWS_SIZE)

pygame.display.set_caption("Snake")
snake.draw(screen, DARK_GRAY)
cube.draw(screen, DARK_GRAY)
pygame.display.flip()
print("Longueur du serpent :", len(snake), end="")

while True:
    my_clock.tick(FRAMERATE)
    for event in pygame.event.get():
        # TODO: cas où 2 set_direction se cumulent car appui trop rapide sur les touches

        if event.type == QUIT:
            exit()

        if event.type == KEYDOWN and event.key in snake.DIRECTIONS.keys():
            snake.set_direction(event.key)

    snake.move()
    if snake.move_on_itself():
        break

    if snake.eat(cube):
        cube.move(WINDOWS_SIZE)

    screen.fill(BLACK)
    snake.draw(screen, DARK_GRAY)
    cube.draw(screen, DARK_GRAY)
    pygame.display.flip()
    print("\rLongueur du serpent :", len(snake), end="")

print("")
print("HA HA !! Tu t'es mangé toi-même !! La longueur atteinte est de", len(snake), "!!")
input("Appuie sur ENTREE pour quitter...")

pygame.quit()

