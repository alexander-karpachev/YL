import enum
from random import randint
from time import sleep

import pygame
import sys
import os

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FPS = 30

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOW_SIZE)


class GameColors(enum.Enum):
    border = white = pygame.Color('white')
    background = black = pygame.Color('black')

    cell_color = [
        pygame.Color('black'),
        pygame.Color('gray'),
        pygame.Color('yellow'),
        pygame.Color('green'),
        pygame.Color('blue'),
    ]


class Board:
    cell_size = 20
    left = 10
    top = 10
    filled = False

    # создание поля
    def __init__(self, width=0, height=0):
        if width == 0:
            self.width = (WINDOW_WIDTH - 2 * self.left) // self.cell_size
        else:
            self.width = width
        if height == 0:
            self.height = (WINDOW_HEIGHT - 2 * self.top) // self.cell_size
        else:
            self.height = height
        self.board = self.create_board()
        self.fill_board()

    def create_board(self):
        return [[0] * self.width for _ in range(self.height)]

    def paint(self):
        if self.filled:
            return
        for r in range(self.height):
            for c in range(self.width):
                if self.board[r][c] == 3:
                    self.board[r][c] = 4

    def fill_board(self, cells_count=200):
        while cells_count > 0:
            c = randint(0, self.width - 1)
            r = randint(0, self.height - 1)
            if self.board[r][c] == 0:
                self.board[r][c] = 1
                cells_count -= 1

    def get_empty(self):
        while True:
            c = randint(0, self.width - 1)
            r = randint(0, self.height - 1)
            if self.board[r][c] == 0:
                return r, c

    def get_cell_rect(self, j, i, border=0):
        top = self.top + j * self.cell_size + border
        left = self.left + i * self.cell_size + border
        width = self.cell_size - 2 * border
        height = self.cell_size - 2 * border
        return left, top, width, height

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, s):
        row_num = 0
        col_num = 0
        for r in self.board:
            for c in r:
                pygame.draw.rect(s, GameColors.border.value, self.get_cell_rect(row_num, col_num), 1)
                pygame.draw.rect(s, GameColors.cell_color.value[c], self.get_cell_rect(row_num, col_num, 3), 0)
                col_num += 1
            col_num = 0
            row_num += 1

    def get_click(self, pos):
        cell = self.get_cell(pos)
        self.on_click(cell)

    def on_click(self, cell):
        pass

    def get_cell(self, pos):
        x, y = pos
        col = (x - self.left) // self.cell_size
        row = (y - self.top) // self.cell_size
        if not 0 <= row <= self.height - 1 or not 0 <= col <= self.width - 1:
            return None
        return row, col

    def get_cell_color(self, row, col):
        return GameColors.board_colors.value[self.board[row][col]]


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def fill(b, r, c):
    if b.filled:
        return
    board = b.board
    if r < 0 or c < 0 or r > b.height - 1 or c > b.width - 1:
        return
    if board[r][c] != 0:
        return
    print(r, c, board[r][c])
    board[r][c] = 2
    screen.fill(GameColors.cell_color.value[0])
    b.render(screen)
    clock.tick(FPS)
    pygame.display.flip()
    sleep(0.1)
    fill(b, r + 1, c)
    fill(b, r, c - 1)
    fill(b, r - 1, c)
    fill(b, r, c + 1)
    board[r][c] = 3


def main():
    bg = pygame.Color('black')

    board = Board()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        if not running:
            break

        # recurcive draw
        x, y = board.get_empty()
        fill(board, x, y)
        board.paint()
        board.filled = True

        screen.fill(bg)
        board.render(screen)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.display.quit()


if __name__ == '__main__':
    main()
