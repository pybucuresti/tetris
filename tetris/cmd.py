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
    def __init__(self, square):
        self.rects = {
            (0,0): MyRectangle(square, 4, 0),
            (0,1): MyRectangle(square, 4, 1),
            (1,1): MyRectangle(square, 5, 1),
            (1,2): MyRectangle(square, 5, 2),
        }
        self.dead = False

    def move(self, dx, dy):
        if self.check_collision():
            for rect in self.rects.values():
                ocupado[rect.posX, rect.posY] = rect
                self.dead = True
            return
        for rect in self.rects.values():
            rect.posX += dx
            rect.posY += dy

    def check_collision(self):
        slist = sorted(self.rects.keys())
        last_block = self.rects[slist[-1]]
        hit_bottom = last_block.posY + 1 >= num_vert_squares 
        hit_others = ocupado.get((last_block.posX, last_block.posY), False)
        return hit_bottom or hit_others

    def blit_to(self, screen):
        for rect in self.rects.values():
            rect.blit_to(screen)

def main():
    pygame.init()
    screen = pygame.display.set_mode(screen_size)

    blue_square = pygame.image.load(ROOT_PATH + 'images/square-16x16-blue.png')

    pygame.time.set_timer(pygame.USEREVENT, 500)
    my_shape = TetrisShape(blue_square)
    while True:
        if my_shape.dead:
            my_shape = TetrisShape(blue_square)
        event = pygame.event.wait()
        if event.type == pygame.KEYUP:
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
