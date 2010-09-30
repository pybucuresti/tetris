import os
import sys
import pygame
from random import randint

ROOT_PATH = os.path.dirname(__file__) + '/'
square_size = 16
speed = [0, square_size]
black = 0, 0, 0
num_horiz_squares = 10
num_vert_squares = 25

screen_size = width, height = num_horiz_squares*square_size, num_vert_squares*square_size

UP_ARROW = 273
LEFT_ARROW = 276
DOWN_ARROW = 274
RIGHT_ARROW = 275


class MyRectangle(object):
    def __init__(self, square):
        self.posX = randint(0, num_horiz_squares - 1)
        self.posY = 0
        self.square = square

    def blit_to(self, screen):
        rect = self.square.get_rect().move([self.posX*square_size, self.posY*square_size])
        screen.blit(self.square, rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode(screen_size)

    blue_square = pygame.image.load(ROOT_PATH + 'images/square-16x16-blue.png')
    #blue_rect = blue_square.get_rect()
    pygame.time.set_timer(pygame.USEREVENT, 500)
    my_rect = MyRectangle(blue_square)
    while True:
        event = pygame.event.wait()
        #for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if event.key == DOWN_ARROW:
               my_rect.posY += 1
            if event.key == LEFT_ARROW:
               my_rect.posX -= 1
            if event.key == RIGHT_ARROW:
               my_rect.posX += 1
        elif event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.USEREVENT:
            my_rect.posY += 1

        screen.fill(black)
        my_rect.blit_to(screen)
        pygame.display.flip()
