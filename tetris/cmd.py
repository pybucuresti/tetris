import os
import sys
import pygame

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
def main():
    pygame.init()
    screen = pygame.display.set_mode(screen_size)

    blue_square = pygame.image.load(ROOT_PATH + 'images/square-16x16-blue.png')
    blue_rect = blue_square.get_rect()
    pygame.time.set_timer(pygame.USEREVENT, 500)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == DOWN_ARROW:
                   blue_rect = blue_rect.move([0, square_size]) 
                if event.key == LEFT_ARROW:
                   blue_rect = blue_rect.move([-square_size, 0]) 
                if event.key == RIGHT_ARROW:
                   blue_rect = blue_rect.move([square_size, 0]) 
            elif event.type == pygame.QUIT: sys.exit()
            elif event.type == pygame.USEREVENT:
                blue_rect = blue_rect.move(speed)

        screen.fill(black)
        screen.blit(blue_square, blue_rect)
        pygame.display.flip()
