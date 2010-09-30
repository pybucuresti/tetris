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

red_square = pygame.image.load(ROOT_PATH + 'images/square-16x16-red.png')
green_square = pygame.image.load(ROOT_PATH + 'images/square-16x16-green.png')
yellow_square = pygame.image.load(ROOT_PATH + 'images/square-16x16-yellow.png')
blue_square = pygame.image.load(ROOT_PATH + 'images/square-16x16-blue.png')

ocupado = {}

UP_ARROW = 273
LEFT_ARROW = 276
DOWN_ARROW = 274
RIGHT_ARROW = 275

class MyRectangle(object):
    def __init__(self, square, posX, posY):
        self.posX = posX
        self.posY = posY
        self.square = square

    def blit_to(self, screen):
        rect = self.square.get_rect().move([self.posX*square_size, self.posY*square_size])
        screen.blit(self.square, rect)

class TetrisShape(object):
    def __init__(self):
        self.rects = (
            MyRectangle(red_square, 4, 0),
            MyRectangle(green_square, 4, 1),
            MyRectangle(yellow_square, 5, 1),
            MyRectangle(blue_square, 5, 2),
        )
        self.dead = False
        self.center = 2

    def move(self, dx, dy):
        if self.check_collision(dx, dy):
            if dy != 0:
                for rect in self.rects:
                    ocupado[rect.posX, rect.posY] = rect
                    self.dead = True
            return
        for rect in self.rects:
            rect.posX += dx
            rect.posY += dy

    def check_collision(self, dx, dy):
        for rect in self.rects:
            if rect.posY + dy >= num_vert_squares:
                return True
            if not (0 <= rect.posX + dx < num_horiz_squares):
                return True
            if ocupado.get((rect.posX+dx, rect.posY+dy), False):
                return True
        return False

    def rotate(self):
        center_rect = self.rects[self.center]
        for rect in self.rects:
            if rect != center_rect:
                delta_x = rect.posX - center_rect.posX
                delta_y = rect.posY - center_rect.posY
                changes = {
                    (-1, -1): (1, -1),
                    (1, -1): (1, 1),
                    (1, 1): (-1, 1),
                    (-1, 1): (-1, -1),

                    (-1, 0): (0, -1),
                    (0, -1): (1, 0),
                    (1, 0): (0, 1),
                    (0, 1): (-1, 0),
                }
                change = changes[(delta_x, delta_y)]
                rect.posX = center_rect.posX + change[0]
                rect.posY = center_rect.posY + change[1]

    def blit_to(self, screen):
        for rect in self.rects:
            rect.blit_to(screen)

def main():
    pygame.init()
    screen = pygame.display.set_mode(screen_size)


    pygame.time.set_timer(pygame.USEREVENT, 500)
    my_shape = TetrisShape()
    while True:
        if my_shape.dead:
            my_shape = TetrisShape()
        event = pygame.event.wait()
        if event.type == pygame.KEYUP:
            if event.key == UP_ARROW:
               my_shape.rotate()
            if event.key == DOWN_ARROW:
               my_shape.move(0, 1)
            if event.key == LEFT_ARROW:
               my_shape.move(-1, 0)
            if event.key == RIGHT_ARROW:
               my_shape.move(1, 0)
            if event.key == pygame.K_ESCAPE:
                sys.exit(1)
        elif event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.USEREVENT:
            my_shape.move(0, 1)

        screen.fill(black)
        my_shape.blit_to(screen)
        for dead_square in ocupado.values():
            dead_square.blit_to(screen)
        pygame.display.flip()
