import os
import sys
import pygame
from random import choice

ROOT_PATH = os.path.dirname(__file__) + '/'
square_size = 16
speed = [0, square_size]
black = 0, 0, 0
num_horiz_squares = 10
num_vert_squares = 25

running = True

screen_size = width, height = num_horiz_squares*square_size, num_vert_squares*square_size

red_square = pygame.image.load(ROOT_PATH + 'images/square-16x16-red.png')
green_square = pygame.image.load(ROOT_PATH + 'images/square-16x16-green.png')
yellow_square = pygame.image.load(ROOT_PATH + 'images/square-16x16-yellow.png')
blue_square = pygame.image.load(ROOT_PATH + 'images/square-16x16-blue.png')
squares = {'red': red_square,
           'green': green_square,
           'yellow': yellow_square,
           'blue': blue_square}

ocupado = {}

UP_ARROW = 273
LEFT_ARROW = 276
DOWN_ARROW = 274
RIGHT_ARROW = 275

dead_lines = []

def check_collision(potential_rects):
    for posX, posY in potential_rects:
        if posY >= num_vert_squares:
            return True
        if not (0 <= posX < num_horiz_squares):
            return True
        if ocupado.get((posX, posY), False):
            return True
    return False

def handle_complete_line():
    complete_squares = dict()
    for tup in ocupado:
        x, y = tup
        if y in complete_squares:
            complete_squares[y] += 1
        else:
            complete_squares[y] = 1
    for line in complete_squares:
        if complete_squares[line] == num_horiz_squares:
            for other_line, time in dead_lines:
                if line == other_line:
                    break
            else:
                dead_lines.append((line, 3))

def clean_ocupado():
    global ocupado
    global dead_lines
    new_ocupado = {}
    new_dead_lines = []
    for line, timer in sorted(dead_lines):
        if timer > 0:
            timer -= 1
            new_dead_lines.append((line, timer))
            continue
        for x, y in ocupado.keys():
            if y < line:
                updated_rect = ocupado[(x, y)]
                updated_rect.posY += 1
                new_ocupado[(x, y + 1)] = updated_rect
            elif y > line:
                new_ocupado[(x, y)] = ocupado[(x, y)]
        ocupado = new_ocupado
        new_ocupado = {}
    
    dead_lines = new_dead_lines
    #dead_lines[:] = []

    if new_ocupado:
        ocupado = new_ocupado
                 

class MyRectangle(object):
    def __init__(self, square, posX, posY):
        self.posX = posX
        self.posY = posY
        self.square = square

    def blit_to(self, screen):
        rect = self.square.get_rect().move([self.posX*square_size, self.posY*square_size])
        screen.blit(self.square, rect)

rects_list = {'snake1': ((0, 0), (0, 1), (1, 1), (1, 2)),
              'snake2': ((1, 0), (0, 1), (1, 1), (0, 2)),
              'bar': ((0, 0), (0, 1), (0, 2), (0, 3)),
              'tshape': ((0, 0), (0, 2), (0, 1), (1, 1)),
              'lshape1': ((0, 0), (0, 2), (0, 1), (1, 0)),
              'lshape2': ((0, 0), (0, 1), (1, 0), (2, 0)),
              'box': ((0, 0), (0, 1), (1, 1), (1, 0))}

class TetrisShape(object):
    def __init__(self):
        global running
        key = choice(rects_list.keys())
        self.rects = []
        my_square = choice(squares.values())
        for i, (x, y) in enumerate(rects_list[key]):
            self.rects.append(MyRectangle(my_square, x + 4, y))
        self.rects = tuple(self.rects)
        self.dead = False
        self.center = 2
        if check_collision((r.posX, r.posY) for r in self.rects):
            running = False

    def move(self, dx, dy):
        potential_rects = []
        for rect in self.rects:
            potential_rects.append((rect.posX+dx, rect.posY+dy))
        if check_collision(potential_rects):
            if dy != 0:
                for rect in self.rects:
                    ocupado[rect.posX, rect.posY] = rect
                    self.dead = True
            return
        for rect in self.rects:
            rect.posX += dx
            rect.posY += dy

    def drop_all_the_way(self):
        while True:
            self.move(0,1)
            if self.dead:
                return

    def rotate(self):
        changes = {
            (-1, -1): (1, -1),
            (1, -1): (1, 1),
            (1, 1): (-1, 1),
            (-1, 1): (-1, -1),

            (-1, 0): (0, -1),
            (0, -1): (1, 0),
            (1, 0): (0, 1),
            (0, 1): (-1, 0),

            (-2, 0): (0, -2),
            (0, -2): (2, 0),
            (2, 0): (0, 2),
            (0, 2): (-2, 0),
        }

        def calculate_change(rect, center_rect):
            if rect == center_rect:
                return (0, 0)
            delta_x = rect.posX - center_rect.posX
            delta_y = rect.posY - center_rect.posY
            change = changes[(delta_x, delta_y)]
            return change

        center_rect = self.rects[self.center]
        potential_rects = []
        for rect in self.rects:
            change = calculate_change(rect, center_rect)
            potential_rects.append((center_rect.posX + change[0],
                                    center_rect.posY + change[1]))
        if check_collision(potential_rects):
            return

        for rect in self.rects:
            change = calculate_change(rect, center_rect)
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
    while running:
        if my_shape.dead:
            handle_complete_line()
            my_shape = TetrisShape()
        event = pygame.event.wait()
        if event.type == pygame.KEYUP:
            if event.key == UP_ARROW:
               my_shape.rotate()
            if event.key == DOWN_ARROW:
               my_shape.drop_all_the_way()
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
        clean_ocupado()
        excluded_lines = [line for line, timer in dead_lines if timer % 2 == 0]
        for square in ocupado.values():
            if square.posY in excluded_lines:
                continue
            square.blit_to(screen)
                    
        pygame.display.flip()
    print "Game over!"
    game_over_image = pygame.image.load(ROOT_PATH + 'images/button.png')
    screen.blit(game_over_image, game_over_image.get_rect())
    pygame.display.flip()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                sys.exit(1)
        elif event.type == pygame.QUIT: sys.exit()
